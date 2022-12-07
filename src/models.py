# python code
import util
from env import *

import json
import time
from tqdm import tqdm 
import numpy as np
import copy
import os
import openai
import re
import pandas as pd
import pickle
# api_key_json = util.load_json(api_key_fp)

# Create and configure logger
import logging
logging.basicConfig(filename="../log/models.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
 
# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
 
##########################################################
##################### BranchingAI ########################
##########################################################
class BranchingAI():

    default_config = {
        'gpt_config': {
            'model': 'davinci',
            'wait_time': 0
        },
        'model_name': 'codex_naive_prompting_v1',
        'task': 'classification'
    }

    def __init__(self, config = default_config):
        # save config
        self.config = config

        # openai settings
        self.gpt_config = config['gpt_config'] if 'gpt_config' in config else {}
        self.gpt_model = self.gpt_config['model'] if 'model' in self.gpt_config else 'davinci'
        if 'code' in self.gpt_model.lower():
            # self.model_type = 'codex'
            logger.warning("[BranchingAI.__init__()] Using personal token")
            self.api_key = util.load_json(api_key_fp)['personal']
            self.gpt_config['wait_time'] = 14 # override config setting
            self.prompting = True
        else:
            # self.model_type = 'gpt'
            logger.warning("[BranchingAI.__init__()] Using ccb_group token")
            self.api_key = util.load_json(api_key_fp)['ccb_group']
            if 'ft' in self.gpt_model.lower():
                self.prompting = False
                self.gpt_config['wait_time'] = 1 # override config setting
            else:
                self.prompting = True 
                self.gpt_config['wait_time'] = 0 # override config setting
        self.gpt_config['api_key'] = self.api_key
        self.gpt_config['model'] = self.gpt_model

        # loading required data
        self.rationale2key = pickle.load(open(final_dataset_dir + 'proscript/rationale2key.pkl', 'rb'))
        self.key2rationale = pickle.load(open(final_dataset_dir + 'proscript/key2rationale.pkl', 'rb'))

        # prompt related attributes
        self.script_template = config['script_template'] if 'script_template' in config else {}
        
        # model settings
        self.task = config['task']
        self.model_name = config['model_name'] # model identifier, e.g. codex_baseline
        self.cache_dir = rationale_cache_dir + 'output/'
        self.naive = True if 'naive' in self.model_name else False
        self.prompting = True if 'prompting' in self.model_name else False
        self.ensemble = True if 'ensemble' in self.model_name else False 


    def init_prompt(self, train_scripts):
        '''
        Desc: initiate prompts from training instances. 
        Use cases:
            - prompting: will formulate all training scripts into self.few_shot_promots, which is a dictionary of prompts key by different rataionles
            - fine-tuning: will formulate all training scripts into the folder of {prompt_dir}/{model_name} for further annotations
        '''
        # check model type
        if self.task == "classification":
            if 'codex' in self.model_name:
                rationale_keys = [k for k in self.key2rationale if k >= 0]
                selected_scripts = self.helper_sample_shots(train_scripts, rationale_keys, pos_only = True)
                if self.naive:
                    self.few_shot_prompts = {
                        ra: "# Python Code\n" + "\n###\n".join([
                            "\n# Example {}".format(i + 1) + self.format_script_prompt(selected_scripts[ra][i], ra, answer = True) 
                            for i in range(len(selected_scripts[ra]))
                        ]) 
                        for ra in rationale_keys
                    }
                #elif 'code_style' in self.model_name:
                else:
                    self.few_shot_prompts = {
                        ra: self.script_template['overview'] + "\n###\n".join([
                            "\n# Test Case {}".format(i + 1) + self.format_script_prompt(selected_scripts[ra][i], ra, answer = True) 
                            for i in range(len(selected_scripts[ra]))
                        ]) 
                        for ra in rationale_keys
                    }
                # prompt_text = self.overview + '\n\n' + formatted_scripts        
                # if save_to_file:
                #     prompt_file = open(self.prompt_dir + self.model_name + '.txt', 'w')
                #     prompt_file.write(prompt_text)
                #     prompt_file.close()
                # return prompt_text
        
            if self.prompting:
                rationale_keys = [k for k in self.key2rationale if k >= 0]
                selected_scripts = self.helper_sample_shots(train_scripts, rationale_keys, pos_only = True)
                if self.naive:
                    self.few_shot_prompts = {
                        ra: "# Python Code\n" + "\n###\n".join([
                            "\n# Example {}".format(i + 1) + self.format_script_prompt(selected_scripts[ra][i], ra, answer = True) 
                            for i in range(len(selected_scripts[ra]))
                        ]) 
                        for ra in rationale_keys
                    }
            else:
                ##TODO
                pass
        else:
            pass
    
    def format_script_prompt(self, script, rationale_key = None, answer = None):
        if 'codex' in self.model_name:
            if self.task == "classification":
                previous_actions = ''
                for i in range(script['branching_info']['branching_idx'] + 1):
                    event = script['steps'][i]
                    previous_actions += ("'{}. {}'").format(i + 1, event)
                prompt = self.script_template['script_template'].format(
                    goal = "'{}'".format(script['goal']),
                    prev_events = previous_actions,
                    branching_step = "'{}'".format(script['branching_info']['branching_step']),
                    op1 = "'{}'".format(script['branching_info']['option 1']),
                    op2 = "'{}'".format(script['branching_info']['option 2']),
                    rationale = self.key2rationale[rationale_key],
                    rationale_explanation = self.script_template['rationale_explanation'][self.key2rationale[rationale_key]]
                )
                if answer is not None:
                    if rationale_key in script['branching_info']['op1_ra']:
                        prompt += " '{}' # option_1".format(script['branching_info']['option 1'])
                    elif rationale_key in script['branching_info']['op2_ra']:
                        prompt += " '{}' # option_2".format(script['branching_info']['option 2'])
                    else:
                        prompt += " 'There is not much difference between option 1 and option 2'"
                return prompt  

            elif self.task == "retrieval":
                pass 
               


    def predict(self, orig_scripts):
        '''
        Desc: Make prediction of a batch of scripts
        Input: 
            - orig_scripts: list of scripts
        Output:
            - scripts: deep-copy of the scripts, with modified content
                - Classification: script['branching_info']['classi_results']
                - Retrieval: script['branching_info']['retrieval_result']
        
        '''
        ### 1. prompt for gpt output
        if 'checkpoint' not in self.config or self.config['checkpoint'] == '':
            # 1.0. make a deep copy as the results would be stored in the `scripts`
            scripts = copy.deepcopy(orig_scripts)

            # 1.1 gpt calls
            timestamp = util.get_current_timestamp()
            for script in tqdm(scripts):
                if self.task == "multi_task":
                    # query about all the rationales if under multi-task setting
                    rationales = [ra for ra in self.rationale2key if self.rationale2key[ra] >= 0]
                    # TODO
                elif self.task == "classification":
                    rationales_keys = script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']
                    # rationales = [self.key2rationale[ra] for ra in all_keys]
                    script['branching_info']['rationale_gpt_output'] = self.predict_gpt_call(script, rationales_keys)
                elif self.task == "retrieval":
                    # TODO
                    pass
                
            # 1.2 dump to cache 
            cache_jsonl = self.cache_dir + 'BAI_' + timestamp + '.jsonl'
            with open(cache_jsonl, 'w') as cache_file:
                for data in scripts:
                    cache_file.write(json.dumps(data))
                    cache_file.write('\n')
        else:
            # 1.3 load from cache
            scripts = util.load_jsonl(self.cache_dir + 'BAI_' + self.config['checkpoint'] + '.jsonl')
        
        ### 2. inference from gpt output
        for script in scripts:
            classi_results = []
            retrieval_text_results = []
            retrieval_key_results = []
            gpt_outputs = script['branching_info']['rationale_gpt_output']
            for ra, gpt_output in gpt_outputs:
                pred_text, pred_answ = self.predict_gpt_output_parser(gpt_output)
                
                # retrieval results
                retrieval_text_results.append(pred_text)
                if pred_answ != 0:
                    retrieval_key_results.append(ra)

                # classification results
                if ra in script['branching_info']['op1_ra']:
                    true_answ = 1
                elif ra in script['branching_info']['op2_ra']:
                    true_answ = 2
                else:
                    true_answ = 0
                classi_results.append({
                    'rationele_text': self.key2rationale[ra],
                    'rationele_key': ra,
                    'true_answ': true_answ, # MAGIC NUMBER: depends on the `option_key` format
                    'pred_answ': pred_answ,
                    'pred_text': pred_text
                })
                
            script['branching_info']['classi_results'] = classi_results
            if self.task == "multi_task":
                script['branching_info']['retrieval_result'] = {
                    'true_answ': script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'],
                    'text_results': retrieval_text_results,
                    'pred_answ': retrieval_key_results
                }
        return scripts

    def predict_gpt_call(self, script, rationales_keys):
        '''
        Decs: Get GPT output for a list of rationales
        Input: 
            - script
            - rationales: list of rationale keys
        Output:
            - [(rationale, gpt_outputs)]
        '''
        gpt_outputs = []
        for key in rationales_keys: 
            formatted_script = self.format_script_prompt(script, key)
            if self.prompting:
                inference_prompt = '{}\n###\n\n# Test Case\n{}'.format(
                    self.few_shot_prompts[key], 
                    formatted_script
                )
            else:
                ##TODO
                pass
            
            gpt_output = util.universal_gpt_call(
                inference_prompt, 
                config = self.gpt_config
            )
            gpt_outputs.append((key, gpt_output))
        return gpt_outputs
    
    def predict_gpt_output_parser(self, gpt_output):
        if self.task == "classification":
            if 'codex' in self.model_name:
                pred_answ = 0
                pred_text = gpt_output.strip().lower()
                if 'option_1' in pred_text:
                    pred_answ = 1
                elif 'option_2' in pred_text:
                    pred_answ = 2
                return pred_text, pred_answ


    def helper_sample_shots(self, train_scripts, rationale_keys, num_shot = 3, pos_only = False):
        '''
        Desc: make sampling choices across the training scripts
        '''

        # self.base_prompts = {}
        script_visit_count = {}
        all_selected_scripts = {}
        current_max_visit = 1
        hard_keys = [3, 4, 6, 9] # MAGIC NUMBER: keys with very few available samples
        for key in rationale_keys:
            # key/ = self.rationale2key[ra]
            if key < 0:
                continue
            pos_count = sum([key in script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'] for script in train_scripts])
            if num_shot > pos_count:
                tmp_num_shot = pos_count
            else:
                tmp_num_shot = num_shot

            ## select scripts
            pos_counter, neg_counter = 0, 0
            selected_scripts = []
            curr_idx = 0
            while True:
                # check curr_idx position
                if curr_idx == len(train_scripts):
                    current_max_visit += 1
                    curr_idx = 0
                    continue
                script = train_scripts[curr_idx]
                script_id = script['curr_index']
                # count_valid = False
                if script_id in script_visit_count:
                    if script_visit_count[script_id] + 1 > current_max_visit:
                        curr_idx += 1
                        continue
                else:
                    script_visit_count[script_id] = 1
                
                # adding script
                if key in script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']:
                    if pos_counter < tmp_num_shot:
                        pos_counter += 1
                        if key not in hard_keys:
                            script_visit_count[script_id] += 1
                        selected_scripts.append(script)
                elif not pos_only:
                    if neg_counter < tmp_num_shot:
                        neg_counter += 1
                        script_visit_count[script_id] += 1
                        selected_scripts.append(script)
                curr_idx += 1

                # stop condition
                if pos_only and len(selected_scripts) >= tmp_num_shot:
                    break
                if not pos_only and len(selected_scripts) >= tmp_num_shot * 2:
                    break

            all_selected_scripts[key] = selected_scripts

        return all_selected_scripts






##########################################################
######################### Tester #########################
##########################################################
from sklearn.metrics import accuracy_score, precision_score
class Tester():
    def __init__(self):
        pass

    def eval_(self, scripts, task):        
        if task == 'retrieval':
            return self.eval_retrieval(scripts)
        elif task == 'classification':
            return self.eval_classification(scripts)
        else:
            raise NotImplementedError

    def eval_retrieval(self, scripts):
        '''
            'true_answ': script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'],
            'text_results': text_results,
            'pred_answ': key_results
        '''
        precision_scores = []
        for script in scripts:
            true_topic = script['branching_info']['retrieval_result']['true_answ']
            pred_topic = script['branching_info']['retrieval_result']['pred_answ']
            precision_scores.append(self.retrieval_precision(true_topic, pred_topic))

        avg_pre = round(np.mean(precision_scores), 2)
        return {
            'avg_pre': avg_pre,
            'pre_scores': precision_scores # list of precisions
        }
    
    # helper precision
    def retrieval_precision(self, label, pred):
        valid_pred = [i for i in pred if i != -1]
        if len(valid_pred) == 0:
            return 0
        precision = round(sum([i in label for i in valid_pred]) / len(valid_pred), 2)
        return precision

    def eval_classification(self, scripts):
        assert 'classi_results' in scripts[0]['branching_info'], "[ERROR] Expect 'classi_results' in scripts['branching_info']!"
        all_pred, all_true = [], []
        script_acc_lst = []
        for script in scripts:
            script_result = script['branching_info']['classi_results']
            
            tmp_acc = sum([r['pred_answ'] == r['true_answ'] for r in script_result]) / len(script_result)
            script_acc_lst.append(round(tmp_acc, 2))
            
            all_pred += [r['pred_answ'] for r in script_result] 
            all_true += [r['true_answ'] for r in script_result] 
        
        # print(script_acc_lst)
        avg_acc = round(np.mean(script_acc_lst), 2)
        all_acc = round(accuracy_score(all_true, all_pred), 2)
        return {
            'avg_acc': avg_acc,
            'all_acc': all_acc,
            'acc_scors': script_acc_lst
        }
# python code
import util
from env import * # TODO: change to import env

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
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


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
    default_rationale_keys = [0, 1, 2, 3, 5, 7]

    def __init__(self, config):
        # save config
        self.config = config

        # model settings
        self.task = config['task']
        self.model_name = config['model_name'] # model identifier, e.g. codex_baseline
        self.cache_dir = rationale_cache_dir + 'output/'
        self.naive = True if 'naive' in self.model_name else False
        self.prompting = True if 'prompting' in self.model_name else False
        self.ensemble = True if 'ensemble' in self.model_name else False 
        # self.multi_rationale = config['multi_rationale'] if 'multi_rationale' in config else False

        # openai settings
        self.gpt_config = config['gpt_config'] if 'gpt_config' in config else {}
        
        # begin change
        # self.gpt_model = self.gpt_config['model'] if 'model' in self.gpt_config else "text-davinci-002"
        # if 'code' in self.gpt_model.lower():
        #     # self.model_type = 'codex'
        #     logger.warning("[BranchingAI.__init__()] Using personal token")
        #     self.api_key = util.load_json(api_key_fp)['personal']
        #     self.gpt_config['wait_time'] = 10 # override config setting
        #     # print('wait_time:', self.gpt_config['wait_time'])
        #     self.prompting = True
        # else:
        #     # self.model_type = 'gpt'
        #     logger.warning("[BranchingAI.__init__()] Using ccb_group token")
        #     self.api_key = util.load_json(api_key_fp)['ccb_group']
        #     if 'ft' in self.gpt_model.lower():
        #         self.prompting = False
        #         self.gpt_config['wait_time'] = 1 # override config setting
        #     else:
        #         self.prompting = True 
        #         self.gpt_config['wait_time'] = 0 # override config setting
        self.gpt_model = "code-davinci-002"
        logger.warning("[BranchingAI.__init__()] Using personal token")
        self.api_key = util.load_json(api_key_fp)['personal']
        self.gpt_config['wait_time'] = 10 #config['gpt_config'] if 'wait_time' in config['gpt_config'] else 10
        self.prompting = True
        ## end change

        # other openai setting
        self.gpt_config['api_key'] = self.api_key
        self.gpt_config['model'] = self.gpt_model
        self.gpt_config['max_tokens'] = 1200

        # loading required data
        self.rationale2key = pickle.load(open(final_dataset_dir + 'proscript/rationale2key.pkl', 'rb'))
        self.key2rationale = pickle.load(open(final_dataset_dir + 'proscript/key2rationale.pkl', 'rb'))

        # prompt related attributes
        self.script_template = config['script_template'] if 'script_template' in config else {}

    def init_prompt(self, train_scripts):
        '''
        Desc: initiate prompts from training instances. 
        Use cases:
            - prompting: will formulate all training scripts into self.few_shot_promots, which is a dictionary of prompts key by different rataionles
            - fine-tuning: will formulate all training scripts into the folder of {prompt_dir}/{model_name} for further annotations
        '''
        if self.task == "retrieval":
            if 'code' in self.model_name:
                # code prompt
                if self.naive:
                    raise NotImplementedError
                elif 'cot' in self.model_name:
                    # cot codex model
                    shot_indices = [0, 1, 2, 3, 4, 16]
                    prompt_sub_cat = self.config["prompt_type"] if "prompt_type" in self.config else "cot_naive"
                    self.few_shot_prompts = [
                        "# TEST CASE\n{}\n###\n\n".format(
                            self.format_script_prompt(train_scripts[i], filename = 'code_prompts/retrieval/{}/{}.py'.format(prompt_sub_cat, i), answer = True)
                        )
                        for i in shot_indices
                    ]
                else:
                    raise NotImplementedError
            else:
                # text prompt
                if "shots" in self.config:
                    shot_indices = self.config['shots']
                else:
                    shot_indices = [0, 1, 2, 3, 4, 16]
                if self.naive:
                    prompt_sub_cat = "naive"
                else:
                    prompt_sub_cat = self.config["prompt_type"] if "prompt_type" in self.config else "cot"
                
                self.few_shot_prompts = [
                    "[Example]\n{}\n###\n\n".format(
                        self.format_script_prompt(
                            train_scripts[i], 
                            filename = 'text_prompts/retrieval/{}/{}.txt'.format(prompt_sub_cat, i), 
                            answer = True
                        )
                    )
                    for i in shot_indices
                ]
        elif self.task == "classification":
            if 'comparison' in self.model_name:
                self.few_shot_prompts = {}
                for key in self.default_rationale_keys:
                    files = [f for f in os.listdir(rationale_prompt_dir + 'text_prompts/classification/comparison/{}'.format(key)) if '.txt' in f]
                    self.few_shot_prompts[key] = [
                        "[Example]\n{}\n###\n\n".format(
                            self.format_script_prompt(
                                train_scripts[i], 
                                filename = 'text_prompts/classification/comparison/{}/{}'.format(key, files[i]), 
                                answer = True
                            )
                        )
                        for i in range(len(files))
                    ]
            elif 'code' in self.model_name:
                # code prompt for classification
                if "shots" in self.config:
                    shot_indices = self.config['shots']
                else:
                    shot_indices = [0, 1, 2, 3, 4, 16]
                if self.naive:
                    prompt_sub_cat = "naive"
                else:
                    prompt_sub_cat = self.config["prompt_type"] if "prompt_type" in self.config else "cot_w_assert"
                
                self.few_shot_prompts = [
                   "# TEST CASE\n{}\n###\n\n".format(
                        self.format_script_prompt(
                            train_scripts[i], 
                            filename = 'code_prompts/classification/{}/{}.py'.format(prompt_sub_cat, i), 
                            answer = True
                        )
                    )
                    for i in shot_indices
                ]
            else:
                # text prompt for classification
                if "shots" in self.config:
                    shot_indices = self.config['shots']
                else:
                    shot_indices = [0, 1, 2, 3, 4, 16]
                if self.naive:
                    prompt_sub_cat = "naive"
                else:
                    prompt_sub_cat = self.config["prompt_type"] if "prompt_type" in self.config else "cot_short"
                
                self.few_shot_prompts = [
                    "[Example]\n{}\n###\n\n".format(
                        self.format_script_prompt(
                            train_scripts[i], 
                            filename = 'text_prompts/classification/{}/{}.txt'.format(prompt_sub_cat, i), 
                            answer = True
                        )
                    )
                    for i in shot_indices
                ]
                
    def format_script_prompt(self, script, rationale_key = None, answer = None, filename = None):
        if self.task == "retrieval":
            if 'code' in self.model_name:
                if self.naive:
                    raise NotImplementedError
                elif 'cot' in self.model_name:
                    if answer is None: 
                        # case 1: prediction time, no answer is provided
                        previous_actions = ''
                        for i in range(script['branching_info']['branching_idx'] + 1):
                            event = script['steps'][i]
                            previous_actions += ("'{}. {}', ").format(i + 1, event)
                        prompt = self.script_template['script_template'].format(
                            goal = "'{}'".format(script['goal']),
                            prev_events = previous_actions,
                            branching_step = "'{}'".format(script['branching_info']['branching_step']),
                            op1 = "'{}'".format(script['branching_info']['option 1']),
                            op2 = "'{}'".format(script['branching_info']['option 2'])
                        )
                        return prompt
                    else:
                        if filename is None:
                            # case 2: annotation time, no cot is provided, output text for annotations
                            raise NotImplementedError
                        else:
                            # case 3: prediction time, look for annotated cot prompts from files
                            with open(rationale_prompt_dir + filename, 'r') as prompt_file:
                                return ''.join(prompt_file.readlines())
                else:
                    raise NotImplementedError
            else:
                # text prompts
                if filename is not None:
                    # case 1: prediction time, look for annotated cot prompts from files
                    with open(rationale_prompt_dir + filename, 'r') as prompt_file:
                        return ''.join(prompt_file.readlines())
                else:
                    if answer is None: 
                        # case 2: prediction time, no answer is provided
                        goal = script['goal']
                        prev_events = '\n'.join([
                            '  {}. {}'.format(i + 1, script['steps'][i]) 
                            for i in range(script['branching_info']['branching_idx'] + 1)
                        ])
                        branching_step = script['branching_info']['branching_step']
                        option1 = script['branching_info']['option 1']
                        option2 = script['branching_info']['option 2']
                        related_rationales = '\n'.join([
                            '- ' + self.key2rationale[rationale_key] + ''
                            for rationale_key in self.default_rationale_keys
                        ])
                        # answers = related_rationales
                        formatted_script = self.script_template['script_template'].format(
                            goal = goal,
                            prev_events = prev_events,
                            branching_step = branching_step,
                            option1 = option1,
                            option2 = option2,
                            related_rationales = related_rationales,
                            question = self.script_template['retrieval_question']
                        ).strip()
                        return formatted_script
                    else:
                        # case 3: annotation time, no cot is provided, output text for annotations
                        raise NotImplementedError
        elif self.task == "classification":
            # case 1: prediction time, look for annotated cot prompts from files
            if filename is not None:
                with open(rationale_prompt_dir + filename, 'r') as prompt_file:
                    return ''.join(prompt_file.readlines())
            # case 2&3: need to do string mulipulation
            if 'comparison' in self.model_name:
                # comparison prompts
                assert rationale_key is not None, 'Expect not-None rationale_key!'
                
                goal = script['goal']
                branching_step = script['branching_info']['branching_step']
                option1 = script['branching_info']['option 1']
                option2 = script['branching_info']['option 2']
                if answer == 1:
                    conclusion = self.script_template[self.key2rationale[rationale_key]].format(
                        'Option_1', 
                        'Option_2'
                    )
                elif answer == 2:
                    conclusion = self.script_template[self.key2rationale[rationale_key]].format(
                        'Option_2', 
                        'Option_1'
                    )
                else:
                    raise NotImplementedError
                conclusion = '\n- Conclusion: ' + conclusion
                prompt = self.script_template['script_template'].format(
                    goal = goal,
                    # prev_events = previous_actions,
                    branching_step = branching_step,
                    option1 = option1,
                    option2 = option2,
                    conclusion = conclusion
                )
                return prompt
            elif 'code' in self.model_name:
                # code prompts
                if answer is None: 
                    # case 2: prediction time, no answer is provided
                    # previous_actions = ''
                    # for i in range(script['branching_info']['branching_idx'] + 1):
                    #     event = script['steps'][i]
                    #     previous_actions += ("'{}. {}', ").format(i + 1, event)
                    related_rationale_keys = script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']
                    related_rationale_list = "['{}']".format("', '".join([self.key2rationale[key] for key in related_rationale_keys]))
                    prompt = self.script_template['script_template'].format(
                        goal = "'{}'".format(script['goal']),
                        # prev_events = previous_actions,
                        branching_step = "'{}'".format(script['branching_info']['branching_step']),
                        op1 = "'{}'".format(script['branching_info']['option 1']),
                        op2 = "'{}'".format(script['branching_info']['option 2']),
                        related_rationale = related_rationale_list
                    )
                    return prompt
                else:
                    # case 3: annotation time, no cot is provided, output text for annotations
                    raise NotImplementedError
            else:
                if answer is None: 
                    # case 2: prediction time, no answer is provided
                    goal = script['goal']
                    # prev_events = '\n'.join([
                    #     '  {}. {}'.format(i + 1, script['steps'][i]) 
                    #     for i in range(script['branching_info']['branching_idx'] + 1)
                    # ])
                    branching_step = script['branching_info']['branching_step']
                    option1 = script['branching_info']['option 1']
                    option2 = script['branching_info']['option 2']
                    related_rationales = '\n'.join([
                        '- ' + self.key2rationale[rationale_key] + ''
                        for rationale_key in script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'] 
                        if rationale_key in self.default_rationale_keys
                    ])
                    # answers = related_rationales
                    formatted_script = self.script_template['script_template'].format(
                        goal = goal,
                        # prev_events = prev_events,
                        branching_step = branching_step,
                        option1 = option1,
                        option2 = option2,
                        related_rationales = related_rationales,
                        question = self.script_template['classification_question']
                    ).strip()
                    return formatted_script
                else:
                    # case 3: annotation time, no cot is provided, output text for annotations
                    raise NotImplementedError

    def predict(self, orig_scripts, checkpoint = None):
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
        if checkpoint is None:
            # 1.0. make a deep copy as the results would be stored in the `scripts`
            scripts = copy.deepcopy(orig_scripts)

            # 1.1 gpt calls
            timestamp = util.get_current_timestamp()
            for script in tqdm(scripts):
                if self.task == "retrieval":
                    script['branching_info']['rationale_gpt_output'] = self.predict_gpt_call(script, rationales_keys = None)
                elif self.task == "classification":
                    rationales_keys = script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']
                    rationales_keys = [key for key in rationales_keys if key in self.default_rationale_keys]
                    script['branching_info']['rationale_gpt_output'] = self.predict_gpt_call(script, rationales_keys)
                else:
                    raise NotImplementedError

            # 1.2 dump to cache 
            cache_jsonl = self.cache_dir + 'BAI_' + timestamp + '.jsonl'
            with open(cache_jsonl, 'w') as cache_file:
                for data in scripts:
                    cache_file.write(json.dumps(data))
                    cache_file.write('\n')

            logger.warning("[BranchingAI.predict()] Predicted {} scripts with model {}, checkpoint: {}".format(
                len(orig_scripts),
                self.model_name,
                timestamp
            ))
        else:
            # 1.3 load from cache
            # print(self.cache_dir + 'output/BAI_' + checkpoint + '.jsonl')
            scripts = util.load_jsonl(self.cache_dir + 'BAI_' + checkpoint + '.jsonl')
            # print(len(scripts))


        ### 2. inference from gpt output
        if self.task == 'retrieval':
            for script in scripts:
                gpt_output = script['branching_info']['rationale_gpt_output']
                retrieval_results = self.predict_gpt_output_parser(gpt_output)
                script['branching_info']['retrieval_result'] = {
                        'true_answ': script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'],
                        'text_results': [
                            r['pred_text']
                            for r in retrieval_results if r['pred_answ'] == 1
                        ],
                        'pred_answ': [
                            r['rationale_key']
                            for r in retrieval_results if r['pred_answ'] == 1
                        ]
                    }
        elif self.task == 'classification':
            if 'comparison' in self.model_name:
                # TODO
                pass 
            else:
                for script in scripts:
                    gpt_output = script['branching_info']['rationale_gpt_output']
                    classi_results = self.predict_gpt_output_parser(gpt_output)
                    
                    for result in classi_results:
                        rationale_key = result['rationale_key']
                        if rationale_key in script['branching_info']['op1_ra']:
                            result['true_answ'] = 1
                        elif rationale_key in script['branching_info']['op2_ra']:
                            result['true_answ'] = 2
                        else:
                            result['true_answ'] = 0
                    script['branching_info']['classi_results'] = classi_results
        else:
            raise NotImplementedError
        return scripts

    def predict_gpt_call(self, script, rationales_keys = None):
        '''
        Decs: Get GPT output for a list of rationales
        Input: 
            - script
            - rationales: list of rationale keys
        Output:
            - [(rationale, gpt_outputs)]
        '''
        if self.task == "retrieval":
            inference_prompt = ''
            if 'code' in self.model_name:
                if 'cot' in self.model_name:
                    formatted_script = "# TEST CASE\n{}".format(
                        self.format_script_prompt(script, answer = None)
                    )
                    if self.prompting:
                        inference_prompt = "".join(self.few_shot_prompts) + formatted_script
                    else:
                        raise NotImplementedError
                    gpt_output = util.universal_gpt_call(
                        inference_prompt, 
                        config = self.gpt_config
                    )
                    return gpt_output
                else:
                    raise NotImplementedError
            else:
                # text prompts
                formatted_script = "[Example]\n{}".format(
                    self.format_script_prompt(script, answer = None)
                )
                if self.prompting:
                    inference_prompt = "".join(self.few_shot_prompts) + formatted_script
                else:
                    raise NotImplementedError
                gpt_output = util.universal_gpt_call(
                    inference_prompt, 
                    config = self.gpt_config
                )
                return gpt_output
            
        elif self.task == "classification":
            if 'comparison' in self.model_name:
                gpt_output = []
                for key in rationales_keys:
                    # stage 1: two-sided prompt
                    formatted_script_1 = "[Example]\n{}".format(self.format_script_prompt(script, rationale_key = key, answer = 1))
                    formatted_script_2 = "[Example]\n{}".format(self.format_script_prompt(script, rationale_key = key, answer = 2))
                    inference_prompt_1 = "".join(self.few_shot_prompts[key]) + formatted_script_1
                    inference_prompt_2 = "".join(self.few_shot_prompts[key]) + formatted_script_2
                    tmp_gpt_output_1 = util.universal_gpt_call(inference_prompt_1, config = self.gpt_config)
                    tmp_gpt_output_2 = util.universal_gpt_call(inference_prompt_2, config = self.gpt_config)

                    # stage 2: gpt_judging
                    # TODO
                    gpt_output.append((key, tmp_gpt_output_1, tmp_gpt_output_2))
            elif 'code' in self.model_name:
                formatted_script = "# TEST CASE\n{}".format(
                    self.format_script_prompt(script, answer = None)
                )
                if self.prompting:
                    inference_prompt = "".join(self.few_shot_prompts) + formatted_script
                else:
                    raise NotImplementedError
                gpt_output = util.universal_gpt_call(
                    inference_prompt, 
                    config = self.gpt_config
                )
            else:
                formatted_script = "[Example]\n{}".format(
                    self.format_script_prompt(script, answer = None)
                )
                if self.prompting:
                    inference_prompt = "".join(self.few_shot_prompts) + formatted_script
                else:
                    raise NotImplementedError
                gpt_output = util.universal_gpt_call(
                    inference_prompt, 
                    config = self.gpt_config
                )
            return gpt_output
        else:
            raise NotImplementedError

    
    def predict_gpt_output_parser(self, gpt_output):
        if self.task == "retrieval":
            pred_text_lst = None
            if 'code' in self.model_name:
                answers = gpt_output.split("if rationale == ")
                all_results = []
                for ans in answers:
                    ans = ans.strip()
                    if len(re.findall("'[^']+'", ans)) != 1:
                        continue
                    rationale = re.findall("'[^']+'", ans)[0][1:-1]
                    # ans_lst = ans.split('\n')[1:]
                    pred_text = ans.strip() # ans_lst[0].strip()
                    # pred_text += '\n' + ans_lst[1].strip()
                    if 'return True' in ans.split('\n')[-1]:
                        pred_answ = 1
                    elif 'return False' in ans.split('\n')[-1]:
                        pred_answ = 0
                    all_results.append({
                        'rationale_text': rationale,
                        'rationale_key': self.rationale2key[rationale],
                        # 'true_answ': true_answ,
                        'pred_answ': pred_answ,
                        'pred_text': pred_text
                    })
                return all_results
            else:
                # text prompt
                all_results = []
                for answer in gpt_output.split('\n- '):
                    answer = answer.lower().strip()
                    if len(answer) == 0:
                        continue
                    ans_lst = answer.split('\n')
                    rationale = ans_lst[0].replace('-', '').replace(':', '').strip()
                    pred_text = copy.copy(answer)
                    if len(answer.split('- conclusion')) > 0:
                        conculsion = answer.split('- conclusion')[-1]
                    else:
                        conculsion = answer
                    if 'do have' in conculsion:
                        pred_answ = 1
                    elif 'do not have' in conculsion:
                        pred_answ = 0
                    else:
                        pred_answ = -1
                    all_results.append({
                        'rationale_text': rationale,
                        'rationale_key': self.rationale2key[rationale],
                        # 'true_answ': true_answ,
                        'pred_answ': pred_answ,
                        'pred_text': pred_text
                    })
                return all_results
        elif self.task == "classification":
            if 'code' in self.model_name:
                # parse code prompt
                answers = gpt_output.split("if rationale == ")
                all_results = []
                for ans in answers:
                    ans = ans.strip()
                    if len(re.findall("'[^']+'", ans)) != 1:
                        continue
                    rationale = re.findall("'[^']+'", ans)[0][1:-1]
                    ans_lst = ans.split('\n')[1:]
                    pred_text = ans_lst[0].strip()
                    pred_text += '\n' + ans_lst[1].strip()
                    if 'option1' in ans_lst[2]:
                        pred_answ = 1
                    elif 'option2' in ans_lst[2]:
                        pred_answ = 2
                    all_results.append({
                        'rationale_text': rationale,
                        'rationale_key': self.rationale2key[rationale],
                        # 'true_answ': true_answ,
                        'pred_answ': pred_answ,
                        'pred_text': pred_text
                    })
                return all_results
            else:
                # parse text prompt
                all_results = []
                for answer in gpt_output.split('\n- '):
                    answer = answer.lower().strip()
                    if len(answer) == 0:
                        continue
                    ans_lst = answer.split('\n')
                    rationale = ans_lst[0].replace('-', '').strip()
                    pred_text = copy.copy(answer)
                    if len(answer.split('- conclusion')) > 0:
                        conculsion = answer.split('- conclusion')[-1]
                    else:
                        conculsion = ''
                    # if 'option_1 is better' in conculsion:
                    #     pred_answ = 1
                    # elif 'option_2 is better' in conculsion:
                    #     pred_answ = 2
                    # else:
                    #     pred_answ = -1
                    if 'option_1' in conculsion:
                        pred_answ = 1
                    elif 'option_2' in conculsion:
                        pred_answ = 2
                    else:
                        pred_answ = -1
                    all_results.append({
                        'rationale_text': rationale,
                        'rationale_key': self.rationale2key[rationale],
                        # 'true_answ': true_answ,
                        'pred_answ': pred_answ,
                        'pred_text': pred_text
                    })
                return all_results
        else:
            raise NotImplementedError


    ##########################################################
    ########################## Eval ##########################
    ##########################################################
    def eval_retrieval(self, scripts, rationale_subset = default_rationale_keys):
        '''
            'true_answ': script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'],
            'text_results': text_results,
            'pred_answ': key_results
        '''
        pre_scores = []
        rec_scores = []
        f1_scores = []
        all_true = []
        all_pred = []
        for script in scripts:
            true_topic = script['branching_info']['retrieval_result']['true_answ']
            pred_topic = script['branching_info']['retrieval_result']['pred_answ']
            true_topic = [1 if i in true_topic else 0 for i in rationale_subset]
            pred_topic = [1 if i in pred_topic else 0 for i in rationale_subset]
            if len(true_topic) != 0:
                pre_scores.append(precision_score(true_topic, pred_topic))
                rec_scores.append(recall_score(true_topic, pred_topic))
                f1_scores.append(f1_score(true_topic, pred_topic))
            all_true += true_topic
            all_pred += pred_topic
        
        avg_f1 = round(np.mean(f1_scores), 2)
        avg_pre = round(np.mean(pre_scores), 2)
        avg_rec = round(np.mean(rec_scores), 2)
        all_pre = round(precision_score(all_true, all_pred), 2)
        all_rec = round(recall_score(all_true, all_pred), 2)
        all_f1 = round(f1_score(all_true, all_pred), 2)
        eval_result = {
            'avg_pre': avg_pre,
            'avg_rec': avg_rec,
            'avg_f1': avg_f1,
            'all_pre': all_pre,
            'all_rec': all_rec,
            'all_f1': all_f1,
            'num_sample': len(scripts)
        }
        self.helper_log_eval(eval_result, scripts, 'retrieval')
        return eval_result

    def eval_classification(self, scripts, relevant_only = False, rationale_subset = default_rationale_keys):
        assert 'classi_results' in scripts[0]['branching_info'], "[ERROR] Expect 'classi_results' in scripts['branching_info']!"
        all_pred, all_true = [], []
        script_acc_lst = []
        for script in scripts:
            script_result = script['branching_info']['classi_results']
            script_result = [r for r in script_result if r['rationale_key'] in rationale_subset]
            if relevant_only:
                script_result = [r for r in script_result if r['true_answ'] != 0]
            if len(script_result) == 0:
                continue
            tmp_acc = sum([
                r['pred_answ'] == r['true_answ'] 
                for r in script_result
            ]) / len(script_result)
            script_acc_lst.append(round(tmp_acc, 2))
            all_pred += [r['pred_answ'] for r in script_result] 
            all_true += [r['true_answ'] for r in script_result]                 
        # print(script_acc_lst)
        avg_acc = round(np.mean(script_acc_lst), 2)
        all_acc = round(accuracy_score(all_true, all_pred), 2)
        
        eval_result = {
            'avg_acc': avg_acc,
            'all_acc': all_acc,
            'conf_ma': self.helper_classification_confusion_matrix(all_pred, all_true)
        }
        self.helper_log_eval(eval_result, scripts, 'classification')
        return eval_result
        

    def helper_classification_confusion_matrix(self, pred_answ, true_answ):
        '''
        Note: true_answ and pred_answ should be list with exact same shape
        '''
        false_unknown = 0
        false_retrieve = 0
        false_predict = 0
        correct_igonre = 0
        correct_predict = 0

        for i in range(len(pred_answ)):
            tmp_pred = pred_answ[i]
            tmp_true = true_answ[i]

            if tmp_pred == 0 and tmp_true != 0:
                false_unknown += 1
            elif tmp_true == 0 and tmp_pred != 0:
                false_retrieve += 1
            elif tmp_true != 0 and tmp_pred != 0:
                if tmp_pred != tmp_true:
                    false_predict += 1
                else:
                    correct_predict += 1 
            else:
                correct_igonre += 1

        return {
            'false_unknown': false_unknown,
            'false_retrieve': false_retrieve,
            'false_predict': false_predict,
            'correct_igonre': correct_igonre,
            'correct_predict': correct_predict
        }

    def helper_log_eval(self, eval_result, scripts, task):
        # save evaluation results
        timestamp = util.get_current_timestamp()
        # save data
        results_jsonl = rationale_results_dir + 'eval_logs/BAI_' + timestamp + '_{}_scripts.jsonl'.format(task)
        with open(results_jsonl, 'w') as cache_file:
            for data in scripts:
                cache_file.write(json.dumps(data))
                cache_file.write('\n')
        # save result
        metric_json = rationale_results_dir + 'eval_logs/BAI_' + timestamp + '_{}_results.json'.format(task)
        with open(metric_json, 'w') as cache_file:
            eval_result_copy = copy.copy(eval_result)
            eval_result_copy['model_config'] = vars(self)
            cache_file.write(json.dumps(eval_result_copy, indent = 4))
            cache_file.write('\n')
        logger.warning("[BranchingAI.helper_log_eval()] Evaluated {} scripts with model {}, checkpoint: {}".format(
            len(scripts),
            self.model_name,
            timestamp
        ))
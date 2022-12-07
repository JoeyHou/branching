


##########################################################
##################### Base-models ########################
##########################################################


from abc import ABC, abstractmethod
from typing import Callable, List, Tuple, Any
class BaseModel(ABC):
    """Base class for all scoring function, 
        given a script, return the ranked list of rationales
    """
    
    # @abstractmethod
    # def __call__(self, script, source = 'proscript'):
    #     raise NotImplementedError


##########################################################
################### Chain-of-though ######################
##########################################################
class GPTDecider(BaseModel):
    """Implement the GPT Decider"""
    def __init__(self, config): #, model_name, prompt_dir, rationale2key = rationale2key, key2rationale = key2rationale):
        self.config = config

        logger.warning("[GPTDecider.__init__()] Using ccb_group token")
        self.api_key = util.load_json(api_key_fp)['ccb_group']
        
        self.key2rationale = config['key2rationale']
        self.rationale2key = config['rationale2key']
        self.gpt_model = config['gpt_model'] if 'gpt_model' in config else 'davinci'
        self.multi_task = config['multi_task'] if 'multi_task' in config else False

        ## gpt parameters
        self.prompt_type = config['prompt_type'] if 'prompt_type' in config else 'naive'
        self.temperature = config['temperature'] if 'temperature' in config else 0.75

        # prompt related attributes
        self.overview = config['overview'] if 'overview' in config else ''
        self.script_template = config['script_template']
        self.classification_questions = config['classification_questions']
        self.prompt_dir = rationale_prompt_dir #config['prompt_dir'] 
        self.model_name = config['model_name']
        # self.prompt_path = self.prompt_dir + self.model_name + '.txt'   
        self.num_shot = config['num_shot'] if 'num_shot' in config else 3
        self.save_prompt = config['save_prompt'] if 'save_prompt' in config else False
        
        # other attributes
        self.debug = config['debug'] if 'debug' in config else False
        self.cache_dir = rationale_cache_dir + 'output/'

    def predict(self, orig_scripts):
        ### 1. prompt for gpt output
        if 'checkpoint' not in self.config or self.config['checkpoint'] == '':
            # 1.0. make a deep copy as the results would be stored in the `scripts`
            scripts = copy.deepcopy(orig_scripts)

            # 1.1 gpt calls
            timestamp = util.get_current_timestamp()
            for script in tqdm(scripts):
                if self.multi_task:
                    # query about all the rationales if under multi-task setting
                    rationales = [ra for ra in self.rationale2key if self.rationale2key[ra] >= 0]
                else:
                    all_keys = script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']
                    rationales = [self.key2rationale[ra] for ra in all_keys]
                script['branching_info']['rationale_gpt_output'] = self.predict_gpt_call(script, rationales)
                    
            # 1.2 dump to cache 
            cache_jsonl = self.cache_dir + 'GPTDecider_' + timestamp + '.jsonl'
            with open(cache_jsonl, 'w') as cache_file:
                for data in scripts:
                    cache_file.write(json.dumps(data))
                    cache_file.write('\n')
        else:
            # 1.3 load from cache
            scripts = util.load_jsonl(self.cache_dir + 'GPTDecider_' + self.config['checkpoint'] + '.jsonl')
        
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
            if self.multi_task:
                script['branching_info']['retrieval_result'] = {
                    'true_answ': script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'],
                    'text_results': retrieval_text_results,
                    'pred_answ': retrieval_key_results
                }
        return scripts
    
    def predict_gpt_call(self, script, rationales): #option_key):
        '''
        Get GPT output for a list of rationales
        Return a list of tuples [(rationale, gpt_outputs)]
        '''

        gpt_outputs = []
        for ra in rationales: 
            inference_prompt = self.pre_format_one_script_for_prompt(script, ra)
            
            # adjust wait_time for fine-tuning models
            if 'ft' in self.gpt_model:
                wait_time = 1
            else:
                wait_time = 0
            
            gpt_output = util.universal_gpt_call(
                inference_prompt, 
                config = {
                    'api_key': self.api_key,
                    'temperature': self.temperature,
                    'model': self.gpt_model,
                    'wait_time': wait_time
                })
            gpt_outputs.append((self.rationale2key[ra], gpt_output))
        return gpt_outputs

    def predict_gpt_output_parser(self, gpt_output):
        pred_text = gpt_output.strip().lower()
        pred_answ = 0
        # check if there is conclusion in the pred_text
        # if len(pred_text.split('- conclusion:')) > 1:
        #     if 'more favorable to pick option_1' in pred_text.split('- conclusion:')[1]:
        #         pred_answ = 1
        #     elif 'more favorable to pick option_2' in pred_text.split('- conclusion:')[1]:
        #         pred_answ = 2

        if len(re.findall('- choice:.+\n', pred_text)) > 0:
            tmp_choice = re.findall('- choice:.+\n', pred_text)[0]
            if 'option_1' in tmp_choice:
                pred_answ = 1
            elif 'option_2' in tmp_choice:
                pred_answ = 2
        return pred_text, pred_answ

    def init_prompt(self, train_scripts):
        self.base_prompts = {}
        self.script_visit_count = {}
        current_max_visit = 1
        hard_keys = [3, 4, 6, 9] # MAGIC NUMBER: keys with very few available samples
        for key in tqdm(self.key2rationale):
            if key < 0:
                continue
            pos_count = sum([key in script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'] for script in train_scripts])
            if self.num_shot > pos_count:
                tmp_num_shot = pos_count
            else:
                tmp_num_shot = self.num_shot

            ## select scripts
            pos_counter, neg_counter = 0, 0
            selected_scripts = []
            curr_idx = 0
            while len(selected_scripts) < tmp_num_shot * 2:
                if curr_idx == len(train_scripts):
                    current_max_visit += 1
                    curr_idx = 0
                    continue
                script = train_scripts[curr_idx]
                script_id = script['curr_index']
                count_valid = False
                if script_id in self.script_visit_count:
                    if self.script_visit_count[script_id] + 1 > current_max_visit:
                        curr_idx += 1
                        continue
                else:
                    self.script_visit_count[script_id] = 1
                
                if key in script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']:
                    if pos_counter < tmp_num_shot:
                        pos_counter += 1
                        if key not in hard_keys:
                            self.script_visit_count[script_id] += 1
                        selected_scripts.append(script)
                else:
                    if neg_counter < tmp_num_shot:
                        neg_counter += 1
                        self.script_visit_count[script_id] += 1
                        selected_scripts.append(script)
                curr_idx += 1
            
            # aggregate prompt based on selected scripts
            prompt = ''
            if self.prompt_type == 'cot':
                # for cot prompt, the main purpose is for export and manual annotations
                for script in selected_scripts:
                    if key in script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']:
                        prompt += '[+++++++++++]'
                        if key in script['branching_info']['op1_ra']:
                            option = 1
                        else:
                            option = 2
                        prompt += '{}\n\n###\n'.format(self.pre_format_one_script_for_prompt(script, self.key2rationale[key], option))
                    else:
                        prompt += '[-----------]'
                        prompt += '{}\n\n###\n'.format(self.pre_format_one_script_for_prompt(script, self.key2rationale[key], 0))
            elif self.prompt_type == 'naive':
                # for naive prompt, the purpose could be prompting or fine-tuning
                for script in selected_scripts:
                    if key in script['branching_info']['op1_ra']:
                        option = 1
                    elif key in script['branching_info']['op2_ra']:
                        option = 2
                    else:
                        option = 0
                    if self.multi_task or option != 0: 
                        prompt += '{}\n\n###\n'.format(self.pre_format_one_script_for_prompt(script, self.key2rationale[key], option))
            elif self.prompt_type == 'naive_agg':
                pass
            self.base_prompts[key] = prompt

            # save to file if it is required
            if self.config['save_prompt']:
                os.system('mkdir -p {} '.format(self.prompt_dir + self.model_name))
                for key in self.base_prompts:
                    file = open(self.prompt_dir + self.model_name + '/' + str(key) + '.txt', 'w')
                    file.write(self.base_prompts[key])
                    file.close()
        return 0

    
    def pre_format_one_script_for_prompt(self, script, rationale, answer = None): 
        if script['branching_info']['branching_idx'] == 0:
            previous_actions = 'None'
        else:
            previous_actions = ''
            for i in range(script['branching_info']['branching_idx']):
                event = script['steps'][i]
                previous_actions += ('\n{}. {}').format(i + 1, event)
        
        if self.prompt_type == 'cot':
            prompt = self.script_template.format(
                rationale,
                script['goal'],
                previous_actions,
                script['branching_info']['branching_step'],
                script['branching_info']['option 1'],
                script['branching_info']['option 2']
            )
            prompt += self.classification_questions[rationale]
            prompt += '\nANSWER\n- Reasoning: As marked at the beginning, we need to reason about "{}",'.format(rationale)
            if answer is not None:
                    if answer == 0:
                        prompt += '\n[ANSWER]\n- Reasoning:\n- Conclusion: Option_1 and Option_2 are NOT different in terms of {}.'.format(rationale)
                    elif answer == 1:
                        prompt += '\n[ANSWER]\n- Reasoning:\n- Conclusion: it is more favorable to pick Option_1 than Option_2 when it comes to {} .'.format(rationale)
                    elif answer == 2:
                        prompt += '\n[ANSWER]\n- Reasoning:\n- Conclusion: it is more favorable to pick Option_2 than Option_1 when it comes to {} .'.format(rationale)
        elif self.prompt_type == 'naive':
            prompt = self.script_template.format(
                rationale,
                script['goal'],
                previous_actions,
                script['branching_info']['branching_step'],
                script['branching_info']['option 1'],
                script['branching_info']['option 2']
            )
            prompt += self.classification_questions[rationale]
            if answer is not None:
                prompt += '\n- Answer\nWhen it comes to {}, '.format(rationale)
                if answer == 0:
                    prompt += 'Option_1 and Option_2 have very little difference.'
                    prompt += '\n- Choice: none'
                elif answer == 1:
                    prompt += 'Option_1 and Option_2 have differences; in particular, Option_1 is better in terms of {}'.format(rationale)
                    prompt += '\n- Choice: Option_1'
                elif answer == 2:
                    prompt += 'Option_1 and Option_2 have differences; in particular, Option_2 is better in terms of {}'.format(rationale)
                    prompt += '\n- Choice: Option_2'
        elif self.prompt_type == 'naive_agg':
            pass
        return prompt 


##########################################################
#################### GPT Retriever #####################
##########################################################
# baseline #2: Naive GPT
class GPTRetriever(BaseModel):
    """Implement the GPT retriever"""
    def __init__(self, config): #, model_name, prompt_dir, rationale2key = rationale2key, key2rationale = key2rationale):
        self.config = config

        # define model type and api_keys
        self.gpt_model = config['gpt_model'] if 'gpt_model' in config else 'davinci'
        if 'code' in self.gpt_model.lower():
            logger.warning("[GPTRetriever.__init__()] Using personal token")
            self.api_key = util.load_json(api_key_fp)['personal']
            self.wait_time = 12
        else:
            logger.warning("[GPTDecider.__init__()] Using ccb_group token")
            self.api_key = util.load_json(api_key_fp)['ccb_group']
            if 'ft' in self.gpt_model.lower():
                self.wait_time = 1
            else:
                self.wait_time = 0

        self.key2rationale = config['key2rationale']
        self.rationale2key = config['rationale2key']

        # prompt related attributes
        self.script_template = config['script_template']
        self.overview = config['overview']
        self.prompt_dir = rationale_prompt_dir #config['prompt_dir'] 
        self.model_name = config['model_name']
        self.prompt_path = self.prompt_dir + self.model_name + '.txt'
        self.temperature = config['temperature'] if 'temperature' in config else 0

        # other attributes
        # self.rationale_metadata = rationale_metadata
        self.debug = config['debug'] if 'debug' in config else False
        self.cache_dir = rationale_cache_dir + 'output/'

    def predict(self, orig_scripts): 
        ### 1. prompt for gpt output
        if 'checkpoint' not in self.config or self.config['checkpoint'] == '':
            # 1.0. make a deep copy as the results would be stored in the `scripts`
            scripts = copy.deepcopy(orig_scripts)

            # 1.1 gpt calls
            timestamp = util.get_current_timestamp()
            for script in tqdm(scripts):
                gpt_output = self.predict_gpt_call(script)
                script['branching_info']['retriever_gpt_output'] = gpt_output
            
            # 1.2 dump to cache 
            cache_jsonl = self.cache_dir + 'GPTRetriever_' + timestamp + '.jsonl'
            with open(cache_jsonl, 'w') as cache_file:
                for data in scripts:
                    cache_file.write(json.dumps(data))
                    cache_file.write('\n')
        else:
            scripts = util.load_jsonl(self.cache_dir + 'GPTRetriever_' + self.config['checkpoint'] + '.jsonl')
        
        ### 2. inference from gpt output
        # all_results = []
        for script in scripts:
            gpt_output = script['branching_info']['retriever_gpt_output']
            text_results, key_results = self.post_gpt_output_parser(gpt_output)
            script['branching_info']['retrieval_result'] = {
                'true_answ': script['branching_info']['op1_ra'] + script['branching_info']['op2_ra'],
                'text_results': text_results,
                'pred_answ': key_results
            }
        return scripts
        
    def predict_gpt_call(self, script):
        '''
        Get GPT output for one of the options
        Return one string (gpt outputs)
        '''
        inference_prompt = self.pre_format_one_script_for_prompt(script, with_answer = False)
        prompt = self.base_prompt + inference_prompt
        gpt_output = util.universal_gpt_call(
            prompt, 
            config = {
                'api_key': self.api_key,
                'model': self.gpt_model,
                'temperature': self.temperature, 
                'max_tokens': 100,
                'wait_time': self.wait_time
            }
        )
        return gpt_output

    def init_prompt(self, scripts = None):
        if scripts is None:
            try:
                self.base_prompt = util.load_txt_prompt(self.prompt_path)
            except:
                print('[ERROR] Prompt file not found!')
                return 1
            return 0
        else:
            if 'save_to_file' in self.config:
                save_to_file = self.config['save_to_file']
            else:
                save_to_file = False
            self.base_prompt = self.pre_make_base_prompt(scripts, save_to_file)
        return 0

    def pre_make_base_prompt(self, shots, save_to_file = False):
        '''
        Aggregate prompts for few-shot setting
        '''
        formatted_scripts = '\n###\n\n'.join(['# example {}'.format(i + 1) + self.pre_format_one_script_for_prompt(shots[i]) for i in range(len(shots))])
        prompt_text = self.overview + '\n\n' + formatted_scripts        
        if save_to_file:
            prompt_file = open(self.prompt_dir + self.model_name + '.txt', 'w')
            prompt_file.write(prompt_text)
            prompt_file.close()
        return prompt_text

    def pre_format_one_script_for_prompt(self, script, with_answer = True): 
        # 1. merge previous event
        if script['branching_info']['branching_idx'] == 0:
            previous_actions = 'None'
        else:
            previous_actions = ''
            for i in range(script['branching_info']['branching_idx']):
                event = script['steps'][i]
                previous_actions += ('\n{}. {}').format(i + 1, event)
        
        # 2. format script with template
        # 2.1 codex models
        if 'codex' in self.model_name:
            prompt = self.script_template.format(
                script['goal'],
                # previous_actions,
                script['branching_info']['branching_step'],
                script['branching_info']['option 1'],
                script['branching_info']['option 2']
            )
            if with_answer:
                all_relevant = script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']
                prompt += '\n[' + ', '.join(["'" + self.key2rationale[k] + "'" for k in all_relevant]) + ']'
            return prompt 
        
        # 2.2 gpt3 models
        if 'gpt3' in self.model_name:
            prompt = self.script_template.format(
                script['goal'],
                # previous_actions,
                script['branching_info']['branching_step'],
                script['branching_info']['option 1'],
                script['branching_info']['option 2']
            )
            if with_answer:
                all_relevant = script['branching_info']['op1_ra'] + script['branching_info']['op2_ra']
                if 'naive' in self.model_name:
                    prompt += '\n[' + ', '.join(["'" + self.key2rationale[k] + "'" for k in all_relevant]) + ']'
                elif 'answ_engineering' in self.model_name:
                    for k in all_relevant:
                        prompt += '\n- Option_1 and Optino_2 differ in terms of {}'.format(self.key2rationale[k])
                    # prompt += '\n[' + ', '.join(["'" + self.key2rationale[k] + "'" for k in all_relevant]) + ']'
            return prompt 

    def post_gpt_output_parser(self, gpt_output):
        if 'gpt3' in self.model_name:
            if 'naive' in self.model_name:
                pred_text_lst = gpt_output[2:-2].split("', '")
            elif 'answ_engineering' in self.model_name:
                pred_text_lst = []
                for line in gpt_output.split('\n'):
                    if 'Option_1 and Optino_2 differ in terms of' in line:
                        pred_text_lst.append(line.replace('- Option_1 and Optino_2 differ in terms of', '').strip())
        elif 'codex' in self.model_name:
            pred_text_lst = gpt_output[2:-2].split("', '")
            # pred_text_lst = gpt_output[1:-1].replace("'", "").split(', ')

        pred_text = np.unique([text for text in pred_text_lst if text in self.rationale2key])
        pred_keys = [self.rationale2key[text] if text in self.rationale2key else -1 for text in pred_text ]
        return list(pred_text), pred_keys



class TreeDecider(BaseModel):

    def __init__(self, config):
        self.config = config

        logger.warning("[TreeDecider.__init__()] Using ccb_group token")
        self.api_key = util.load_json(api_key_fp)['ccb_group']
        
        # general settings
        self.key2rationale = config['key2rationale']
        self.rationale2key = config['rationale2key']
        self.gpt_model = config['gpt_model'] if 'gpt_model' in config else 'davinci'
        self.multi_task = config['multi_task'] if 'multi_task' in config else False

        ## gpt parameters
        self.prompt_type = config['prompt_type'] if 'prompt_type' in config else 'naive'
        self.temperature = config['temperature'] if 'temperature' in config else 0.75

        # prompt related attributes
        self.overview = config['overview'] if 'overview' in config else ''
        self.script_template = config['script_template']
        self.classification_questions = config['classification_questions']
        self.prompt_dir = rationale_prompt_dir # from the env.py
        self.model_name = config['model_name']
        self.num_shot = config['num_shot'] if 'num_shot' in config else 3
        self.save_prompt = config['save_prompt'] if 'save_prompt' in config else False
        
        # other attributes
        self.debug = config['debug'] if 'debug' in config else False
        self.cache_dir = rationale_cache_dir + 'output/'

        # # adjust wait_time for fine-tuning models
        # if 'ft' in self.gpt_model:
        #     wait_time = 1
        # else:
        #     wait_time = 0


    def predict(self, orig_scripts):
        ### 1. prompt for gpt output
        if 'checkpoint' not in self.config or self.config['checkpoint'] == '':
            # 1.0. make a deep copy as the results would be stored in the `scripts`
            scripts = copy.deepcopy(orig_scripts)
            # 1.1 gpt calls
            timestamp = util.get_current_timestamp()
            ## TODO

            # 1.2 dump to cache 
            cache_jsonl = self.cache_dir + 'TreeDecider_' + timestamp + '.jsonl'
            with open(cache_jsonl, 'w') as cache_file:
                for data in scripts:
                    cache_file.write(json.dumps(data))
                    cache_file.write('\n')
        else:
            # 1.3 load from cache
            scripts = util.load_jsonl(self.cache_dir + 'GPTDecider_' + self.config['checkpoint'] + '.jsonl')
        
        ### 2. inference from gpt output
        for script in scripts:
            ## TODO
            pass

        return scripts
    
    def predict_gpt_call(self, script, rationales):
        '''
        Get GPT output for a list of rationales
        Return a list of tuples [(rationale, gpt_output_op1, gpt_output_op2, gpt_output_judge)]
        '''
        gpt_outputs = []
        for ra in rationales:
            inference_prompt_1 = ...##TODO #self.pre_format_one_script_for_prompt(script, ra)
            inference_prompt_2 = ...##TODO
            
            gpt_output_op1 = util.universal_gpt_call(
                inference_prompt_1, 
                config = {
                    'api_key': self.api_key,
                    'temperature': self.temperature,
                    'model': self.gpt_model,
                    # 'wait_time': wait_time
                })
            gpt_output_op2 = util.universal_gpt_call(
                inference_prompt_2, 
                config = {
                    'api_key': self.api_key,
                    'temperature': self.temperature,
                    'model': self.gpt_model,
                    # 'wait_time': wait_time
                })
            
            comparison_prompt = ... ##TODO
            gpt_output_judge = util.universal_gpt_call(
                comparison_prompt, 
                config = {
                    'api_key': self.api_key,
                    'temperature': self.temperature,
                    'model': self.gpt_model,
                    # 'wait_time': wait_time
                })
            gpt_outputs.append((self.rationale2key[ra], gpt_output_op1, gpt_output_op2, gpt_output_judge))

        return gpt_outputs
    
    def predict_gpt_output_parser(self, gpt_output):
        ##TODO
        pass
        # return pred_text, pred_answ

    def init_prompt(self, train_scripts):

        ## Part 1. explanation prompts
        self.prompt_explanation_scripts = {
            k: [
                script for script in train_scripts
                if 'cot_explanation' in script['branching_info'] and 
                k in script['branching_info']['cot_explanation']
            ]
            for k in self.rationale2key.keys()
        }
        self.prompt_explanation_str = {
            k: '\n###\n\n'.join([
                self.make_prompt_for_explanation(
                    script, 
                    k, 
                    answer = script['branching_info']['cot_explanation'][k][1]
                )
                for script in self.prompt_explanation_scripts[k]
            ])
            for k in self.prompt_explanation_scripts
        }
        
        ## Part 2. judgement prompts

    def make_prompt_for_explanation(self, script, rationale, answer = None):
        ##TODO
        pass 

    def make_prompt_for_judging(self, script, rationale, answer = None):
        ##TODO
        pass 
    


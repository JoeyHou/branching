###################################################
################### Codex - COT ###################
#################### Retrieval ####################
###################################################

code_cot_retrieval_script_template = """from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	
	def __init__(self):
		self.goal = {goal}
		self.current_step = {branching_step}
		self.option1 = {op1}
		self.option2 = {op2}
		self.decision_threshold = decision_threshold
	def check_rationale_relevance(self, rationale):
		'''
		Description: return whether or not the given rationale is relevant to the event
		input: 
			- rationale (str)
		output: 
			- True if the difference between two options are larger than the threshold, False otherwise
		'''"""
codex_cot_retrieval_template = {
	'script_template': code_cot_retrieval_script_template
}


###################################################
################### Codex - COT ###################
################# Classification ##################
###################################################
# self.previous_steps = [{prev_events}]
code_prompt_classification_script_template = """class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	
	def __init__(self):
		self.goal = {goal}
		self.current_step = {branching_step}
		self.option1 = {op1}
		self.option2 = {op2}
		self.related_rationale = [{related_rationale}]
	def choose_best_option(self, rationale):
		'''
		Description: return the most appropriate option given the rationale.
		input: 
			- rationale (str)
		output: 
			- the better option (from option1 and option2), return None if the difference does not matter
		'''
		if rationale not in self.related_rationale:
			# If a rationale is out of the scope of consideration, ignore it
			return None"""
codex_prompt_classification_template = {
	'script_template': code_prompt_classification_script_template,
}

###################################################
#################### Text - COT ###################
#################### Retrieval ####################
###################################################
# text_cot_retrieval_script_template = """CONTEXT
# - Goal: {goal}
# - Previous Actions: 
# {prev_events}
# CURRENT EVENT
# {branching_step}
# ALTERNATIVE OPTIONS
# - Option_1: {option1}
# - Option_2: {option2}
# QUESTION
# {question}
# ANSWER
# {answers}"""



###################################################
#################### Text - COT ###################
################# Classification ##################
###################################################
text_prompt_script_template = """CONTEXT
- Goal: {goal}
- Step: {branching_step}
- Option_1: {option1}
- Option_2: {option2}
RELATED RATIONALES
{related_rationales}
QUESTION
{question}
ANSWER"""
text_prompt_template = {
	'script_template': text_prompt_script_template,
	'classification_question': 'For every rationale in RELATED RATIONALES, which one of Option_1 and Option_2 is the better choice?',
	'retrieval_question': 'Does Option_1 and Option_2 have a difference in the following aspect?'
}



###################################################
############# Text - Comparison Prompts ###########
################# Classification ##################
###################################################
text_prompt_script_template_single_rationale = """
- Goal: {goal}
- Current step: {branching_step}
- Option_1: {option1}
- Option_2: {option2}
{conclusion}"""
text_prompt_single_ra_template = {
	'script_template': text_prompt_script_template_single_rationale,
	"[cost] effort / manpower": "{} is more effort-saving than {}, because:",
	"[cost] money / materials": "{} is more affordable than {}, because:",
	"[cost] time": "{} is more time-saving than {}, because:",
	"[outcome] emotional / physical rewards": "{} brings more benifit than {}, because:",
	"[outcome] more options / variety": "{} provides more potential options than {}, because:",
	"[outcome] reliability / certainty / chance of success": "{} is more reliable than {}, because:",
}

text_prompt_comparison_template = {
	'script_template': text_prompt_script_template_single_rationale,
	"[cost] effort / manpower": (
		"Which one is more effort-saving than the other one?",
		"{} is more effort-saving than {}"
	),
	"[cost] money / materials": (
		"Which one is more affordable than the other one?",  
		"{} is more affordable than {}"
	),
	"[cost] time": (
		"Which one is more time-saving than the other one?", 
		"{} is more time-saving than {}"
	),
	"[outcome] emotional / physical rewards": (
		"which one brings more benifit than the other one?", 
		"{} brings more benifit than {}"
	),
	"[outcome] more options / variety": (
		"Which one provides more potential options than the other one?", 
		"{} provides more potential options than {}"
	),
	"[outcome] reliability / certainty / chance of success": (
		"Which one is more reliable than the other one?", 
		"{} is more reliable than {}"
	)
}

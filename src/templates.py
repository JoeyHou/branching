

###################################################
################## Retrieval ######################
###################################################
gpt3_retrieval_overview = '''[[[PROBLEM OVERVIEW]]]
In our daily life, we always need to come up with reasonable rationales for our choices. Following are some rationale options for decision-making, followed by some examples of real-life scenarios. 
[RATIONALE BANK]
1. [cost] effort/manpower: requires less physical effort or other forms of manpower to excute
2. [cost] money/materials: requires spending less money, using less consumables or commodities to excute
3. [cost] time: requires less time to excute one of the options
4. [outcome] emotional/physical rewards: brings more happiness, lead to better lifestyle, facilitate mental/physical/relationship health
5. [outcome] facilitating subsequent events: makes next events easier to happen
6. [outcome] more options/variety: makes results more diverse, leading to wider selections
7. [outcome] personalized results: makes results more personalized, or customized to the person
8. [outcome] reliability/certainty/chance of success: makes the parent event more likely to success or increases the reliability of the overall theme event
9. [prerequisite] materialized(devices, equipments): requires specific devices/equipments/materials/vihicles to excute
10. [prerequisite] non-materialized(skills, knowledge, time): requires specific knowledge/experience/time/skill to excute
11. [prerequisite] outside support(people, environment): requires supports from people/environment/system/social context to excute
'''
gpt3_retrieval_script_template_naive = '''
[CONTEXT]
- Goal: {}
- Event: {}
[OPTIONS]
- Option_1: {}
- Option_2: {}
[QUESTION]
Consider the Option_1 and Option_2 from [OPTIONS], select from the [RATIONALE BANK] rationales that Option_1 and Option_2 have a huge difference (at most six):
[ANSWER]'''
# gpt3_retrieval_script_template_smart = '''
# [CONTEXT]
# - Goal: {}
# - Event: {}
# [OPTIONS]
# - Option_1: {}
# - Option_2: {}
# [QUESTION]
# Consider the Option_1 and Option_2 from [OPTIONS], select from the [RATIONALE BANK] rationales that Option_1 and Option_2 have a huge difference (at most six):
# [ANSWER]'''

###################################################
#################### Decider ######################
###################################################



###################################################
############### Chain-of-thoughts #################
###################################################
cot_topic_context = {

}
cot_script_template = '''
CONTEXT: 
{goal}
{previous_steps}

STEP: {branching_step}

OPTIONS: 
To achieve the STEP within the CONTEXT, there are two options:
- Option 1: {option_1}
- Option 2: {option_2}

KEY FACTOR: {rationale}, which means {rationale_context}

REASONING: 
Considering the factor of {rationale}, {option} is the better option because of the following reason:
{reasoning}
'''



###################################################
################### GPT - Naive ###################
################# Classification ##################
###################################################
gpt_naive_classification_questions = {
	'[cost] effort / manpower': "does one of the options requires less physical effort or other forms of manpower to excute while another does not?",
	'[cost] money / materials': "does one of the options requires spending less money, using less consumables or commodities to excute while another does not?",
	'[cost] time': "does one of the options requires less time to excute one of the options while another does not?",
	'[outcome] emotional / physical rewards': "does one of the options brings more happiness, lead to better lifestyle, facilitate mental/physical/relationship health while another does not?",
	'[outcome] facilitating subsequent events': "does one of the options makes next events easier to happen while another does not?",
	'[outcome] more options / variety': "does one of the options makes results more diverse, leading to wider selections while another does not?",
	'[outcome] personalized results': "does one of the options makes results more personalized, or customized to the person while another does not?",
	'[outcome] reliability / certainty / chance of success': "does one of the options makes the parent event more likely to success or increases the reliability of the overall theme event while another does not?",
	'[prerequisite] materialized (devices, equipments)': "does one of the options requires specific devices/equipments/materials/vihicles to excute while another does not?",
	'[prerequisite] non-materialized (skills, knowledge, time)': "does one of the options requires specific knowledge/experience/time/skill to excute while another does not?",
	'[prerequisite] outside support (people, environment)': "does one of the options requires supports from people/environment/system/social context to excute while another does not?"
}
gpt_naive_classification_overview = '''[[[PROBLEM OVERVIEW]]]
In our daily life, we always need to come up with reasonable rationales for our choices. Following are examples of rationale for decision-making. 
'''
gpt_naive_classification_script_template = '''
Topic: {}
CONTEXT
- Goal: {}
- Previous Actions: {}
PARENT EVENT
{}
BRANCHING OPTIONS
- Option_1: {}
- Option_2: {}
QUESTION
Consider the Option_1 and Option_2 from BRANCHING OPTIONS, answer the following question:
'''
# gpt_naive_classi_template = {
# 	"rationale_explanation": codex_naive_rationale_explanation,
# 	"script_template": codex_naive_classi_script_template
# }



###################################################
################## Codex - Naive ##################
################## Classification #################
###################################################
codex_naive_rationale_explanation = {
	'[cost] effort / manpower': 'physical effort or other forms of manpower to excute',
	'[cost] money / materials': 'the cost of money or concrete materials',
	'[cost] time': 'the time required to accomplish the goal',
	'[outcome] emotional / physical rewards': 'the emotional or physical rewards brought by the action, such as mental or physical health, relationshps, social recognition, self esteen, etc',
	'[outcome] facilitating subsequent events': 'the level of difficulty to carry out the next events after current events',
	'[outcome] more options / variety': 'the variaty and diversity of the possible choices and outcomes',
	'[outcome] personalized results': 'the level of personalization, such as personalized ads, products and services',
	'[outcome] reliability / certainty / chance of success': 'whether or not the intended goal can be achieved with successfully and reliably',
	'[prerequisite] materialized (devices, equipments)': 'requirements that is in concrete forms, such as devices, vihicles, and tools',
	'[prerequisite] non-materialized (skills, knowledge, time)': 'requirements that is not in concrete forms, such as skills, knowledge, and time',
	'[prerequisite] outside support (people, environment)': 'support or permission from the outside of us, such as natural or social environment, people, or institutions',
}

codex_naive_classi_script_template = """
goal = {goal} # overall goal
previous_events = [{prev_events}] # events that happened before
event = {branching_step} # step to decide on
option_1 = {op1} # 1st option
option_2 = {op2} # 2nd option
rationale = {rationale} # {rationale_explanation}
choice ="""

codex_naive_classi_template = {
	"rationale_explanation": codex_naive_rationale_explanation,
	"script_template": codex_naive_classi_script_template
}



###################################################
################## Codex - Codify #################
################## Classification #################
###################################################
codex_naive_rationale_explanation = {
	'[cost] effort / manpower': 'physical effort or other forms of manpower to excute',
	'[cost] money / materials': 'the cost of money or concrete materials',
	'[cost] time': 'the time required to accomplish the goal',
	'[outcome] emotional / physical rewards': 'the emotional or physical rewards brought by the action, such as mental or physical health, relationshps, social recognition, self esteen, etc',
	'[outcome] facilitating subsequent events': 'the level of difficulty to carry out the next events after current events',
	'[outcome] more options / variety': 'the variaty and diversity of the possible choices and outcomes',
	'[outcome] personalized results': 'the level of personalization, such as personalized ads, products and services',
	'[outcome] reliability / certainty / chance of success': 'whether or not the intended goal can be achieved with successfully and reliably',
	'[prerequisite] materialized (devices, equipments)': 'requirements that is in concrete forms, such as devices, vihicles, and tools',
	'[prerequisite] non-materialized (skills, knowledge, time)': 'requirements that is not in concrete forms, such as skills, knowledge, and time',
	'[prerequisite] outside support (people, environment)': 'support or permission from the outside of us, such as natural or social environment, people, or institutions',
}
codex_codify_overview = """
# python code
import commonsense_knowledge_base as ckb # this is a knowledege base with extremely good commonsense knowledge
class Event():
	def __init__(self, goal, all_steps, current_step, option_1, option_2):
		self.goal = goal # overall goal
		self.all_steps = all_steps # all steps so far
 		self.current_step = current_step # current step to work on
		self.option_1 = option_1 # 1st option
		self.option_2 = option_2 # 2nd option 
	def pick_best_option(self, rationale):
		# calculate the reward, cost, and constrains of picking each option
		context = ckb.build_context(self.goal, self.all_steps)
		option_1_score = ckb.get_reward(self.option_1, rationale, context) + ckb.get_cost(self.option_1, rationale, context) + ckb.get_constrain(self.option_1, rationale, context)
		option_2_score = ckb.get_reward(self.option_2, rationale, context) + ckb.get_cost(self.option_2, rationale, context) + ckb.get_constrain(self.option_2, rationale, context)
		# return the better option, based on the reward
		if option_1_score > option_2_score:
			return self.option_1
		elif option_1_score < option_2_score:
			return self.option_2
		else:
			return 'There is not much difference between option 1 and option 2'
"""
codex_codify_script_template = '''
goal = {goal} # overall goal
all_steps = [{prev_events}] # all steps so far
current_step = {branching_step} # step to decide on
option_1 = {op1} # 1st option
option_2 = {op2} # 2nd option
event = Event(goal, all_steps, current_step, option_1, option_2) # make event object
rationale = {rationale} # {rationale_explanation}
choice = event.pick_best_option(rationale)
print(choice)
# expected output:
#'''

codex_codif_template = {
	"rationale_explanation": codex_naive_rationale_explanation,
	"overview": codex_codify_overview,
	"script_template": codex_codify_script_template
}


###################################################
################### Codex - COT ###################
#################### Multitask ####################
###################################################


code_cot_script_templat = """
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	
	def __init__(self):
		self.goal = {goal}
		self.previous_steps = [{prev_events}]
		self.current_step = {branching_step}
		self.option1 = {op1}
		self.option2 = {op2}

	def choose_best_option(self, rationale):
		'''
		Description: return the most appropriate option given the rationale.
		input: 
			- rationale (str)
		output: 
			- the better option (from option1 and option2), return None if the difference does not matter
		'''
		"""
code_cot_rationale_template_pos = """if rationale == {rationale}:
			# [TODO] reasoning
			[TODO] assert(
			return self.{option}
		"""
code_cot_rationale_template_neg = """if rationale == {rationale}:
			# [TODO] reasoning
			return None
		"""


###################################################
############### Codex - Retrival Only #############
###################################################
codex_naive_rationale_explanation = {
	'[cost] effort / manpower': 'physical effort or other forms of manpower to excute',
	'[cost] money / materials': 'the cost of money or concrete materials',
	'[cost] time': 'the time required to accomplish the goal',
	'[outcome] emotional / physical rewards': 'the emotional or physical rewards brought by the action, such as mental or physical health, relationshps, social recognition, self esteen, etc',
	'[outcome] facilitating subsequent events': 'the level of difficulty to carry out the next events after current events',
	'[outcome] more options / variety': 'the variaty and diversity of the possible choices and outcomes',
	'[outcome] personalized results': 'the level of personalization, such as personalized ads, products and services',
	'[outcome] reliability / certainty / chance of success': 'whether or not the intended goal can be achieved with successfully and reliably',
	'[prerequisite] materialized (devices, equipments)': 'requirements that is in concrete forms, such as devices, vihicles, and tools',
	'[prerequisite] non-materialized (skills, knowledge, time)': 'requirements that is not in concrete forms, such as skills, knowledge, and time',
	'[prerequisite] outside support (people, environment)': 'support or permission from the outside of us, such as natural or social environment, people, or institutions',
}

codex_overview = '''
# python code
import commonsense_knowledge_base as ckb # this is a knowledege base with extremely good commonsense knowledge
class Event():
	def __init__(self, event, option_1, option_2):
		self.event = event
		self.option_1 = option_1
		self.option_2 = option_2 
		
	def get_rationale(self):
		related_rationales = []
		for rationale in self.rationale_list:
			relevant = ckb.is_relevant(self.event, rationale) # use commonsense knowledge to infer if the event and the rationale is related
			if relevant == True:
				related_rationales.append(rationale)
		return related_rationales
'''
codex_script_template = '''
event = """
- Theme: {}
- Event: {}
""" # context information about the event
option_1 = "{}" # first potential option
option_2 = "{}" # second potential option
e = Event(event, option_1, option_2) # make event object
print(e.get_rationale()) # get a list of rationales that's related to the event(e), based on knowledge from commonsense_knowledge_base
# expected output'''


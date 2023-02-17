from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'go back in time'
		self.previous_steps = ['1. decided to go back in time', '2. go to school for quantum mechanics', ]
		self.current_step = 'go to school for quantum mechanics'
		self.option1 = 'go to a class at a university'
		self.option2 = 'go to a class at a community college'
		self.decision_threshold = decision_threshold
	def check_rationale_relevance(self, rationale):
		'''
		Description: return whether or not the given rationale is relevant to the event
		input: 
			- rationale (str)
		output: 
			- True if the difference between two options are larger than the threshold, False otherwise
		'''
		if rationale == '[cost] effort / manpower':
			#
			#
			return True
		if rationale == '[cost] money / materials':
			#
			#
			return True
		if rationale == '[cost] time': 
			#
			#
			return True
		if rationale == '[outcome] emotional / physical rewards':
			#
			#
			return True
		if rationale == '[outcome] more options / variety':
			# 
			#
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			#
			#
			return True
from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'air out the musty basement'
		self.previous_steps = ['1. decided to air out the musty basement', '2. put breathing mask on', ]
		self.current_step = 'put breathing mask on'
		self.option1 = 'put on a reusable mask'
		self.option2 = 'put on an n-95 single-use mask'
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
			return False
		if rationale == '[cost] money / materials':
			# 
			#
			return True
		if rationale == '[cost] time':
			# 
			#
			return False
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
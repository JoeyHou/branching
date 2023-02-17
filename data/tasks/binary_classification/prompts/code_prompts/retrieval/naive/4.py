from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'buy milk from the store'
		self.previous_steps = ['1. decided to buy milk from the store', '2. decide which store to go to', ]
		self.current_step = 'decide which store to go to'
		self.option1 = 'go to the closest store'
		self.option2 = 'go to the store with the most options'
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
			return False
		if rationale == '[cost] time':
			# 
			#
			return True
		if rationale == '[outcome] emotional / physical rewards':
			# 
			#
			return False
		if rationale == '[outcome] more options / variety':
			# 
			#
			return True
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			#
			return True
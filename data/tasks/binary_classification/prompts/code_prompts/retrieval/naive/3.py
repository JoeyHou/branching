from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'place the skeleton on the counter'
		self.previous_steps = ['1. take the skeleton to the cashier', '2. get close to counter', '3. lift skeleton up', ]
		self.current_step = 'lift skeleton up'
		self.option1 = "life the skeleton on one's own"
		self.option2 = 'ask the cashier for help'
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
			return False
		if rationale == '[outcome] emotional / physical rewards':
			#
			#
			return False
		if rationale == '[outcome] more options / variety':
			#
			#
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			#
			#
			return True
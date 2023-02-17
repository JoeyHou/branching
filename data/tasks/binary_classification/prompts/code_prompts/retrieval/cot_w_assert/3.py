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
			assert abs(self.option1.on_ones_own.physical_effort - self.option2.ask_for_help.physical_effort) > self.decision_threshold
			return True
		if rationale == '[cost] money / materials':
			#
			assert abs(self.option1.on_ones_own.cost_of_money - self.option2.ask_for_help.cost_of_money) < self.decision_threshold
			return False
		if rationale == '[cost] time':
			#
			assert abs(self.option1.on_ones_own.cost_of_time - self.option2.ask_for_help.cost_of_time) < self.decision_threshold
			return False
		if rationale == '[outcome] emotional / physical rewards':
			#
			assert abs(self.option1.on_ones_own.rewards - self.option2.ask_for_help.rewards) < self.decision_threshold
			return False
		if rationale == '[outcome] more options / variety':
			#
			assert abs(self.option1.on_ones_own.variety - self.option2.ask_for_help.variety) < self.decision_threshold
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			#
			assert abs(self.option1.on_ones_own.success_rate - self.option2.ask_for_help.success_rate) > self.decision_threshold
			return True
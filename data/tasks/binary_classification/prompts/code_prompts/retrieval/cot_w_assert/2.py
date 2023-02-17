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
			assert abs(self.option1.reusable_mask.effort_to_put_on - self.option2.n_95_mask.effort_to_put_on) < self.decision_threshold
			return False
		if rationale == '[cost] money / materials':
			# 
			assert abs(self.option1.reusable_mask.cost_of_money - self.option2.n_95_mask.cost_of_money) > self.decision_threshold
			return True
		if rationale == '[cost] time':
			# 
			assert abs(self.option1.reusable_mask.cost_of_time - self.option2.n_95_mask.cost_of_time) < self.decision_threshold
			return False
		if rationale == '[outcome] emotional / physical rewards':
			# 
			assert abs(self.option1.reusable_mask.health_protection - self.option2.n_95_mask.health_protection) > self.decision_threshold
			return True
		if rationale == '[outcome] more options / variety':
			# 
			assert abs(self.option1.reusable_mask.available_choices - self.option2.n_95_mask.available_choices) < self.decision_threshold
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			assert abs(self.option1.reusable_mask.protection_reliability - self.option2.n_95_mask.protection_reliability) > self.decision_threshold
			return True
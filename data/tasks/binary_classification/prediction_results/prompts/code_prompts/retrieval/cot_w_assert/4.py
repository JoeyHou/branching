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
			assert abs(self.option1.closest_store.moving_effort - self.option2.store_with_most_options.moving_effort) > self.decision_threshold
			return True
		if rationale == '[cost] money / materials':
			# 
			assert abs(self.option1.closest_store.money_cost - self.option2.store_with_most_options.money_cost) < self.decision_threshold
			return False
		if rationale == '[cost] time':
			# 
			assert abs(self.option1.closest_store.moving_time - self.option2.store_with_most_options.moving_time) > self.decision_threshold
			return True
		if rationale == '[outcome] emotional / physical rewards':
			# 
			assert abs(self.option1.closest_store.rewards - self.option2.store_with_most_options.rewards) < self.decision_threshold
			return False
		if rationale == '[outcome] more options / variety':
			# 
			assert abs(self.option1.closest_store.choice_of_milk_available - self.option2.store_with_most_options.choice_of_milk_available) > self.decision_threshold
			return True
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			assert abs(self.option1.closest_store.overall_reliability - self.option2.store_with_most_options.overall_reliability) > self.decision_threshold
			return True
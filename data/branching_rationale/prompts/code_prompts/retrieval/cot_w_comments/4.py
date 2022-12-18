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
			# In most cases, the human effort required for going to the closest store is less than going to the one with the most options, making the first one the better option.
			assert abs(self.option1.closest_store.moving_effort - self.option2.store_with_most_options.moving_effort) > self.decision_threshold
			return True
		if rationale == '[cost] money / materials':
			# In most cases, the money or materials required to go to the closest store and to go to the one with the most options are the same: neither of them cost any money!
			assert abs(self.option1.closest_store.money_cost - self.option2.store_with_most_options.money_cost) < self.decision_threshold
			return False
		if rationale == '[cost] time':
			# In most cases, the time required for going to the closest store is less than going to the one with the most options, making the first one the better option.
			assert abs(self.option1.closest_store.moving_time - self.option2.store_with_most_options.moving_time) > self.decision_threshold
			return True
		if rationale == '[outcome] emotional / physical rewards':
			# In most cases, the emotional or physical rewards bring up by going to the closest store and going to the one with the most options do not differ by too much: neither of them provide any reward
			assert abs(self.option1.closest_store.rewards - self.option2.store_with_most_options.rewards) < self.decision_threshold
			return False
		if rationale == '[outcome] more options / variety':
			# In most cases, going to the store with the most options would have more choices of milk while going to the closest store would have limited options.
			assert abs(self.option1.closest_store.choice_of_milk_available - self.option2.store_with_most_options.choice_of_milk_available) > self.decision_threshold
			return True
		if rationale == '[outcome] reliability / certainty / chance of success':
			# Buying the milk is the goal here. In most cases, going to the store with the most options would make the overall goal: buy milk from the store, more likely to success. It is also more reliable.
			assert abs(self.option1.closest_store.overall_reliability - self.option2.store_with_most_options.overall_reliability) > self.decision_threshold
			return True
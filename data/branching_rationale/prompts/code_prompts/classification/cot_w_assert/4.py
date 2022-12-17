
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	
	def __init__(self):
		self.goal = 'buy milk from the store'
		self.previous_steps = ['1. decided to buy milk from the store', '2. decide which store to go to', ]
		self.current_step = 'decide which store to go to'
		self.option1 = 'go to the closest store'
		self.option2 = 'go to the store with the most options'
		self.related_rationale = [
			'[cost] effort / manpower', # require less human effort
			'[cost] time', # save time
			'[outcome] reliability / certainty / chance of success', # higher chance of success
			'[outcome] more options / variety' # more options in future steps
		] # we only consider these rationales in our decision process
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
			return None
		if rationale == '[cost] effort / manpower':
			# 
			assert (self.option1.closest_store.effort_getting_destination < self.option2.store_with_most_options.effort_getting_destination)
			return self.option1
		if rationale == '[cost] time':
			# 
			assert (self.option1.closest_store.time_getting_destination < self.option2.store_with_most_options.time_getting_destination)
			return self.option1
		if rationale == '[outcome] more options / variety':
			# 
			assert (self.option1.closest_store.choice_of_milk_available < self.option2.store_with_most_options.choice_of_milk_available)
			return self.option2
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			assert (self.option1.closest_store.overall_reliability < self.option2.store_with_most_options.overall_reliability)
			return self.option2
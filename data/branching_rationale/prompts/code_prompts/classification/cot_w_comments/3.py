class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'place the skeleton on the counter'
		self.previous_steps = ['1. take the skeleton to the cashier', '2. get close to counter', '3. lift skeleton up', ]
		self.current_step = 'lift skeleton up'
		self.option1 = "lift the skeleton on one's own"
		self.option2 = 'ask the cashier for help'
		self.related_rationale = [
			'[cost] effort / manpower', # require less human effort
			'[outcome] reliability / certainty / chance of success' # higher chance of success
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
			# In most cases, the human effort required for lifting a skeleton on one's own is more than doing it with the help of others, making the later one the better option.
			assert (self.option1.on_ones_own.physical_effort > self.option2.ask_for_help.physical_effort)
			return self.option2
		if rationale == '[outcome] reliability / certainty / chance of success':
			# Lifting up the item is the goal here. In most cases, lifting an item with the help of others would more likely to success than doing it on one's own, making the second option more promising
			assert (self.option1.on_ones_own.success_rate < self.option2.ask_for_help.success_rate)
			return self.option2
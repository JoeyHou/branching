class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'place the skeleton on the counter'
		self.previous_steps = ['1. take the skeleton to the cashier', '2. get close to counter', '3. lift skeleton up', ]
		self.current_step = 'lift skeleton up'
		self.option1 = "life the skeleton on one's own"
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
			# 
			#
			return self.option2
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			#
			return self.option2

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
			#
			return self.option1
		if rationale == '[cost] time':
			# 
			#
			return self.option1
		if rationale == '[outcome] more options / variety':
			# 
			#
			return self.option2
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			#
			return self.option2
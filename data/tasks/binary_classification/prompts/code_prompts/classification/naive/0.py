class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.	
	def __init__(self):
		self.goal = 'go out for a picnic'
		self.previous_steps = ['1. decided to go out for a picnic', '2. take a shower', '3. get ready for the day', '4. get in the car', '5. drive to the park', '6. park the car', ]
		self.current_step = 'park the car'
		self.option1 = 'park along the street'
		self.option2 = 'try to park inside the park'
		self.related_rationale = [
			'[cost] money / materials', # save money
			'[outcome] more options / variety', # more options in future steps
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
		if rationale == '[cost] money / materials':
			# 
			#
			return self.option1
		if rationale == '[outcome] more options / variety':
			# 
			#
			return self.option1
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			#
			return self.option2
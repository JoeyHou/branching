class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.	
	def __init__(self):
		self.goal = 'air out the musty basement'
		self.previous_steps = ['1. decided to air out the musty basement', '2. put breathing mask on', ]
		self.current_step = 'put breathing mask on'
		self.option1 = 'put on a reusable mask'
		self.option2 = 'put on an n-95 single-use mask'
		self.related_rationale = [
			'[cost] money / materials', # save money
			'[outcome] emotional / physical rewards', # provide extra rewards to people
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
			# In most cases, a reusable mask would cost much less than an n-95 single-use mask, not to mention a reusable mask can be reused and save more.
			assert (self.option1.reusable_mask.cost_of_money < self.option2.n_95_mask.cost_of_money)
			return self.option1
		if rationale == '[outcome] emotional / physical rewards':
			# In most cases, wearing an n-95 mask would provide more protection against the environment than wearing a reusable mask, making the first option more healthy
			assert (self.option1.reusable_mask.health_protection < self.option2.n_95_mask.health_protection)
			return self.option1
		if rationale == '[outcome] reliability / certainty / chance of success':
			# Protect ourselves with mask is the goal here. In most cases, wearing an n-95 mask would provide more protection against the environment than wearing a reusable mask, making the first option more reliable
			assert (self.option2.reusable_mask.protection_reliability > self.option1.n_95_mask.protection_reliability)
			return self.option2
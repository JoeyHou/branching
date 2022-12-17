class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'start practicing with friends'
		self.previous_steps = ['1. learn how to play football', '2. contact friends to set up a time', ]
		self.current_step = 'contact friends to set up a time'
		self.option1 = 'make a public post about playing football in facebook group'
		self.option2 = 'call friends one at a time to see their available time'
		self.related_rationale = [
			'[cost] effort / manpower', # require less human effort
			'[cost] time', # save time
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
			assert (self.option1.social_media.effort_to_contact_friends < self.option2.phone_call.effort_to_contact_friends)
			return self.option1
		if rationale == '[cost] time':
			# 
			assert (self.option1.social_media.cost_of_time < self.option2.phone_call.cost_of_time)
			return self.option1
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			assert (self.option2.social_media.reliability_of_communication > self.option1.phone_call.reliability_of_communication)
			return self.option2

		
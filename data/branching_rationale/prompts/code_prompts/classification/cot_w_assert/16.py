class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.	
	def __init__(self):
		self.goal = 'go back in time'
		self.previous_steps = ['1. decided to go back in time', '2. go to school for quantum mechanics', ]
		self.current_step = 'go to school for quantum mechanics'
		self.option1 = 'go to a class at a university'
		self.option2 = 'go to a class at a community college'
		self.related_rationale = [
			'[cost] effort / manpower', # require less human effort
			'[cost] money / materials', # save money
			'[cost] time', # save time
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
		if rationale == '[cost] effort / manpower':
			# 
			assert (self.option1.university.effort_to_study > self.option2.community_college.effort_to_study)
			return self.option2
		if rationale == '[cost] money / materials':
			# 
			assert (self.option1.university.tuition_cost > self.option2.community_college.tuition_cost)
			return self.option2
		if rationale == '[cost] time': 
			# 
			assert (self.option1.university.graduation_time > self.option2.community_college.graduation_time)
			return self.option2
		if rationale == '[outcome] emotional / physical rewards':
			# 
			assert (self.option1.university.sense_of_achievement > self.option2.community_college.sense_of_achievement)
			return self.option1
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			assert (self.option1.university.knowledge_taught > self.option2.community_college.knowledge_taught)
			return self.option1
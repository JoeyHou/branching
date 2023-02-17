from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'go back in time'
		self.previous_steps = ['1. decided to go back in time', '2. go to school for quantum mechanics', ]
		self.current_step = 'go to school for quantum mechanics'
		self.option1 = 'go to a class at a university'
		self.option2 = 'go to a class at a community college'
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
			assert abs(self.option1.university.effort_to_study - self.option2.community_college.effort_to_study) > self.decision_threshold
			return True
		if rationale == '[cost] money / materials':
			#
			assert abs(self.option1.university.tuition_cost - self.option2.community_college.tuition_cost) > self.decision_threshold
			return True
		if rationale == '[cost] time': 
			#
			assert abs(self.option1.university.graduation_time - self.option2.community_college.graduation_time) > self.decision_threshold
			return True
		if rationale == '[outcome] emotional / physical rewards':
			#
			assert abs(self.option1.university.sense_of_achievement - self.option2.community_college.sense_of_achievement) > self.decision_threshold
			return True
		if rationale == '[outcome] more options / variety':
			# 
			assert abs(self.option1.university.choice_available - self.option2.community_college.choice_available) < self.decision_threshold
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			#
			assert abs(self.option1.university.knowledge_taught - self.option2.community_college.knowledge_taught) > self.decision_threshold
			return True
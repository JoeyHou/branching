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
			# In most cases, the human effort required for going to a class at a university is more than that of going to a class at a community college.
			assert abs(self.option1.university.effort_to_study - self.option2.community_college.effort_to_study) > self.decision_threshold
			return True
		if rationale == '[cost] money / materials':
			# In most cases, the money or materials required for a university is more than that for a community college
			assert abs(self.option1.university.tuition_cost - self.option2.community_college.tuition_cost) > self.decision_threshold
			return True
		if rationale == '[cost] time': 
			# In most cases, the time required for going to a university (around 4 years) is more than that of going to a community college (around 2 years).
			assert abs(self.option1.university.graduation_time - self.option2.community_college.graduation_time) > self.decision_threshold
			return True
		if rationale == '[outcome] emotional / physical rewards':
			# In most cases, the emotional rewards bring up by going to a university is more than going to a community college since the first one makes people feel more prouded and sense of achievement
			assert abs(self.option1.university.sense_of_achievement - self.option2.community_college.sense_of_achievement) > self.decision_threshold
			return True
		if rationale == '[outcome] more options / variety':
			# In most cases, the availability of university or community college depends on the location, which makes it hard to conclude with one has more options or varieties.
			assert abs(self.option1.university.choice_available - self.option2.community_college.choice_available) < self.decision_threshold
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			# go back in time is the goal here. In most cases, go to university would provide more in depth knowledge about quantum mechanics than community colleges, making the option 1 more reliable
			assert abs(self.option1.university.knowledge_taught - self.option2.community_college.knowledge_taught) > self.decision_threshold
			return True
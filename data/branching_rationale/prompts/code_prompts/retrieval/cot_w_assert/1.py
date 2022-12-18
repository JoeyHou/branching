from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'start practicing with friends'
		self.previous_steps = ['1. learn how to play football', '2. contact friends to set up a time', ]
		self.current_step = 'contact friends to set up a time'
		self.option1 = 'make a public post about playing football in facebook group'
		self.option2 = 'call friends one at a time to see their available time'
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
			assert abs(self.option1.social_media.effort_to_contact_friends - self.option2.phone_call.effort_to_contact_friends) > self.decision_threshold
			return True
		if rationale == '[cost] money / materials':
			# 
			assert abs(self.option1.social_media.cost_of_money - self.option2.phone_call.cost_of_money) < self.decision_threshold
			return False
		if rationale == '[cost] time':
			# 
			assert abs(self.option1.social_media.cost_of_time - self.option2.phone_call.cost_of_time) > self.decision_threshold
			return True
		if rationale == '[outcome] emotional / physical rewards':
			# 
			assert abs(self.option1.social_media.rewards - self.option2.phone_call.rewards) < self.decision_threshold
			return False
		if rationale == '[outcome] more options / variety':
			# 
			assert abs(self.option1.social_media.available_choices - self.option2.phone_call.available_choices) < self.decision_threshold
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			assert abs(self.option1.social_media.reliability_of_communication - self.option2.phone_call.reliability_of_communication) > self.decision_threshold
			return True
		
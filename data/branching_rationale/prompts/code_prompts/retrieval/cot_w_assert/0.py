from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'go out for a picnic'
		self.previous_steps = ['1. decided to go out for a picnic', '2. take a shower', '3. get ready for the day', '4. get in the car', '5. drive to the park', '6. park the car', ]
		self.current_step = 'park the car'
		self.option1 = 'park along the street'
		self.option2 = 'try to park inside the park'
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
			assert abs(self.option1.street.effort_for_parking - self.option2.inside_the_park.effort_for_parking) < self.decision_threshold
			return False
		if rationale == '[cost] money / materials':
			#
			assert abs(self.option1.street.cost_of_parking - self.option2.inside_the_park.cost_of_parking) > self.decision_threshold
			return True
		if rationale == '[cost] time':
			#
			assert abs(self.option1.street.time_for_parking - self.option2.inside_the_park.time_for_parking) < self.decision_threshold
			return False
		if rationale == '[outcome] emotional / physical rewards':
			#
			assert abs(self.option1.street.reward_of_parking - self.option2.inside_the_park.reward_of_parking) < self.decision_threshold
			return False
		if rationale == '[outcome] more options / variety':
			#
			assert abs(self.option1.street.choice_of_parking_space - self.option2.inside_the_park.choice_of_parking_space) > self.decision_threshold
			return True
		if rationale == '[outcome] reliability / certainty / chance of success':
			#
			assert abs(self.option1.street.overall_reliability - self.option2.inside_the_park.overall_reliability) > self.decision_threshold
			return True
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
			#
			return False
		if rationale == '[cost] money / materials':
			#
			#
			return True
		if rationale == '[cost] time':
			#
			#
			return False
		if rationale == '[outcome] emotional / physical rewards':
			#
			#
			return False
		if rationale == '[outcome] more options / variety':
			#
			#
			return True
		if rationale == '[outcome] reliability / certainty / chance of success':
			#
			#
			return True
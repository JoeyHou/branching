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
			#
			return True
		if rationale == '[cost] money / materials':
			# 
			#
			return False
		if rationale == '[cost] time':
			# 
			#
			return True
		if rationale == '[outcome] emotional / physical rewards':
			# 
			#
			return False
		if rationale == '[outcome] more options / variety':
			# 
			#
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			# 
			#
			return True
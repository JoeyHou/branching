from commonsense_knowledge_base import decision_threshold
class Procedure:
	# Given two options to perform an action, choose the most appropriate one based on some rationale.
	def __init__(self):
		self.goal = 'place the skeleton on the counter'
		self.previous_steps = ['1. take the skeleton to the cashier', '2. get close to counter', '3. lift skeleton up', ]
		self.current_step = 'lift skeleton up'
		self.option1 = "life the skeleton on one's own"
		self.option2 = 'ask the cashier for help'
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
			# In most cases, the human effort required for lifting a skeleton on one's own is more than doing it with the help of others, making the later one the better option.
			assert abs(self.option1.on_ones_own.physical_effort - self.option2.ask_for_help.physical_effort) > self.decision_threshold
			return True
		if rationale == '[cost] money / materials':
			# In most cases, the money or materials required to lift the skeleton on one's own and to ask the cashier for help are the same: neither of them cost any money!
			assert abs(self.option1.on_ones_own.cost_of_money - self.option2.ask_for_help.cost_of_money) < self.decision_threshold
			return False
		if rationale == '[cost] time':
			# In most cases, the time required to lift the skeleton on one's own and to ask the cashier for help does not differ by too much: both of them costs a few seconds.
			assert abs(self.option1.on_ones_own.cost_of_time - self.option2.ask_for_help.cost_of_time) < self.decision_threshold
			return False
		if rationale == '[outcome] emotional / physical rewards':
			# In most cases, the emotional or physical rewards bring up by lifting the skeleton on one's own and to ask the cashier do not differ by too much: neither of them provide any reward
			assert abs(self.option1.on_ones_own.rewards - self.option2.ask_for_help.rewards) < self.decision_threshold
			return False
		if rationale == '[outcome] more options / variety':
			# In most cases, neither lifting the skeleton on one's own or asking the cashier for help could provide much variety in terms of options or outcome: for both of them, there only one way of doing that.
			assert abs(self.option1.on_ones_own.variety - self.option2.ask_for_help.variety) < self.decision_threshold
			return False
		if rationale == '[outcome] reliability / certainty / chance of success':
			# Lifting up the item is the goal here. In most cases, lifting an item with the help of others would more likely to success than doing it on one's own, making the second option more promising
			assert abs(self.option1.on_ones_own.success_rate - self.option2.ask_for_help.success_rate) > self.decision_threshold
			return True
class Procedure:
  """Given two options to perform an action, choose the most appropriate one based on some rationale."""
  def __init__(self):
    self.goal = "Have a picnic at the park"
    self.previous_steps = ["Decide on a destination", "Pack", "Drive to the park"]
    self.current_step = "Find parking at the busy park"
    self.option0 = "Park in a garage"
    self.option1 = "Park at curbside"
  def choose_best_option(self, rationale):
    """Return the most appropriate option given the rationale."""
    if (rationale == 'save money'):
      return self.option1
    if (rationale == 'save time'):
      return self.option0
    if (rationale == 'emotion'):
      return None
    if (rationale == 'something irrelevant'):
      return None
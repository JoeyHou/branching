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
      # Parking meters at the curbside usually charge a lot less than garages.
      assert(option1.cost_for_parking < option0.cost_for_parking)
      return self.option1
    if (rationale == 'save time'):
      # Near a busy park, curbside parking is usually limited, so time will be spent searching for a spot. However, there is usually more spots in the garage.
      assert(option0.time_to_find_parking < option1.time_to_find_parking)
      return self.option0
    if (rationale == 'emotion'):
      return None
    if (rationale == 'something irrelevant'):
      return None
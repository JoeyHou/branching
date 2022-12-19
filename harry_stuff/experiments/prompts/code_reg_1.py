def choose_best_option(goal, step, rationale):
    # goal: "watch a movie at the cinema"
    # step: "park the car"
    options = ["park on the street", "park at a garage"]
    if rationale == "save money":
        return options[0]
    elif rationale == "convenient":
        return options[1]
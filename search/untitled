# Fail Admissible
def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.
    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.
    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.
    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.
    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.
    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state

    "*** YOUR CODE HERE ***"
    currentState = actualState = state[0]
    remainingFood = state[1].asList()
    heuristics = []

        distance, food = max([(util.manhattanDistance(currentState, c), c) for c in remainingFood])
        heuristics += [distance]
        currentState = food
        remainingFood.remove(food)

    return sum(heuristics)
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import math

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state
        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    closed = []
    fringe = util.Stack()
    currentState = problem.getStartState()
    levelNum = 0 
    fringe.push((levelNum,(currentState, None, 0)))
    route = []    #[(level #, dir)]
    while not fringe.isEmpty():
        currentStateCap = fringe.pop()
        currentState = currentStateCap[1]
        currentStateLevel = currentStateCap[0]
        if problem.isGoalState(currentState[0]):
            rtn = [d for (l, d) in route if d is not None] + [currentState[1]]
            return rtn
        if levelNum > currentStateLevel:
            route = [(l, d) for (l , d) in route if l < currentStateLevel]
        
        if currentState[0] not in closed:
            closed.append(currentState[0])
            levelNum = currentStateLevel + 1
            route += [(currentStateLevel, currentState[1])]
            for child_state in problem.getSuccessors(currentState[0]):
                fringe.push((levelNum, child_state))
    return []
    
def getPath(node):
    path = []
    nextNode = node
    while nextNode is not None:
        path = [nextNode[0][1]] + path
        nextNode = nextNode[1]
    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed = []
    fringe = util.Queue()
    currentState = problem.getStartState()
    closed.append(currentState)
    # If the currentState is the goal, return no action
    if problem.isGoalState(currentState):
        return []
    # Add root's successors to the fringe
    for child_state in problem.getSuccessors(currentState):
        fringe.push((child_state, None))
    
    while (fringe.isEmpty() == False):
        currentStateNode = fringe.pop() 
        currentState = currentStateNode[0]  # state for expansion
        
        # If the currentState is the goal, return the path
        if problem.isGoalState(currentState[0]):
            rtn = getPath(currentStateNode)
            return rtn
        # Look for the soln along the currentState
        if currentState[0] not in closed:
            closed.append(currentState[0])
            for child_state in problem.getSuccessors(currentState[0]):
                fringe.push((child_state, currentStateNode))
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    closed = []             
    fringe = util.PriorityQueue()     
    currentState = problem.getStartState()
    closed.append(currentState)
    # If the currentState is the goal, return no action
    if problem.isGoalState(currentState):
        return []
    # Add root's successors to the fringe
    for child_state in problem.getSuccessors(currentState):
        cost = child_state[2]
        fringe.push((child_state, None, cost), cost)
    
    while (fringe.isEmpty() == False):
        currentStateNode = fringe.pop() 
        currentState = currentStateNode[0]  # state for expansion
        stepCost = currentStateNode[2]      # accumulated cost up to the current state
        # If the currentState is the goal, return the path
        if problem.isGoalState(currentState[0]):
            return getPath(currentStateNode)
        # Look for the soln along the currentState
        if currentState[0] not in closed:
            closed.append(currentState[0])
            for child_state in problem.getSuccessors(currentState[0]):
                cost = stepCost+child_state[2]
                fringe.push((child_state, currentStateNode, cost), cost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    closed = []
    fringe = util.PriorityQueue()
    currentState = problem.getStartState()
    closed.append(currentState)
    # If the currentState is the goal, return no action
    if problem.isGoalState(currentState):
        return []
    # Add root's successors to the fringe
    for child_state in problem.getSuccessors(currentState):
        cost = child_state[2]
        fringe.push((child_state, None, cost), cost + heuristic(child_state[0], problem))
    
    while (fringe.isEmpty() == False):
        currentStateNode = fringe.pop() 
        currentState = currentStateNode[0]  # state for expansion
        stepCost = currentStateNode[2]      # accumulated cost up to the current state
        # If the currentState is the goal, return the path
        if problem.isGoalState(currentState[0]):
            return getPath(currentStateNode)
        # Look for the soln along the currentState
        if currentState[0] not in closed:
            closed.append(currentState[0])
            for child_state in problem.getSuccessors(currentState[0]):
                cost = stepCost+child_state[2]
                fringe.push((child_state, currentStateNode, cost), cost + heuristic(child_state[0], problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
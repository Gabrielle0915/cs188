# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import time

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        currentGhostStates = currentGameState.getGhostStates()
        currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
        newGhostPositions = successorGameState.getGhostPositions()
        currentGhostPositions = currentGameState.getGhostPositions()

        sumGhostDistances = []
        foodList = newFood.asList()
        foodDistance = 0
        ghostAround = False
        scoreDifference = successorGameState.getScore() - currentGameState.getScore()
        additionalFactor = 0

        for i in range(0, len(newGhostPositions)):
            ghostDistance = util.manhattanDistance(newGhostPositions[i], newPos)
            sumGhostDistances += [ghostDistance]
            if newScaredTimes[i] == 0 and ghostDistance < 4:
                ghostAround = True
        
        if action == Directions.STOP:
            additionalFactor -= 5
        
        if currentScaredTimes.count(0) < newScaredTimes.count(0):
            additionalFactor += 5
        
        if ghostAround:
            return additionalFactor + min(sumGhostDistances) + scoreDifference
        
        if len(foodList) > 0:
            distance, closestFood = min([(util.manhattanDistance(newPos, food), food) for food in foodList])
            if distance != 0:
                foodDistance = 0 - distance
            else:
                foodDistance = 10
        
        if currentGameState.getNumFood() > successorGameState.getNumFood():
            additionalFactor += 100
        
        return foodDistance + scoreDifference + additionalFactor 

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
          gameState.isWin():
            Returns whether or not the game state is a winning state
          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, myDepth, agentIndex, numGhost):
            if gameState.isLose() or gameState.isWin() or myDepth == 0:
                return self.evaluationFunction(gameState)
            v = - float("inf")
            legalMoves = gameState.getLegalActions(0)
            for action in legalMoves:
                successorState = gameState.generateSuccessor(0, action)
                v = max(v, minValue(successorState, myDepth, 1, numGhost))
            return v

        def minValue(gameState, myDepth, agentIndex, numGhost):
            if gameState.isLose() or gameState.isWin() or myDepth == 0:
                return self.evaluationFunction(gameState)
            v = float("inf")
            legalMoves = gameState.getLegalActions(agentIndex)
            for action in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numGhost:
                    v = min(v, maxValue(successorState, myDepth - 1, agentIndex + 1, numGhost))
                else:
                    v = min(v, minValue(successorState, myDepth, agentIndex + 1, numGhost))
            return v
    
        legalMoves = gameState.getLegalActions()
        numGhost = gameState.getNumAgents() - 1
        bestScore = -float("inf")
        bestAction = Directions.STOP
        for action in legalMoves:
            successorState = gameState.generateSuccessor(0, action)
            score = max(bestScore, minValue(successorState, self.depth, 1, numGhost))
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, myDepth, agentIndex, numGhost, myAlpha, myBeta):
            if gameState.isLose() or gameState.isWin() or myDepth == 0:
                return self.evaluationFunction(gameState)
            v = - float("inf")
            legalMoves = gameState.getLegalActions(0)
            for action in legalMoves:
                successorState = gameState.generateSuccessor(0, action)
                v = max(v, minValue(successorState, myDepth, 1, numGhost, myAlpha, myBeta))
                if v > myBeta:
                    return v
                myAlpha = max(myAlpha, v)
            return v

        def minValue(gameState, myDepth, agentIndex, numGhost, myAlpha, myBeta):
            if gameState.isLose() or gameState.isWin() or myDepth == 0:
                return self.evaluationFunction(gameState)
            v = float("inf")
            legalMoves = gameState.getLegalActions(agentIndex)
            for action in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numGhost:
                    v = min(v, maxValue(successorState, myDepth - 1, agentIndex + 1, numGhost, myAlpha, myBeta))
                else:
                    v = min(v, minValue(successorState, myDepth, agentIndex + 1, numGhost, myAlpha, myBeta))
                if v < myAlpha:
                    return v
                myBeta = min(myBeta, v)
            return v
    
        legalMoves = gameState.getLegalActions()
        numGhost = gameState.getNumAgents() - 1
        bestScore = -float("inf")
        bestAction = Directions.STOP
        alpha = -float("inf")
        beta = float("inf")
        for action in legalMoves:
            successorState = gameState.generateSuccessor(0, action)
            score = max(bestScore, minValue(successorState, self.depth, 1, numGhost, alpha, beta))
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(score, alpha)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, myDepth, agentIndex, numGhost):
            if gameState.isLose() or gameState.isWin() or myDepth == 0:
                return self.evaluationFunction(gameState)
            v = - float("inf")
            legalMoves = gameState.getLegalActions(0)
            for action in legalMoves:
                successorState = gameState.generateSuccessor(0, action)
                v = max(v, expValue(successorState, myDepth, 1, numGhost))
            return v

        def expValue(gameState, myDepth, agentIndex, numGhost):
            if gameState.isLose() or gameState.isWin() or myDepth == 0:
                return self.evaluationFunction(gameState)
            v = 0
            legalMoves = gameState.getLegalActions(agentIndex)
            for action in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numGhost:
                    v = v + maxValue(successorState, myDepth - 1, agentIndex + 1, numGhost)
                else:
                    v = v + expValue(successorState, myDepth, agentIndex + 1, numGhost)
            return v/len(legalMoves)
    
        legalMoves = gameState.getLegalActions()
        numGhost = gameState.getNumAgents() - 1
        bestScore = -float("inf")
        bestAction = Directions.STOP
        for action in legalMoves:
            successorState = gameState.generateSuccessor(0, action)
            score = max(bestScore, expValue(successorState, self.depth, 1, numGhost))
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    elif currentGameState.isLose():
        return -float("inf")

    foodCount = currentGameState.getNumFood()
    ghostPositions = currentGameState.getGhostPositions()
    currentPosition = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    score = currentGameState.getScore()
    scaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    sumGhostDistances = []
    ghostAround = False

    for i in range(0, len(ghostPositions)):
        ghostDistance = util.manhattanDistance(ghostPositions[i], currentPosition)
        sumGhostDistances += [ghostDistance]
        if scaredTimes[i] == 0 and ghostDistance < 4:
            ghostAround = True
    
    if ghostAround:
        return min(sumGhostDistances) + score - scaredTimes.count(0) - foodCount 
    
    if foodCount > 0:
        if len(foodList) > 0:
            distance, closestFood = min([(util.manhattanDistance(currentPosition, food), food) for food in foodList])
            if distance != 0:
                foodDistance = - distance
            else:
                foodDistance = 10
    return score + foodDistance

# Abbreviation
better = betterEvaluationFunction
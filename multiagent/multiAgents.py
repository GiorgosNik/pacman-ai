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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        from util import manhattanDistance
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
        score=successorGameState.getScore()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        fieldSize = len(newFood.asList())
        foodDistance=fieldSize+1
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        scaredTimer=min(newScaredTimes)
        if newPos in currentGameState.getCapsules():        #increase score for capsules
            score=score+1000
        elif currentGameState.getFood()[newPos[0]][newPos[1]]:  #increase score for food
            score=score+100
        else:
            for node in newFood.asList():                #we detract the distance of the closes food dot
                if newFood[node[0]][node[1]] and manhattanDistance(newPos, node) < foodDistance:
                    foodDistance = manhattanDistance(newPos, node) - 2
            score = score - foodDistance
        for ghost in successorGameState.getGhostPositions():            #we increase the score for scared ghosts close to us
            if manhattanDistance(ghost, newPos)<=3:
                if scaredTimer>manhattanDistance(ghost, newPos):
                    score=score+1000
                else:
                    score=-10000+manhattanDistance(ghost, newPos)*100

        return score

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

    def MAX_VALUE(self, gameState,Depth):
        if gameState.isWin() or gameState.isLose() or Depth >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)       #Return the evaluation if we reached the end
        actions = gameState.getLegalActions(0)
        minValues=[]
        for action in actions:
            minValues.append(self.MIN_VALUE(gameState.generateSuccessor(0, action), Depth + 1)) #Return the max of the possible moves
        return max(minValues)

    def MIN_VALUE(self, gameState,Depth) :
        if gameState.isWin() or gameState.isLose() or Depth >= self.depth * gameState.getNumAgents():      #If we must end the search
            return self.evaluationFunction(gameState)           #We return the evaluation
        agent = Depth % gameState.getNumAgents()    #We use this to know which ghost we are
        actions = gameState.getLegalActions(agent)
        if agent == gameState.getNumAgents() - 1:
            minValues=[]                #If we are the last one, we got to the player move next
            for action in actions:
                minValues.append(self.MAX_VALUE(gameState.generateSuccessor(agent, action), Depth + 1) )
        else:
            minValues=[]                #Else we move on to the next ghost
            for action in actions:
                minValues.append(self.MIN_VALUE(gameState.generateSuccessor(agent, action), Depth + 1))
        return min(minValues)          #We return the min value

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

        actions=gameState.getLegalActions(0)
        minValues=[]
        for action in actions:          #For each action of the player
            minValues.append(self.MIN_VALUE(gameState.generateSuccessor(0, action), 1)) #get the minValues of the ghost moves
        maxValue = max(minValues)           #Get the max of MinValues
        best=[]
        for index in range(len(minValues)):     #Get all moves that lead to such score
            if minValues[index] == maxValue:
                best.append(index)
        chosenIndex = random.choice(best)
        return actions[chosenIndex]             #Return one of those at random



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        a=-100000000000000000000        #This getAction is the same as miniMax, only differnece beeing we have a and b
        b=a*-1                          #We set these to very small and very big numbers
        actions=gameState.getLegalActions(0)
        minValues=[]
        for action in actions:
            minValues.append(self.MIN_VALUEAB(gameState.generateSuccessor(0, action), 1,a,b))   #And we pass them on to the min function
            a=max(a,max(minValues))            #We end the search when a>b to avoid expanding the rest
            if a>b:
                break
        maxValue = max(minValues)           #We return same as minimax
        best=[]
        for index in range(len(minValues)):
            if minValues[index] == maxValue:
                best.append(index)
        chosenIndex = random.choice(best)
        return actions[chosenIndex]


    def MAX_VALUEAB(self, gameState,Depth,a,b):
        if gameState.isWin() or gameState.isLose() or Depth >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(0)
        minValues=[]
        for action in actions:
            minValues.append(self.MIN_VALUEAB(gameState.generateSuccessor(0, action), Depth + 1,a,b))
            a=max(a,max(minValues))     #We raise a to be the max of the returned values
            if a>b:                     #Break to avoid expanding in vain
                break
        return max(minValues)

    def MIN_VALUEAB(self, gameState,Depth,a,b) :
        if gameState.isWin() or gameState.isLose() or Depth >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        agent = Depth % gameState.getNumAgents()
        actions = gameState.getLegalActions(agent)
        if agent == gameState.getNumAgents() - 1:
            minValues=[]
            for action in actions:
                minValues.append(self.MAX_VALUEAB(gameState.generateSuccessor(agent, action), Depth + 1,a,b) )
                b=min(b,min(minValues))             #We lower the b to be the min of the minvalues so far
                if a>b:                             #Break to avoid expanding in vain
                    break
        else:
            minValues=[]
            for action in actions:
                minValues.append(self.MIN_VALUEAB(gameState.generateSuccessor(agent, action), Depth + 1,a,b))
                b=min(b,min(minValues))
                if a>b:
                    break
        return min(minValues)
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def MAX_VALUE(self, gameState,Depth):       #The same as standard miniMax MAX_VALUE
        if gameState.isWin() or gameState.isLose() or Depth >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(0)
        minValues=[]
        for action in actions:
            minValues.append(self.RandomGhost(gameState.generateSuccessor(0, action), Depth + 1))
        return max(minValues)

    def RandomGhost(self, gameState,Depth) :   #The same as the sandarm miniMax MIN_VALUE, with a small difference in return
        if gameState.isWin() or gameState.isLose() or Depth >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        agent = Depth % gameState.getNumAgents()
        actions = gameState.getLegalActions(agent)
        minValues = []
        if agent == gameState.getNumAgents() - 1:
            for action in actions:
                minValues.append(self.MAX_VALUE(gameState.generateSuccessor(agent, action), Depth + 1) )
        else:
            for action in actions:
                minValues.append(self.RandomGhost(gameState.generateSuccessor(agent, action), Depth + 1))
        return sum(minValues)/len(minValues)        #We return the average score of min, because each branch has equal chance
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        actions=gameState.getLegalActions(0)        #Same getAction as normal miniMax
        minValues=[]
        for action in actions:
            minValues.append(self.RandomGhost(gameState.generateSuccessor(0, action), 1))
        maxValue = max(minValues)
        best=[]
        for index in range(len(minValues)):
            if minValues[index] == maxValue:
                best.append(index)
        chosenIndex = random.choice(best)
        return actions[chosenIndex]




def betterEvaluationFunction(currentGameState):
    from util import manhattanDistance
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    #This function return the score of the state, minus the Manhattan Distance from the closest capsule if there is one
    score=currentGameState.getScore()
    distances=[]
    for capsule in currentGameState.getCapsules():
        distances.append(manhattanDistance(currentGameState.getPacmanPosition(),capsule))
    if len(distances)>0:
        score=score-min(distances)
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

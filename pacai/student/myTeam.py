from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.agents.capture.dummy.DummyAgent',
        second = 'pacai.agents.capture.dummy.DummyAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """
    firstAgent = OffenseAgent
    secondAgent = DefenseAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

class OffenseAgent(ReflexCaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at `pacai.core.baselineTeam` for more details about how to create an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)

        # Your initialization code goes here, if you need any.

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()
        myPos = successor.getAgentState(self.index).getPosition()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance


        # Get opponent positions
        isRedGhost = self.red and successor.isOnRedSide(myPos)
        isBlueGhost = (not self.red) and successor.isOnBlueSide(myPos)

        if not isRedGhost and not isBlueGhost:
            opponentIndices = self.getOpponents(successor)
            minOpponentDistance = None

            for opponentIndex in opponentIndices:
                opponentPos = successor.getAgentState(opponentIndex).getPosition()
                d = self.getMazeDistance(myPos, opponentPos)

                if minOpponentDistance is None or d < minOpponentDistance:
                    minOpponentDistance = d

                if minOpponentDistance < 3:
                    features['distanceToOpponent'] = -10000

        # Get remaining food
        if (successor.isOnBlueTeam):
            features['numFood'] = len(successor.getRedFood().asList())
        else:
            features['numFood'] = len(successor.getBlueFood().asList())  
        
        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -5,
            'distanceToOpponent': 1,
            'numFood': -5
        }

class DefenseAgent(ReflexCaptureAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2
        }
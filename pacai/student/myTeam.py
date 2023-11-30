from pacai.agents.capture.capture import CaptureAgent
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions
import math
from pacai.util import probability
from pacai.core.actions import Actions

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

class OffenseAgent(CaptureAgent):

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
        self.featExtractor = FeatureExtractor()
        self.weights = {}
        self.epsilon = 0.05
        self.alpha = 0.2
        self.gamma = 0.8
        self.discount = 0.9

    def getQValue(self, state, action):
        features = self.featExtractor.getFeatures(state, action, self)
        qVal = 0.0
        for feature, count in features.items():
            if feature not in self.weights:
                continue
            qVal += self.weights[feature] * count
        return qVal
    
    def getValue(self, state):
        legalActs = self.getLegalActions(state)
        if not legalActs:
            return 0.0
        max = -math.inf
        for act in legalActs:
            val = self.getQValue(state, act)
            if val > max:
                max = val
        return max
    
    def getPolicy(self, state):
        legalActs = self.getLegalActions(state)
        if not legalActs:
            return None
        max = -math.inf
        maxAct = None
        for act in legalActs:
            val = self.getQValue(state, act)
            if val > max:
                max = val
                maxAct = act
        return maxAct
    
    def chooseAction(self, state):
        isDoRandomAct = probability.flipCoin(self.epsilon)
        legalActs = self.getLegalActions(state)
        if not legalActs:
            return None
        if isDoRandomAct:
            return probability.random.choice(legalActs)
        else:
            return self.getPolicy(state)
    
    def update(self, state, action, nextState, reward):
        features = self.featExtractor.getFeatures(self.featExtractor, state, action)
        sample = reward + self.discountRate * self.getValue(nextState)
        error = sample - self.getQValue(state, action)
        for feature, count in features.items():
            if feature not in self.weights:
                self.weights[feature] = self.alpha * error * count
            else:
                self.weights[feature] += self.alpha * error * count
    
    def final(self, state):
        print(self.weights)

    def getLegalActions(self, state):
        return state.getLegalActions(self.index)

class FeatureExtractor:
    def getFeatures(self, state, action, agent):
        # Extract the grid of food and wall locations and get the ghost locations.
        food = agent.getFood(state)
        walls = state.getWalls()
        ghosts = [state.getAgentState(op).getPosition() for op in agent.getOpponents(state)]

        features = {}
        features["bias"] = 1.0

        # Compute the location of pacman after he takes the action.
        x, y = state.getAgentPosition(agent.index)
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # Count the number of ghosts 1-step away.
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in
                Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # If there is no danger of ghosts then add the food feature.
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

         # Compute distance to the nearest food.
        dist = math.inf
        foodList = food.asList()
        myPos = state.getAgentPosition(agent.index)

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            dist = min([agent.getMazeDistance(myPos, food) for food in foodList])

        if dist is not None:
            # Make the distance a number less than one otherwise the update will diverge wildly.
            features["closest-food"] = float(dist) / (walls.getWidth() * walls.getHeight())

        for key in features:
            features[key] /= 10.0

        return features


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

        # Keep to the middle when no invaders
        if len(invaders) == 0:
            middleDistance = [self.getMazeDistance(myPos, (12, 8))]
            features['middle'] = min(middleDistance)

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2,
            'middle': -10
        }
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions

class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
        #print(self.index)
    
    def minimaxFunction(self, gameState, depth, agentIndex):
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.getEvaluationFunction()(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)
        if len(legalMoves) == 0:
            return self.getEvaluationFunction()(gameState)
        
        otherTeamSize = len(getOpponents(gameState))

        #for a in invaders:

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        #print(self.getOpponents(gameState))

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        foodList = self.getFoodYouAreDefending(gameState).asList()

        width = (gameState.getInitialLayout().width)
        height = (gameState.getInitialLayout().height)

        wallsCoord = (gameState.getWalls().asList())

        if len(invaders) == 0:    #If there are no attackers on our side
            if gameState.isOnRedTeam(self.index):  #if we are on red team
                x = -1
                middleCoord = (width/2 + x,height/2)
                test = (int(middleCoord[0]), int(middleCoord[1]))
                while middleCoord in wallsCoord:
                    x -= 1
                    middleCoord = (width/2 + x, height/2)

                middleDistance = [self.getMazeDistance(myPos, middleCoord)]
                features['middle'] = min(middleDistance)
            if not gameState.isOnRedTeam(self.index):
                x = 1
                middleCoord = (width/2 + x,height/2)
                #print(middleCoord)
                test = (int(middleCoord[0]), int(middleCoord[1]))

                while middleCoord in wallsCoord:
                    x += 1
                    middleCoord = (width/2 + x, height/2)

                middleDistance = [self.getMazeDistance(myPos, middleCoord)]
                features['middle'] = min(middleDistance)


        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)
            
        #if myState.isScaredGhost():
            #print("Scared")


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
            'reverse': -2,
            'middle': -10
        }

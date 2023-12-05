from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions
from pacai.agents.search.multiagent import MultiAgentSearchAgent
import random


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
        #print("test")
        if depth == 0 and agentIndex in self.getTeam(gameState):
            myState = gameState.getAgentState(agentIndex)
            myPos = myState.getPosition()
            #print("test")
            invaders = []
            for x in self.getOpponents(gameState):
                enemyState = gameState.getAgentState(x)
                enemyPos = enemyState.getPosition()
                invaders.append(enemyPos)
            #print("test")
            invading = invaders[0]
            for x in invaders:
                if x[0] < invading[0]:
                    invading = x
            dists = [self.getMazeDistance(myPos, invading)]
            #print(dists)
            return dists

        if depth == 0 and agentIndex in self.getOpponents(gameState):
            #print("test")
            return 1

        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth -= 1 
            

        legalMoves = gameState.getLegalActions(agentIndex)
        #if len(legalMoves) == 0:
            #return self.getEvaluationFunction()(gameState)
        
        otherTeamSize = len(self.getOpponents(gameState)) 
        
        if agentIndex in self.getTeam(gameState):
            return min(self.minimaxFunction(gameState.generateSuccessor(agentIndex, actions),
                                            depth, agentIndex + 1) for actions in legalMoves)
        
        if agentIndex in self.getOpponents(gameState):
            return max(self.minimaxFunction(gameState.generateSuccessor(agentIndex, actions),
                                            depth, agentIndex + 1) for actions in legalMoves)

        #for a in invaders:

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        #print(self.getOpponents(gameState))
        #print(self.getTeam(gameState))
        #print(gameState.getNumAgents())  

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
                test = (int(middleCoord[0]), int(middleCoord[1]))

                while middleCoord in wallsCoord:
                    x += 1
                    middleCoord = (width/2 + x, height/2)

                middleDistance = [self.getMazeDistance(myPos, middleCoord)]
                features['middle'] = min(middleDistance)

        if (len(invaders) > 0):
            
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            #print(dists)
            features['invaderDistance'] = min(dists)
            '''
            legalMoves = gameState.getLegalActions()
            scores = [self.minimaxFunction(gameState.generateSuccessor(0, actions), 1, 0)
                    for actions in legalMoves]
            bestScore = min(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.
            features['invaderDistance'] = chosenIndex
            #return legalMoves[chosenIndex]
            '''

        if myState.isScaredGhost():
            run = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            for x in run:
                print(run)
                #if (x == 1) or (x == 2):       

        


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

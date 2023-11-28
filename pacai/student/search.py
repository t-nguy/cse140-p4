"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from ..util.stack import Stack
from ..util.queue import Queue
from ..util.priorityQueue import PriorityQueue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    start = problem.startingState()

    fringe = Stack()
    fringe.push((start, []))
    visited = [start]

    while len(fringe) > 0:
        pos, actions = fringe.pop()

        if problem.isGoal(pos):
            return actions

        for child, direction, cost in problem.successorStates(pos):
            if child not in visited:
                fringe.push((child, actions + [direction]))
                visited.append(child)

    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    start = problem.startingState()

    fringe = Queue()
    fringe.push((start, []))
    visited = [start]

    while len(fringe) > 0:
        pos, actions = fringe.pop()

        if problem.isGoal(pos):
            # print("Actions: ", actions)
            return actions

        for child, direction, cost in problem.successorStates(pos):
            if child not in visited:
                fringe.push((child, actions + [direction]))
                visited.append(child)

    return []

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    start = problem.startingState()

    fringe = PriorityQueue()
    fringe.push((start, []), 0)
    visited = [start]

    while len(fringe) > 0:
        (pos, actions) = fringe.pop()

        if problem.isGoal(pos):
            return actions

        for child, direction, cost in problem.successorStates(pos):
            if child not in visited:
                childActions = actions + [direction]
                childCost = problem.actionsCost(childActions)
                fringe.push((child, childActions), childCost)
                visited.append(child)

    return []

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    start = problem.startingState()

    fringe = PriorityQueue()
    fringe.push((start, []), 0)
    visited = [start]

    while len(fringe) > 0:
        pos, actions = fringe.pop()

        if problem.isGoal(pos):
            print("Actions len: ", len(actions))
            return actions

        for child, direction, cost in problem.successorStates(pos):
            if child not in visited:
                childActions = actions + [direction]
                childCost = problem.actionsCost(childActions)
                fringe.push((child, childActions), childCost + heuristic(child, problem))
                visited.append(child)

    return []
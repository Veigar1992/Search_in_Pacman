# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()
class Node:
    def __init__(self, state, path, problem,cost,h):
        self.state = state
        self.path = path
        self.problem = problem
        self.cost = cost
        self.h = h
    def __str__(self):
        string = str(self.state)
        string += "\t"
        string += str(self.path)
        return string

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    ExploredSet = set()
    frontier = util.Stack()
    start = Node(problem.getStartState(), [], problem,0,0)
    frontier.push(start)
    res = []
    ExploredSet.add(problem.getStartState())
    successordir = {}
    while True:
    #    if frontier.isEmpty(): return False
        n = frontier.pop()
        if problem.isGoalState(n.state): return res
        if successordir.has_key(n.state):
            successors=successordir[n.state]
        else:
           successors=problem.getSuccessors(n.state)
           successordir[n.state]=successors
        find = False
        for successor in successors:
            if successor[0] not in ExploredSet:
                ExploredSet.add(successor[0])
                newNode = Node(successor[0],[],problem,0,0)
                frontier.push(n)
                frontier.push(newNode)
                find = True
                res.append(successor[1])
                break
        if not find:
            res.pop()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    ExploredSet = set()
    frontier = util.Queue()
    start = Node(problem.getStartState(), [], problem,0,0)
    frontier.push(start)
    print start
    ExploredSet.add(problem.getStartState())
    while True:
        if frontier.isEmpty(): return False
        n = frontier.pop()
        if problem.isGoalState(n.state): return n.path
        for successor in problem.getSuccessors(n.state):
            if successor[0] not in ExploredSet:
                ExploredSet.add(successor[0])
                state = successor[0]
                path = n.path[:]
                path.append(successor[1])
                newNode = Node(state,path,problem,0,0)
                frontier.push(newNode)

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    frontier=util.PriorityQueue()
    ExploredSet = set()
    start = Node(problem.getStartState(), [], problem,0.0,0.0)
    frontier.push(start,start.cost)
    print start
    while True:
        if frontier.isEmpty(): return False
        n = frontier.pop()
        if problem.isGoalState(n.state): return n.path
        if n.state not in ExploredSet:
            ExploredSet.add(n.state)
            for successor in problem.getSuccessors(n.state):
                cost = n.cost
                cost += successor[2]
                state = successor[0]
                path = n.path[:]
                path.append(successor[1])
                newNode = Node(state,path,problem,cost,0.0)
                frontier.push(newNode,cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    frontier=util.PriorityQueue()
    ExploredSet = set()
    start = Node(problem.getStartState(), [], problem,0.0,0.0)
    frontier.push(start,start.cost+start.h)
    print start
    while True:
        if frontier.isEmpty(): return False
        n = frontier.pop()
        if problem.isGoalState(n.state): return n.path
        if n.state not in ExploredSet:
            ExploredSet.add(n.state)
            for successor in problem.getSuccessors(n.state):
                cost = n.cost
                cost += successor[2]
                state = successor[0]
                path = n.path[:]
                path.append(successor[1])
                h = heuristic(state, problem)
                newNode = Node(state,path,problem,cost,h)
                frontier.push(newNode,cost+h)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

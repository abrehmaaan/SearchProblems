import sys
import util
sys.setrecursionlimit(10000)

### Model (search problem)

class TransportationProblem(object):
    def __init__(self, N):
        # N = number of blocks
        self.N = N
    def startState(self):
        return 1
    def isEnd(self, state):
        return state == self.N
    def succAndCost(self, state):
        # return list of (action, newState, cost) triples
        result = []
        if state+1<=self.N:
            result.append(('walk', state+1, 1))
        if state*2<=self.N:
            result.append(('tram', state*2, 2))
        return result

### Algorithms

def printSolution(solution):
    totalCost, history = solution
    print('totalCost: {}'.format(totalCost))
    for item in history:
        print(item)

def backtrackingSearch(problem):
    # Best solution found so far (dictionary because of python scoping technicality)
    best = {
        'cost': float('+inf'),
        'history': None
    }
    def recurse(state, history, totalCost):
        # At state, having undergone history, accumulated
        # totalCost.
        # Explore the rest of the subtree under state.
        if problem.isEnd(state):
            # Update the best solution so far
            if totalCost<best['cost']:
                best['cost'] = totalCost
                best['history'] = history
            return
        # Recurse on children
        for action, newState, cost in problem.succAndCost(state):
            recurse(newState, history+[(action, newState, cost)], totalCost+cost)
    recurse(problem.startState(), history=[], totalCost=0)
    return (best['cost'], best['history'])

def dynamicProgramming(problem):
    cache = {} # state -> futureCost(state)
    def futureCost(state):
        # Base case
        if problem.isEnd(state):
            return 0
        if state in cache: # Exponential savings
            return cache[state]
        # Actually doing work
        result = min(cost+futureCost(newState) \
                for action, newState, cost in problem.succAndCost(state))
        cache[state] = result
        return result
    return (futureCost(problem.startState()), [])

def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    frontier.update(problem.startState(), 0)
    while True:
        # Move from frontier to explored
        state, pastCost = frontier.removeMin()
        if problem.isEnd(state):
            return (pastCost, [])
        # Push out on the frontier
        for action, newState, cost in problem.succAndCost(state):
            frontier.update(newState, pastCost+cost)

def DFS(problem):
    stack = [(problem.startState(), [], 0)]
    while stack:
        state, path, totalCost = stack.pop()
        if problem.isEnd(state):
            return (totalCost, path)
        for action, newState, cost in problem.succAndCost(state):
            stack.append((newState, path + [(action, newState, cost)], totalCost+cost))

def aStarSearch(problem, heuristic):
    frontier = util.PriorityQueue()
    frontier.update(problem.startState(), heuristic(problem.startState(), problem.N))
    while True:
        # Move from frontier to explored
        state, pastCost = frontier.removeMin()
        if problem.isEnd(state):
            return (pastCost, [])
        # Push out on the frontier
        for action, newState, cost in problem.succAndCost(state):
            totalCost = pastCost + cost + heuristic(newState, problem.N) # Add the heuristic cost to the total cost
            frontier.update(newState, totalCost)

def manhattan_heuristic(state, end_state):
    return abs(state - end_state)

### Main

problem = TransportationProblem(N=40)
print("Back Tracking Search: ")
printSolution(backtrackingSearch(problem))
print("\nDynamic Problem: ")
printSolution(dynamicProgramming(problem))
print("\nUniform Cost Search: ")
printSolution(uniformCostSearch(problem))
print("\nDepth First Search: ")
printSolution(DFS(problem))
print("\nA* Search: ")
printSolution(aStarSearch(problem, manhattan_heuristic))
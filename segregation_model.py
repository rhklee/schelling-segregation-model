import random 
from collections import namedtuple

Agent = namedtuple('Agent', ['agent_type', \
                             'pop_percent', \
                             'satisfaction_threshold'])

PERCENT_A = .5
PERCENT_B = .5
TYPE_A = "o"
TYPE_B = "x"
TYPE_EMPTY = "_"

agent_a = Agent(agent_type = TYPE_A, \
                pop_percent = PERCENT_A, \
                satisfaction_threshold = .7)

agent_b = Agent(agent_type = TYPE_B, \
                pop_percent = PERCENT_B, \
                satisfaction_threshold = .66)

SATISFIED = "S"
NOT_SATISFIED = "NS"

NBHD_DIM = 40
#sh = SATISFACTION_THRESHOLD = .75
ITERATIONS = 400
TIME_LAG = 0.05

def create_nbhd(percentA, percentB, dimSize): 
    from itertools import repeat, chain
    if percentA + percentB > 1:
        raise ValueError("Poorly defined percentages")
    
    size = dimSize ** 2
    numA = int(size * percentA)
    numB = int(size * percentB)
    numEmpty = size - (numA + numB)

    allAgentTypes = list(chain(repeat(TYPE_A, numA), \
                            repeat(TYPE_B, numB), \
                            repeat(TYPE_EMPTY, numEmpty)))
    random.shuffle(allAgentTypes)
    return create_agent_board(allAgentTypes, dimSize) 

def create_agent_board(allAgentTypes, dimSize):
    size = dimSize ** 2
    return [ [ { 'type': agentType, 'satisfactionState': None } \
               for agentType in allAgentTypes[rowBegin:rowEnd] ] \
             for rowBegin, rowEnd in \
             zip(range(0, size - dimSize + 1, dimSize), \
                 range(dimSize, size + 1, dimSize)) ]

def calc_similar_neighbor_ratio(nbhd, rowInd, colInd): 
    totalNeighbors = 0
    totalSameTypeNeighbors = 0
    for neighbor in get_neighbors(nbhd, rowInd, colInd):
        if neighbor['type'] == TYPE_A or neighbor['type'] == TYPE_B:
            totalNeighbors += 1 
            if neighbor['type'] == nbhd[rowInd][colInd]['type']:
                totalSameTypeNeighbors += 1
    return (totalSameTypeNeighbors / totalNeighbors) \
            if totalNeighbors != 0 else 0

def get_neighbors(nbhd, rowInd, colInd):
    dimSize = len(nbhd)
    upperLeftCoords = (rowInd - 1 if rowInd - 1 >= 0 else rowInd, \
                       colInd - 1 if colInd - 1 >= 0 else colInd)
    lowerRightCoords = (rowInd + 1 if rowInd + 1 < dimSize else rowInd, \
                        colInd + 1 if colInd + 1 < dimSize else colInd)
    return [ nbhd[i][j] for i in range(upperLeftCoords[0], \
                                       lowerRightCoords[0]+1) \
                        for j in range(upperLeftCoords[1], \
                                       lowerRightCoords[1]+1) \
             if i != rowInd or j != colInd ]

def get_agent_satisfaction(agentSimilarNeighbors, agentType):
    satisfactionThreshold = agent_a.satisfaction_threshold \
                            if agentType == agent_a.agent_type \
                            else agent_b.satisfaction_threshold
    return SATISFIED \
            if satisfactionThreshold <= agentSimilarNeighbors \
            else NOT_SATISFIED

def update_satisfaction_state(nbhd):
    """Update satisfaction state based on satisfaction thresholds."""
    for rowInd, row in enumerate(nbhd):
        for colInd, agent in enumerate(row):
            if agent['type'] == TYPE_EMPTY:
                continue

            agentSimilarNeighbors = calc_similar_neighbor_ratio(nbhd, \
                                                            rowInd, \
                                                            colInd)
            agent['satisfactionState'] = \
                    get_agent_satisfaction(agentSimilarNeighbors, \
                                           agent['type'])
def relocate_unsatisfied(nbhd):
    from copy import deepcopy
    nbhdDim = len(nbhd)
    unsatisfiedAndEmptySpots = [ (i,j) for i in range(nbhdDim) \
                                       for j in range(nbhdDim) \
                                       if nbhd[i][j]['satisfactionState'] \
                                            == NOT_SATISFIED \
                                       or nbhd[i][j]['type'] == TYPE_EMPTY ]
    fromToCoords = zip(unsatisfiedAndEmptySpots, \
                        random.sample(unsatisfiedAndEmptySpots, \
                                      len(unsatisfiedAndEmptySpots)))
    newNbhd = deepcopy(nbhd)
    for (fromRow, fromCol), (toRow, toCol) in fromToCoords:
        newNbhd[toRow][toCol] = nbhd[fromRow][fromCol]
    return newNbhd

def getSatisfactionMarker(satisfactionState):
    return '*' if satisfactionState == NOT_SATISFIED else ' '

def stringify_board(board):
    return '\n'.join(''.join(rowVal['type'] + \
                             getSatisfactionMarker(rowVal['satisfactionState']) \
                             for rowVal in row) \
                     for row in board)

if __name__ == '__main__':
    from time import sleep
    import sys
    nbhd = create_nbhd(PERCENT_A, PERCENT_B, NBHD_DIM)

    for iter_num in range(ITERATIONS):
        update_satisfaction_state(nbhd)
        nbhd = relocate_unsatisfied(nbhd)
        print("Iteration {} board:".format(iter_num))
        print('{}'.format(stringify_board(nbhd)), end='\n')
        sleep(TIME_LAG)




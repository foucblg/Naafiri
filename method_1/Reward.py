from cube import cube_resolved

def calculate_reward(cube):
    reward=correct_position(cube)/40 - penalité
    return reward

def STOCKAGE(mvt):
    L=[]
    L.append(mvt)
    return L


def penalité(mvt):
    a=len(STOCKAGE(mvt))-1
    if STOCKAGE[a]==mvt :
        return 100
    else :
        return 0

def correct_position(cube):
    a=0
    #corner permutation
    for i in range(len(cube.corner_permutation)):
        if i == cube.corner_permutation[i]:
            a+=1
    
    #corner orientation
    for i in range(len(cube.corner_orentation)):
       if 0 == cube.corner_orentation[i]:
            a+=1 

    #edge permutation
    for i in range(len(cube.edge_permutation)):
        if i == cube.edge_permutation[i]:
            a+=1
    
    #edge orientation
    for i in range(len(cube.edge_orientation)):
       if 0 == cube.edge_orientation[i]:
            a+=1 

    return a
# 40 correct position

print(correct_position(cube_resolved))

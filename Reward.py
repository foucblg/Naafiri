from cube import cube_resolved

def calculate_reward():

    reward=correct_position()/63
    return reward


def correct_position(cube):
    a=0
    #corner permutation
    for i in range(len(cube.corner_permutation)):
        print(i)
        print(cube.corner_permutation[i])
        if i == cube.corner_permutation[i]:
            a+=1
    print(f'a = {a}')
    #corner orientation
    for i in range(len(cube.corner_orentation)):
       if 0 == cube.corner_orentation[i]:
            a+=1 
    print(f'a = {a}')
    #edge permutation
    for i in range(len(cube.edge_permutation)):
        if i == cube.edge_permutation[i]:
            a+=1
    print(f'a = {a}')
    #edge orientation
    for i in range(len(cube.edge_orientation)):
       if 0 == cube.edge_orientation[i]:
            a+=1 
    print(f'a = {a}')
    return a
# 40 correct position

#print(correct_position(cube_with_one_move))
print(correct_position(cube_resolved))
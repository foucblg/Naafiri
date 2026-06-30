"""
codages couleurs
bleu : 0
orange : 1
jaune : 2
rouge : 3
blanc : 4
vert : 3
"""

from copy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import *
from random import randint
from collections import deque


cubeCible = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5, 5, 5, 5, 5]]

def affiche(cube):
    tab = [[-1 for i in range(12)] for e in range(9)]
    for i in range(3):
        tab[i][3:6] = cube[4][3*i:3*(i+1)]
        tab[i+3] = cube[3][3*i:3*(i+1)]+cube[0][3*i:3*(i+1)]+cube[1][3*i:3*(i+1)]+cube[5][3*i:3*(i+1)]
        tab[i+6][3:6] = cube[2][3*i:3*(i+1)]

    couleur = [(0,0,255),(255,165,0),(255,255,0),(255,0,0),(255,255,255),(0,255,0)]
    tab2 = [[False for i in range(12)] for e in range(9)]
    for i in range(9):
        for j in range(12):
            tab2[i][j] = (0,0,0) if tab[i][j] == -1 else couleur[tab[i][j]]

    plt.imshow(tab2)
    plt.show()


# Mouvements

def rotation(Face,sens):
    """sens est vrai pour tourner dans le sens horaire"""
    face = deepcopy(Face)
    if sens:
        face[1],face[5],face[7],face[3] = face[3],face[1],face[5],face[7]
        face[0],face[2],face[8],face[6] = face[6],face[0],face[2],face[8]
    else:
        face[1],face[5],face[7],face[3] = face[5],face[7],face[3],face[1]
        face[0],face[2],face[8],face[6] = face[2],face[8],face[6],face[0]
    return face



def R(Cube):
    cube = deepcopy(Cube)
    cube[1] = rotation(cube[1],True)
    t = [cube[0][2],cube[0][5],cube[0][8]]
    for i in [4,5,2,0]:
        if i == 5:
            a,b,c = 6,3,0
        else:
            a,b,c = 2,5,8
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def Rp(Cube):
    cube = deepcopy(Cube)
    cube[1] = rotation(cube[1],False)
    t = [cube[0][2],cube[0][5],cube[0][8]]
    for i in [2,5,4,0]:
        if i == 5:
            a,b,c = 6,3,0
        else:
            a,b,c = 2,5,8
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def R2(Cube):
    return R(R(Cube))

def L(Cube):
    cube = deepcopy(Cube)
    cube[3] = rotation(cube[3],True)
    t = [cube[0][0],cube[0][3],cube[0][6]]
    for i in [2,5,4,0]:
        if i == 5:
            a,b,c = 8,5,2
        else:
            a,b,c = 0,3,6
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def Lp(Cube):
    cube = deepcopy(Cube)
    cube[3] = rotation(cube[3],False)
    t = [cube[0][0],cube[0][3],cube[0][6]]
    for i in [4,5,2,0]:
        if i == 5:
            a,b,c = 8,5,2
        else:
            a,b,c = 0,3,6
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def L2(Cube):
    return L(L(Cube))

def U(Cube):
    cube = deepcopy(Cube)
    cube[4] = rotation(cube[4],True)
    t = [cube[0][0],cube[0][1],cube[0][2]]
    for i in [3,5,1,0]:
        (cube[i][0],cube[i][1],cube[i][2]),t = t,(cube[i][0],cube[i][1],cube[i][2])
    return cube

def Up(Cube):
    cube = deepcopy(Cube)
    cube[4] = rotation(cube[4],False)
    t = [cube[0][0],cube[0][1],cube[0][2]]
    for i in [1,5,3,0]:
        (cube[i][0],cube[i][1],cube[i][2]),t = t,(cube[i][0],cube[i][1],cube[i][2])
    return cube

def U2(Cube):
    return U(U(Cube))

def D(Cube):
    cube = deepcopy(Cube)
    cube[2] = rotation(cube[2],True)
    t = [cube[0][6],cube[0][7],cube[0][8]]
    for i in [1,5,3,0]:
        (cube[i][6],cube[i][7],cube[i][8]),t = t,(cube[i][6],cube[i][7],cube[i][8])
    return cube

def Dp(Cube):
    cube = deepcopy(Cube)
    cube[2] = rotation(cube[2],False)
    t = [cube[0][6],cube[0][7],cube[0][8]]
    for i in [3,5,1,0]:
        (cube[i][6],cube[i][7],cube[i][8]),t = t,(cube[i][6],cube[i][7],cube[i][8])
    return cube

def D2(Cube):
    return D(D(Cube))

def F(Cube):
    cube = deepcopy(Cube)
    cube[0] = rotation(cube[0],True)
    t = [cube[1][0],cube[1][3],cube[1][6]]
    for i in [2,3,4,1]:
        if i == 4:
            a,b,c = 6,7,8
        elif i == 2:
            a,b,c = 2,1,0
        elif i == 3:
            a,b,c = 8,5,2
        else:
            a,b,c = 0,3,6
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def Fp(Cube):
    cube = deepcopy(Cube)
    cube[0] = rotation(cube[0],False)
    t = [cube[1][0],cube[1][3],cube[1][6]]
    for i in [4,3,2,1]:
        if i == 4:
            a,b,c = 6,7,8
        elif i == 2:
            a,b,c = 2,1,0
        elif i == 3:
            a,b,c = 8,5,2
        else:
            a,b,c = 0,3,6
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def F2(Cube):
    return F(F(Cube))

def B(Cube):
    cube = deepcopy(Cube)
    cube[5] = rotation(cube[5],True)
    t = [cube[1][2],cube[1][5],cube[1][8]]
    for i in [4,3,2,1]:
        if i == 4:
            a,b,c = 0,1,2
        elif i == 2:
            a,b,c = 8,7,6
        elif i == 3:
            a,b,c = 6,3,0
        else:
            a,b,c = 2,5,8
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def Bp(Cube):
    cube = deepcopy(Cube)
    cube[5] = rotation(cube[5],False)
    t = [cube[1][2],cube[1][5],cube[1][8]]
    for i in [2,3,4,1]:
        if i == 4:
            a,b,c = 0,1,2
        elif i == 2:
            a,b,c = 8,7,6
        elif i == 3:
            a,b,c = 6,3,0
        else:
            a,b,c = 2,5,8
        (cube[i][a],cube[i][b],cube[i][c]),t = t,(cube[i][a],cube[i][b],cube[i][c])
    return cube

def B2(Cube):
    return B(B(Cube))



def voisins1(Cube):
    cube = deepcopy(Cube)
    return [[R(cube),'R'],[Rp(cube),'Rp'],[R2(cube),'R2'],[L(cube),'L'],[Lp(cube),'Lp'],[L2(cube),'L2'],[U(cube),'U'],[Up(cube),'Up'],[U2(cube),'U2'],[D2(cube),'D2'],[D(cube),'D'],[Dp(cube),'Dp'],[F(cube),'F'],[Fp(cube),'Fp'],[F2(cube),'F2'],[B2(cube),'B2'],[B(cube),'B'],[Bp(cube),'Bp']]

def voisins2(Cube):
    cube = deepcopy(Cube)
    return [[R(cube),'R'],[Rp(cube),'Rp'],[R2(cube),'R2'],[L(cube),'L'],[Lp(cube),'Lp'],[L2(cube),'L2'],[U(cube),'U'],[Up(cube),'Up'],[U2(cube),'U2'],[D2(cube),'D2'],[D(cube),'D'],[Dp(cube),'Dp'],[F2(cube),'F2'],[B2(cube),'B2']]

def voisins3(Cube):
    cube = deepcopy(Cube)
    return [[R2(cube),'R2'],[L2(cube),'L2'],[U(cube),'U'],[Up(cube),'Up'],[U2(cube),'U2'],[D2(cube),'D2'],[D(cube),'D'],[Dp(cube),'Dp'],[F2(cube),'F2'],[B2(cube),'B2']]

def voisins4(Cube):
    cube = deepcopy(Cube)
    return [[R2(cube),'R2'],[L2(cube),'L2'],[U2(cube),'U2'],[D2(cube),'D2'],[F2(cube),'F2'],[B2(cube),'B2']]



coups = [D,Dp,R,Rp,L,Lp,U,Up,B,Bp,F,Fp]

def melange(nb):
    cube = deepcopy(cubeCible)
    tab = [coups[randint(0,11)] for i in range(nb)]
    for i in tab:
        cube = i(cube)

    return cube



def G2(Cube):
    L = [(Cube[4][7],Cube[0][1]),(Cube[4][3],Cube[3][1]),(Cube[4][5],Cube[1][1]),(Cube[4][1],Cube[5][1]),(Cube[2][1],Cube[0][7]),(Cube[2][3],Cube[3][7]),(Cube[2][5],Cube[1][7]),(Cube[2][7],Cube[5][7]),(Cube[0][3],Cube[3][5]),(Cube[0][5],Cube[1][3]),(Cube[5][3],Cube[1][5]),(Cube[5][5],Cube[3][3])]

    for i in L:
        if i[0] == 1 or i[0] == 3:
            return False

        elif i[0] == 0 or i[0] == 5:
            if i[1] == 2 or i[1] == 4:
                return False
    return True


def G3(Cube):
    for i in Cube[4]:
        if i != 4 and i!= 2:
            return False

    for i in Cube[2]:
        if i != 4 and i!= 2:
            return False
    return True

def G4(Cube):
    for i in Cube[0]:
        if i != 0 and i!= 5:
            return False

    for i in Cube[5]:
        if i != 5 and i!= 0:
            return False

    for i in Cube[1]:
        if i != 1 and i!= 3:
            return False

    for i in Cube[3]:
        if i != 1 and i!= 3:
            return False

    for face in Cube:
        n = 0
        for i in [face[0],face[2],face[6],face[8]]:
            if i == face[4]:
                n += 1
        if n%2 == 1:
            return False


##
def testG2():
    for _ in range(100):
        cube1 = cubeCible
        for i in range(50):
            cube1 = voisins2(cube1)[randint(0,13)][0]

        if G2(cube1) == False:
            affiche(cube1)
            return False
        else:
            print('ok')

#testG2()

def testG3():
    for _ in range(100):
        cube1 = cubeCible
        for i in range(50):
            cube1 = voisins3(cube1)[randint(0,9)][0]

        if G3(cube1) == False:
            affiche(cube1)
            return False
        elif G2(cube1) == False:
            affiche(cube1)
            return False
        else:
            print('ok')

#testG3()


def testG4():
    for _ in range(100):
        cube1 = voisins4(cubeCible)[randint(0,5)][0]
        for i in range(50):
            cube1 = voisins4(cube1)[randint(0,5)][0]

        if G4(cube1) == False:
            affiche(cube1)
            return False
        else:
            print('ok')

#testG4()

def id(Cube):
    cube = str(Cube)
    id = ''
    for i in cube:
        if i != ',' and i != '[' and i!=']' and i != ' ':
            id += i
    return id


def cubeDansG(g,nb = 50):
    """donne un exemple de cube dans le groupe numéro g"""
    if g == 1:
        f = voisins1
        a = 17
    elif g == 2:
        f = voisins2
        a = 13
    elif g == 3:
        f = voisins3
        a = 9
    elif g == 4:
        f = voisins4
        a = 5
    J = []
    cube1 = deepcopy(cubeCible)
    for i in range(nb):
        n = f(cube1)[randint(0,a)]
        cube1 = n[0]
        J.append(n[1])
    return cube1

#affiche(cubeDansG(4))
#print(cubeDansG(1,15))


#on parcours dans G1, on cherche à aller dans G2
def parcours1(Cube):
    cube = deepcopy(Cube)
    d = {id(cube):('','')}
    pos = [cube,'']
    M = deque([pos])
    while not G2(pos[0]):
        v = voisins1(pos[0])
        for i in v:
            if id(i[0]) not in d:
                M.append(i)
                d[id(i[0])] = (id(pos[0]),i[1])
        pos = M.popleft()
    Res = []
    pos = id(pos[0])
    while pos != id(cube):
        tab = d[pos]
        pos = tab[0]
        Res.append(tab[1])
    return Res

"""
t1 = time()
print(parcours1(cubeExemple))
print(time() - t1)
"""
#cubeExemple1 = B(Dp(Rp(Up(R(cubeExemple)))))

#on parcours dans G2, on cherche à aller dans G3
def parcours2(Cube):
    cube = deepcopy(Cube)
    d = {id(cube):('','')}
    pos = [cube,'']
    M = deque([pos])
    while not G3(pos[0]):
        v = voisins2(pos[0])
        for i in v:
            if id(i[0]) not in d:
                M.append(i)
                d[id(i[0])] = (id(pos[0]),i[1])
        pos = M.popleft()
    Res = []
    pos = id(pos[0])
    while pos != id(cube):
        tab = d[pos]
        pos = tab[0]
        Res.append(tab[1])
    return Res

#cubeExemple2 = cubeDansG(2,30)
#print(G2(cubeExemple2),cubeExemple2)
"""
t1 = time()
print(parcours2(cubeDansG(2,10)))
print(time() - t1)
"""
#on parcours dans G3, on cherche à aller dans G4
def parcours3(Cube):
    cube = deepcopy(Cube)
    d = {id(cube):('','')}
    pos = [cube,'']
    M = deque([pos])
    while not G4(pos[0]):
        v = voisins3(pos[0])
        for i in v:
            if id(i[0]) not in d:
                M.append(i)
                d[id(i[0])] = (id(pos[0]),i[1])
        pos = M.popleft()
    Res = []
    pos = id(pos[0])
    while pos != id(cube):
        tab = d[pos]
        pos = tab[0]
        Res.append(tab[1])
    return Res

#print(parcours3(cubeDansG(3)))

#on parcours dans G4, on cherche à aller dans G5 (cube résolu)
def parcours4(Cube):
    cube = deepcopy(Cube)
    d = {id(cube):('','')}
    pos = [cube,'']
    M = deque([pos])
    while pos[0] != cubeCible:
        v = voisins4(pos[0])
        for i in v:
            if id(i[0]) not in d:
                M.append(i)
                d[id(i[0])] = (id(pos[0]),i[1])
        pos = M.popleft()
    Res = []
    pos = id(pos[0])
    while pos != id(cube):
        tab = d[pos]
        pos = tab[0]
        Res.append(tab[1])
    return Res







































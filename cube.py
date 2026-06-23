import random
import matplotlib.pyplot as plt

# 0: UFR
# 1: UFL
# 2: UBL
# 3: UBR
# 4: DFR
# 5: DFL
# 6: DBL
# 7: DBR

# 0: UR
# 1: UF
# 2: UL
# 3: UB
# 4: DR
# 5: DF
# 6: DL
# 7: DB
# 8: FR
# 9: FL
# 10: BL
# 11: BR

corner_permutation = [i for i in range(8)]
corner_orentation = [0 for _ in range(8)]
edge_permutation = [i for i in range(12)]
edge_orientation = [0 for _ in range(12)]


class Cube:
    def __init__(self, cp, co, ep, eo):
        self.corner_permutation = cp
        self.corner_orientation = co
        self.edge_permutation = ep
        self.edge_orientation = eo

    # -------------------------
    # DEBUG
    # -------------------------
    def __str__(self):
        return (
            f"Corners perm: {self.corner_permutation}\n"
            f"Corners orient: {self.corner_orientation}\n"
            f"Edges perm: {self.edge_permutation}\n"
            f"Edges orient: {self.edge_orientation}\n"
        )
    def to_vector(self):
        L = [i for i in self.corner_permutation]
        L+= [i for i in self.corner_orientation]
        L+= [i for i in self.edge_permutation]
        L+= [i for i in self.edge_orientation]
        return L

    def copy(self):
        return Cube(
            self.corner_permutation[:],
            self.corner_orientation[:],
            self.edge_permutation[:],
            self.edge_orientation[:]
        )

    def show(self):
        tab = [[-1 for _ in range(12)] for _ in range(9)]
        tab[1][4] = 0
        tab[4][1] = 1
        tab[4][4] = 2
        tab[4][7] = 3
        tab[4][10] = 4
        tab[7][4] = 5
        
        pos_corners = [
            [(3,5),(2,5),(3,6)],
            [(3,3),(3,2),(2,3)],
            [(0,3),(3,0),(3,11)],
            [(0,5),(3,8),(3,9)],
            [(5,5),(5,6),(6,5)],
            [(5,3),(6,3),(5,2)],
            [(5,0),(5,11),(8,3)],
            [(8,5),(5,8),(5,9)],
                       ]
        col_corners = [
            [2,0,3],
            [2,1,0],
            [0,1,4],
            [0,3,4],
            [2,3,5],
            [2,5,1],
            [1,4,5],
            [5,3,4],
                       ]
        pos_edges = [
            [(1,5),(3,7)],
            [(2,4),(3,4)],
            [(1,3),(3,1)],
            [(0,4),(3,10)],
            [(7,5),(5,7)],
            [(5,4),(6,4)],
            [(5,1),(7,3)],
            [(8,4),(5,10)],
            [(4,5),(4,6)],
            [(4,2),(4,3)],
            [(4,0),(4,11)],
            [(4,8),(4,9)],
                     ]
        col_edges = [
            [0,3],
            [0,2],
            [0,1],
            [0,4],
            [5,3],
            [2,5],
            [1,5],
            [5,4],
            [2,3],
            [1,2],
            [1,4],
            [3,4],
                     ]

        for i in range(8):
            pos = pos_corners[i]
            col = col_corners[self.corner_permutation[i]]
            for p_i, p in enumerate(pos):
                tab[p[0]][p[1]] = col[(p_i + self.corner_orientation[i])%3]
            
        for i in range(12):
            pos = pos_edges[i]
            col = col_edges[self.edge_permutation[i]]
            for p_i, p in enumerate(pos):
                tab[p[0]][p[1]] = col[(p_i + self.edge_orientation[i])%2]

        couleurs = [(255,165,0),(0,255,0),(255,255,255),(0,0,255),(255,255,0),(255,0,0)]
        tab2 = [[False for i in range(12)] for e in range(9)]
        for i in range(9):
            for j in range(12):
                tab2[i][j] = (0,0,0) if tab[i][j] == -1 else couleurs[tab[i][j]]

        plt.imshow(tab2)
        plt.show()

    # -------------------------
    # CORE UTILS
    # -------------------------
    def _cycle(self, arr, idx):
        tmp = arr[:]
        n = len(idx)
        for i in range(n):
            arr[idx[i]] = tmp[idx[(i - 1) % n]]

    # -------------------------
    # MOVE TABLE
    # -------------------------
    MOVES = {
        "U": {
            "cp": [[0, 3, 2, 1]],
            "ep": [[0, 3, 2, 1]],
            "co": [],
            "eo": []
        },
        "U'": {
            "cp": [[1, 2, 3, 0]],
            "ep": [[1, 2, 3, 0]],
            "co": [],
            "eo": []
        },

        "D": {
            "cp": [[4, 5, 6, 7]],
            "ep": [[4, 5, 6, 7]],
            "co": [],
            "eo": []
        },
        "D'": {
            "cp": [[7, 6, 5, 4]],
            "ep": [[7, 6, 5, 4]],
            "co": [],
            "eo": []
        },

        "F": {
            "cp": [[0, 1, 5, 4]],
            "ep": [[1, 8, 5, 9]],
            "co": [0, 1, 4, 5],
            "eo": [1, 8, 5, 9]
        },
        "F'": {
            "cp": [[0, 4, 5, 1]],
            "ep": [[1, 9, 5, 8]],
            "co": [0, 1, 4, 5],
            "eo": [1, 8, 5, 9]
        },

        "B": {
            "cp": [[2, 3, 7, 6]],
            "ep": [[3, 10, 7, 11]],
            "co": [2, 3, 6, 7],
            "eo": [3, 10, 7, 11]
        },
        "B'": {
            "cp": [[2, 6, 7, 3]],
            "ep": [[3, 11, 7, 10]],
            "co": [2, 3, 6, 7],
            "eo": [3, 10, 7, 11]
        },

        "R": {
            "cp": [[0, 4, 7, 3]],
            "ep": [[0, 8, 4, 11]],
            "co": [0, 3, 4, 7],
            "eo": [0, 8, 4, 11]
        },
        "R'": {
            "cp": [[0, 3, 7, 4]],
            "ep": [[0, 11, 4, 8]],
            "co": [0, 3, 4, 7],
            "eo": [0, 8, 4, 11]
        },

        "L": {
            "cp": [[1, 2, 6, 5]],
            "ep": [[2, 9, 6, 10]],
            "co": [1, 2, 5, 6],
            "eo": [2, 9, 6, 10]
        },
        "L'": {
            "cp": [[1, 5, 6, 2]],
            "ep": [[2, 10, 6, 9]],
            "co": [1, 2, 5, 6],
            "eo": [2, 9, 6, 10]
        }
    }

    # -------------------------
    # APPLY MOVE
    # -------------------------
    def move(self, m):
        m = Cube.MOVES[m]

        cp = self.corner_permutation[:]
        co = self.corner_orientation[:]
        ep = self.edge_permutation[:]
        eo = self.edge_orientation[:]

        # corners permutation
        for cycle in m["cp"]:
            self._cycle(cp, cycle)

        # edges permutation
        for cycle in m["ep"]:
            self._cycle(ep, cycle)

        # corner orientation
        for i in m["co"]:
            self.corner_orientation[i] = (co[i] + 1) % 3

        # edge orientation
        for i in m["eo"]:
            self.edge_orientation[i] = eo[i] ^ 1

        self.corner_permutation = cp
        self.edge_permutation = ep

    def shuffle(self, n=20):
        moves = list(Cube.MOVES.keys())

        last_move = None

        for _ in range(n):
            m = random.choice(moves)

            # évite les répétitions inutiles (ex: U puis U')
            while last_move and m[0] == last_move[0]:
                m = random.choice(moves)

            self.move(m)
            last_move = m


cube_resolved = Cube(corner_permutation, corner_orentation, edge_permutation, edge_orientation)
#cube_resolved.move("F")
#cube_resolved.edge_orientation[0] = 1
#cube_resolved.show()

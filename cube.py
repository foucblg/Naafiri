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

cp = [i for i in range(8)]
corner_orentation = [0 for _ in range(8)]
ep = [i for i in range(12)]
eo = [0 for _ in range(12)]


class Cube:
    def __init__(self, cp, co, ep, eo):
        self.cp = cp
        self.co = co
        self.ep = ep
        self.eo = eo

    # -------------------------
    # DEBUG
    # -------------------------
    def __str__(self):
        return (
            f"Corners perm: {self.cp}\n"
            f"Corners orient: {self.co}\n"
            f"Edges perm: {self.ep}\n"
            f"Edges orient: {self.eo}\n"
        )
    def to_vector(self):
        L = [i for i in self.cp]
        L+= [i for i in self.co]
        L+= [i for i in self.ep]
        L+= [i for i in self.eo]
        return L

    def copy(self):
        return Cube(
            self.cp[:],
            self.co[:],
            self.ep[:],
            self.eo[:]
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
            col = col_corners[self.cp[i]]
            for p_i, p in enumerate(pos):
                tab[p[0]][p[1]] = col[(p_i + self.co[i])%3]
            
        for i in range(12):
            pos = pos_edges[i]
            col = col_edges[self.ep[i]]
            for p_i, p in enumerate(pos):
                tab[p[0]][p[1]] = col[(p_i + self.eo[i])%2]

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
        # --- FACE HAUT (UP) ---
        "U": {
            "cp": [3, 0, 1, 2, 4, 5, 6, 7],
            "co": [0, 0, 0, 0, 0, 0, 0, 0],
            "ep": [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
            "eo": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        
        # --- FACE BAS (DOWN) ---
        "D": {
            "cp": [0, 1, 2, 3, 5, 6, 7, 4],
            "co": [0, 0, 0, 0, 0, 0, 0, 0],
            "ep": [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11],
            "eo": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },

        # --- FACE AVANT (FRONT) ---
        "F": {
            "cp": [1, 5, 2, 3, 0, 4, 6, 7],
            "co": [1, 2, 0, 0, 2, 1, 0, 0],
            "ep": [0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11],
            "eo": [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0] # F retourne 4 arêtes
        },

        # --- FACE ARRIÈRE (BACK) ---
        "B": {
            "cp": [0, 1, 3, 7, 4, 5, 2, 6],
            "co": [0, 0, 1, 2, 0, 0, 2, 1],
            "ep": [0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7],
            "eo": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1] # B retourne 4 arêtes
        },

        # --- FACE DROITE (RIGHT) ---
        "R": {
            "cp": [4, 1, 2, 0, 7, 5, 6, 3],
            "co": [2, 0, 0, 1, 1, 0, 0, 2],
            "ep": [8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0],
            "eo": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },

        # --- FACE GAUCHE (LEFT) ---
        "L": {
            "cp": [0, 2, 6, 3, 4, 1, 5, 7],
            "co": [0, 1, 2, 0, 0, 2, 1, 0],
            "ep": [0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11],
            "eo": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
    }

    # -------------------------
    # APPLY MOVE
    # -------------------------
    def move(self, m_name):
        m = Cube.MOVES[m_name]
        
        # 1. On calcule les nouveaux tableaux
        # On va chercher l'ancienne pièce (cp) et son ancienne orientation (co)
        # à l'index d'origine (m["cp"][i]), puis on y ajoute la torsion du mouvement.
        
        new_cp = [self.cp[m["cp"][i]] for i in range(8)]
        new_co = [(self.co[m["cp"][i]] + m["co"][i]) % 3 for i in range(8)]
        
        new_ep = [self.ep[m["ep"][i]] for i in range(12)]
        new_eo = [(self.eo[m["ep"][i]] + m["eo"][i]) % 2 for i in range(12)]

        # 2. On met à jour l'état du cube
        self.cp = new_cp
        self.co = new_co
        self.ep = new_ep
        self.eo = new_eo

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


cube_resolved = Cube(cp, corner_orentation, ep, eo)
# cube_resolved.move("R")
# cube_resolved.move("F")
# # cube_resolved.cp[0] = 1
# # cube_resolved.cp[1] = 0
# print(cube_resolved)
# cube_resolved.show()

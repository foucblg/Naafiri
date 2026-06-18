# 0: URF
# 1: UFL
# 2: ULB
# 3: UBR
# 4: DFR
# 5: DLF
# 6: DBL
# 7: DRB

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
corner_orentiation = [0 for i in range(8)]
edge_permutation = [i for i in range(12)]
edge_orientation = [0 for i in range(12)]


class Cube:
    def __init__(self, corner_permutation, corner_orentiation,edge_permutation, edge_orientation):
        self.corner_permutation = corner_permutation
        self.corner_orentiation = corner_orentiation
        self.edge_permutation = edge_permutation
        self.edge_orientation = edge_orientation
    def U(self):
        for i in range(1, 4):
            self.corner_permutation[i] = self.corner_permutation[i-1]
            self.edge_permutation[i] = self.edge_permutation[i-1]
        self.corner_permutation[0] = self.corner_permutation[3]
        self.edge_permutation[0] = self.edge_permutation[3]



cube_resolved = Cube(corner_permutation, corner_orentiation, edge_permutation, edge_orientation)
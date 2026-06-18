# 0: URF
# 1: UFL
# 2: ULB
# 3: UBR
# 4: DFR
# 5: DLF
# 6: DBL
# 7: DRB

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

cube = Cube(corner_permutation, corner_orentiation, edge_permutation, edge_orientation)
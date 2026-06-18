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
corner_orentation = [0 for _ in range(8)]
edge_permutation = [i for i in range(12)]
edge_orientation = [0 for _ in range(12)]


class Cube:
    def __init__(self, corner_permutation, corner_orentation,edge_permutation, edge_orientation):
        self.corner_permutation = corner_permutation
        self.corner_orentation = corner_orentation
        self.edge_permutation = edge_permutation
        self.edge_orientation = edge_orientation

    def __str__(self):
                return (
            f"Corner permutation : {self.corner_permutation}\n"
            f"Corner orientation : {self.corner_orentation}\n"
            f"Edge permutation : {self.edge_permutation}\n"
            f"Edge orientation : {self.edge_orientation}\n"
        )

    def copy(self):
        return Cube(
            self.corner_permutation[:],
            self.corner_orentation[:],
            self.edge_permutation[:],
            self.edge_orientation[:]
        )


    def U(self):
        tmp_corners = self.corner_permutation[:]
        tmp_edges = self.edge_permutation[:]
        self.corner_permutation[0] = tmp_corners[3]
        self.corner_permutation[3] = tmp_corners[2]
        self.corner_permutation[2] = tmp_corners[1]
        self.corner_permutation[1] = tmp_corners[0]
        self.edge_permutation[0] = tmp_edges[3]
        self.edge_permutation[3] = tmp_edges[2]
        self.edge_permutation[2] = tmp_edges[1]
        self.edge_permutation[1] = tmp_edges[0]
        
    def U_prime(self):
        tmp_corners = self.corner_permutation[:]
        tmp_edges = self.edge_permutation[:]
        self.corner_permutation[3] = tmp_corners[0]
        self.corner_permutation[2] = tmp_corners[3]
        self.corner_permutation[1] = tmp_corners[2]
        self.corner_permutation[0] = tmp_corners[1]
        self.edge_permutation[3] = tmp_edges[0]
        self.edge_permutation[2] = tmp_edges[3]
        self.edge_permutation[1] = tmp_edges[2]
        self.edge_permutation[0] = tmp_edges[1]



cube_resolved = Cube(corner_permutation, corner_orentation, edge_permutation, edge_orientation)

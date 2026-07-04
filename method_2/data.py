from cube import cube_resolved
from torch import save

def random_generation():
    L = []
    for i in range (3):
        for _ in range(int(100)):
            cube = cube_resolved.copy()
            cube.shuffle(i)
            L.append(cube.to_one_list())
    save(L, "method_2/data.pt")

def generate_test():
    L = []
    for i in range (3):
        for _ in range(int(10)):
            cube = cube_resolved.copy()
            cube.shuffle(i)
            L.append(cube.to_one_list())
    save(L, "method_2/test.pt")

random_generation()
# generate_test()

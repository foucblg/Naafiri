from cube import cube_resolved
from torch import save

def random_generation():
    L = []
    samples_per_depth = {1: 1000, 2: 2000, 3: 3000, 4: 8000, 5: 12000, 6: 16000}
    for i in range (1,7):
        for _ in range(samples_per_depth[i]):
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

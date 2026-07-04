from cube import cube_resolved

def random_generation():

    fichier = open("method_2/data.txt", "w")
    for i in range (3):
        for _ in range(int(10)):
            cube = cube_resolved.copy()
            cube.shuffle(i)
            fichier.write(f"{cube.to_one_list()}\n")
    return fichier

def generate_test():
    fichier = open("method_2/test.txt", "w")
    for i in range (30):
        for _ in range(int(10)):

            cube = cube_resolved.copy()
            cube.shuffle(i)
            fichier.write(f"[{str(cube.to_vector())},{i}]\n")
    return fichier

random_generation()
# generate_test()

from cube import cube_resolved

def random_generation():

    fichier = open("data.txt", "w")
    
    for i in range (30):               #nombre de melange
        for _ in range(int(1000)):            #mélangé X fois

            cube = cube_resolved.copy()
            cube.shuffle(i)
            fichier.write(f"[{str(cube.to_vector())},{i}]\n")
    return fichier

def generate_test():
    fichier = open("test.txt", "w")
    
    for i in range (30):               #nombre de melange
        for _ in range(int(10)):            #mélangé X fois

            cube = cube_resolved.copy()
            cube.shuffle(i)
            fichier.write(f"[{str(cube.to_vector())},{i}]\n")
    return fichier

random_generation()
generate_test()

from cube import cube_resolved

def random_generation():

    fichier = open("data.txt", "w")
    
    for i in range (10):               #nombre de melange
        for j in range(10):            #mélangé X fois

            cube = cube_resolved.copy()
            cube.shuffle(j)
            fichier.write(f"{cube},{i}\n")
    return fichier

random_generation()
    

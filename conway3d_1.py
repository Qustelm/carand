import copy
import numpy
import random
import sys
from tqdm import tqdm

args = sys.argv[1:]
CZ = int(args[0])
CX = int(args[1])
CY = int(args[2])
seed = int(args[3])
iters = int(args[4])
rule1 = int(args[5])
rule2 = int(args[6])

world = [[[0 for i in range(CX)] for j in range(CY)] for t in range(CZ)]

bin_seed = bin(seed)[2:]
x_,y_,z_=0,0,0
for i in range(len(bin_seed)):
    if i%CX==0:
        x_=0
        y_+=1
        if i%(CX*CY)==0:
            z_+=1
            y_=0
    world[z_][y_][x_] = int(bin_seed[i])
    x_+=1


def logic(world):
    alive_coords = []
    cp_world = copy.deepcopy(world)
    for z in range(len(cp_world)):
        for y in range(len(cp_world[z])):
            for x in range(len(cp_world[z][y])):
                neighbors = 0
                cell = cp_world[z][y][x]
                neighbors_cells = [
                    [z,y,x-1],
                    [z,y,x+1],

                    [z,y-1,x],
                    [z,y-1,x-1],
                    [z,y-1,x+1],
                    [z,y+1,x],
                    [z,y+1,x-1],
                    [z,y+1,x+1],

                    [z-1,y,x],
                    [z-1,y,x-1],
                    [z-1,y,x+1],
                    [z-1,y-1,x],
                    [z-1,y-1,x-1],
                    [z-1,y-1,x+1],
                    [z-1,y+1,x],
                    [z-1,y+1,x-1],
                    [z-1,y+1,x+1],
                    
                    [z+1,y,x],
                    [z+1,y,x-1],
                    [z+1,y,x+1],
                    [z+1,y-1,x],
                    [z+1,y-1,x-1],
                    [z+1,y-1,x+1],
                    [z+1,y+1,x],
                    [z+1,y+1,x-1],
                    [z+1,y+1,x+1],
                ]

                for i in neighbors_cells:
                    try:
                        if cp_world[i[0]][i[1]][i[2]] == 1:
                            neighbors+=1
                    except:
                        pass

                if cp_world[z][y][x] == 0:
                    if neighbors >= rule1:
                        world[z][y][x] = 1
                elif cp_world[z][y][x] == 1:
                    if neighbors >= 1 and neighbors <= rule2:
                        world[z][y][x] = 1
                    else:
                        world[z][y][x] = 0

    return world


for i in tqdm(range(iters)):
    world = logic(world)

def shaker(s):
    new_s = list(s)
    for i in range(len(new_s)):
        j = (i * 17 + 5) % len(new_s)
        new_s[i], new_s[j] = new_s[j], new_s[i]
    return ''.join(new_s)

def shaker2(s):
    new_s = list(s)
    for i in range(len(new_s)):
        j = (i * 12 + 5) % len(new_s)
        new_s[i], new_s[j] = new_s[j], new_s[i]
    return ''.join(new_s)

random_string = ""
for z in range(len(world)):
    for y in range(len(world[z])):
        for x in range(len(world[z][y])):
            random_string += str(world[z][y][x])


for k in range(100):
    random_string = shaker(random_string)
for k in range(100):
    random_string = shaker2(random_string)


with open("rand", 'w') as file:
    file.write(random_string)

import pygame
from math import cos, sin, sqrt, radians
import time
import copy
import numpy
import random
pygame.init()

W = 500
H = 500

CZ = 10
CX = 10
CY = 10

SIZE = 20

screen = pygame.display.set_mode((W, H))
 
world = [[[0 for i in range(CX)] for j in range(CY)] for t in range(CZ)]
seed = 123**12
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


'''
configuration = []
for sveshnikov in configuration:
    world[sveshnikov[2]][sveshnikov[1]][sveshnikov[0]] = 1
'''

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
                    if neighbors == 3:
                        world[z][y][x] = 1
                        alive_coords.append([x, y, z])
                elif cp_world[z][y][x] == 1:
                    if neighbors >= 2 and neighbors <= 3:
                        world[z][y][x] = 1
                        alive_coords.append([x, y, z])
                    else:
                        world[z][y][x] = 0
                       
    return world, alive_coords


bx, by, bz = 250, 250, 0

def Mx(phi, x, y, z):
    rot_matrix = numpy.array([[1, 0, 0], [0, cos(phi), sin(phi)], [0, -sin(phi), cos(phi)]])
    new_matrix = numpy.dot(numpy.array([x, y, z]), rot_matrix)
    return new_matrix

def My(phi, x, y, z):
    rot_matrix = numpy.array([[cos(phi), 0, -sin(phi)], [0, 1, 0], [sin(phi), 0, cos(phi)]])
    new_matrix = numpy.dot(numpy.array([x, y, z]), rot_matrix)
    return new_matrix

def Mz(phi, x, y, z):
    rot_matrix = numpy.array([[cos(phi), sin(phi), 0], [-sin(phi), cos(phi), 0], [0, 0, 1]])
    new_matrix = numpy.dot(numpy.array([x, y, z]), rot_matrix)
    return new_matrix

class Point3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotateX(self, angle):
        self.x, self.y, self.z = Mx(angle, self.x, self.y, self.z)
    def rotateY(self, angle):
        self.x, self.y, self.z = My(angle, self.x, self.y, self.z)
    def rotateZ(self, angle):
        self.x, self.y, self.z = Mz(angle, self.x, self.y, self.z)

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x+bx, self.y+by), 1)


angleX = 0
angleY = 0
angleZ = 0
class Face:
    def __init__(self, points):
        self.points = points
        self.center = 0
        self.update_center()

    def update_center(self):
        total_x = sum([point.x for point in self.points])
        total_y = sum([point.y for point in self.points])
        total_z = sum([point.z for point in self.points])
        num_points = len(self.points)
        self.center = Point3d(total_x/num_points, total_y/num_points, total_z/num_points)

    def draw(self):
        arr = []
        for i in range(len(self.points)):
            arr.append((self.points[i].x+bx, self.points[i].y+by))
        pygame.draw.polygon(screen, (100+self.center.z*.4, 0, 0), arr)
        for i in range(len(self.points)):
            pygame.draw.aaline(screen, (255, 255, 255), (self.points[i].x+bx, self.points[i].y+by), (self.points[(i+1)%len(self.points)].x+bx, self.points[(i+1)%len(self.points)].y+by))

def get_distance(p1, p2):
    return sqrt( (p1.x-p2.x)**2 + (p1.y-p2.y)**2 + (p1.z-p2.z)**2)

class Cube:
    def __init__(self, x, y, z, size):
        self.faces = [
            Face([Point3d(x, y, z), Point3d(x + size, y, z), Point3d(x + size, y, z + size), Point3d(x, y, z + size)]),
            Face([Point3d(x, y, z), Point3d(x, y + size, z), Point3d(x + size, y + size, z), Point3d(x + size, y, z)]),
            Face([Point3d(x, y, z), Point3d(x, y, z + size), Point3d(x, y + size, z + size), Point3d(x, y + size, z)]),
            Face([Point3d(x + size, y, z), Point3d(x + size, y + size, z), Point3d(x + size, y + size, z + size), Point3d(x + size, y, z + size)]),
            Face([Point3d(x, y, z + size), Point3d(x + size, y, z + size), Point3d(x + size, y + size, z + size), Point3d(x, y + size, z + size)]),
            Face([Point3d(x, y + size, z), Point3d(x, y + size, z + size), Point3d(x + size, y + size, z + size), Point3d(x + size, y + size, z)])
        ]
        self.center = Point3d(0, 0, 0)
        for k in self.faces:
            for t in k.points:
                self.center.x += t.x
                self.center.y += t.y
                self.center.z += t.z

        self.center.x/=8
        self.center.y/=8
        self.center.z/=8

    def draw(self):
        
        self.faces.sort(key=lambda face: face.center.z, reverse=True)
        for face in range(len(self.faces)-1, -1, -1):
            self.faces[face].update_center()
            self.faces[face].draw()

    def rotate(self, angle_x, angle_y, angle_z):
        for i in self.faces:
            for j in i.points:
                j.rotateX(angle_x)
                j.rotateY(angle_y)
                j.rotateZ(angle_z)

cubes = []

angleX = 10
angleY = 10
angleZ = 10

step = 1
angles = [25, 45, 0]
timer = 0
while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.KEYDOWN:
            #d-100
            #a-97
            if i.key == 32:
                world, coords, = logic(world)
                print(coords)

            if i.key == pygame.K_RIGHT:
                angles[1]+=step
                for dicks in cubes:
                    dicks.rotate(radians(0), radians(angleY), radians(0))
            if i.key == pygame.K_LEFT:
                angles[1]-=step
                for dicks in cubes:
                    dicks.rotate(radians(0), radians(-angleY), radians(0))
            if i.key == pygame.K_DOWN:
                angles[0]+=step
                for dicks in cubes:
                    dicks.rotate(radians(angleX), radians(0), radians(0))
            if i.key == pygame.K_UP:
                angles[0]-=step
                for dicks in cubes:
                    dicks.rotate(radians(-angleX), radians(0), radians(0))
            if i.key == 100:
                angles[2]+=step
                for dicks in cubes:
                    dicks.rotate(radians(0), radians(0), radians(angleZ))
            if i.key == 97:
                angles[2]-=step
                for dicks in cubes:
                    dicks.rotate(radians(0), radians(0), radians(-angleZ))

    screen.fill((0, 0, 0))
    angles[1]+=5
    #angles[2]+=1
    if timer%2 == 0:
        #print(world)
        cubes = []
        world, coords = logic(world)
        for balls in coords:
            obj = Cube(balls[0]*SIZE-CX*SIZE/2, balls[1]*SIZE-CY*SIZE/2, balls[2]*SIZE-CZ*SIZE/2, SIZE)
            obj.rotate(radians(angles[0]), radians(angles[1]), radians(angles[2]))
            cubes.append(obj)
    timer += 1
    faces = []
    
    for efimus in cubes:
        efimus.draw()
    for efimus in cubes:
        faces += efimus.faces

    faces.sort(key=lambda face: face.center.z, reverse=True)
    for face in range(len(faces)-1, -1, -1):
        faces[face].update_center()
        faces[face].draw()

    pygame.image.save(screen, f"C:/Users/Admin/Downloads/captured/7/{timer}.jpeg")
    pygame.display.update()
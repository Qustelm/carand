import copy
import sys
args = sys.argv[1:]
seed = int(args[0])
iters = int(args[1])

world = ["0", "0"] + [i for i in bin(seed)[2:]] + ["0", "0"]

def logic(world, rule):
	bin_rule = bin(rule)[2:]
	bin_rule = "0"*(8 - len(bin_rule)) + bin_rule
	cp_world = world + []
	for i in range(1, len(cp_world)-1, 1):
		state = cp_world[i-1]+cp_world[i]+cp_world[i+1]
		world[i] = bin_rule[::-1][int(state, 2)]

	return ["0"] + world + ["0"]

world = logic(world, 45)

for i in range(iters):
	world = logic(world, 45)

rand_string = ''.join(world[len(world)//2:])
print(rand_string)
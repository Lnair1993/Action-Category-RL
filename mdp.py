from utils import vector_add
import copy
import random

class MDP:
    def __init__(self, grid, terminals, actlist, obj_act, obj_loc, obj_order,
                 non_obj_loc, obj_state, init, gamma = 0.9):
        grid.reverse()
        self.grid = grid #row 0 on bottom
        self.terminals = terminals
        self.gamma = gamma
        self.agent_init = init
        self.actlist = actlist

        #ACR+Q learning
        self.obj_loc = obj_loc
        self.obj_order = obj_order
        self.obj_act = obj_act
        self.non_obj_loc = non_obj_loc
        self.obj_state = obj_state

        state1 = [init]
        for elt in obj_order:
            state1.append(obj_state[elt])

        self.state_init = tuple(state1)

    def reset(self):  #Reset game world
        non_obj_loc = self.non_obj_loc
        for elt in non_obj_loc.keys():
            if "Portal" not in elt and "Chest" not in elt and "Lever" not in elt:
                loc = non_obj_loc[elt]
                self.grid[loc[1]][loc[0]] = None

    def R(self, state):  #Reward function, given a state
        state1 = list(state)
        agent_state = state1[0]
        return self.grid[agent_state[1]][agent_state[0]]

    def T(self, state, action, obj): #Transition, given state and action
        if action is None:
            return state
        elif action == "push" or action == "pick":
            return self.interact(state, action, obj)
        elif action == "wait":
            return state
        elif action == "teleport":
            return self.interact(state, action, obj)
        elif action == "open":
            return self.interact(state, action, obj)
        elif action == "pull":
            return self.interact(state, action, obj)
        else:
            return self.go(state, action)

    def interact(self, state, action, obj):
        state1 = list(state)
        agent_state = state1[0]

        if obj is None:                 #No objects
            return state
        else:                           #Object exists
            if action in self.obj_act[obj] and action in ["push","pick"]:
                idx = self.obj_order.index(obj) + 1
                state1[idx] = 0
                door_loc = self.non_obj_loc[obj]
                self.grid[door_loc[1]][door_loc[0]] = -0.04
                return tuple(state1)
            elif action in self.obj_act[obj] and action == "teleport":
                idx = self.obj_order.index(obj) + 1
                state1[idx] = 0
                port_location = self.non_obj_loc[obj]
                state1[0] = port_location
                return tuple(state1)
            elif action in self.obj_act[obj] and action == "pull":
                #Activates portal
                idx = self.obj_order.index(obj) + 1
                state1[idx] = 0
                port_location = self.non_obj_loc[obj]
                port_name = self.obj_loc[port_location]
                idx = self.obj_order.index(port_name) + 1
                state1[idx] = 1
                return tuple(state1)
            elif action in self.obj_act[obj] and action == "open":
                idx = self.obj_order.index(obj) + 1
                state1[idx] = 0
                key_loc = self.non_obj_loc[obj]
                key_name = self.obj_loc[key_loc]
                idx = self.obj_order.index(key_name) + 1
                state1[idx] = 1
                return tuple(state1)
            else:                       #Invalid action on object
                return state

    def go(self, state, action): #Basic movement actions
        grid = self.grid
        cols = len(grid[0])
        rows = len(grid)
        state1 = list(state)

        if action == "up":
            direction = (0,1)
        elif action == "down":
            direction = (0,-1)
        elif action == "left":
            direction = (-1,0)
        elif action == "right":
            direction = (1,0)
        else:
            print "Invalid action"

        #Noisy actions
        '''p = 0.8 #Probability of correct action
        rand_noise = random.uniform(0,1)
        if rand_noise > p:
            direction = list(direction)
            direction[0] = int(not(direction[0]))
            direction[1] = int(not(direction[1]))
            direction = tuple(direction)'''

        state1[0] = vector_add(state1[0], direction)
        x, y = state1[0][0], state1[0][1]
        if x in range(cols) and y in range(rows) and grid[y][x] is not None:
            return tuple(state1)
        else:
            return state

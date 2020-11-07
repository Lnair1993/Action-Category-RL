#Python Ver 2.7.12

from mdp import *
from rl import *

gamma = 0.9
init = (4,3)
world = 2

R = -0.04
actions = ["up","down","left","right","push"] #List of agent actions
start_world = [[R, R, R, R, R, -10, R, +100],
               [R, R, -10, R, R, R, R, R],
               [None, None, None, None, None, None, None, None],
               [R, R, R, R, R, R, R, R],
               [-10, R, R, -10, R, None, None, None],
               [R, R, R, R, R, R, R, R],
               [R, R, R, R, -10, None, None, None]]

term_states = [(5,6),(7,6),(2,5),(0,2),(3,2),(4,0)]

obj_state = {"Button1":1}
obj_order = ["Button1"] #Order in which objects rep in state
obj_loc = {(7,1):"Button1"}
obj_act = {"Button1":["push"]} #ACR
non_obj_loc = {"Button1":(3,4)}

#Initialize MDP
env = MDP(start_world, term_states, actions, obj_act, obj_loc, obj_order,
          non_obj_loc, obj_state, init, gamma)

N_episodes = 100
N_OAC = 30
OAC_flag = True
epsilon = 0.1

#Initialize Q-learning agent
agent = QLearningAgent(env, N_OAC, OAC_flag)

for episode in range(N_episodes):
    run_single_trial(agent, env, epsilon, episode)
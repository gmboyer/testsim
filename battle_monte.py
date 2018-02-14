import random
import numpy as np
import pandas
from collections import Counter
import matplotlib.pyplot as plt
import sys
import copy
import math
import time

from battle_scripts import *
from inventory_scripts import *
from character_scripts import *
from input_params import *



def battle_monte(c1_name = 'Rhonda', c1_sex = 'female', c1_str = 6, c1_dex = 6,
                 c1_con = 6, c1_int = 6, c1_wis = 6, c1_cha = 6, c1_lck = 0,
                 c1_SpAbil = [], c1_dualw = False, c1_armor = 'none',
                 c1_fightstyle = 'none', c2_name = 'Rufus', c2_sex = 'male',
                 c2_str = 6, c2_dex = 6, c2_con = 6, c2_int = 6, c2_wis = 6,
                 c2_cha = 6, c2_lck = 0, c2_SpAbil = [], c2_dualw = False,
                 c2_armor = 'none', c2_fightstyle = 'none', it = 2, dis = 0):

    # start the stopwatch!
    start_time = time.time()

    # specify characters here. This will override those in input params
    # current SpAbil supported: armor training, berserk, combat dicipline, sneak attack
    character_1 = {
        'name': c1_name,
        'sex': c1_sex,
        'stats':{'STR': c1_str,
                 'DEX': c1_dex,
                 'CON': c1_con,
                 'INT': c1_int,
                 'WIS': c1_wis,
                 'CHA': c1_cha,
                 'LCK': c1_lck},
        'SpAbil': c1_SpAbil,
        'primary hand': {'fist': 1},
        'offhand': {'fist': 1}, # fist for no weapon
        'dual-wielding': c1_dualw,
        'inventory': {'primary hand': {'fist': 1}, 'offhand': {'fist': 1}, 'backpack': {'knife': 1, 'greatsword': 1, 'longbow': 1}},
        'armor': c1_armor,
        'fighting style': c1_fightstyle,
        'armor bonus': 0, # extra armor bonus not imparted by armor
        'pace': 1,
        'natural weapons': [['fist', 2]],
        'initialized' : False,
        'in combat': False,
    }

    character_2 = {
        'name': c2_name,
        'sex': c2_sex,
        'stats':{'STR': c2_str,
                 'DEX': c2_dex,
                 'CON': c2_con,
                 'INT': c2_int,
                 'WIS': c2_wis,
                 'CHA': c2_cha,
                 'LCK': c2_lck},
        'SpAbil': c2_SpAbil,
        'primary hand': {'fist': 1},
        'offhand': {'fist': 1}, # fist for no weapon
        'dual-wielding': c2_dualw,
        'inventory': {'primary hand': {'fist': 1}, 'offhand': {'fist': 1}, 'backpack': {'knife': 1, 'greatsword': 1, 'longbow': 1}},
        'armor': c2_armor,
        'fighting style': c2_fightstyle,
        'armor bonus': 0, # extra armor bonus not imparted by armor
        'pace': 1,
        'natural weapons': [['fist', 2]],
        'initialized' : False,
        'in combat': False,
    }

    scene_generic = {
        #entities: [what it is, how many, countdown]
        'entities': [['flowers', 'carpet of', 2], ['grass', 'field of', 3], ['bunnies', 'several', 1]],
        'place': 'field',
        'theme': 'normal',
        'inventory': {'on ground': {'rapier': 1,'spear': 1,'greatsword': 1}}
    }



    # fight a bunch of times
    winner_list = []
    turn_list = []
    for i in range(it):
        seed = random.randrange(sys.maxsize)
        rng = random.Random(seed)
        c1 = derive_stats(copy.deepcopy(character_1)) # makes modifiable copy of the original char dictionary
        c2 = derive_stats(copy.deepcopy(character_2)) # makes modifiable copy of the original char dictionary
        scene = copy.deepcopy(scene_generic) # makes modifiable copy of the original scene dictionary
        fight_outcome = fight(c1, c2, it, surprised = [False, False], distance = dis, scene = scene)
        winner_list.append(fight_outcome[0]['name'])
        turn_list.append(fight_outcome[2])
        print("Progress {:2.1%}".format(i / it), end="\r")

    # stop the stopwatch
    print("Time elapsed: ", time.time() - start_time, " seconds")

    # plot winners
    if it > 1:
        winner_counts = Counter(winner_list)
        df_winner = pandas.DataFrame.from_dict(winner_counts, orient='index')
        df_winner.plot(kind='bar', legend=None)
        plt.ylabel('Count')
        plt.xlabel('Winner')

        turn_counts = Counter(turn_list)
        df_turns = pandas.DataFrame.from_dict(turn_counts, orient='index')
        df_turns.sort_index(inplace=True)
        df_turns.plot(kind='bar', legend=None)
        plt.ylabel('Count')
        plt.xlabel('Duration of battle (rounds)')




# if __name__ == '__main__':
#     main()

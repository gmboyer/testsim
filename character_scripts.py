import random
import numpy as np
import pandas
from collections import Counter
import matplotlib.pyplot as plt
from sys import exit
import copy
import math

# load order is important
from input_params import *
from battle_scripts import *
from inventory_scripts import *
from bestiary import *

class Entity(object):
    # initialize entity with a dictionary of properties
    def __init__(self, all_properties):
        self.all_properties = copy.deepcopy(all_properties)

class Character(Entity):

    # initialize entity with a dictionary of properties
    def __init__(self, char):
        self.char = copy.deepcopy(char)
        self.stats = self.char.get('stats')

    # input type is the bestiary dictionary used for randomizing appearance
    # default is by id, then by race
    def randomize_appearance(self, randtype = None):
        if randtype == None:
            randtype = self.char['id']
        self.char['sex'] = random.choice(['female', 'male'])
        self.randomize_name(randtype)
        if randtype != 'creature':
            self.char['race'] = randtype
        else:
            self.char['race'] = random.choice(['human', 'dwarf', 'elf', 'lizardfolk', 'catfolk'])

    # A function to randomize a character's name.
    # It first tries to name the character using any 'name' keys in the character's dictionary
    # If none are available, it tries to name the character using any 'name' keys in the character's race (if any)
    # If this doesn't work, it then the character's name is set equal to its id
    def randomize_name(self, char_id):
        lookup_creature_by_id = eval('char_' + char_id.replace(" ", "_"))
        if lookup_creature_by_id['race'] != lookup_creature_by_id['id']:
            try:
                lookup_creature_by_race = eval('char_' + lookup_creature_by_id['race'].replace(" ", "_"))
            except:
                lookup_creature_by_race = lookup_creature_by_id
        else:
            lookup_creature_by_race = lookup_creature_by_id
        if "names" in lookup_creature_by_id.keys():
            self.char['name'] = random.choice(lookup_creature_by_id['names'])
        elif "female names" in lookup_creature_by_id.keys() and self.char['sex'] == 'female':
            self.char['name'] = random.choice(lookup_creature_by_id['female names'])
        elif "male names" in lookup_creature_by_id.keys() and self.char['sex'] == 'male':
            self.char['name'] = random.choice(lookup_creature_by_id['male names'])
        elif "names" in lookup_creature_by_race.keys():
            self.char['name'] = random.choice(lookup_creature_by_race['names'])
        elif "female names" in lookup_creature_by_race.keys() and self.char['sex'] == 'female':
            self.char['name'] = random.choice(lookup_creature_by_race['female names'])
        elif "male names" in lookup_creature_by_race.keys() and self.char['sex'] == 'male':
            self.char['name'] = random.choice(lookup_creature_by_race['male names'])
        else:
            self.char['name'] = "the %s" % lookup_creature_by_id['id']

        if "last names" in lookup_creature_by_id.keys():
            self.char['name'] = "%s %s" % (self.char['name'], random.choice(lookup_creature['last names']))

    def randomize_class(self, classtype = None):
        if classtype == None:
            classtype = random.choice(['warrior', 'thief', 'cleric', 'mage'])

        if classtype == 'warrior':
            self.char['class'] = random.choice(['soldier', 'pirate', 'fighter', 'gladiator'])
        elif classtype == 'thief':
            self.char['class'] = random.choice(['rogue', 'bandit', 'hunter', 'assassin'])
        elif classtype == 'cleric':
            self.char['class'] = random.choice(['priest', 'druid', 'bishop', 'exorcist'])
        elif classtype == 'mage':
            self.char['class'] = random.choice(['sorcerer', 'wizard', 'warlock', 'necromancer'])

    # function to modify characterbbased on partial character dictionary
    def modify(self, partial_char_dict):
        for key in partial_char_dict.keys():
            self.char[key] = partial_char_dict[key]

# CODE FOR TESTING
# c1 = Character(character_1)
# c1.randomize_appearance("normal")
# c1.randomize_class()
# c2 = Character(character_2)
# c2.randomize_appearance("goblin")
# c2.randomize_class()
#
# print c1.char['name'], "the", c1.char['race'], c1.char['class']
# print c2.char['name'], "the", c2.char['race'], c2.char['class']
#
#
# fighter1 = derive_stats(copy.deepcopy(c1.char)) # makes modifiable copy of the original char dictionary
# fighter2 = derive_stats(copy.deepcopy(c2.char)) # makes modifiable copy of the original char dictionary
# fight_winner = fight(fighter1, fighter2, it, surprised=[False, False], distance = 9)
#
# exit(1)

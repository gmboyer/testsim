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
from bestiary import *
from character_scripts import *
from battle_scripts import *
from inventory_scripts import *
from description_scripts import *




# create main character
c1 = Character(char_creature)
c1.randomize_appearance("creature")
c1.randomize_class()
c1.modify(char_goblin)

# modify character race
# c1.modify(char_unicorn)
c1.randomize_appearance()

# further modification
# c1.modify(char_wispy_the_coffer_corpse)
# c1.modify({'skill':["stealth"]})

# deposit starting equipment into gear
deposit_item(c1.char, 'backpack', {'knife': 3, 'spear': 1})
print "starting inventory:", c1.char['inventory']
print list_inv(c1.char['inventory']['backpack'])

prev_scene = scene_generic



class Scene(object):

    # initialize class
    def __init__(self):
        self.scene = copy.deepcopy(scene_generic) # assign basic scene dictionary

    # function to modify scene based on partial scene dictionary
    def modify(self, partial_scene_dict):
        for key in partial_scene_dict.keys():
            self.scene[key] = partial_scene_dict[key]

    # def clean_scene(self):
    #     entities_to_pop = [entity for entity in self.scene['entities'] if 0 in entity[2]] # the last entry in entities should be its countdown timer
    #     for entity in entities_to_pop:
    #         entity_index = self.scene['entities'].index(entity)
    #         self.scene['entities'].pop(entity_index)

    # generate a random scene based on previous one
    def generate_random_scene(self):
        new_scene = {}
        surroundings = random.choice(["forest", "desert"])
        theme = random.choice(["normal", "haunted"])
        new_scene['place'] = WR("[desc_" + surroundings + "]") # determines objects / creatures in scene
        new_scene['theme'] = WR("[desc_" + theme + "]") # determines object flavor / creatures / creature theme

        # creature has to be related to surroundings or theme or both, but not neither
        while True:
            creature_based_on_surroundings = random.choice([True, False])
            creature_based_on_theme = random.choice([True, False])
            if not creature_based_on_surroundings and not creature_based_on_theme:
                pass
            else:
                break

        theme_modify = False
        if creature_based_on_surroundings and not creature_based_on_theme:
            rand_creature_table = "[rand_enc_table_" + surroundings + "]"
        elif not creature_based_on_surroundings and creature_based_on_theme:
            rand_creature_table = "[rand_enc_table_" + theme + "]"
        else: # creature based on both surroundings and theme
            rand_creature_table = "[rand_enc_table_" + surroundings + "]"
            theme_modify = True

        new_scene['narrative'] = "%s arrived at %s." % (c1.char['name'], new_scene['place'])

        # determine if a creature is in this scene
        new_scene['creature'] = WR(rand_creature_table)
        new_scene['hostile creature'] = False

        if new_scene['creature'] != 'nothing':
            # create creature stats
            creature = Character(char_creature)
            creature.modify(eval("char_" + new_scene['creature'].replace(" ", "_")))
            creature.randomize_appearance(creature.char['id'])

            # modify the creature based on the needs of the scene
            if theme_modify:
                creature.modify({'name' : creature.char['name'] + ' themed with ' + theme + ' theme'})
                creature.char['theme'].append(theme) # doesn't do anything yet, but could use derive_stats to assign weaknesses/strengths based on theme

            # integrate the creature into the scene
            new_scene['creature stats'] = derive_stats(creature.char)

            # determine how the creature acts in the scene
            creature_reaction = random.choice(creature.char['reaction'])

            # string together the scene narrative
            new_scene['narrative'] += " There is a %s %s here." % (new_scene['creature'], random.choice(creature.char['idle']))
            new_scene['narrative'] += " It wants to %s!" % (creature_reaction)

            # if creature is hostile, flag the scene for combat
            if creature_reaction == 'fight':
                new_scene['hostile creature'] = True

        # determine if there is treasure in the scene
        new_scene['treasure'] = random.choice(['nothing', 'nothing', 'nothing', 'meager', 'trove'])
        if new_scene['treasure'] != 'nothing':
            if new_scene['treasure'] == 'meager':
                new_scene['treasure'] = {'gold piece': rolldN_ne(10), 'dull gem': 1}
            elif new_scene['treasure'] == 'trove':
                new_scene['treasure'] = {'gold piece': rolldN_ne(1000), 'sparkling gem': 1}

            if len(new_scene['treasure']) > 0:
                new_scene['treasure narrative'] = "Inside a treasure chest was " + list_inv(new_scene['treasure']) + "!"
            else:
                new_scene['treasure narrative'] = "The treasure chest was empty."
        self.modify(new_scene)


class Adventure(Scene):
    def enter(self):
        print "%s the %s %s sets out on an adventure" % (c1.char['name'], c1.char['race'], c1.char['class'])
        prev_scene = None # the adventure is starting. No previous scene.

        while True:
            hit_enter()
            c1.char = derive_stats(c1.char)
            # mutate the scene
            self.generate_random_scene()
            print "current inventory", c1.char["inventory"]

            # describe the scene
            m2(self.scene['narrative'])

            # handle any hostile creatures in the scene
            if self.scene['hostile creature']:

                while True:
                    # determine distance
                    distance = rolldN_ne(4)

                    # assign the hostile creature's statistics as c2
                    c2 = derive_stats(copy.deepcopy(self.scene['creature stats']))

                    # sneaky characters can try to sneak past enemies
                    if "stealth" in c1.char['skill'][0]:
                        print "%s tries to sneak past..." % (c1.char['name'])
                        sneak_winner = opposed_roll("DEX", "INT", c1.char, c2)
                        if sneak_winner[0] == c1.char:
                            print "The %s did not see %s" % (c2['id'], pronoun(c1.char, "him"))
                            break
                        else:
                            print "%s spotted %s!"  % (c2['id'], c1.char['name'])

                    # peaceful characters will try talking before resorting to a fight
                    if "peace" in c1.char['ideal']:
                        if ("bloodlust" in c2['ideal'] and test('CHA', c1.char) >= full_success_thresh) \
                        or ("bloodlust" not in c2['ideal'] and test('CHA', c1.char) >= partial_success_thresh) \
                        or "peace" in c2['ideal']:
                            print "%s talked %s way out of the fight." % (c1.char['name'], pronoun(c1.char, "his"))
                            break
                        else:
                            print "%s tried to talk %s way out of the fight but this made the %s more hostile!\n" % (c1.char['name'], pronoun(c1.char, "his"), c2['id'])

                    # if the character cannot get out of the fight:
                    winner, loser = fight(c1.char, c2, 1, surprised = [False, False], distance = distance, scene = self.scene)
                    print "winner name:", winner['name']
                    c1.char['winner names'].append(winner['name'])
                    print "loser name:", loser["name"]
                    c1.char['battles won'] += 1
                    if winner != c1.char:
                        return 'death'

                    if len(loser['inventory']) > 0:
                        print "\n%s loots the remains of %s..." % (c1.char['name'], loser['name'])
                        for place in loser['inventory'].keys():
                            if len(loser['inventory'][place]) > 0:
                                print "... looted %s!" % list_inv(loser['inventory'][place])
                                deposit_item(c1.char, 'backpack', loser['inventory'][place])

                    if len(self.scene['inventory']) > 0:
                        print "All gear from scene to be looted:", self.scene['inventory']
                        for place in self.scene['inventory']:
                            print "THIS gear from scene to be looted:", weapon
                            if self.scene['inventory'] != [] \
                            and "natural weapon" not in weapon_table[weapon]:
                                deposit_item(winner, 'backpack', {weapon: 1})

                    break

            if self.scene['treasure'] != 'nothing':
                print self.scene['treasure narrative']
                deposit_item(c1.char, 'backpack', self.scene['treasure'])
                self.scene['treasure'] = 'nothing'


            if c1.char['shaken']:
                c1.char = derive_stats(c1.char)
                unshake(c1.char)
            if c1.char['bleeding']:
                unbleed_result = test('CON', c1.char)
                if unbleed_result >= full_success_thresh:
                    print "%s stopped bleeding." % (c1.char['name'])
                    c1.char['bleeding'] = False
                elif unbleed_result >= partial_success_thresh:
                    print "%s continues bleeding..." % (c1.char['name'])
                else:
                    print "%s succumbed to bleeding and fell unconcious!" % (c1.char['name'])
                    return 'death'

            # have character react to scene (generate/change needs)
            # resolve scene according to character needs
            # reevaluate character needs
            # loop until death

class Death(Scene):
    def enter(self):
        print "\n%s died!" % (c1.char['name'])
        print "%s fought in %d battles." % (pronoun(c1.char, "he").title(), c1.char['battles won'])
        print "Game over!"
        print "winner names:", c1.char['winner names']
        exit(1)


class Map(object):

    scenes = {
        'adventure': Adventure(),
        'death': Death(),
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return Map.scenes[scene_name]

    def opening_scene(self):
        return self.next_scene(self.start_scene)

class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()

        while True:
            print "\n--------"
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

a_map = Map('adventure')
a_game = Engine(a_map)
a_game.play()

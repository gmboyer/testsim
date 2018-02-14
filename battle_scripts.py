import random
import numpy as np
import pandas
from collections import Counter
import matplotlib.pyplot as plt
import sys
import copy
import math

# load order is important
# from character_scripts import *
from input_params import *
from inventory_scripts import *


# FIGHTING STYLE table
fighting_style_table = {
    'none':         [ 0,  0],
    'well-rounded': [-1,  1],
    'defensive':    [ 1, -1],
    'finesse':      [-2, -2],
    'powerful':     [ 2,  2],
    'dual-weapon':  [ 0,  0], # handled in derive_stats()
}

combat_table = {
    '0': [3, 'knocked out'],
    '1': [2, 'disarm and trip'],
    '2': [2, 'critical strike'],
    '3': [1, 'winds of war'],
    '4': [1, 'unexpected strike'],
    '5': [1, 'recover'],
    '6': [1, 'feint'],
    '7': [0, 'feint'],
    '8': [0, 'change stance'],
    '9': [0, 'mind games'],
    '10': [0, 'miss!'],
    '11': [0, 'miss!'],
    '12': [0, 'demoralize'],
    '13': [1, 'wind-up'],
    '14': [1, 'winds of war'],
    '15': [2, 'pushback'],
    '16': [2, 'knockdown'],
    '17': [3, 'extra attack'],
    '18': [3, 'disarm'],
    '19': [4, 'bleeding'],
    '20': [4, 'incapacitation'],
    '21': [5, 'incapacitation'],
}

# opportunities that arise in the combat table
# 1st entry: what actor may roll
# 2nd entry: what target may roll
opportunity_table = {
    'incapacitation': ['STR', ['STR', 'DEX']],
    'knocked out':  ['DEX', ['STR','DEX']],
    'critical strike': ['DEX', ['STR','DEX']],
    'unexpected strike': ['DEX', ['INT','DEX']],
    'bleeding': ['STR', ['STR', 'CON']],
    'extra attack': ['STR', ['STR', 'DEX']],
    'wind-up': 'none',
    'feint': ['DEX',['DEX','INT']],
    'mind games': ['INT','INT'],
    'demoralize': [['STR','CHA'],'WIS'],
    'recover': [['DEX', 'CON'], 'DEX'],
    'knockdown': ['STR', ['STR', 'DEX']],
    'change stance': [['DEX','INT'], ['INT']],
    'disarm and trip': [['DEX','STR'], ['DEX', 'STR']],
    'disarm': [['DEX','STR'], ['DEX', 'STR']],
    'winds of war': [['INT','WIS','CHA'], ['DEX', 'STR']],
    'pushback': ['STR', 'STR'],
}



# function for rolling an exploding N-sided die
def rolldN(N):
    result_of_roll = random.randint(1, N)
    total = result_of_roll

    explosion_satisfied = False
    while explosion_satisfied == False:
        if result_of_roll == N:
            result_of_roll = random.randint(1, N)
            total = total + result_of_roll
        else:
            explosion_satisfied = True
    return total

# function for rolling a non-exploding N-sided die
def rolldN_ne(N):
    return random.randint(1,N)

# function to take the higer of two dedicate
def higher(stat1, stat2):
    stat1_roll = stat1
    stat2_roll = stat2
    if stat1 != 0:
        stat1_roll = rolldN(stat1)
    if stat2 != 0:
        stat2_roll = rolldN(stat2)
    if stat1_roll >= stat2_roll:
        return stat1_roll
    else:
        return stat2_roll

# function for rolling 4d6 and dropping the lowest
def roll_4d6_drop_lowest():
    fourd6 = [rolldN_ne(6), rolldN_ne(6), rolldN_ne(6), rolldN_ne(6)]
    return sum(fourd6)-min(fourd6)

# function for rolling 3d6
def roll_3d6():
    return rolldN_ne(6) + rolldN_ne(6) + rolldN_ne(6)

# function for rolling 2d10
def roll_2d10():
    return rolldN_ne(10) + rolldN_ne(10)

# function to lookup and apply gender pronouns
def pronoun(c, lookup_string):
    pronoun_vals = {
        'he': 0,
        'him': 1,
        'his': 2,
        'himself': 3,
    }
    f_pro = ['she', 'her', 'her', 'herself']
    m_pro = ['he', 'him', 'his', 'himself']
    o_pro = ['it', 'it', 'its', 'itself']
    if c['sex'] == 'female':
        return f_pro[pronoun_vals[lookup_string]]
    elif c['sex'] == 'male':
        return m_pro[pronoun_vals[lookup_string]]
    else:
        return o_pro[pronoun_vals[lookup_string]]

# functions for printing messages when combat iterations = 1
# example: m('This is a','message with', 4, 'arguments')
def m0(*arg):
    # if detail <= 0 and it == 1:
        # print(' '.join([str(item) for item in arg]))
    return
def m1(*arg):
    # if detail <= 1 and it == 1:
        # print(' '.join([str(item) for item in arg]))
    return
def m2(*arg):
    # if detail <= 2 and it == 1:
        # print(' '.join([str(item) for item in arg]))
    return

# make a stat test
def test(stat, char):
    return higher(char['stats'][stat], char['stats']['LCK']) - char['wound penalty']

# apply shift to attack result
def shift(attack_roll, c_actor, c_target):
    c_actor = derive_stats(c_actor)
    c_target = derive_stats(c_target)

    if c_actor['current hand'] == 'primary':
        shift_left = 'primary left shift'
        shift_right = 'primary right shift'
        c_actor[shift_left] = weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][0]
        c_actor[shift_right] = weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][1]
    else:
        shift_left = 'offhand left shift'
        shift_right = 'offhand right shift'
        c_actor[shift_left] = weapon_table[list(c_actor['inventory']['offhand'].keys())[0]][0]
        c_actor[shift_right] = weapon_table[list(c_actor['inventory']['offhand'].keys())[0]][1]

    # include shift from fighting style
    c_actor[shift_left] += fighting_style_table[c_actor['fighting style']][0]
    c_actor[shift_right] += fighting_style_table[c_actor['fighting style']][1]

    # dual-wielding characters shift to center by 2
    if c_actor['dual-wielding']:
        # SpAbil: Fighting Style Dual-Weapon. No penalty to primary-hand atack when dual-wielding
        if c_actor['current hand'] == 'primary' and c_actor['fighting style'] == 'dual-weapon':
            pass
        else:
            c_actor[shift_left] += 2
            c_actor[shift_right] -= 2

    if c_actor['prone']:
        c_actor[shift_left] += 2
        c_actor[shift_right] -= 2

    if c_target['prone']:
        c_actor[shift_left] -= 2
        c_actor[shift_right] += 2

    if attack_roll <= 10:
        attack_result = attack_roll + c_actor[shift_left] - c_target['wounds']
    else:
        attack_result = attack_roll + c_actor[shift_right] + c_target['wounds']

    return attack_result

def opposed_roll(actor_test, target_test, c_actor, c_target):
    c_actor = derive_stats(c_actor)
    c_target = derive_stats(c_target)

    if isinstance(actor_test, list):
        # choose the highest stat among choices available
        beststat = actor_test[0] # starting point for choosing highest stat
        for stat in actor_test:
            if c_actor['stats'][stat] > c_actor['stats'][beststat]:
                beststat = stat
        actor_test = beststat

    if isinstance(target_test, list):
        # choose the highest stat among choices available
        beststat = target_test[0] # starting point for choosing highest stat
        for stat in target_test:
            if c_target['stats'][stat] > c_target['stats'][beststat]:
                beststat = stat
        target_test = beststat

    c_actor_roll = test(actor_test, c_actor)
    c_target_roll = test(target_test, c_target)

    opposed_roll_resolved = False
    while not opposed_roll_resolved:
        if c_actor_roll > c_target_roll:
            win_order = [c_actor, c_target]
            opposed_roll_resolved = True
        elif c_actor_roll < c_target_roll:
            win_order = [c_target, c_actor]
            opposed_roll_resolved = True
        elif c_actor['stats'][actor_test] > c_target['stats'][target_test]:
            win_order = [c_actor, c_target]
            opposed_roll_resolved = True
        elif c_actor['stats'][actor_test] < c_target['stats'][target_test]:
            win_order = [c_target, c_actor]
            opposed_roll_resolved = True
        else:
            c_actor_roll = test(actor_test, c_actor)
            c_target_roll = test(target_test, c_target)

    m1(c_actor['name'], 'tested', actor_test, 'and got', \
            c_actor_roll, 'against', c_target['name'], '\'s', \
            target_test, 'of', c_target_roll)

    win_order.append(c_actor_roll)
    win_order.append(c_target_roll)

    # returns [winner dict, loser dict, winner roll, loser roll]
    return win_order

# calculate a character's defensive range
def derive_armor(char):
    # calculate defensive range
    defense_lowrange =  11 - char['stats']['DEX']/2 - char['armor bonus'] - armor_table[char['armor']][0]
    defense_highrange =  10 + char['stats']['STR']/2 + char['armor bonus'] + armor_table[char['armor']][0]

    # SpAbil: Fighting Style (Defensive). Increase defensive range by 1
    if char['fighting style'] == 'defensive':
        defense_lowrange -= 4
        defense_highrange += 4

    # apply shield bonus
    # print "OFFHAND INV KEYS", char['inventory']['offhand'].keys()
    # print "PRIMARY INV KEYS", char['inventory']['primary hand'].keys()
    if 'shield' in list(char['offhand'].keys()):
        defense_lowrange -= 1
        defense_highrange += 1
    if 'shield' in list(char['primary hand'].keys()):
        defense_lowrange -= 1
        defense_highrange += 1

    # apply defensive range (no need to return anything)
    char['defense range'] = [defense_lowrange, defense_highrange]


# calculate a character's 'derived stats' and append
def derive_stats(char):

    # calculate the character's defensive range
    derive_armor(char)

    # initialize conditions upon character creation
    # but do not overwrite current number of wounds, etc.
    if not char['initialized']:
        char['initialized'] = True
        # include the misc conditions
        char['two-handing'] = False
        char['berserking'] = False
        char['bleeding'] = False
        char['shaken'] = False
        char['wounds'] = 0
        char['death door'] = False
        char['prone'] = False

    # conditions that are overwritten after battle
    if not char['in combat']:
        char['current hand'] = 'primary'
        char['wind-up'] = [False, 0] # [is winding up?, turn to be released]

    # calculate wound penalty
    if char['berserking']:
        # SpAbil: Berserk. Ignore wound penalties while berserking
        char['wound penalty'] = 0
    elif char['wounds'] > 0:
        char['wound penalty'] = 2
    else:
        char['wound penalty'] = 0

    # calculate whether the character is weilding a 2H weapon
    if "fist" not in list(char['inventory']['primary hand'].keys())[0] and "claw" not in list(char['inventory']['primary hand'].keys())[0]:
        if '2H' in eval_prefix_name("item", list(char['inventory']['primary hand'].keys())[0])['keywords']:
            char['two-handing'] = True

    return char



def roll_combat_table(attack_result):
    if attack_result < 0:
        attack_result = 0
    if attack_result > 21:
        attack_result = 21
    damage = combat_table[str(attack_result)][0]
    opportunity = combat_table[str(attack_result)][1]
    hit_result = [damage, opportunity]
    return hit_result


def haveSpAbil(target, ability):
    if ability in target['SpAbil']:
        return True
    else:
        return False

    # attempt to unshake
def unshake(c_actor):
    c_actor = derive_stats(c_actor)

    if c_actor['shaken']:
        unshake_roll = test('WIS', c_actor)
        m0(c_actor['name'], 'rolls WIS to unshake and gets a', unshake_roll)
        if unshake_roll >= partial_success_thresh:
            c_actor['shaken'] = False

def get_natural_weapon_hand(c_actor):
    all_nat_weaps = [weapon[0] for weapon in c_actor['natural weapons'] if "1H" in weapon_table[weapon[0]]]
    if len(all_nat_weaps) > 1:
        return random.choice(all_nat_weaps)
    elif len(all_nat_weaps) == 1:
        return all_nat_weaps[0]
    else:
        print("get_natural_weapon_hand error: no natural weapons available")

# function to evaluate current weaponry in gear and surroundings and retrieve/switch weapons around
# returns c_actor, scene after shifting weaponry around
evaluate_weaponry_bugtesting = False
def evaluate_weaponry(c_actor, c_target, distance, scene):
    count_evaluations = -1 # the first evaluation will count as '0'
    char_before_this_eval = [copy.deepcopy(c_actor)]

    # evaluate situation, determine needs, converge on weapon choice
    while True:

        char_before_this_eval.append(copy.deepcopy(c_actor))
        count_evaluations += 1
        derive_armor(c_actor) # because shields may have been equipped/unequipped, rederive armor
        # Break out of weapon evaluation loop if nothing has
        # changed between consecutive loops
        if char_before_this_eval[-2] == char_before_this_eval[-1] and count_evaluations != 0:
            break
        elif count_evaluations == 1:
            if evaluate_weaponry_bugtesting:
                m0("Number of times weapon(s) evaluated:", count_evaluations)
                m0("Primary hand:", c_actor['inventory']['primary hand'])
                m0("Offhand:", c_actor['inventory']['offhand'])
            pass
        else:
            if evaluate_weaponry_bugtesting:
                m0("Number of times weapon(s) evaluated:", count_evaluations)
                m0("Primary hand:", c_actor['inventory']['primary hand'])
                m0("Offhand:", c_actor['inventory']['offhand'])

        if evaluate_weaponry_bugtesting:
            m0("GEAR:", c_actor['inventory'])
            m0("GEAR IN SCENE:", scene['inventory'])

        if count_evaluations > c_actor['stats']['INT']/2 - 1:
            break

        # determine needs for ONE HAND AT A TIME
        hand_considered, hand_not_considered = 'primary hand', 'offhand'

        # weapon need keywords
        req_keywords, forb_keywords, pref_keywords, prefnot_keywords = ['weapon'], ['0H'], [], []

        if hand_considered == 'primary hand':
            prefnot_keywords += ['unarmed']

        if hand_considered == 'offhand':
            req_keywords += ['natural weapon']

        if c_actor['fighting style'] == "powerful":
            if hand_considered == 'primary weapon':
                pref_keywords += ['2H']

        if c_actor['fighting style'] == "finesse":
            pref_keywords += ['1H', 'light']
            prefnot_keywords += ['2H']

        if c_actor['fighting style'] == "dual-weapon":
            pref_keywords += ['1H', 'light']
            prefnot_keywords += ['2H', 'shield']

        if c_actor['fighting style'] == "well-rounded":
            pref_keywords += ['1H', 'adaptable']

        if c_actor['dual-wielding']:
            req_keywords += ['1H', 'light']

        if distance > 0:
            pref_keywords += ['ranged']
            prefnot_keywords += ['melee']
        if distance <= 0:
            req_keywords += ['melee']

        if distance <= 0:
            if c_actor['stats']['STR'] < 6:
                pref_keywords += ['light', '1H']
                prefnot_keywords += ['large', '2H']
            if c_actor['stats']['STR'] >= 8:
                pref_keywords += ['large', '2H']
                prefnot_keywords += ['light']
            if c_actor['stats']['DEX'] >= 8:
                pref_keywords += ['light', '1H']


        # # remove dupes
        # req_keywords = list(set(req_keywords))
        # forb_keywords = list(set(forb_keywords))
        # pref_keywords = list(set(pref_keywords))
        # prefnot_keywords = list(set(prefnot_keywords))

        needs_keywords = {"req": req_keywords, "forb": forb_keywords, "pref": pref_keywords, "prefnot": prefnot_keywords}

        if evaluate_weaponry_bugtesting:
            m0("NEEDS KEYWORDS:", needs_keywords)

        # hand needs determined


        # pick best weapon in surroundings and on person or in hand based on needs
        chosen_items = {}
        for place in list(c_actor['inventory'].keys()):
            chosen_items[place] = dict([[choose_item(c_actor['inventory'][place], needs_keywords).get('name', 'fist'), 1]])

        for place in list(c_actor['inventory'].keys()):
            chosen_items[place] = dict([[choose_item(c_actor['inventory'][place], needs_keywords).get('name', 'fist'), 1]])

        chosen_items_final = dict([[choose_item(chosen_items[place], needs_keywords).get('name', 'fist'), 1] for place in list(chosen_items.keys())])


        chosen_item = choose_item(chosen_items_final, needs_keywords)

        if evaluate_weaponry_bugtesting:
            m0("NEEDS:", needs_keywords)

        if evaluate_weaponry_bugtesting:
            m0("CHOSEN ITEM:", chosen_item.get('name'))

        # chosen item is already in considered hand
        if chosen_item == list(c_actor['inventory'][hand_considered].keys()):
            if evaluate_weaponry_bugtesting:
                print("chosen item was already in the character currently considered hand:", hand_considered)
                print("no action needs to be taken!")
        # chosen item in other hand
        elif chosen_item['name'] in list(c_actor['inventory']['offhand'].keys()):
            if evaluate_weaponry_bugtesting:
                print("chosen item for this hand was in the character's OTHER hand:", hand_not_considered)
            if "natural weapon" not in weapon_table[list(c_actor['inventory'][hand_considered].keys())[0]]:
                deposit_item(c_actor, hand_not_considered, {list(c_actor['inventory'][hand_considered].keys())[0]: 1})
            c_actor['inventory'][hand_considered] = {chosen_item['name']: 1}
            if "natural weapon" not in weapon_table[list(c_actor['inventory'][hand_not_considered].keys())[0]]:
                deposit_item(c_actor, hand_considered, {list(c_actor['inventory'][hand_not_considered].keys())[0]: 1})
        # chosen item in backpack
        elif chosen_item['name'] in list(c_actor['inventory']['backpack'].keys()):
            if evaluate_weaponry_bugtesting:
                print("chosen item was in the character's gear")
            if "natural weapon" not in weapon_table[list(c_actor['inventory'][hand_considered].keys())[0]]:
                deposit_item(c_actor, 'backpack', {list(c_actor['inventory'][hand_considered].keys())[0] : 1})
            c_actor['inventory'][hand_considered] = {chosen_item['name']: 1}
            withdraw_item(c_actor, 'backpack', {chosen_item['name']: 1}, True)
        # chosen item in scene
        elif chosen_item['name'] in list(c_actor['inventory']['on the ground'].keys()):
            if evaluate_weaponry_bugtesting:
                print("chosen item was", list(scene['inventory'].keys())[0])
            if "natural weapon" not in weapon_table[list(c_actor['inventory'][hand_considered].keys())[0]]:
                deposit_item(c_actor, 'backpack', {list(c_actor['inventory'][hand_considered].keys())[0] : 1})
            c_actor['inventory'][hand_considered] = {chosen_item['name']: 1}
            withdraw_item(scene, 'on the ground', {chosen_item['name']: 1}, True)

        else:
            print("Choose weapon error!")

        # chosen weapon equipped. Time to reevaluate situation

        # switch hand to be considered
        hand_considered, hand_not_considered = hand_not_considered, hand_considered

    return c_actor, scene


def fight(c1, c2, iterations, surprised, distance, scene):
    c1 = derive_stats(c1)
    c2 = derive_stats(c2)
    c1['in combat'], c2['in combat'] = True, True

    # Surprise and Initiative: Determine surprise, and test DEX to see who acts first
    if surprised[0] and surprised[1]:
        m2(c1['name'], 'and', c2['name'], 'surprise each other!')
        initiative_result = opposed_roll('DEX','DEX', c1, c2)
        c_actor = initiative_result[0]
        c_target = initiative_result[1]
    elif surprised[0] and not surprised[1]:
        m2(c2['name'], 'surprises', c1['name'], '!')
        c_actor, c_target = c2, c1
    elif not surprised[0] and surprised[1]:
        m1(c1['name'], 'surprises', c2['name'], '!')
        c_actor, c_target = c1, c2
    else:
        m2(c1['name'], 'and', c2['name'], 'begin to fight!')
        initiative_result = opposed_roll('DEX','DEX', c1, c2)
        c_actor = initiative_result[0]
        c_target = initiative_result[1]

    round_counter = 1
    battle_resolved = False
    while not battle_resolved:

        c1 = derive_stats(c1)
        c2 = derive_stats(c2)

        m0('TURN:', round_counter)
        m0('Acting:', c_actor['name'])

        m0('With wounds:', c_actor['wounds'])
        m0('Is shaken?', c_actor['shaken'])



        # attempt to keep Bleeding in check
        if c_actor['bleeding']:
            bleed_roll = test('CON', c_actor)
            m1(c_actor['name'], 'tested CON to stop bleeding and rolled a', bleed_roll)
            if full_success_thresh > bleed_roll >= partial_success_thresh:
                m1(c_actor['name'], 'is still bleeding.')
            elif bleed_roll >= full_success_thresh:
                c_actor['bleeding'] = False
                m1(c_actor['name'], 'stopped the bleeding.')
            else:
                m1(c_actor['name'], 'succumbed to bleeding and fell unconscious!')
                battle_resolved = True
                winner, loser = c_target, c_actor
                break

        # attempt to unshake
        if c_actor['shaken']:
            unshake_roll = test('WIS', c_actor)
            m0(c_actor['name'], 'rolls WIS to unshake and gets a', unshake_roll)
            if unshake_roll >= partial_success_thresh:
                c_actor['shaken'] = False

        # attempt to get up from Prone
        if c_actor['prone']:
            get_up_roll = test('DEX', c_actor)
            m1(c_actor['name'], 'rolls DEX to stand up and gets a', get_up_roll)
            if get_up_roll >= full_success_thresh:
                c_actor['prone'] = False
                m1(c_actor['name'], 'stood up!')
            elif get_up_roll >= partial_success_thresh:
                c_actor['prone'] = False
                m1(c_actor['name'], 'stood up!')
            else:
                m1(c_actor['name'], 'remains prone.')

        # have the actor evaluate / adjust weaponry
        c_actor, scene = evaluate_weaponry(c_actor, c_target, distance, scene)


        # give the current actor 1 attack at the start of each round
        # dual-wielding characters get two attacks instead
        if not c_actor['dual-wielding']: # NOT Dual-Wielding
            c_actor['attacks remaining'] = 1
        else:
            c_actor['attacks remaining'] = 2

        ### MOVEMENT
        c_actor['moves remaining'] = c_actor['pace']
        while c_actor['moves remaining'] > 0:
            if distance > weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][3]       \
            and not c_actor['prone']:
                ### character is able/willing to move
                # take a double move
                if distance > 2 * c_actor['pace']:
                    distance -= 2 * c_actor['pace']
                    c_actor['attacks remaining'] = 0
                    m1(c_actor['name'], 'rushes toward', c_target['name'], 'but hasn\'t reached', pronoun(c_target, 'him'))
                    break
                # charge if within charging range and have a close-range weapon
                elif c_actor['moves remaining'] < distance <= 2 * c_actor['moves remaining'] and weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][3] == 0:
                    distance = 0
                    c_actor['attacks remaining'] = 1
                    m1(c_actor['name'], 'charged into', c_target['name'], '!')
                    break
                # move forward if a double move and charge is not necessary
                elif distance > 1:
                    distance -= 1
                    c_actor['moves remaining'] -= 1
                    m1(c_actor['name'], 'moved closer to',c_target['name'])
                elif distance == 1:
                    distance -= 1
                    c_actor['moves remaining'] -= 1
                    m1(c_actor['name'], 'moved within striking distance of',c_target['name'])
            # if prone and target is outside of weapon range
            elif c_actor['prone']                                          \
            and (distance > weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][3]      \
            or distance > weapon_table[list(c_actor['inventory']['offhand'].keys())[0]][3]):
                distance -= 1
                c_actor['moves remaining'] -= 1
                m1(c_actor['name'], 'crawled closer to', c_target['name'])
            # If wielding a ranged weapon and target is too close, move backward
            elif distance < weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][2]     \
            and not c_actor['prone']:
                distance += 1
                c_actor['moves remaining'] -= 1
                m1(c_actor['name'], 'moved away from', c_target['name'])
            else:
                break

        m0('Distance:', distance)

        # if outside of weapon's range, can't attack
        if weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][2] < distance > weapon_table[list(c_actor['inventory']['primary hand'].keys())[0]][3] \
        and  weapon_table[list(c_actor['inventory']['offhand'].keys())[0]][2] < distance > weapon_table[list(c_actor['inventory']['offhand'].keys())[0]][3]:
            c_actor['attacks remaining'] = 0
            # choose new weapon if available

        # if current actor has remaining attacks, make them
        while c_actor['attacks remaining'] > 0:

            ### Make attack roll
            if c_target['death door']:
                attack_roll = rolldN_ne(20)
                attack_dietype = 'd20'
            elif c_target['shaken'] == True:
                attack_roll = roll_2d10()
                attack_dietype = '2d10'
            else:
                attack_roll = roll_3d6()
                attack_dietype = '3d6'

            # SpAbil: Berserk. If actor is berserking, roll d20 for attacks
            if c_target['berserking'] or c_actor['berserking']:
                attack_roll = rolldN_ne(20)
                attack_dietype = 'd20'

            # SpAbil: Combat Dicipline. Actor ALWAYS rolls 2d10
            if haveSpAbil(c_actor, 'combat dicipline'):
                attack_roll = roll_2d10()
                attack_dietype = '2d10'

            # apply shift to attack roll
            attack_result = shift(attack_roll, c_actor, c_target)

            try:
                m0('Current Hand:', c_actor['current hand'])
                m0('Primary Left Shift:', c_actor['primary left shift'], 'Primary Right Shift:', c_actor['primary right shift'])
                m0('Offhand Left Shift:', c_actor['offhand left shift'], 'Offhand Right Shift:', c_actor['offhand right shift'])
            except:
                pass

            if c_actor['current hand'] == 'primary':
                m1(c_actor['name'], 'attacks with', pronoun(c_actor, 'his'), list(c_actor['inventory']['primary hand'].keys())[0], '.')
            elif c_actor['current hand'] == 'Offhand':
                m1(c_actor['name'], 'attacks with', pronoun(c_actor, 'his'), list(c_actor['inventory']['offhand'].keys())[0], '.')
            else:
                m0('ERROR: Which hand is current hand?')

            m0('Attack Roll:', attack_roll, 'rolled with', attack_dietype)
            m0('Attack Result:', attack_result)

            # apply Wind-Up shift (if any)
            if c_actor['wind-up'][0] and round_counter == c_actor['wind-up'][1]:
                if attack_result <= 10:
                    attack_result -= 2
                else:
                    attack_result += 2
                c_actor['wind-up'][0] = False
                c_actor['wind-up'][1] = 0
                m1(c_actor['name'], 'releases the Wind-Up! Attack result:', attack_result)

            # target gets a chance to burn luck die if their situation is dire
            dire_range = [1, 20] # what is considered dire? [low, high]
            if dire_range[0] >= attack_result or attack_result >= dire_range[1]:
                if c_target['wounds'] > 0 and c_target['stats']['LCK'] > 0:
                    original_attack_result = attack_result # needed for reporting
                    burn_luck_result = rolldN(c_target['stats']['LCK'])
                    if dire_range[0] >= attack_result:
                        attack_result = attack_result + burn_luck_result
                        if attack_result >= 10:
                            attack_result = 10 #prevents overshooting center
                    elif attack_result >= dire_range[1]:
                        attack_result = attack_result - burn_luck_result
                        if attack_result <= 11:
                            attack_result = 11 #prevents overshooting center
                    if c_target['stats']['LCK'] == 4:
                        c_target['stats']['LCK'] = 0
                    else:
                        c_target['stats']['LCK'] -= 2
                    m1(c_target['name'], 'burned luck and rolled', burn_luck_result, \
                        'shifting the attack result from', original_attack_result, 'to', attack_result)

            # determine the effect of the attack
            attack_effect = roll_combat_table(attack_result)
            attack_opportunity = attack_effect[1]

            # Prone characters can't take advantage of opportunities
            if c_actor['prone']:
                attack_opportunity = ''
                m1(c_actor['name'], 'is prone and cannot take advantage of opportunities.')

            # calculate initial damage
            attack_damage = attack_effect[0]


            ################################################
            ########## Combat Table Opportunities ##########
            ################################################
            opp_result = [c_actor['name'], c_target['name'], 0, 0]

            # Opportunity: Miss!
            if attack_opportunity == 'miss!':
                m1(c_actor['name'], 'missed!')

            # Opportunity: Winds of War
            if attack_opportunity == 'winds of war':
                if c_actor['stats']['LCK'] < 12:
                    stat_to_test = opportunity_table[attack_opportunity]
                    m1(c_actor['name'], 'is trying to improve', pronoun(c_actor, 'his'), 'luck.')
                    opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                    if opp_result[0]['name'] == c_actor['name']:
                        if c_actor['stats']['LCK'] == 0:
                            c_actor['stats']['LCK'] = 4
                        else:
                            c_actor['stats']['LCK'] += 2
                        m1(c_actor['name'], 'increased', pronoun(c_actor, 'his'), 'luck!')
                    else:
                        m1(c_target['name'], 'prevented it!')
                else:
                    m1(c_actor['name'], 'had the opportunity to improve', pronoun(c_actor, 'his'), 'luck but', pronoun(c_actor, 'he'), 'is already at max!')

            # Opportunity: Disarm. Disarm the target's primary or offhand weapon.
            if attack_opportunity == 'disarm':
                if "natural weapon" not in weapon_table[list(c_target['inventory']['primary hand'].keys())[0]] or "natural weapon" not in weapon_table[list(c_target['inventory']['offhand'].keys())[0]] or not c_target['prone']:
                    stat_to_test = opportunity_table[attack_opportunity]
                    m1(c_actor['name'], 'is trying to disarm and/or knock', c_target['name'], 'to the ground!')
                    opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                    if opp_result[0]['name'] == c_actor['name']:
                        if "natural weapon" not in weapon_table[list(c_target['inventory']['primary hand'].keys())[0]]:
                            deposit_item(scene, 'on ground', c_target['inventory']['primary hand'])
                            weapname = list(c_target['inventory']['offhand'].keys())[0]
                            c_target['inventory']['primary hand'] = {get_natural_weapon_hand(c_target): 1}
                            m1(c_actor['name'], 'disarmed', c_target['name'], 'of the', weapname, 'in', pronoun(c_target, 'his'), 'primary hand!')
                        if "natural weapon" not in weapon_table[list(c_target['inventory']['offhand'].keys())[0]]:
                            deposit_item(scene, 'on ground', c_target['inventory']['offhand'])
                            weapname = list(c_target['inventory']['offhand'].keys())[0]
                            c_target['offhand'] = {get_natural_weapon_hand(c_target): 1}
                            m1(c_actor['name'], 'disarmed', c_target['name'], 'of the', weapname, 'in', pronoun(c_target, 'his'), 'off-hand!')
                    else:
                        m1(c_target['name'], 'resisted!')
                else:
                    m1(c_actor['name'], 'had the opportunity to disarm', c_target['name'], 'down but', pronoun(c_target, 'he'), 'is not holding a weapon.')
                # because shields may have been equipped/unequipped, rederive armor
                derive_armor(c_target)

            # Opportunity: Disarm and Trip. Fully disarm the target of primary and offhand weapon and knock prone.
            if attack_opportunity == 'disarm and trip':
                if "natural weapon" not in weapon_table[list(c_target['inventory']['primary hand'].keys())[0]] or "natural weapon" not in weapon_table[list(c_target['inventory']['offhand'].keys())[0]] or not c_target['prone']:
                    stat_to_test = opportunity_table[attack_opportunity]
                    m1(c_actor['name'], 'is trying to disarm and/or knock', c_target['name'], 'to the ground!')
                    opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                    if opp_result[0]['name'] == c_actor['name']:
                        if "natural weapon" not in weapon_table[list(c_target['inventory']['primary hand'].keys())[0]]:
                            deposit_item(scene, 'on ground', c_target['inventory']['primary hand'])
                            weapname = list(c_target['inventory']['offhand'].keys())[0]
                            c_target['inventory']['primary hand'] = {get_natural_weapon_hand(c_target): 1}
                            m1(c_actor['name'], 'disarmed', c_target['name'], 'of the', weapname, 'in', pronoun(c_target, 'his'), 'primary hand!')
                        if "natural weapon" not in weapon_table[list(c_target['inventory']['offhand'].keys())[0]]:
                            deposit_item(scene, 'on ground', c_target['inventory']['offhand'])
                            weapname = list(c_target['inventory']['offhand'].keys())[0]
                            c_target['offhand'] = {get_natural_weapon_hand(c_target): 1}
                            m1(c_actor['name'], 'disarmed', c_target['name'], 'of the', weapname, 'in', pronoun(c_target, 'his'), 'off-hand!')
                        if not c_target['prone']:
                            c_target['prone'] = True
                            m1(c_target['name'], 'was knocked down!')
                    else:
                        m1(c_target['name'], 'resisted!')
                else:
                    m1(c_actor['name'], 'had the opportunity to disarm and knock', c_target['name'], 'down but', pronoun(c_target, 'he'), 'is already prone and disarmed.')
                # because shields may have been equipped/unequipped, rederive armor
                derive_armor(c_target)

            # Opportunity: Knockdown
            if attack_opportunity == 'knockdown':
                if not c_target['prone']:
                    stat_to_test = opportunity_table[attack_opportunity]
                    m1(c_actor['name'], 'is trying to knock', c_target['name'], 'to the ground!')
                    opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                    if opp_result[0]['name'] == c_actor['name']:
                        c_target['prone'] = True
                        m1(c_target['name'], 'was knocked down!')
                    else:
                        m1(c_target['name'], 'resisted!')
                else:
                    m1(c_actor['name'], 'had the opportunity to knock', c_target['name'], 'down but', pronoun(c_target, 'he'), 'is already prone.')

            # Opportunity: Shaken
            if attack_opportunity == 'feint' or attack_opportunity == 'mind games' or attack_opportunity == 'demoralize' or attack_opportunity == 'change stance':
                if not c_target['shaken']:
                    stat_to_test = opportunity_table[attack_opportunity]
                    m1(c_actor['name'], 'is trying to shake', c_target['name'], 'by using', attack_opportunity)
                    opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                    if opp_result[0]['name'] == c_actor['name']:
                        c_target['shaken'] = True
                        m1(c_target['name'], 'is shaken!')
                    else:
                        m1(c_target['name'], 'resisted!')
                else:
                    m1(c_actor['name'], 'had the opportunity to shake', c_target['name'], 'but', pronoun(c_target, 'he'), 'is already shaken.')

            # Opportunity: Recover. Recover from a wound or the Shaken status
            if attack_opportunity == 'recover':
                if c_actor['wounds'] > 0:
                    stat_to_test = opportunity_table[attack_opportunity]
                    m1(c_actor['name'], 'is trying to recover from a wound...')
                    opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                    if opp_result[0]['name'] == c_actor['name']:
                        c_actor['wounds'] -= 1
                        m1(c_actor['name'], 'recovered from one wound!')
                    else:
                        m1(c_target['name'], 'prevented it!')
                elif c_actor['shaken'] == True:
                    stat_to_test = opportunity_table[attack_opportunity]
                    m1(c_actor['name'], 'is trying to recover from Shaken...')
                    opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                    if opp_result[0]['name'] == c_actor['name']:
                        c_actor['shaken'] = False
                        m1(c_actor['name'], 'recovered from being shaken!')
                    else:
                        m1(c_target['name'], 'prevented it!')
                else:
                    m1(c_actor['name'], 'had the opportunity to recover but', pronoun(c_actor, 'he'), 'is fine!')

            # Opportunity: Unexpected Strike
            if attack_opportunity == 'unexpected strike':
                stat_to_test = opportunity_table[attack_opportunity]
                m1(c_actor['name'], 'is going for an unexpected strike!')
                opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                if opp_result[0]['name'] == c_actor['name']:
                    crit_damage = 2
                    attack_damage += crit_damage
                    m1('Unexpected strike!', crit_damage, 'extra damage dealt!')
                else:
                    m1(c_target['name'], 'saw it coming and resisted!')

            # Opportunity: Critical Strike
            if attack_opportunity == 'critical strike':
                stat_to_test = opportunity_table[attack_opportunity]
                m1(c_actor['name'], 'is going for a critical strike!')
                opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                if opp_result[0]['name'] == c_actor['name']:
                    crit_damage = 4
                    attack_damage += crit_damage
                    m1('Critical strike!', crit_damage, 'extra damage dealt!')
                else:
                    m1(c_target['name'], 'resisted!')

            # Opportunity: Incapacitation
            if attack_opportunity == 'incapacitation':
                m1(c_actor['name'], 'tries for an incapacitating strike!')
                stat_to_test = opportunity_table[attack_opportunity]
                opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                if opp_result[0]['name'] == c_actor['name']:
                    m1(c_actor['name'], 'incapacitated', c_target['name'], '!!!')
                    battle_resolved = True
                    winner, loser = c_actor, c_target
                    break
                else:
                    m1(c_target['name'], 'resisted!')

            # Opportunity: Knocked Out
            if attack_opportunity == 'knocked out':
                m1(c_actor['name'], 'tries for a knockout blow!')
                stat_to_test = opportunity_table[attack_opportunity]
                opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                if opp_result[0]['name'] == c_actor['name']:
                    m1(c_actor['name'], 'knocked out', c_target['name'], '!!!')
                    battle_resolved = True
                    winner, loser = c_actor, c_target
                    break
                else:
                    m1(c_target['name'], 'resisted!')

            # Opportunity: Extra Attack
            if attack_opportunity == 'extra attack':
                m1(c_actor['name'], 'is trying for an extra attack!')
                stat_to_test = opportunity_table[attack_opportunity]
                opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                if opp_result[0]['name'] == c_actor['name']:
                    c_actor['attacks remaining'] += 1
                else:
                    m1(c_target['name'], 'resisted!')

            # Opportunity: Wind-Up
            if attack_opportunity == 'wind-up':
                c_actor['wind-up'][0] = True
                c_actor['wind-up'][1] = round_counter + 2 # wind-up to be released next turn
                m1(c_actor['name'], 'is Winding-Up...')

            # Opportunity: Bleeding
            if attack_opportunity == 'bleeding':
                m1(c_actor['name'], 'is going for a bleeding strike!')
                stat_to_test = opportunity_table[attack_opportunity]
                opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                if opp_result[0]['name'] == c_actor['name']:
                    c_target['bleeding'] = True
                    m1('Success!', c_target['name'], 'is bleeding!')
                else:
                    m1(c_target['name'], 'resisted!')

            # Opportunity: Pushback
            if attack_opportunity == 'pushback':
                m1(c_actor['name'], 'tries to push', c_target['name'], 'back!')
                stat_to_test = opportunity_table[attack_opportunity]
                opp_result = opposed_roll(stat_to_test[0], stat_to_test[1], c_actor, c_target)
                if opp_result[0]['name'] == c_actor['name']:
                    distance += 3
                    m1('Success!', c_target['name'], 'was shoved backward!')
                else:
                    m1(c_target['name'], 'resisted!')

            ### Apply damage
            m0('Two-Handing:', c_actor['two-handing'])

            # SpAbil: Sneak Attack. Deal 1 extra damage on attack rolls of 5 or less.
            if attack_result <= 4 and haveSpAbil(c_actor, 'sneak attack'):
                attack_damage += 2
                m1(c_actor['name'], 'dealt extra damage with Sneak Attack (SpAbil)!')

            # reduce any damage by 1 if attack result is in target defense range
            if attack_damage > 0 and c_target['defense range'][0] <= attack_result <= c_target['defense range'][1]:
                attack_damage -= 1

            # reduce damage by 1 if target got full success in opportunity opposed roll and won
            if attack_damage > 0 and opp_result[3] >= full_success_thresh and opp_result[0]['name'] == c_target['name']:
                attack_damage -= 1
                m1(c_target['name'], 'reduced damage by rolling a full success!')

            # SpAbil: Armor Training. Reduce damage by 1
            if attack_damage > 0 and c_target['defense range'][0] <= attack_result <= c_target['defense range'][1] and haveSpAbil(c_target, 'armor training') and c_target['armor'] != 'none':
                attack_damage = attack_damage - 1
            # apply Shaken and damage
            if attack_damage > 0 and not c_target['shaken']:
                c_target['shaken'] = True
                attack_damage = attack_damage - 1
                c_target['wounds'] = c_target['wounds'] + attack_damage
            elif attack_damage > 0 and c_target['shaken']:
                c_target['wounds'] = c_target['wounds'] + attack_damage
            # SpAbil: Berserk. If wounded, go berserk.
            if haveSpAbil(c_target, 'berserk') and attack_damage > 0:
                c_target['berserking'] = True

            # if target's wound threshold exceeded, they are at Death's Door
            if not c_target['death door'] and c_target['wounds'] >= c_target['stats']['CON']/2:
                c_target['death door'] = True


            m0('Target Shaken?', c_target['shaken'])
            m0('Wounds Dealt', attack_damage)


            # characters with extra attacks
            if c_actor['attacks remaining'] > 0:
                c_actor['attacks remaining'] -= 1
                if c_actor['attacks remaining'] > 0:
                    m1(c_actor['name'], 'makes an extra attack!')
                # Dual-Wielding characters make a single offhand attack
                if c_actor['dual-wielding'] and c_actor['attacks remaining'] == 1:
                    c_actor['current hand'] = 'Offhand'
                    m1(c_actor['name'], 'makes an offhand weapon attack!')

        # Dual-Wielding characters switch back to primary weapon at the end of the round
        if c_actor['dual-wielding']:
            c_actor['current hand'] = 'primary'

        if iterations == 1 and detail <= 1:
            hit_enter()

        m1('\n') #add a space between rounds
        attack_damage = 0
        round_counter = round_counter + 1
        c_actor, c_target = c_target, c_actor

        if round_counter >= 50:
            winner = {"name": 'DRAW', "inventory": {}}
            loser = {"name": 'DRAW', "inventory": {}}
            break

    m2(winner['name'].title(), 'won the fight!')
    c_actor['in combat'], c_target['in combat'] = False, False

    # deposit all equipment belonging to the loser into their 'inventory' for easy looting by the winner
    places_to_check = ['primary hand', 'offhand']
    for place in places_to_check:
        if loser['inventory'].get(place) != None \
        and "natural weapon" not in weapon_table[list(loser['inventory'][place].keys())[0]] \
        and len(loser[place]) > 0:
            deposit_item(winner, 'backpack', {list(loser['inventory'][place].keys())[0]: 1})

    return [winner, loser, round_counter - 1]

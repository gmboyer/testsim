import random
import math
import sys

# load order is important
from input_params import *
# from character_scripts import *
from battle_scripts import *

# function to join a name to a prefix and evaluate the resulting string
# arguments are strings
# returns an evaluated variable
def eval_prefix_name(prefix, name):
    return eval(prefix + "_" + name.replace(" ", "_"))

# function to clean up a list of items; removing items with 0 or []
# input is in the form of {"itemA name": 1, "itemB name": 33, ...}
# output is in the same form
def clean_inventory(item_list):
    if len(item_list) > 0:
        return dict([item for item in list(item_list.items()) if 0 not in item or [] not in item or None not in item])
    else:
        return {}


# function to choose best item from entity's inventory based on need keywords
# keyword_dict is in the form of {'req': [keywords required], 'forb': [keywords forbidden], 'pref': [keywords preferred], 'prefnot': [keywords not preferred]}
# e.g. {'req': ['weapon'], 'forb': ['ranged'], 'pref': ['blade'], 'prefnot': ['blunt', 'light', 'shield']}
def choose_item(entity, keyword_dict):
    clean_inventory(entity)

    # make a list of all item dictionaries in pack
    all_items = [item[0] for item in list(entity.items())]
    if len(all_items) != 0 or all_items != [None]:

        # create a list of item (and natural weapon) dictionaries
        all_items_dict = [eval_prefix_name("item", item_name) for item_name in all_items if "natural weapon" not in weapon_table.get(item_name, "natural weapon")]
        all_items_dict += [eval_prefix_name("nat_weap", item_name) for item_name in all_items if "natural weapon" in weapon_table.get(item_name, "non-nat weapon")]

        # search pack for items with keywords that match all keywords in keyword_dict['req']
        potential_items = [item for item in all_items_dict if len(set(item['keywords']).intersection(set(keyword_dict.get('req', [])))) == len(keyword_dict.get('req'))]

        # search pack for items that match forbidden keywords
        forbidden_items = [item for item in all_items_dict if len(set(item['keywords']).intersection(set(keyword_dict.get('forb', [])))) >= 1]

        # subtract any forbidden items from suitable items
        qualifying_items = [item for item in potential_items if item not in forbidden_items]

        if len(qualifying_items) > 0:
            # prioritize most useful items amongst qualifying items based on preferred keywords
            if len(keyword_dict.get('pref', [])) > 0 or len(keyword_dict.get('prefnot', [])) > 0:
                n_matching_best = [len(set(item['keywords']).intersection(set(keyword_dict.get('pref', [])))) for item in qualifying_items]
                n_matching_worst = [len(set(item['keywords']).intersection(set(keyword_dict.get('prefnot', [])))) for item in qualifying_items]
                n_matching_diff = [a_i - b_i for a_i, b_i in zip(n_matching_best, n_matching_worst)]
                best_n_match = max(n_matching_diff)

                # pick item that best fulfills preferred and preferred-not keywords
                best_items = [i for indx, i in enumerate(qualifying_items) if n_matching_diff[indx] == best_n_match]

                # assign remaining list to qualifying items
                qualifying_items = best_items

            # choose randomly among considered items remaining
            chosen_item = random.choice(qualifying_items)
            gear_index = all_items.index(chosen_item['name']) # index of chosen item in character gear list

            # this is the dictionary entry of the chosen item
            chosen_item_dict = chosen_item

            # return item's dictionary
            return chosen_item_dict

        else:
            return {}
    else:
        return {}


# function to add items to a character's inventory
# Input: entity_slot is an entity's inventory slot (e.g. c_actor['inventory']['backpack'])
def deposit_item(entity, slot, items_to_deposit):
    # clean up inventory
    clean_inventory(items_to_deposit)

    # merge items with inventory
    entity['inventory'][slot] = { k: entity['inventory'][slot].get(k, 0) + items_to_deposit.get(k, 0) for k in set(entity['inventory'][slot]) | set(items_to_deposit) }

# a function to return a readable string representing a gear inventory:
# input is in the form of [["item name", number of items], ...];
# e.g. [["itemA", 4], ["itemB", 558]]
# output is in the form of a string, e.g. "4 itemAs and 558 itemBs"
def list_inv(gear):
    gear = list(gear.items())
    number_item =  ["%d %s" % (item[1], item[0]) if item[1] == 1 else "%d %ss" % (item[1], item[0]) for item in gear]
    if len(number_item) > 2:
        return ", ".join(number_item[:-1]) + ", and " + number_item[len(number_item)-1]
    elif len(number_item) == 2:
        return number_item[0]  + " and " + number_item[1]
    elif len(number_item) == 1:
        return number_item[0]
    else:
        return "nothing"

# function to withdraw items from inventory.
# If strict is True, items MUST be withdrawn as specified, or else nothing happens
# If strict is False, specified items will be withdrawn as much as possible
# returns a dict of items withdrawn in the style of 'inventory',
# e.g. {'gold piece' 9, 'apple', 1}
def withdraw_item(char, slot, items_to_withdraw, strict):
    # clean up inventory
    clean_inventory(items_to_withdraw)
    items_to_withdraw = list(items_to_withdraw.items())

    # check which items are in inventory
    withdrawn_item_names = [item[0] for item in items_to_withdraw]
    char_gear_names = [item[0] for item in list(char['inventory'][slot].items())]
    matching_items = [item for item in items_to_withdraw if item[0] in char_gear_names]

    # check if cancel withdraw if strict
    if strict:
        for item in matching_items:
            if list(char['inventory'][slot].items())[char_gear_names.index(item[0])][1] < item[1]:
                return []

    # withdraw matching items
    withdraw_list = []
    for item in matching_items:
        if list(char['inventory'][slot].items())[char_gear_names.index(item[0])][1] >= item[1]:
            withdraw_list.append(item)
            char['inventory'][slot][item[0]] -= item[1]
        else:
            withdraw_list.append([item[0], char['inventory'][char_gear_names.index(item[0])][1]])
            char['inventory'][slot][item[0]] = 0

    clean_inventory(char['inventory'][slot])

    return dict(withdraw_list)

# function to trade items between two inventories.
# If strict is true, the trade will not happen if terms are not met
# If strict is false, the trade will proceed as much as it can
def trade_item(char1, char2, items_char1_will_trade, items_char2_will_trade, strict):
    char1_items_withdrawn = withdraw_item(char1, items_char1_will_trade, strict)
    char2_items_withdrawn = withdraw_item(char2, items_char2_will_trade, strict)
    deposit_item(char1, items_char2_will_trade)
    deposit_item(char2, items_char1_will_trade)

# function to buy items from a merchant depending on need keywords
# 'merchant' needs to be a dictionary with a populated 'inventory' key
# 'discount' needs to be a fraction representing fraction of total cost
# e.g. discount = 0.1 means 10% off. Discount = 0 means no discount.
# Negative discounts means higher prices.
def shop_item(char, merchant, need_keyword, discount = 0):
    item_chosen = choose_item(merchant, need_keyword)
    if len(item_chosen) > 0:
        cost = int(math.ceil(item_chosen['cost'] * (1 - discount))) # round up to nearest integer
        money_to_spend = [['gold piece', cost]]
        trade_item(char, merchant, money_to_spend, [[item_chosen['name'], 1]], True)
        return item_chosen, money_to_spend


nat_weap_fist = {
    'name': 'fist',
    'keywords': ['weapon', 'melee', 'natural weapon', '1H', 'unarmed'],
    'cost': 0,
}

nat_weap_claw = {
    'name': 'claw',
    'keywords': ['weapon', 'melee', 'natural weapon', '1H'],
    'cost': 0,
}

nat_weap_bite = {
    'name': 'bite',
    'keywords': ['weapon', 'melee', 'natural weapon', '0H'],
    'cost': 0,
}

nat_weap_hoof = {
    'name': 'hoof',
    'keywords': ['weapon', 'melee', 'natural weapon', '1H'],
    'cost': 0,
}

nat_weap_horn = {
    'name': 'horn',
    'keywords': ['weapon', 'melee', 'natural weapon', '0H'],
    'cost': 0,
}

item_knife = {
    'name': 'knife',
    'keywords': ['weapon', 'light', 'concealable', 'blade', 'melee', '1H'],
    'cost': 1,
}

item_shield = {
    'name': 'shield',
    'keywords': ['weapon', 'shield', 'melee', 'light', '1H'],
    'cost': 5,
}

item_longsword = {
    'name': 'longsword',
    'keywords': ['weapon', 'adaptable', 'blade', 'melee', '1H'],
    'cost': 50,
}

item_spear = {
    'name': 'spear',
    'keywords': ['weapon', 'adaptable', 'thrusting', 'melee', 'reach', '1H'],
    'cost': 3,
}

item_rapier = {
    'name': 'rapier',
    'keywords': ['weapon', 'light', 'melee', 'thrusting', '1H'],
    'cost': 3,
}


item_greatsword = {
    'name': 'greatsword',
    'keywords': ['weapon', 'large', 'blade', 'melee', '2H'],
    'cost': 200,
}

item_large_healing_potion = {
    'name': 'large healing potion',
    'keywords': ['healing', 'immediate', 'consumable', 'large', 'tasty'],
    'cost': 20,
}

item_large_full_heal_potion = {
    'name': 'large full heal potion',
    'keywords': ['healing', 'immediate', 'consumable', 'large'],
    'cost': 20,
}

item_small_healing_potion = {
    'name': 'small healing potion',
    'keywords': ['healing', 'immediate', 'consumable'],
    'cost': 20,
}

item_first_aid_kit = {
    'name': 'first aid kit',
    'keywords': ['healing', 'consumable', 'slow'],
    'cost': 10,
}

item_apple = {
    'name': 'apple',
    'keywords': ['food', 'consumable', 'sweet', 'small'],
    'cost': 1,
}

item_orange = {
    'name': 'orange',
    'keywords': ['food', 'consumable', 'sweet', 'small'],
    'cost': 1,
}

item_chicken_pot_pie = {
    'name': 'chicken pot pie',
    'keywords': ['food', 'consumable', 'savory', 'large'],
    'cost': 8,
}

item_gold_piece = {
    'name': 'gold piece',
    'keywords': ['currency', 'small', 'gold', 'pretty'],
    'cost': 1,
}

item_dull_gem = {
    'name': 'dull gem',
    'keywords': ['valuable', 'small', 'stone', 'pretty'],
    'cost': 10,
}

item_sparkling_gem = {
    'name': 'sparkling gem',
    'keywords': ['valuable', 'small', 'stone', 'pretty'],
    'cost': 50,
}

item_fire_knife = {
    'name': 'fire knife',
    'keywords': ['weapon', 'blade', 'fire', 'light', 'melee', '1H'],
    'cost': 600,
}

item_mace = {
    'name': 'mace',
    'keywords': ['weapon', 'blunt', 'melee', '1H'],
    'cost': 19,
}

item_arrow = {
    'name': 'arrow',
    'keywords': ['ammo', 'piercing', 'bow'],
    'cost': 1,
}

item_longbow = {
    'name': 'longbow',
    'keywords': ['weapon', 'piercing', 'ranged', '2H'],
    'cost': 1,
}


# WEAPON table
# [shift left, shift right, min range(0 = melee, 1 = near, 2 = far, 3 = very far, etc.), max range, ...features...]
weapon_table = {
    'fist':             [ 2, -2,  0, 0],
    'knife':            [-1, -1,  0, 0],
    'throwing knife':   [-1, -1,  1, 1],
    'rapier':           [-2, -2,  0, 0],
    'estoc':            [-2, -2,  0, 0],
    'shortsword':       [ 0,  0,  0, 0],
    'longsword':        [ 1,  1,  0, 0],
    'greatsword':       [ 2,  2,  0, 0],
    'spear':            [-1,  1,  0, 1],
    'shield':           [ 1, -1,  0, 0],
    'longbow':          [ 0,  0,  1, 8],
    'shortbow':         [ 0,  0,  1, 4],
    'crossbow':         [ 0,  0,  1, 9],
    'claw':             [ 0,  0,  0, 0],
    'hoof':             [ 0,  0,  0, 0],
    'horn':             [ 0,  0,  0, 0],
    'bite':             [ 0,  0,  0, 0],
}

# append weapon keywords to weapon_table
for weapon in list(weapon_table.keys()):
    try:
        weapon_table[weapon] += eval("item_" + weapon.replace(" ", "_"))['keywords']
    except:
        pass
    try:
        weapon_table[weapon] += eval("nat_weap_" + weapon.replace(" ", "_"))['keywords']
    except:
        pass


# ARMOR table
armor_table = {
    'none':         [0, 'light'],
    'padded':       [1, 'light'],
    'chainmail':    [2, 'medium'],
    'platemail':    [3, 'heavy'],
}


# character1 = {
#     'name': 'Glinda',
#     'inventory': [['gold piece', 387], ['knife', 1], ['mace', 1], ['fire knife', 1], ['small healing potion', 1], ['large healing potion', 1], ['large full heal potion', 0], ['first aid kit', 1]],
#     'weakness': ['fire', 'blunt'],
#     'fighting style': 'powerful',
#     'INT': 8,
# }
#
# character2 = {
#     'name': 'Rufus',
#     'inventory': [['knife', 1], ['mace', 1]],
#     'weakness': ['fire', 'blade'],
#     'fighting style': 'finesse',
#     'INT': 6,
# }






''' EXAMPLES TO FOLLOW

# MUST, FORBID, PRIORITIZE
need_keyword = [['healing', 'consumable', 'large'], ['slow'], ['tasty']]

treasure = [['shield', 1], ['apple', 6], ['knife', 1], ['small healing potion', 2]]

print "\n Glinda's current gear:", character1['inventory']

print "\n Glinda found treasure!", treasure

deposit_item(character1, treasure)

print "\n Glinda's gear after adding treasure:", character1['inventory']

print "\n Glinda is trying to withdraw seven apples and a small healing potion from her inventory"

items_withdrawn = withdraw_item(character1, [['apple', 7], ['small healing potion', 1]], False)

print "\n Glinda withdrew these items:", items_withdrawn
print "\n Glinda's gear looks like this:", character1['inventory']


print "\n Glinda is trying to buy a large healing potion"

gold_withdrawn = withdraw_item(character1, [['gold pieces', item_large_healing_potion['cost']]], True)
if len(gold_withdrawn) > 0:
    deposit_item(character1, [['large healing potion', 1]])
    print "\n Glinda bought the large healing potion"
    print "\n Her gear afterward:", character1['inventory']

merchant = {
    'name': 'Huddins',
    'inventory': [['gold piece', 200], ['small healing potion', 11], ['longsword', 2], ['orange', 8], ['chicken pot pie', 1]],
}

print '\n Glinda is feeling hungry and would prefer something savory. She looks at a merchant\'s wares:', merchant['inventory']

need_keyword = [['food'], [], ['savory'], []]
print '\n Glinda has the following needs:', need_keyword

chosen_item = choose_item(merchant, need_keyword)

print '\n Glinda has picked this to buy:', chosen_item

trade_item(character1, merchant, [['gold piece', chosen_item['cost']]], [[chosen_item['name'], 1]], True)

print '\n The merchant now has:', merchant['inventory']
print '\n Glifta now has:', character1['inventory']

withdraw_item(character1, [['chicken pot pie', 1]], True)
print "\n Glifta ate the pot pie."

need_keyword = [['food'], [], ['sweet'], []]
print '\n Glifta is still hungry, now for something sweet:', need_keyword
item, cost = shop_item(character1, merchant, need_keyword)
print '\n Glifta bought a(n)', item['name'], 'which cost', cost[0][1], 'gold piece(s)'
print '\n Glifta now has:', character1['inventory']
print '\n Merchant now has:', merchant['inventory']


        # use up consumable item
        # if 'consumable' in chosen_item_dict['keywords']:
        #     char['inventory'][gear_index][1] -= 1
        #
        # # clean inventory again
        # clean_inventory(char)


# print "\n Keywords the item MUST have:", need_keyword[0]
# print "\n Keywords the item CANNOT have:", need_keyword[1]
# print "\n Keywords to prioritize items:", need_keyword[2]
#
#
# item_dict = choose_item(character1, need_keyword)
#
# print "\n an item was picked?", len(item_dict) > 0
# if len(item_dict)>0:
#     print "\n The item was:", item_dict['name']
# print "\n current gear:", character1['inventory']




    ## stuff that used to be in deposit_item()
    # if there is a match already in gear, add number
    # if len(gear_index) > 0:
    #     # add items if positive
    #     if number > 0:
    #         char['inventory'][gear_index[0]][1] += number
    #     # subtract items if valid value
    #     elif number < 0 and abs(number) <= char['inventory'][gear_index[0]][1]:
    #         char['inventory'][gear_index[0]][1] += number
    #     else:
    #         m0('Withdrawing too much!')
    #     # remove entry from inventory if reduced to 0 (cleanup)
    #     if char['inventory'][gear_index[0]][1] <= 0:
    #         char['inventory'].pop(gear_index[0])
    # else:
    #     # create inventory entry
    #     char['inventory'].append([item_to_deposit, number])
    #
    # return char['inventory']
'''

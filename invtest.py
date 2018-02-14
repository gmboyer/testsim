import random

# placing an item into an inventory
# taking an item out of an inventory
# taking account of special items ***

# prefix evaluator
def prefix_eval(prefix, string):
    return eval(prefix + "_" + string.replace(" ", "_"))

# simple script to merge (add) inventory dictionaries
# returns an inventory dictionary
def add_items(target_inv, inv_to_add):
    x = target_inv
    y = inv_to_add
    return { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }

# returns the total weight of an inventory (float)
def get_inventory_weight(target_inv):
    n_items = target_inv.values()
    item_weights = [prefix_eval("item", key).get("weight", 0) for key in target_inv.keys()]
    total_weight = sum([item*weight for item,weight in zip(n_items, item_weights)])
    return total_weight

# Withdraws specified inventory from target inventory
# Returns an inventory dictionary of withdrawn items.
# If demanding more items than in inventory,
# withdraw as many items as possible.
def withdraw_items(target_inv, inv_to_withdraw):

    inv_actually_withdrawn = {}

    for item in inv_to_withdraw.items():
        # check if item to withdraw exists in inventory
        if item[0] in target_inv.keys():
            # check if n items to withdraw is greater than n items in inventory
            if item[1] > target_inv.get(item[0]):
                inv_actually_withdrawn[item[0]] = target_inv.get(item[0])
                target_inv[item[0]] = 0
            else:
                inv_actually_withdrawn[item[0]] = item[1]
                target_inv[item[0]] -= item[1]
        else:
            pass

    return inv_actually_withdrawn

# function to remove inventory entries with n = 0
def clean_inventory(target_inv):
    for item in target_inv.items():
        if item[1] <= 0:
            del target_inv[item[0]]


# function to choose best item from inventory based on need keywords
# keyword_dict is in the form of {'req': [keywords required], 'forb': [keywords forbidden], 'pref': [keywords preferred], 'prefnot': [keywords not preferred]}
# e.g. {'req': ['weapon'], 'forb': ['ranged'], 'pref': ['blade'], 'prefnot': ['blunt', 'light', 'shield']}
# returns id of chosen item, or string "nothing" if nothing fulfilled needs.
def choose_item(target_inv, keyword_dict):

    req_keywords = keyword_dict.get("req", [])
    forb_keywords = keyword_dict.get("forb", [])
    pref_keywords = keyword_dict.get("pref", [])
    prefnot_keywords = keyword_dict.get("prefnot", [])

    # remove duplicate keywords
    req_keywords = list(set(req_keywords))
    forb_keywords = list(set(forb_keywords))
    pref_keywords = list(set(pref_keywords))
    prefnot_keywords = list(set(prefnot_keywords))

    # make a list of all item names in target_inv
    all_items = [item[0] for item in target_inv.items()]

    # if there are items in target's inventory...
    if len(all_items) > 0:

        # create a list of item dictionaries
        all_items_dict = [prefix_eval("item", item_name) for item_name in all_items]

        # search pack for items with keywords that match all keywords in keyword_dict['req']
        potential_items = [item for item in all_items_dict if len(set(item['keywords']).intersection(set(req_keywords))) == len(keyword_dict.get('req'))]

        # search pack for items that match forbidden keywords
        forbidden_items = [item for item in all_items_dict if len(set(item['keywords']).intersection(set(forb_keywords))) >= 1]

        # subtract any forbidden items from suitable items
        qualifying_items = [item for item in potential_items if item not in forbidden_items]

        if len(qualifying_items) > 0:
            # prioritize most useful items amongst qualifying items based on preferred keywords
            if len(keyword_dict.get('pref', [])) > 0 or len(keyword_dict.get('prefnot', [])) > 0:
                n_matching_best = [len(set(item['keywords']).intersection(set(pref_keywords))) for item in qualifying_items]
                n_matching_worst = [len(set(item['keywords']).intersection(set(prefnot_keywords))) for item in qualifying_items]
                n_matching_diff = [a_i - b_i for a_i, b_i in zip(n_matching_best, n_matching_worst)]
                best_n_match = max(n_matching_diff)

                # pick item that best fulfills preferred and preferred-not keywords
                best_items = [i for indx, i in enumerate(qualifying_items) if n_matching_diff[indx] == best_n_match]

                # assign remaining list to qualifying items
                qualifying_items = best_items

            # choose randomly among considered items remaining
            chosen_item = random.choice(qualifying_items)

            # return item's id
            return chosen_item["id"]

        else:
            return "nothing"
    else:
        return "nothing"


# choose best weapon based on keywords
# see choose_item for keyword_dict format
# returns name and location of best weapon
def choose_weapon(target, keyword_dict):
    # check for available weapons on person
    # primary hand, offhand, natural weaponry, inventory

    return chosen_weapon, weapon_location



# tests below

def script_drink():
    print "You drink and feel okay."

item_gold_piece = {"id": "gold piece", "keywords": ["shiny", "valuable"], "weight": 0.1}
item_chalice = {"id": "chalice", "keywords": ["bejeweled", "valuable", "cup"], "use": script_drink, "weight": 1}
item_sword = {"id": "sword", "keywords": ["melee", "weapon", "1H", "blade"], "weight": 10}
item_knife = {"id": "knife", "keywords": ["melee", "weapon", "1H", "blade", "light"], "weight": 1}
item_mace = {"id": "mace", "keywords": ["melee", "weapon", "1H", "blunt"], "weight": 12}
item_armor = {"id": "armor", "keywords": ["armor"], "weight": 20}

treasure = {"gold piece" : 200, "chalice" : 1}

char_PC = {
           "inventory": {"gold piece": 16, "sword": 1, "mace": 1},
           }

# add treasure to char_PC inventory
char_PC["inventory"] = add_items(char_PC["inventory"], treasure)

print char_PC["inventory"]

# print weight of inventory
print get_inventory_weight(char_PC["inventory"])

# repeat - add more treasure to inventory and check weight
char_PC["inventory"] = add_items(char_PC["inventory"], treasure)
print char_PC["inventory"]
print get_inventory_weight(char_PC["inventory"])

# withdraw 50 coins
left_behind = withdraw_items(char_PC["inventory"], {"gold piece":50})
print left_behind
print char_PC["inventory"]

# attempt to withdraw 5000 coins
left_behind = withdraw_items(char_PC["inventory"], {"gold piece":5000})
print left_behind
print char_PC["inventory"]

# clean 0-values from inventory
clean_inventory(char_PC["inventory"])
print char_PC["inventory"]

# have the character choose an item from their inventory based on keywords
keyword_dict = {'req': ['weapon']}
print choose_item(char_PC["inventory"], keyword_dict)

# ... get pickier with item selection
keyword_dict = {'req': ['weapon'], 'forb': ['ranged'], 'pref': ['blade'], 'prefnot': ['light', 'blunt']}
print choose_item(char_PC["inventory"], keyword_dict)

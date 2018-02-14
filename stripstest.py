# # Problem:
# # Initial state: status(hurt), near(enemy), at(dungeon library)
# # Goal state: status(healthy)
#
# # Actions:
#     # attack
#         # preconditions: near([enemy]), holding([weapon])
#         # postconditions: status(battling)
#     # use healing magic
#         # preconditions: sufficient magic points
#         # postconditions: status(healthy)
#     # retrieve [healing potion]
#         # preconditions: have([healing potion]), holding(nothing)
#         # postconditions: holding([healing potion])
#     # use [sword]
#         # precondition: holding([sword]), near([enemy]), status(battling)
#         # postconditions: enemy.status(dead)
#     # use [healing potion]
#         # precondition: holding([healing potion])
#         # postconditions: status(healthy)
#     # skill [medicine]
#         # precondition: status(not battling), have([medical supplies])
#         # postcondition: status(healthy)
#     # move [hospital]
#         # precondition: status(not restrained), near([hospital])
#         # postcondition: at([hospital]), near([doctor])
#     # communicate [doctor]
#         # precondition: near([doctor])
#         # postcondition: status(healthy)
#     # take [healing potion]
#         # precondition: near([healing potion]), holding(nothing)
#         # postcondition: holding([healing potion])
#
# import random
#
# # function to move "who" to "where" (both arguments input as strings)
# def move(who, where):
#     who["at"] = where
#     who["near"] = eval(where).get("near")
#
# def attack(who):
#     if who["status"] == "healthy":
#         who["status"] = "unhealthy"
#     else:
#         who["status"] = "dead"
#
# def take(who, what):
#     who["holding"] = what
#     who["nearby"] = who["nearby"] - [what]
#
# def heal(who):
#     if who["status"] == "unhealthy":
#         who["status"] = "healthy"
#
# def pick_direction(who):
#     nearby_places = [place for place in who["nearby"] if eval(place).get("what") == "place"]
#     return random.choice(nearby_places)
#
#
# def take_action(action, who = None, what = None, where = None):
#     conditions_met = True
#     for precondition in eval("conditions_" + action).get("precondition"):
#         if not eval(precondition): # if any precondition is not met...
#             conditions_met = False
#             break
#     if conditions_met:
#         eval(action + "(who = " + who + "what = " + what + "where = " + where + ")")
#
# move_conditions = {"preconditions": ["'restrained' not in who.get(status)],
#                     "postconditions": ["who['at'] = where", "who['nearby'] = eval(where).get('nearby', None)"],
#                     }
#
# # def use(who, item, target = None):
# # class Item:
# #     def __init__(self, item_dict):
# #         self.preconditions = item_dict.get("preconditions")
# #         self.postconditions = item_dict.get("postconditions")
# #
# #     def use(self, user, target):
# # assign with adventurer_sword = Item(sword)
# # do stuff
#
# # items have sets of preconditions and postconditions for their use
# sword = {"what": "item",
#          "preconditions": xxx,
#          "postconditions": xxx,
#          }
#
# hospital = {"what": "place",
#             "at": "town",
#             "near": ["doctor", "town"],
#             }
#
# doctor = {"what": "creature",
#           "race": "human",
#           "name": "Horace",
#           "at": "hospital",
#           "near": ["town"]
#           "actions": ["move", "retrieve", "use", "communicate", "skill"],
#           "holding": ["medical supplies"],
#           "skill": ["medicine"],
#           }
#
# adventurer = {"what": "creature",
#               "race": "human",
#               "name": "Linda"
#               "at": "dungeon library",
#               "near": ["healing potion", "goblin"]
#               "actions": ["move", "retrieve", "use", "communicate", "skill"],
#               "holding": "sword",
#               "skill": "combat",
#               "enemy":
#               }

# pre and post-conditions designated above by state(subject)
# AI strategy:
# 1) search for post-conditions that match goal state.
# 2) Backtrack to current state using available actions. Monte-carlo?
# 3) Choose shortest, safest route.

# If a solution can't be found, put goal on hold and pursue next goal.


# goal: get to RoomC

import random
import copy

nobody = {"dict_name": "nobody", "at": "nowhere", "near": ["nothing", "actor_adventurer"]}
nothing = {"dict_name": "nothing", "at": "nowhere", "near": ["nothing", "actor_adventurer"]}
nowhere = {"dict_name": "nowhere", "near": ["nothing", "actor_adventurer"]}

def pick_where(who):
    nearby_places = [place for place in who["near"] if eval(place).get("what") == "place"]
    if len(nearby_places) > 0:
        return random.choice(nearby_places)
    else:
        return "nowhere"

def pick_who(who):
    nearby_actors = [actor for actor in who["near"] if eval(actor).get("what") == "actor"]
    if len(nearby_actors) > 0:
        return random.choice(nearby_actors)
    else:
        return "nobody"

def pick_what(who):
    nearby_things = [thing for thing in who["near"] if eval(thing).get("what") == "thing"]
    if len(nearby_things) > 0:
        return random.choice(nearby_things)
    else:
        return "nothing"


def move(actor = nobody, who = nobody, what = nothing, where = nowhere):
    eval(actor["at"])["near"].remove(actor["dict_name"]) # remove the actor from the 'near' list of the old place
    update_near(actor["at"]) # remove actor from the 'near' list of all things in the old place
    actor["at"] = str(where.get("dict_name")) # move the actor to the new place
    where["near"] += [actor.get("dict_name")] # update the new place's 'near' list with the actor
    update_near(where["dict_name"]) # add actor to the 'near' list of all things in the new place


# function to update the 'near' lists of all things in a place.
# e.g. when an actor moves, when an item is taken, etc.
def update_near(where):
    where = eval(where)
    for thing in where["near"]:
        if eval(thing).get("what") != "place":
            eval(thing)["near"] = where["near"]

def take(actor = None, who = None, what = None, where = None):
    actor["holding"] = what
    actor["nearby"] = actor["nearby"].remove(what) # remove the item from the actor's surroundings
    eval(actor["at"]).get("nearby").remove(what) # remove the item from the place's surroundings


def unlock(actor = None, who = None, what = None, where = None):
    actor["holding"] = "nothing" # consume held key


def try_action(action, actor = "nobody", who = "nobody", what = "nothing", where = "nowhere"):
    conditions_met = True
    for precondition in eval("conditions_" + action).get("preconditions"):
        if not eval(precondition): # if any precondition is not met...
            conditions_met = False
            break
    if conditions_met:
        what_to_do = str(action + "(actor =" + actor + ", who = " + who + ", what = " + what + ", where = " + where + ")")
        eval(what_to_do)
        return what_to_do


conditions_move = {"preconditions": ["'restrained' not in eval(actor).get('status')"]}
conditions_take = {"preconditions": ["'nothing' in eval(actor).get('holding')"]}
conditions_open_lock = {"preconditions": ["'key' in eval(actor).get('holding')"]}



place_RoomA = {"dict_name": "place_RoomA", "what": "place", "near": ["place_RoomB", "actor_adventurer"]}
place_RoomB = {"dict_name": "place_RoomB", "what": "place", "near": ["place_RoomA", "place_RoomC", "place_RoomI"]}
place_RoomC = {"dict_name": "place_RoomC", "what": "place", "near": ["place_RoomB", "place_RoomD", "place_RoomK"]}
place_RoomD = {"dict_name": "place_RoomD", "what": "place", "near": ["place_RoomC", "place_RoomL"]}
place_RoomI = {"dict_name": "place_RoomI", "what": "place", "near": ["place_RoomB", "place_RoomJ"]}
place_RoomJ = {"dict_name": "place_RoomJ", "what": "place", "near": ["place_RoomI", "thing_key"]}
place_RoomK = {"dict_name": "place_RoomK", "what": "place", "near": ["place_RoomC", "place_RoomL"]}
place_RoomL = {"dict_name": "place_RoomL", "what": "place", "near": ["place_RoomD", "place_RoomK"]}

    #   Maze layout:
    #
    #
    #
    #   J       D---L (end)
    #   |       |   |
    #   I---B---C---K
    #       |
    #       A (start)
    #
    # most direct solutions: [place_RoomB, place_RoomC, place_RoomD, place_RoomL]
    #                        [place_RoomB, place_RoomC, place_RoomK, place_RoomL]



actor_adventurer = {"dict_name": "actor_adventurer",
                    "what": "actor",
                    "at": "place_RoomA",
                    "near": ["place_RoomB"],
                    "status": ["healthy"],
                    }

thing_key = {"dict_name": "key",
             "what": "thing"}

achieved_success = False
best_move_record = []

for i in range(1, 2):
    # create a random plan
    # move(who = actor_adventurer, where = place_RoomA) # return to start
    this_move_record = []
    for ii in range(1, 20):
        actor_nearby = pick_who(actor_adventurer)
        thing_nearby = pick_what(actor_adventurer)
        place_nearby = pick_where(actor_adventurer)
        random_action = random.choice(["move"])
        what_was_done = try_action(action = random_action, actor = "actor_adventurer", who = actor_nearby, what = thing_nearby, where = place_nearby)
        this_move_record.append(what_was_done)
        if "place_RoomL" in actor_adventurer.get("at"):
            achieved_success = True
            break

    # update best (shortest) successful plan
    if len(best_move_record) == 0 and achieved_success:
        best_move_record = this_move_record
    if achieved_success and len(this_move_record) < len(best_move_record):
        best_move_record = this_move_record

print "achieved success?", achieved_success
print "best n moves:", len(best_move_record)
print "what was done:", best_move_record

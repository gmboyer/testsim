import random
from random_lists import *
import re
from difflib import SequenceMatcher

#check similarity between words, return a similarity ratio
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# defining a function for rolling a dN, where N is the # of sides
# _ne stands for non-exploding
def rolldN_ne(N):
    return random.randint(1, N)

# WR stands for Weighted roll.
# This function takes a list containing traits, each with a
# chance of "sticking" if a d100% rolls below the weighted value.

# WRfull accepts a list in the form of [["s1", n1], ["s2", n2],...]
# where "s1" and "s2" are strings and n1 and n2 are numbers.
# It then randomly picks an entry and rolls a d100. If the result
# is less or equal to the entry's number, then the entry "sticks".
# If not, then the function tries again with another random entry.
# The function returns a list: ["s", n, d100 result]

def WRfull(myList):
    while True:
        myPick = random.choice(myList)
        myRoll = rolldN_ne(100)
        if myRoll <= myPick[1]:
            break
        else:
            pass
    return [myPick[0], myPick[1], myRoll]

# funtion to check if a string is evaluatable as a variable;
# used in getSublists() to check for typos in bracketed strings
def can_eval(myString):
    try:
        eval(myString)
        return True
    except:
        return False

myPattern = r"(?<=\[).+?(?=\])" #regex to recognizes contents of brackets []
myPattern = r"\[(.*?)\]" #simpler regex that should also work
# myChoicePattern = r"\[(.*?|.*?)\]"
myPatternNoChoice = r"\[([^|[]]*.*)\]"

# this returns a string where bracketed lists are looked up with WRshort
def getSublists(myString):
    split_string = myString.split()
    sublists = re.findall(myPattern, myString)
    result_list = [""]

    for i in range(len(sublists)):
        if can_eval(sublists[i]) == True:
            chosen = 0
            while chosen == 0:
                similar_count = 0
                result = WRfull(eval(sublists[i]))[0]
                for ii in range(len(result_list)):
                    if similar(result, result_list[ii]) > 0.8:
                        similar_count = similar_count + 1
                if similar_count == 0:
                    result_list.append(result)
                    chosen = 1


            split_string[split_string.index("[" + sublists[i] + "]")] = result
        else:
            split_string[split_string.index("[" + sublists[i] + "]")] = "NULL!"
    return " ".join(split_string)

# WR is a function to take a string and automatically roll on sublists
# contained within brackets, filling them in "mad libs"-style
def WR(myString):
    # try:
    result = getSublists(myString)

    while len(re.findall(myPattern, result)) > 0:
            result = getSublists(result)
    return result

    # except:
        # return "Something went wrong!"

# print WR("[ad_loc_desc]")
# print WR("You must venture to the [ad_loc_desc] to retrieve the treasure")

''' Example below
# An example list showing traits and their
# percent chance of "sticking" if picked

trait = [
    ["Blue-eyed",       30],
    ["Yellow-toothed",  70],
    ["Red-mouthed",     10],
    ["Evil-tongued",    80],
    ["Small-brained",   40],
    ["Loud-mouthed",    30],
    ["Frog-lipped",     15],
    ["Thick-skinned",   60],
    ["Four-eyed",       50],
    ["friends with a [summon] that is [trait]", 100],
    ["owned by a [affinity] affinity summoner who wants to " \
        "capture a [summon] that is [trait]", 100],
    ]

summon = [
    ["Cow",             30],
    ["Harpy",           70],
    ["Vampire",         10],
    ["Wolf",            80],
    ["Skeleton",        40],
    ["Necrophidius",    30],
    ["Gelatinous Cube", 15],
    ["Carrion Crawler", 60],
    ["Beholder",        10],
    ]

affinity = [
    ["Undead",          35],
    ["Construct",       15],
    ["Animal",          70],
    ["Plant",           50],
    ["Dragon",          10],
    ]

print WR("This [summon] is [trait]")
'''


"""
Issues: if the string has characters that touch brackets, this will cause
an error when run through WR(). Needs a regex fix.
"""

from random_lists import *
from description_scripts import *

# current SpAbil supported: armor training, berserk, combat dicipline, sneak attack
char_character_1 = {
    'id': 'character 1',
    'name': 'Rufus',
    'sex': 'male',
    'race': 'human',
    'class': 'character',
    'goal': ['survival', 'fame'],
    'ideal': ['greed'],
    'preferred surroundings': ['natural'],
    'SpAbil': [''],
    'primary weapon': 'fist', # fist for no weapon
    'offhand weapon': 'fist',
    'dual-wielding': False,
    'inventory': [['arrow', 3], ['longsword', 1], ['shield', 1]],
    'armor': 'none',
    'fighting style': 'none',
    'armor bonus': 0, # extra armor bonus not imparted by armor
    'pace': 1,
    'weakness': [],
    }

char_character_2 = {
    'id': 'character 2',
    'name': 'Glinda',
    'sex': 'female',
    'race': 'human',
    'goal': ['survival', 'wealth'],
    'ideal': ['benevolence'],
    'preferred surroundings': ['pretty', 'open', 'natural', 'grassy'],
    'SpAbil': [''],
    'primary weapon': 'fist',
    'offhand weapon': 'fist', # fist for no weapon
    'dual-wielding': False,
    'inventory': [['arrow', 3], ['greatsword', 1], ['shield', 1]],
    'armor': 'none',
    'fighting style': 'none',
    'armor bonus': 0, # extra armor bonus not imparted by armor
    'pace': 1,
    'weakness': [],
    }


# A generic set of statistics
char_creature = {
    'id': 'creature',
    'name': 'Generic',
    'sex': 'female',
    'race': 'generic',
    'goal': ['survival'],
    'ideal': ['greed'],
    'concept': ['generic creature'],
    'preferred surroundings': [],
    'stats':{'STR': 6,
             'DEX': 6,
             'CON': 6,
             'INT': 6,
             'WIS': 6,
             'CHA': 6,
             'LCK': 0},
    'SpAbil': [],
    'skill': [''],
    'primary hand': {'fist': 1},
    'offhand': {'fist':1}, # fist for no weapon
    'dual-wielding': False,
    'inventory': {'primary hand': {'claw': 1}, 'offhand': {'claw': 1}, 'backpack':{'knife':1, 'greatsword':1}},
    'armor': 'none',
    'fighting style': 'none',
    'armor bonus': 0, # extra armor bonus not imparted by armor
    'pace': 1,
    'weakness': [],
    'initialized': False,
    'in combat': False,
    'battles won': 0,
    'winner names': [],
    'theme': [],
    'idle': ['standing'], # "there is a creature #### here"
    'reaction': ['fight'],
    'natural weapons only': False, # is able to wield artificial weapons
    'natural weapons': [['fist', 2]],
}


['Kekkson', 'Wamir', 'Veltalia', 'Griffet', 'Xolias']
['Rod', 'Steve', 'Rufus', 'Rupert', 'Jamie']
['Mary', 'Linda', 'Glinda', 'Alyssa', 'Risa']


char_goblin = {
    'id': 'goblin',
    'race': 'goblin',
    'ideal': ['greed'],
    'stats':{'STR': 12,
             'DEX': 12,
             'CON': 12,
             'INT': 12,
             'WIS': 12,
             'CHA': 12,
             'LCK': 12},
    'SpAbil': ['sneak attack'],
    'inventory': {'primary hand': {'claw': 1}, 'offhand': {'claw': 1}, 'backpack':{'knife':1, 'greatsword':1}},
    'goblin': ['fight', 'fight', 'chat'],
    'names': ['Glak', 'Glof', 'Mipp', 'Baff', 'Lugga', 'Bugga', 'Bop'],
    'natural weapons': [['claw', 2]],
}

char_skeleton = {
    'id': 'skeleton',
    'race': 'skeleton',
    'ideal': ['bloodlust'],
    'SpAbil': [''],
    # 'inventory': [['spear', 1]],
    'reaction': ['fight', 'rattle its bones', 'make spooky noises'],
}

char_orc = {
    'id': 'orc',
    'race': 'orc',
    'ideal': ['greed', 'bloodlust'],
    'SpAbil': ['berserk'],
    # 'inventory': [['knife', 1]],
    'armor': 'chainmail',
    'reaction': ['fight'],
    'names': ['Grogun', 'Horgut', 'Cracktooth', 'Skullcracker', 'Bashfist', 'Slugglugger', 'Breakneck'],
}

char_skeleton_knight = {
    'id': 'skeleton knight',
    'race': 'skeleton',
    'ideal': ['bloodlust'],
    'SpAbil': [''],
    # 'inventory': [['longsword', 1]],
    'offhand weapon': 'shield',
    'armor': 'platemail',
    'reaction': ['fight', 'brood in lonely melancholy'],
    'names': ['the Shadow Knight', 'the Dark Vigil', 'the Knight of Darkness'],
}

char_unicorn = {
    'id': 'unicorn',
    'race': 'unicorn',
    'ideal': ['peace'],
    'SpAbil': [''],
    # 'inventory': [],
    'reaction': ['fight', 'prance', 'gallop majestically', 'watch knowingly'],
    'natural weapons only': True,
    'natural weapons': [['horn', 1], ['hoof', 4], ['bite', 1]],
}

char_wood_elf = {
    'id': 'wood elf',
    'race': 'wood elf',
    'ideal': ['peace'],
    # 'inventory': [['longbow', 1], ['knife', 1]],
    'reaction': ['fight', 'sing sweet melodies', 'hug trees'],
    'male names': ['Elfy', 'Melfy', 'Gelfy', 'Belfy'],
    'female names': ['Elfa', 'Melfa', 'Gelfa', 'Belfa'],
}

char_wispy_the_coffer_corpse = {
    'id': 'wispy the coffer corpse',
    'name': "Wispy",
    'race': 'coffer corpse',
    'STR': 10,
    'primary weapon': 'claw',
    'offhand weapon': 'claw', # fist for no weapon
    'natural weapons': [['claw', 2], ['bite', 1]],
}

char_fire_lizard = {
    'id': 'fire lizard',
    'race': 'reptile',
    'theme': ['fire'],
    'idle': ['lurking', 'waiting'],
    'reaction': ['fight', 'lick its own eye with a slick lizard tongue', 'lay on a rock in the sun'],
    'natural weapons only': True,
    'natural weapons': [['bite', 1]],
}

# example of using WR inside of a dictionary reference
plant_idle = [
    ['blooming', 100],
    ['growing', 100],
    ['photosynthesizing', 20],
]

# cactus man reference for flavor AND stats
char_cactus_folk = {
    'id': 'cactus folk',
    'race': 'cactus folk',
    'ideal': ['peace', 'benevolence', 'bloodlust'],
    'idle': ['lurking', 'dancing', 'wiggling', 'waiting', WR("[plant_idle]")],
    'female names': ["Cactus-Jill", "Cactus-Jessica", "Cactus-Jillian", "Cactus-Jimima"],
    'male names': ["Cactus-John", "Cactus-James", "Cactus-Jud", "Cactus-Jeremy"],
    'reaction': ['fight', 'pretending poorly to be a normal cactus', 'continue to be all prickly'],
}

char_bunny = {
    'id': 'bunny',
    'race': 'bunny',
    'reaction': ['nibble clover', 'hop around', 'stare blankly'],
    'natural weapons only': True,
}
char_wild_horse = {
    'id': 'wild horse',
    'race': 'horse',
    'reaction': ['prance', 'gallop majestically'],
    'natural weapons only': True,
    'natural weapons': [['hoof', 4], ['bite', 1]],
}

scene_generic = {
    #entities: [what it is, how many, countdown]
    'entities': [['flowers', 'carpet of', 2], ['grass', 'field of', 3], ['bunnies', 'several', 1]],
    'place': 'field',
    'theme': 'normal',
    'inventory': {'on ground':{'rapier':1,'spear':1,'greatsword':1}}
}



object_list = {
    'evergreen': ['natural', 'tree', 'wood', 'alive', 'pretty', 'large'],
    'sunflower': ['natural', 'flower', 'wood', 'alive', 'pretty', 'medium-sized'],
    'dead tree': ['natural', 'tree', 'wood', 'dead', 'ugly'],
    'boulder': ['natural', 'rock', 'stone', 'nonliving', 'large', 'heavy'],
    'cabinet': ['artificial', 'large', 'heavy', 'furniture', 'container', 'wood', 'nonliving'],
    'table': ['artificial', 'large', 'heavy', 'furniture', 'wood', 'nonliving', 'flat'],
    'wooden door': ['artificial', 'large', 'heavy', 'door', 'wood', 'nonliving', 'flat'],
    'metal door': ['artificial', 'large', 'heavy', 'door', 'metal', 'nonliving', 'flat'],
    'holy altar': ['artificial', 'good', 'holy', 'nonliving', 'furniture', 'stone', 'decorated'],
    'unholy altar': ['artificial', 'evil', 'unholy', 'nonliving', 'furniture', 'stone', 'decorated'],
}

mood_list = {
    'neutral': ['natural', 'artificial', 'tree', 'wood', 'alive', 'large', 'medium-sized', 'nonliving'],
    'positive': ['natural', 'flower', 'tree', 'alive', 'pretty'],
    'negative': ['dead', 'ugly', 'evil', 'haunted', 'demonic','dirty'],
    'spooky': ['dead', 'evil', 'haunted', 'demonic', 'unholy', 'dark'],
}

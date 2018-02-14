adventure_location = [
    ["cathedral",   10],
    ["cave",        50],
    ["house",       25],
    ["library",     30],
    ["mine",        40],
    ["tower",       40],
    ["castle",      40],
    ]

adjective_evil = [
    ["bloody",      25],
    ["nasty",       10],
    ["unholy",      30],
    ["desecrated",  50],
    ["infernal",    50],
    ["beastly",     40],
]

adjective_haunted = [
    ["spectral",      25],
    ["hollow",       10],
    ["unholy",      30],
    ["desecrated",  50],
    ["eerie",    50],
    ["rattling",     40],
    ["dark",     50],
    ["unsettling",     50],
]

subject_demonic = [
    ["demon",       25],
    ["devil",       10],
    ["fiend",       30],
    ["succubus",    40],
    ["spirit",      50],
    ["beast",       50],
]

creature_organization = [
    ["legion",          50],
    ["horde",           50],
    ["troupe",          50],
    ["tribe",           50],
    ["clan",            50],
    ["kingdom",         50],
    ["cabal",           50],
    ["club",            50],
]

creature_title = [
    ["soldier",         50],
    ["captain",         50],
    ["wizard",          50],
    ["lord",            50],
]

subject_haunted = [
    ["[creature_haunted]",                              100],
    ["[creature_haunted] [creature_organization]",      100],
    ["[creature_haunted] [creature_title]",             100],
]

creature_haunted = [
    ["undead",          100],
    ["lich",            100],
    ["ghost",           100],
    ["wraith",          100],
    ["necromancer",     100],
    ["skeleton",        100],
]

rand_enc_table_forest = [
    ["nothing",         100],
    ["wood elf",         60],
    ["goblin",           50],
    ["orc",              10],
    ["unicorn",           5]
]

rand_enc_table_haunted = [
    ["nothing",         100],
    ["skeleton",         50],
    ["skeleton knight",  10],
]

rand_enc_table_normal = [
    ["nothing",         100],
    ["wild horse",       50],
    ["bunny",            50],
]

rand_enc_table_desert = [
    ["nothing",         100],
    ["fire lizard",      50],
    ["cactus folk",       20],
]

desc_haunted = [
    ["[adjective_evil] [adventure_location] of the [adjective_evil] [subject_demonic]",   50],
    ["[adjective_haunted] [adventure_location] of the [adjective_haunted] [subject_haunted]",   50],
]

desc_forest = [
    ["a forest", 100],
]

desc_desert = [
    ["craggy plains of cracked mud", 100],
    ["dry outcrop", 100],
]

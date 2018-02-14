detail = 0 # how much detail should be reported? (0 = most, 3 = least)
# it = 1 # how many iterations?

# function to hit enter to advance turns
def hit_enter():
    typed = input("\nHit Enter\n")
    while typed != "":
        if typed == "help":
            print("")
            print("i for inventory")
            print("d0 for maximum combat detail")
            print("d1 for minimal combat detail")
            print("d2 for no combat detail")
            typed = input("\nHit Enter\n")
        if typed == "i":
            print("INVENTORY:", list_inv(c1.char['inventory']))
            typed = input("\nHit Enter\n")
        if typed == "d0":
            print("(not yet implemented)")
            print("Maximum combat detail enabled.")
            typed = input("\nHit Enter\n")
        if typed == "d1":
            print("(not yet implemented)")
            print("Minimal combat detail enabled.")
            typed = input("\nHit Enter\n")
        if typed == "d2":
            print("(not yet implemented)")
            print("Combat detail disabled.")
            typed = input("\nHit Enter\n")

partial_success_thresh = 4
full_success_thresh = 8

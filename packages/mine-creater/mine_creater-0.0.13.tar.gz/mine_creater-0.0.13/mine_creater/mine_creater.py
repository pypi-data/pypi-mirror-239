import os
import time



Player = None
Version = None
CanBoot = None

def nnd():
    print("What is your render distance?")
    try:
        var = int(input(">> "))  # Convert input to an integer
        if var <= 0:
            print("Render distance is too low. Render distance must be at least 1")
            time.sleep(5)
            nnd()
        elif var > 49:
            print("Render distance is too high. The maximum is 49")
        else:
            if CanBoot == False:
                print("Version too old idiot!")
            else:
                print("Welcome to Minecraft!")
    
            
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        nnd()

def make(game):
    global Player, Version, CanBoot  # Declare global variables to modify them
    if game.lower() == "minecraft":
        if not Player or Player.strip() == "":
            print("Invalid Name.")
        else:
            print("Hello " + Player + "!")
            if Version is None:
                print("Version is not set. Please set the version to 'newest' or 'oldest'.")
            elif Version.lower() == "newest":
                print("Version set to 'Newest Version'")
                CanBoot = True
                nnd()
            elif Version.lower() == "oldest":
                print("Version set to 'Oldest Version'")
                CanBoot = False
                nnd()
            else:
                print("Invalid Version")
    else:
        print("That's a lame game!")






















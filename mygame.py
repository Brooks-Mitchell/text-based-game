# text game version 0.8

from sys import exit
from textwrap import dedent
import random

# TODO 1.) Add ASCII art
# TODO 2.) Put ASCII art and text in separate file
# TODO 3.) Revamp combat and inventory system with player and equipment stats, Health points for player and enemies

inventory = ["copper_sword"]
goblin_alive = 'alive'
dragon_alive = 'alive'
demon_lord = 'alive'



# this is a base class that will define common things that all scenes do.
class Scene(object):
    def enter(self):
        exit(1)

class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

        current_scene.enter()



class Death(Scene):

    def enter(self):
        exit(1)


class TownSquare(Scene):
    def enter(self):
        print(dedent("""
            You are an adventurer out to kill the Demon Lord!
            But before you can do so you must accept quests from the
            adventurer's guild and upgrade your equipment!

            You are in the town square.

            To the west is the armorer.

            To the south is the guild.

            To the east is the wilderness.

            Where would you like to go?
            """))
        # print(inventory)  test
        action = input("> ")


        if action == "west" or action == "armorer":
            print(dedent("""
                You go to the armorer.
            """))
            return 'the_armory'

        elif action == "south" or action == "guild":
                print(dedent("""
                    You go to the guild.
                """))
                return 'the_guild'

        elif action == "east" or action == "wilderness":
            print(dedent("""
                You go to the wilderness.
            """))
            return 'the_wilderness'

        else:
            print("That doesn't work")
            return 'town_square'

class TheArmory(Scene):

    def enter(self):
        print(dedent("""
            You walk into the armorer's shop.
            He's a stout dwarf hammering on something.
            """))

        if "copper_sword" in inventory and goblin_alive == 'alive':
            print("Sorry, I've got nothing for you. Go kill the goblins!")
            return "town_square"

        elif "copper_sword" in inventory and goblin_alive == 'dead':
            print("Good job killing the goblins. Here, take this iron sword")
            inventory[0] = 'iron_sword'
            return "town_square"

        elif 'iron_sword' in inventory and dragon_alive == 'alive':
            print("I'll have something better for you after you've slayed the dragon")
            return "town_square"

        elif 'iron_sword' in inventory and dragon_alive == 'dead':
            print("Good, have this diamond sword")
            inventory[0] = 'diamond_sword'
            return "town_square"


class TheGuild(Scene):

    def enter(self):
        print(dedent("""
            You enter the adventurer's guild and speak with the (person)
            """))

        if "copper_sword" in inventory and goblin_alive == 'alive':
            print("Sorry, I've got nothing for you. Go kill the goblins!")
            return "town_square"

        elif "copper_sword" in inventory and goblin_alive == "dead":
            print("Go to the armory to get new gear!")
            return "town_square"

        elif "iron_sword" in inventory and goblin_alive == 'dead':
            print("Good job killing the goblins. Go kill dragon")
            inventory[0] = 'iron_sword'
            return "town_square"

        elif "iron_sword" in inventory and dragon_alive == 'alive':
            print("I'll have something else for you after you've slayed the dragon")
            return "town_square"

        elif "iron_sword" in inventory and dragon_alive == 'dead':
            print("Go kill the Demon Lord, silly.")
            inventory[0] = 'diamond_sword'
            return "town_square"



class TheWilderness(Scene):

    def enter(self):
        print(dedent("""
            You head east out of town for a few miles.
            The houses and farms become more scarce, until
            you're standing at an intersection.

            To the north you see small tracks.

            To the south you see fog.

            To the east you see smoke.

            Which way do you go?
            """))


        direction = input("> ")

        if direction == "north":
            print("You follow the tracks.")
            return 'goblin1'

        elif direction == "south":
            print("You forge ahead into the dark and unrelenting fog.")
            return 'demon_lord'

        elif direction == "east":
            print("You set forth towards the smell of burning flesh.")
            return 'dragon1'
        else:
            print("It doesn't seem you've made up your mind.")
            return "the_wilderness"


class Goblin1(Scene):

    def enter(self):
        print(dedent("""
            The tracks lead you through the trees and you and find a big fat Gobbo!
            """))

        goblin_counter = 0
        turn_counter = 0
        while True:

            print("""attack | heal | dodge | parry
            """)
            action = input("""What do you do:
            """)
            if action == 'attack':
                goblin_counter += 1
            turn_counter += 1
            if turn_counter == 5:
                print('The Gobbo wrecked you something awful')
                return 'death'
            elif goblin_counter == 2:
                print("You defeated the gobbo")
                global goblin_alive
                goblin_alive = 'dead'
                return 'town_square'
            else:
                gob_quips = ["The goblin spits at you!",
                "The goblin attempts to bite your ankle!",
                "The goblin yells about BMW drivers not using their turn signal!"
                ]
                print(random.choice(gob_quips))


class Dragon1(Scene):

    def enter(self):
        print(dedent("""
            You walk through the burned forest, the smoke burning your nostrils and tickling your lungs.

            You reach a smoldering crater and before you stands the Mighty Flame Lizard!
            """))

        dragon_counter = {"attack" : 0, "heal" : 0, "dodge" : 0, "parry" : 0}
        turn_counter = 0
        while True:

            if 'iron_sword' not in inventory:
                print('The dragon melts your copper sword, and it sticks to your flesh.')
                return 'death'
            print("attack | heal | dodge | parry")
            action = input('What do you do: ')
            if action == 'attack':
                dragon_counter["attack"] = dragon_counter.get("attack", 0) +1
            if action == 'heal':
                dragon_counter["heal"] = dragon_counter.get("heal", 0) +1
            if action == 'dodge':
                dragon_counter["dodge"] = dragon_counter.get("dodge", 0) +1
            if action == 'parry':
                dragon_counter["dodge"] = dragon_counter.get("dodge", 0) +1
            turn_counter += 1
            print(dragon_counter)
            if turn_counter == 15:
                print('The draggo wrecked you good')
                return 'death'
            elif dragon_counter.get("attack") >= 3 and dragon_counter.get("dodge") >= 2 and dragon_counter.get("heal") >= 1 :                          ###########
                print("You defeated the draggo!")
                global dragon_alive
                dragon_alive = 'dead'
                return 'town_square'
            else:
                drag_quips = ["The dragon spits fire at you!",
                "The dragon attempts to bite your ankle!",
                "The dragon goes on a rant about inflation!"
                ]
                print(random.choice(drag_quips))


# scene 5 and maybe 6
class DemonLord(Scene):

    def enter(self):
        print(dedent("""
        You walk through the woods for hours. It gets pretty spooky.

        Finally, you cross a swamp and enter a delapidated castle.

        At the top you prepare to fight the Demon Lord Jim.

        He is a lanky skeleton boy with a sword and staff.
        """))


        demon_counter = {"attack" : 0, "heal" : 0, "dodge" : 0, "parry" : 0}
        turn_counter = 0
        while True:

            if 'diamond_sword' not in inventory:
                print('The Demon Lord Eldritch blasts you into another dimension.')
                return 'death'
                
            print("attack | heal | dodge | parry")
            action = input('What do you do: ')
            if action == 'attack':
                demon_counter["attack"] = demon_counter.get("attack", 0) +1
            if action == 'heal':
                demon_counter["heal"] = demon_counter.get("heal", 0) +1
            if action == 'dodge':
                demon_counter["dodge"] = demon_counter.get("dodge", 0) +1
            if action == 'parry':
                demon_counter["dodge"] = demon_counter.get("dodge", 0) +1

            turn_counter += 1

            print(demon_counter)

            if turn_counter == 30:
                print('The Demon Lord added you to his undead army!')
                return 'death'
            elif demon_counter.get("attack") >= 4 and demon_counter.get("dodge") >= 2 and demon_counter.get("heal") >= 2 and demon_counter.get("parry") >= 2 :
                print("You defeated the Jim!")
                global demon_alive
                demon_alive = 'dead'
                return 'finished'
            else:
                dem_quips = ["The Demon Lord spits a death ray at you!",
                "The Demon Lord attempts to bite your ankle!",
                "The Demon Lord calls you mean name!"
                ]
                print(random.choice(dem_quips))


# victory scene
class Finished(Scene):
    def enter(self):
        print("You won! Good job.")
        return 'finished'


class Map(object):

    scenes = {
        'town_square': TownSquare(),
        'the_armory': TheArmory(),
        'the_guild': TheGuild(),
        'the_wilderness': TheWilderness(),
        'goblin1' : Goblin1(),
        'dragon1' : Dragon1(),
        'demon_lord' : DemonLord(),
        'death': Death(),
        'finished': Finished(),
    }

    # starts map class, takes self and start_scene
    def __init__(self, start_scene):
        self.start_scene = start_scene

    # the function next_scene takes self and scene_name. Value that is returned is a get method on the scenes dictionary above
    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        return val

    # 
    def opening_scene(self):
        return self.next_scene(self.start_scene)


a_map = Map('town_square')
a_game = Engine(a_map)
a_game.play()

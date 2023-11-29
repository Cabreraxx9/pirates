from game import location
#There is some pretense that the game might not be played over the term
# so we use a custom function announce to print things instead of print
from game.display import announce
import game.config as config
import game.items as items
from game.events import *

#Demo island inherits from location (demo island is a location)

class DemoIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        #Object oriented handling. Super() refers to the parent class
        #(Location in this case)
        #So this runs the initializer of Location
        self.name = "island"
        self.symbol = "I" #symbol for map"
        self.visitable = True #Marks the island as a place the pirates can visit
        self.locations = {} #Dictionary of sub-locations on the island
        self.locations["armory"] = Armory(self)
        self.locations["Forest"] = Forest(self)
        self.locations["bar"] = Bar(self)
        self.locations["cafe"] = Cafe(self)
        self.locations["bathroom"] = Bathroom(self)
        self.locations["dock"] = Dock(self)
        

        #where do the pirates start
        self.starting_location = self.locations["dock"]
    
    def enter(self, ship):
        #what to do when the ship visits this location on the map
        announce("arrived at death island") 
#boiler plate code for starting a visit.
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()  
        super().visit()    
#Sub_locations(dock, armory, Forest, bar, cafe, and bathroom)
class Dock(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "dock"
        #the verbs dict was set up by the super() init
        # "go north" has handling that cause sublocation to just get the direction
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["northeast"] = self
        self.verbs["southeast"] = self
        
    def enter(self):
        announce ("You are now docking. Your ship is now docked at death island. You'll need a passcode to get back on the ship")
    #one of the core function .Contains everything that
    #more complex actions should have dedicated functions to handle them
    def passcode(self):
        code = input("Enter the secret word to get back on the ship")
        if code == "ghost":
            return True
        else:
            return False
                
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            announce("you return to your ship")
            #Boilerplater code that stops the visit
            #this calls my passcode function and set it equal to true
        if self.passcode() == True:   
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["armory"]
            #text will be printed by "enter" in Armory()
        if (verb == "northeast"):
            config.the_player.next_loc = self.main_location.locations["bar"]
            #text will be printed by "enter" in Bar()
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["cafe"]
            #text will be printed by "enter" in Cafe()
        if (verb == "southeast"):
            config.the_player.next_loc = self.main_location.locations["bathroom"]
            #text will be printed by "enter" in Bathroom()
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Forest"]
            #text will be printed by "enter" in Forest()
       

class Armory(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "armory"
        self.verbs["northeast"] = self
        self.verbs["east"] = self
        self.verbs["southeast"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self

        #Add a weapon to take!
        self.verbs["take"] = self
        self.item_in_armory = Assault_Rifle()
    
    def enter (self):
        description = "You walk into the armory on the island and see a glowing letter G near the weapon cache"
        if self.item_in_armory != None:

         description = description + "and you see a " + self.item_in_armory.name + " in a weapon cache."
        announce(description)
    
    def process_verb(self, verb, cmd_list, nouns):
    
        if (verb == "south"):
            announce("you are returning to back to the dock")
            config.the_player.next_loc = self.main_location.locations["dock"]
        if (verb == "east"):
            announce("you are heading toward the bar")
            config.the_player.next_loc = self.main_location.locations["bar"]
            #text will be printed by "enter" in Armory()
        
        
        if(verb == "take"):
            #the player will type something like 'take gun"
            if(self.item_in_armory == None):
                announce("you've already taken the gun")
            #they just typed "take"
            elif( len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_armory
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the cache.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_armory = None
                    config.the_player.go = True
                    at_least_one = True
                
                if at_least_one == False:
                    announce ("You don't see one of those around.")

                
                 
class Forest(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Forest"
        self.verbs["north"] = self
        self.verbs["east"] = self
        self.event_chance = 100
        self.events.append(drowned_pirates.DrownedPirates())
        
    def enter(self):
        announce ("You are now entering Forest and see a hoard of zombie pirates.")
    
    def process_verb(self, verb, cmd_list, nouns):

        if (verb == "north"):
            announce("you are returning to back to the dock")
            config.the_player.next_loc = self.main_location.locations["dock"]
        if (verb == "east"):
            announce("you are heading toward the bathroom")
            config.the_player.next_loc = self.main_location.locations["bathroom"]
              
class Bar(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "bar"
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["southeast"] = self
    
    def enter(self):
        announce ("You are now entering the bar and see a glowing letter O in a liqiour bottle.")
    
    def process_verb(self, verb, cmd_list, nouns):

        if (verb == "west"):
            announce("you are heading to the armory")
            config.the_player.next_loc = self.main_location.locations["armory"]
            
            
        if (verb == "east"):
            announce("you are heading toward the cafe")
            config.the_player.next_loc = self.main_location.locations["cafe"]

        if (verb == "southwest"):
            announce("you are going back to the dock")
            config.the_player.next_loc = self.main_location.locations["dock"]
            

class Cafe(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "cafe"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        
    def enter(self):
        announce ("You are now entering a cafe and see a glowiing letter S in a coffee mug.")
    
    def process_verb(self, verb, cmd_list, nouns):

        if (verb == "north"):
            announce("you are heading toward the bar")
            config.the_player.next_loc = self.main_location.locations["bar"]
            
            
        if (verb == "south"):
            announce("you are heading toward the bathroom")
            config.the_player.next_loc = self.main_location.locations["bathroom"]

        if (verb == "west"):
            announce("you are going back to the dock")
            config.the_player.next_loc = self.main_location.locations["dock"]
            
class Bathroom(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "bathroom"
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["northwest"] = self

    def enter(self):
        announce ("You are now in the bathroom and see a glowing letter T in the Toilet.")
    
    def process_verb(self, verb, cmd_list, nouns):

        if (verb == "west"):
            announce("you are heading to the cafe")
            config.the_player.next_loc = self.main_location.locations["cafe"]
            
            
        if (verb == "east"):
            announce("you are heading toward the bathroom")
            config.the_player.next_loc = self.main_location.locations["Forest"]

        if (verb == "northwest"):
            announce("you are going back to the dock")
            config.the_player.next_loc = self.main_location.locations["dock"]


class Katana(items.Item):
    def __init__(self):
        super().__init__("cutlass", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class Assault_Rifle(items.Item):
    def __init__(self):
        super().__init__("assault-rifle", 400) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,100)
        self.firearm = True
        self.charges = 1
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"

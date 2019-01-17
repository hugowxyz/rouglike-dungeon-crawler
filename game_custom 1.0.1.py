import random, csv, time

class Weapon:
    base_damage = random.randint(20, 45)
    def __init__(self, name, tier):
        self.name = name
        self.damage = self.base_damage * tier
       
class Armour:
    base_defense = random.randint(10, 30)
    def __init__(self, name, tier):
        self.name = name
        self.defense = self.base_defense * tier

    
#Base Player Class
class Player:

    #Base attributes
    gold = 0
    levelUp = 100 #Changes after EXP is bigger or equal to this. Changes by 70%
    exp = 0 #Gets exp after killing monster. Base EXP get is 20. Modifies by the tier of the enemy
    health = 5000 #Will change later when I add potions
    mana_points = 50 #Not much to do with this
    attack_points = 50 #How much attack you deal, modifiable when levels up
    defense_points = 100 #Not much to do with this

    inventory = []

    def __init__(self, name): #Contractor??
        self.name = name #Setting name which is not used much
 
    def check_levelUp(self): #Boolean to check if leveled up
        return self.exp >= self.levelUp
        
    def check_death(self): #Boolean to check if health is lower than 0
        return self.health <= 0
                


#Base Monster Class
class Monster:
    #Made this more interesting cause all of its stats are modifiable by its tier
    def __init__(self, tier, race, health, defense):
        self.tier = tier #Setting preset tier when calling it
        self.race = race #Race is defined in "curr_dungeon"
        self.health = health #Health is defined in "curr_dungeon", modified by tier
        self.att = (self.health/5) * (self.tier/.5) #Based on health
        self.defense = defense * self.tier #Modified by tier AND health

    def check_death(self): #Check Death
        return self.health <= 0

def load_shop_inventory():
    shop_inventory = []
    curr_shop_index = []
    curr_shop = [["Health Potion", 20], ["Mana Potion", 10]]
    
    with open("Shop_Inventory.txt", "r") as inventory:
        reader = csv.reader(inventory)
        for line in reader:
            shop_inventory.append(line)
        inventory.close()

    for n in range(5):
        item_index = random.randint(2, 10)
        curr_shop_index.append(item_index)

    for index in range(len(shop_inventory)):
        if index in curr_shop_index:
            curr_shop.append(shop_inventory[index])

    return curr_shop

def dungeon():
    #Dungeons could be read from a file!
    dungeons = [["Whisp Valley", "Undead", 50], ["Wellhaven", "Human", 70],
                ["Whitecrest", "Human", 70], ["Wasted Quarters", "Orc", 75],
                ["Specter Yard", "Undead", 50], ["Coral Pits", "Human", 70],
                ["Killing Yard", "Undead", 50], ["Fire Grotto", "Orc", 75],
                ["Broken Tunnels", "Orc", 75], ["Crystals", "Human", 70]]

    curr_dungeon =  random.choice(dungeons) #Pick a random dungeon which has all of info in the same sub-list!

    enemy = Monster(1, curr_dungeon[1], curr_dungeon[2],
                    curr_dungeon[2]/10) #Calling Monster with information from the dungeons

    return enemy, curr_dungeon #returning values; used in game()

#Combat with a monster; called from combat()
def combat_phase(tier, enemy, player):
    enemy.tier = tier #Getting tier
    enemy.health = enemy.health * tier #Modifying the health by tier
    enemy.att = (enemy.health/20) * (enemy.tier/0.5) #Same with this
    #Complicated way of writing all of the attributes; could've been done in a shorter way
    print("\nYou approach the enemy! It's a tier {} enemy!".format(getattr(enemy, "tier")),
          "Its stats:", "\nRace:", getattr(enemy, "race"), "\nHealth:",getattr(enemy, "health"),
          "\nAttack:", getattr(enemy, "att"), "\nDefense:", getattr(enemy, "defense"), "\n")

    #Original health to reset the health for other monsters
    orig_health_enemy = getattr(enemy, "health")
    #Just in case I want to reset the player's health
    orig_health_player = getattr(player, "health")
    #For leveling up this attr
    orig_attack_player = getattr(player, "attack_points")
    #For leveling up this attr
    orig_defense_player = getattr(player, "defense_points")
    #Boolean to check death of monster
    over_enemy = False
    #Boolean to check death of player
    over_player = False
    #This is the counter for the SPECIAL MOVE
    counter = 0

    #This doens't work so I did a break statement in the loop
    while not over_enemy or not over_player:
                 
        if counter == 4: #If it's bigger than 4 then I reset it
            counter = 0

        if counter != 3: #This is for normal moves; probably could've done it in an easier way
            playerTurn = input("1. Attack! 2. Attack!\nSay: "), print("You attack!\n")
            enemy.health = getattr(enemy, "health") - getattr(player, "attack_points")
            player.health = getattr(player, "health") - getattr(enemy, "att")
            print("Player's Health:", getattr(player, "health"),
              "\nEnemy's Health:", getattr(enemy, "health"))

        elif counter == 3: #Special move where the attack of the player is doubled
            playerTurn = input("1. SPECAL Attack! 2. SPECIAL Attack!\nSay: "), print("You attack!\n")
            enemy.health = getattr(enemy, "health") - (getattr(player, "attack_points") * 2)
            player.health = getattr(player, "health") - getattr(enemy, "att")
            print("Player's Health:", getattr(player, "health"),
              "\nEnemy's Health:", getattr(enemy, "health"))

        over_enemy = enemy.check_death() #Checking death
        over_player = player.check_death() #Checking death

        counter += 1 #Increasing coubnter for the special attack

        if over_enemy: #If the enemy dies I add level to player and check level up too
            exp_gained = 20 * enemy.tier #20 is the base EXP get and tier is the modifier
            player.exp += exp_gained #Adding them up
            gold_found = random.randint(10, 30) * tier
            player.gold += gold_found
            print("You have slain the enemy! You have gained {} EXP!".format(exp_gained)) #Giving the user information
            print("Current EXP: {}/{}".format(player.exp, player.levelUp)) #Telling user how much more EXP he needs
            print("It appears that you found {} gold too!".format(gold_found))   
            if player.check_levelUp(): #Here I check level up
                player.levelUp *= 1.7 #If the user Does level up, then I increase the levelUp by 70%
                print("="* 40) #Print out a full row of = to attract attention
                print("You have leveled up! Current EXP: {}/{}".format(player.exp, player.levelUp))
                valid_options = ["1", "2", "3"]
                userIn = "yes"
                while userIn not in valid_options:
                    print("Choose three attributes to level up!\n1. Health\n2. Attack\n3. Defense")
                    userIn = input("Say: ")
                    if userIn == "1":
                        player.health = orig_health_player * 1.2
                    elif userIn == "2":
                        player.attack_points = orig_attack_player * 1.2
                    elif userIn == "3":
                        player.defense_points = orig_defense_player * 1.2

                #Here is the easier way that I found!
                print("Current Stats:","\nHealth:",player.health, "\nAttack:",
                      player.attack_points, "\nMana Points:", player.mana_points, "\nDefense:",
                      player.defense_points)
            break
        

        if over_player:
            print("You died!")
            quit()

    enemy.health = orig_health_enemy
    
def check_inventory(player):
        items = []
        
        for item in player.inventory:
            print(item)
        userIn = input("Do nothing")

def combat(curr_dungeon, enemy, player):
    print("You enter the dungeon...")

    minion_pos = []

    for n in range(3):
        minion = random.randint(1, 25)
        minion_pos.append(minion)

    mini_boss_pos = random.randint(30, 35)

    boss_pos = random.randint(36, 40)
        
    for turns in range(40):
        userIn = input("ANY key: Go further! 2. Check Inventory\nSay: ")
        if userIn == "2":
            check_inventory(player)
        if turns in minion_pos:
            combat_phase(1, enemy, player)
        if turns == mini_boss_pos:
            combat_phase(2, enemy, player)
        if turns == boss_pos:
            combat_phase(3, enemy, player)

    print("="*40), print("You finished the dungeon!\n")
    game(player)
        
def menu():
    name = input("Welcome to [World]!\nPlease enter a name: ")
    player = Player(name)

    sword = Weapon("Novice Sword", 1)
    armour = Armour("Novice Armour", 1)

    player.inventory.append([sword.name, sword.damage])
    player.inventory.append([armour.name, armour.defense])

    return player

def game_menu():
    options = ["1", "2", "3"]
    while True:
        print("What do you want to do in [World]?\n1. Dungeons\n2. Shops\n3. Quit")
        userIn = input("Say: ")
        if userIn in options:
            break
    return userIn
    
def game(player):

    userIn = game_menu()
    if userIn == "1":
        enemy, curr_dungeon = dungeon()
        print("\nDungeons randomly pop up!\nA dungeon popped up:",
              curr_dungeon[:2])
        userIn = input("Press ANY key to accept! ")
        combat(curr_dungeon, enemy, player)
    elif userIn == "2":

        curr_shop = load_shop_inventory()

        print("Welcome to the Shopping District!\nWhat do you want to buy?\n")

        for item in curr_shop:
            print(*item)

        userIn = input("Say: ")

        #Add something
        
    else:
        quit()
    game_menu()
    

player = menu()
game(player)

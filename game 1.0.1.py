import random

class Player:

    health = 100
    mana_points = 50
    attack_points = 20
    defense_points = 0

    def __init__(self, name):
        self.name = name
        
    def check_death(self):
        return self.health <= 0

class Monster:
    mp = 0
    
    def __init__(self, tier, race, health, defense):
        self.tier = tier
        self.race = race
        self.health = (health * tier)
        self.att = (self.health/5) * (self.tier/.5)
        self.defense = defense * self.tier

    def check_death(self):
        return self.health <= 0
    
def dungeon():
    dungeons = [["Whisp Valley", "Undead", 50], ["Wellhaven", "Human", 70],
                ["Whitecrest", "Human", 70], ["Wasted Quarters", "Orc", 80],
                ["Specter Yard", "Undead", 50], ["Coral Pits", "Human", 70],
                ["Killing Yard", "Undead", 50], ["Fire Grotto", "Orc", 80],
                ["Broken Tunnels", "Orc", 80], ["Crystals", "Human", 70]]

    curr_dungeon =  random.choice(dungeons)

    enemy = Monster(1, curr_dungeon[1], curr_dungeon[2],
                    curr_dungeon[2]/10)

    return enemy, curr_dungeon

def combat_phase(tier, enemy, player):
    setattr(enemy, "tier", tier)
    print("You approach the enemy! It's a tier {} enemy!".format(getattr(enemy,"tier")),
          "Its stats:", "\nRace:", getattr(enemy, "race"), "\nHealth:",getattr(enemy, "health"),
          "\nAttack:", getattr(enemy, "att"), "\nDefense:", getattr(enemy, "defense"))


    
def combat(curr_dungeon, enemy, player):
    print("You enter the dungeon...")

    minion_pos = []

    for n in range(3):
        minion = random.randint(1, 25)
        minion_pos.append(minion)

    mini_boss_pos = random.randint(30, 35)

    boss_pos = random.randint(36, 40)
        
    for turns in range(40):
        userIn = input("Go further!")
        if turns in minion_pos:
            print("You encounter a minion!")
            combat_phase(1, enemy, player)
        if turns == mini_boss_pos:
            print("You encounter a mini boss!")
            combat_phase(2, enemy, player)
        if turns == boss_pos:
            print("You encounter a BOSS!")
            combat_phase(3, enemy, player)
        
def menu():
    name = input("Welcome to [World]!\nPlease enter a name: ")
    player = Player(name)
    return player

def game(player):
    enemy, curr_dungeon = dungeon()
    print("\nDungeons randomly pop up!\nA dungeon popped up:",
          curr_dungeon[:2])
    userIn = input("Press ANY key to accept! ")
    combat(curr_dungeon, enemy, player)
    

player = menu()
game(player)

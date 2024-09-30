import random
import replit
import json
from colored import fore, back, style, attr

colorChoice = fore.WHITE
#You are a traveler who has unexpectedly fallen into the world of Pythor.
#Your goal? Defeat Python the great.
messageslog = []
grid = []
equippedItems = []

colorOptions = {
  "Red": fore.RED,
  "Green": fore.GREEN,
  "Blue": fore.BLUE,
  "White": fore.WHITE
}

defaultSettings = input("Hey! Do you want your world to have default generation settings(Press|enter|for yes)?\n")
if defaultSettings == "":
  GridSetting = 100
  WaterSetting = 450
  MountainSetting = 200
  DitchSetting = 150
  colorOptions = "White"
else:
  while True:
    try:
      GridSetting = int(input("How large do you want your world to be?\n"))
      break
    except:
      pass
  while True:
    try:
      WaterSetting = int(input("How much water do you want?\n"))
      break
    except:
      pass
  while True:
    try:
      MountainSetting = int(input("How mountany do you want your terrain to be?\n"))
      break
    except:
      pass
  while True:
    try:
      DitchSetting = int(input("How many holes do you want to be in the ground?\n"))
      break
    except:
      pass
  


gridsize = GridSetting
inventory = []
#changed grid from 10 to 100

menuOpen = True

gridsize_visible = 9

cameraPos = (0, 0)

# creates large grid
for i in range(gridsize):
  grid.append([])
  for j in range(gridsize):
    grid[i].append(None)
  #print(i)

EndScreen = ""
EndScreen += "######==##==##==######====######==##==##==####==========\n"
EndScreen += "######==##==##==######====######==###=##==#####=========\n"
EndScreen += "==##====##==##==##========##======###=##==##==##========\n"
EndScreen += "==##====######==####======####====######==##==##========\n"
EndScreen += "==##====##==##==##========##======##=###==##==##========\n"
EndScreen += "==##====##==##==######====######==##=###==#####=========\n"
EndScreen += "==##====##==##==######====######==##==##==####==========\n"

#for i in grid:
#  print(i)

#def sayHello(location="World"):
#  print("Hello " + location + "!")

#sayHello()
#sayHello("Earth")
#sayHello("Mars")

#def school(subject="math"):
#  print("I love " + subject)

#school()

#class fruit


#  def __init__(self, _flavor="Sweet"):
#    self.flavor = _flavor
def GainItem(_item):
  inventory.append(_item)
  messageslog.append(_item + " was added to your inventory")


class Entity:

  def __init__(self, name="Entity", _icon="¿"):
    self.name = name
    self.icon = _icon

  def OnSteppedOn(self):
    return True


class Item(Entity):

  def __init__(self, name="Item", _icon="i"):
    Entity.__init__(self, name, _icon)

  def OnSteppedOn(self):
    inventory.append(self)
    return super().OnSteppedOn()


class Weapon(Item):

  def __init__(self, name="Weapon", _icon="t", _damage=(1, 11)):
    super().__init__(name, _icon)
    self.damage = _damage
    self.magic = False


BearFist = Weapon("Bear Fist", "m", (1, 3))
Claw = Weapon("Claw", "f", (3, 5))
BroomOfDestruction = Weapon("Broom of Destruction", "Y", (1, 11))
SwordOfSwording = Weapon("Sword Of Swording", "S", (5, 15))
Scythe = Weapon("Scythe", "J", (1, 8))


class Terrain(Entity):

  def __init__(self, _icon="_"):
    Entity.__init__(self, "Terrain", _icon)

  def OnSteppedOn(self):
    return False


mountain = Terrain("Ʌ")
ditch = Terrain("V")
water = Terrain(fore.BLUE + "_")


class Container(Entity):

  def __init__(self, _name="Container", _icon="n", _contents=[]):
    Entity.__init__(self, "Container", _icon)
    self.contents = _contents

  def OnSteppedOn(self):
    for item in self.contents:
      GainItem(item)
    return True


class Creature(Entity):

  def __init__(self,
               _name="Creature",
               _icon="X",
               _maxHP=10,
               _weapon=None,
               _pos=(0, 0)):
    Entity.__init__(self, _name, _icon)
    self.maxHP = _maxHP
    self.currentHP = self.maxHP
    self.weapon = _weapon
    self.pos = _pos

  def Damage(self, Damage=1):
    messageslog.append(self.name + " Took " + str(Damage) + " Damage")
    self.currentHP -= Damage
    if self.currentHP <= 0:
      self.Die()

  def Die(self):
    messageslog.append(self.name + " Died!")
    #self.icon = fore.RED + "#" + colorChoice
    grid[self.pos[0]][self.pos[1]] = InstantiateContainer(self.name)

  def GetDamageRange(self):
    return self.weapon.damage

  def Attack(self, target):
    target.Damage(
      random.randrange(self.GetDamageRange()[0],
                       self.GetDamageRange()[1]))
    messageslog.append(self.name + " attacks with their " + self.weapon.name)

  def OnSteppedOn(self):
    if self.currentHP > 0:
      messageslog.append("Player attacks with their " + player.weapon.name)
      self.Attack(player)
      messageslog.append(player.weapon.damage[1])
      player.Attack(self)
      messageslog.append("There is something in the way and OUCH!")
    return False


class Player(Creature):

  def Die(self):
    print(EndScreen)
    return quit()


#Banana = fruit("Banana Flavor")
#Apple = fruit()
#
#print(Banana)
#print(Banana.flavor)
#print(Apple)
#print(Apple.flavor)


#print(a, b, c)
#print(f, e, d)
#print(x, y, z)
def LOADJSON(file):
  File = open(file)
  # Opening JSON file
  JSON = json.load(File)
  File.close()
  return JSON


Weapons = LOADJSON("Weapons.json")


def InstantiateWeapon(weapon):
  return Weapon(weapon,\
                Weapons[weapon]["Icon"],\
                Weapons[weapon]["Damage"])


Beasteary = LOADJSON("Beasteary.json")


def InstantiateCreature(creature, Position=(0, 0)):
  return Creature(creature,\
                  Beasteary[creature]["Icon"],\
                  Beasteary[creature]["HP"],\
                  InstantiateWeapon(Beasteary[creature]["Weapon"]),\
                  Position)


def InstantiateContainer(creature):
  return Container("WarChest",\
                  "$",\
                  Loot(creature)
                  )


Goblin = InstantiateCreature("Goblin")
player = Player("Player", "P", 1000, BearFist)


def Loot(_creature="Golem"):
  LootTable = Beasteary[_creature]["Loot Table"]
  messageslog.append(fore.RED + "Loot Being Generated" + colorChoice)
  loot = []
  for item in list(LootTable):
    if random.randrange(0, 100) < LootTable[item]["Chance"]:
      for i in range(random.randint(LootTable[item]["Quantity"][0],\
                                   LootTable[item]["Quantity"][1])):
        loot.append(item)
  return loot


print(Goblin.weapon.damage)

#                  x value            , y value
playerPos = [random.randrange(0, gridsize), random.randrange(0, gridsize)]

amount_of_water = int(WaterSetting)
#randomly places (amount_of_pools) tiles of water across the map
for i in range(0, amount_of_water):
  grid[random.randrange(0, gridsize)][random.randrange(0, gridsize)] = water
  #Experimental!
# for j in range(0, random.randint(4,7)):
#   grid[random.randrange(0, gridsize)-2+random.randint(0,4)][random.randrange(0, gridsize)-2+random.randint(0,4)] = water

#randomley places (amount_of_ditch) tiles of ditch across the map
amount_of_ditch = int(DitchSetting)
for i in range(0, amount_of_ditch):
  grid[random.randrange(0, gridsize)][random.randrange(0, gridsize)] = ditch

#border of mountains around map
for i in range(0, gridsize):
  grid[i][0] = mountain
  grid[i][-1] = mountain
  grid[0][i] = mountain
  grid[-1][i] = mountain

amount_of_mountains = int(MountainSetting)

# randomly placed mountain around the map.
for i in range(0, amount_of_mountains):
  grid[random.randrange(0, gridsize)][random.randrange(0, gridsize)] = mountain

for i in range(0, gridsize):
  #gets random position
  randomPosition = (random.randrange(1, gridsize - 1),
                    random.randrange(1, gridsize - 1))
  #gets random position that isn't water
  while grid[randomPosition[0]][randomPosition[1]] == water:
    randomPosition = (random.randrange(1, gridsize - 1),
                      random.randrange(1, gridsize - 1))
  # sets randomPosition to goblin
  grid[randomPosition[0]][randomPosition[1]] = InstantiateCreature(
    random.choice(list(Beasteary)),
    randomPosition)  #InstantiateCreature("Goblin")

grid[playerPos[0]][playerPos[1]] = player

#grid[playerPos[0] + 3][playerPos[1] + 4] = Goblin
"""for i in grid:
  tempRow = ""
  for j in i:
    if j == None:
      tempRow += "_"
    elif type(j) != str:
      tempRow += j.icon
    else:
      tempRow += j
    tempRow += " "
  print(tempRow)"""


def RenderGrid():
  cameraPos = (playerPos[0], playerPos[1])
  replit.clear()
  for i in range(-int(gridsize_visible / 2), int(gridsize_visible / 2) + 1):
    tempRow = colorChoice + ""
    # run the j for loop for the rows surrounding playerPos within the gridsize_visible range
    for j in range(-int(gridsize_visible / 2), int(gridsize_visible / 2) + 1):
      # display the x,y values surrounding the playerPos within the gridsize_visible range
      gridSpace = grid[(j + cameraPos[0]) % gridsize][(-i + cameraPos[1]) %
                                                      gridsize]
      if gridSpace == None:
        tempRow += colorChoice + "_"
      elif type(gridSpace) != str:
        try:
          tempRow += gridSpace.icon + colorChoice
        except:
          print(gridSpace)
          print(gridSpace.icon)
      else:
        tempRow += gridSpace
      tempRow += " "
    print(tempRow)
  for message in messageslog:
    print(colorChoice + str(message))
  messageslog.clear()


RenderGrid()

def ViewInventory():
  replit.clear()
  print(inventory)
  userInput = input()

def PlayerMove():
  oldPos = playerPos.copy()
  #Guarantee that input is valid
  print(colorChoice + str(playerPos))
  while True:
    userInput = ""
    while not "wasdqmi".__contains__(userInput.lower()) or len(userInput) != 1:
      userInput = input(colorChoice + "WASD to move\n")
    #Look at the playerposition on the grid
    #Delete the player at that position
    if userInput.lower() == "w":
      #Tweak the player position
      playerPos[1] += 1
    elif userInput.lower() == "a":
      #Tweak the player position
      playerPos[0] -= 1
    elif userInput.lower() == "s":
      #Tweak the player position
      playerPos[1] -= 1
    elif userInput.lower() == "d":
      #Tweak the player position
      playerPos[0] += 1
    elif userInput.lower() == "q":
      print(EndScreen)
      return quit()
    elif userInput.lower() == "m":
      return True
    elif userInput.lower() == "i":
      ViewInventory()
    else:
      print("User entered", userInput, "which is not valid")
    if grid[playerPos[0]][playerPos[1]] == None:
      break
    if type(grid[playerPos[0]][playerPos[1]]) != str:
      if not grid[playerPos[0]][playerPos[1]].OnSteppedOn():
        #Revert to old position (bump into wall)
        playerPos[0] = oldPos[0]
        playerPos[1] = oldPos[1]
        break
      else:
        break
    else:
      break
  #Insert the player onto new position on grid
  grid[oldPos[0]][oldPos[1]] = None
  grid[playerPos[0]][playerPos[1]] = player
  RenderGrid()
  #print("WORKING")
  return False


def HandleMenu():
  global colorChoice
  while True:
    try:
      replit.clear()
      print("Choose a color from this list.")
      for colorOption in colorOptions.keys():
        print(colorOptions[colorOption] + colorOption + colorChoice)
      colorChoice = colorOptions[input().capitalize()]
      RenderGrid()
      break
    except:
      continue
  return False
  
  replit.clear()
  print(defaultSetting)
  print(WaterSetting)
  print(MountainSetting)
  print(DitchSetting)
  return False


#print(EndScreen)
while True:
  menuOpen = PlayerMove()
else:
  print(EndScreen)
#PlayerName = input("Please enter your name: ")

#PlayerInput = input("Nice to meet you, " + PlayerName +
#                    ", what is your social security number? ")
#PlayerInput = input("That's interesting...")

#if PlayerInput.lower() == "yes it is.":
#  print("You've gone too far, " + PlayerName)
#else:
#  print("Goodbye!")

#PlayerInput = print("Goodbye!") if PlayerInput = input("Yes it is.") print ("You've gone too far, Michael")

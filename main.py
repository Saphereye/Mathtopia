import pyglet
import os
import sys
from pyglet.window import key
from typing import Union, Optional, List
from dataclasses import dataclass

def ResourcePath(relativePath: str) -> Union[bytes, str]:
    # Get the directory of the current script
    currentDirectory = os.path.dirname(os.path.abspath(__file__))

    # Move one directory up and then into 'Assets'
    assetsDirectory = os.path.join(currentDirectory, 'Assets')

    try:
        # If running from a PyInstaller bundle, use the temporary _MEIPASS directory
        basePath = sys._MEIPASS
    except AttributeError:
        # Otherwise, use the absolute path to the assets directory
        basePath = os.path.abspath(assetsDirectory)

    # Return the full path to the resource
    return os.path.join(basePath, relativePath)

window = pyglet.window.Window()

# Music Player Details
bgMusicPlayer = pyglet.media.Player()
bgMusic = pyglet.media.load(ResourcePath("Music/MathtopiaTheme.wav"))
bgMusicPlayer.queue(bgMusic)
bgMusicPlayer.play()
bgMusicPlayer.loop = True

# World Dimensions
worldWidth = 300
worldHeight = 300
worldX = 50
worldY = 50

# Level Information
currentLevel = 0
numberOfLevels = 6

# Adding font, to be used for text
pyglet.font.add_file(ResourcePath('Font/Minecraft.ttf'))
minecraftText = pyglet.font.load('Minecraft')

# Title screen text
titleScreenLabel = pyglet.text.Label('Mathtopia', font_name='Minecraft', font_size=72, x=100, y=225)
partLabel = pyglet.text.Label('The beginning', font_name='Minecraft', font_size=18, x=100, y=200)
pressSpaceToContinueLabel = pyglet.text.Label('Press SPACE to continue', font_name='Minecraft', font_size=18, x=162.5,
                                              y=100)

# End screen text
thankYouLabel = pyglet.text.Label('Thank You for Playing :)', font_name='Minecraft', font_size=20, x=150, y=270)
creatorLabel = pyglet.text.Label('-Saphereye', font_name='Minecraft', font_size=20, x=150, y=230)


# 'World operator' and 'Goal' labels with their positions
worldOperatorLabel = pyglet.text.Label('World Operator', font_name='Minecraft', font_size=20, x=412.5, y=300)
goalLabel = pyglet.text.Label('Goal', font_name='Minecraft', font_size=20, x=462.5, y=150)

playerImage = pyglet.image.load(ResourcePath('Images/Player.png'))

plusImage = pyglet.image.load(ResourcePath('Images/Plus.png'))
minusImage = pyglet.image.load(ResourcePath('Images/Minus.png'))
multiplicationImage = pyglet.image.load(ResourcePath('Images/Multiplication.png'))
divisionImage = pyglet.image.load(ResourcePath('Images/Division.png'))

oneImage = pyglet.image.load(ResourcePath('Images/One.png'))
twoImage = pyglet.image.load(ResourcePath('Images/Two.png'))
threeImage = pyglet.image.load(ResourcePath('Images/Three.png'))
fourImage = pyglet.image.load(ResourcePath('Images/Four.png'))
fiveImage = pyglet.image.load(ResourcePath('Images/Five.png'))
sixImage = pyglet.image.load(ResourcePath('Images/Six.png'))
sevenImage = pyglet.image.load(ResourcePath('Images/Seven.png'))
eightImage = pyglet.image.load(ResourcePath('Images/Eight.png'))
nineImage = pyglet.image.load(ResourcePath('Images/Nine.png'))
zeroImage = pyglet.image.load(ResourcePath('Images/Zero.png'))

backgroundImage = pyglet.image.load(ResourcePath('Images/Background.png'))

class Cell:
    def __init__(self, x, y, width, height, batch, isVisible, spriteImage):
        self.isVisible = isVisible
        self.isNumber = False
        self.isSymbol = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.batch = batch
        self.obj = None
        self.image = spriteImage
        self.dir = "UP"

        # if isSymbol
        self.symbol = '+'

        # if Number
        self.number = 1

    def draw(self):
        if self.isVisible:
            worldMap.put(self.x, self.y, self)
            self.obj = pyglet.sprite.Sprite(self.image, self.x + worldX, self.y + worldY, batch=self.batch)


class List2D:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.value = [None for _ in range(width * height)]
        """
        (1,3) (2,3) (3,3)       6 7 8
        (1,2) (2,2) (3,2)   =>  3 4 5   => [0 1 2 3 4 5 6 7 8]
        (1,1) (2,1) (3,1)       0 1 2
        """

    def put(self, x, y, element):
        # Insert element at position (x,y)
        # x and y are inserted as 1...n
        self.value[(x - 1) + (y - 1) * self.width] = element

    def get(self, x, y):
        # Call value at position (x,y)
        # Possible returns :- None, Player, Symbol, Number
        return self.value[(x - 1) + (y - 1) * self.width]


class Player(Cell):
    global worldMap

    def __init__(self, x, y, width, height, batch, isVisible, spriteImage):
        super().__init__(x, y, width, height, batch, isVisible, spriteImage)

    def move(self, x, y):
        worldMap.put(self.x, self.y, None)
        self.x = x
        self.y = y
        worldMap.put(self.x, self.y, self)
        self.draw()

    def move_up(self):
        worldMap.put(self.x, self.y, None)
        self.y = self.y + self.height if (self.y + self.height) < worldHeight else (self.y + self.height) % worldHeight
        worldMap.put(self.x, self.y, self)
        self.draw()
        self.dir = "UP"

    def move_down(self):
        worldMap.put(self.x, self.y, None)
        self.y = self.y - self.height if (self.y - self.height) >= 0 else (self.y - self.height) % worldHeight
        worldMap.put(self.x, self.y, self)
        self.draw()
        self.dir = "DOWN"

    def move_right(self):
        worldMap.put(self.x, self.y, None)
        self.x = self.x + self.width if (self.x + self.width) < worldWidth else (self.x + self.width) % worldWidth
        worldMap.put(self.x, self.y, self)
        self.draw()
        self.dir = "RIGHT"

    def move_left(self):
        worldMap.put(self.x, self.y, None)
        self.x = self.x - self.width if (self.x - self.width) >= 0 else (self.x - self.width) % worldWidth
        worldMap.put(self.x, self.y, self)
        self.draw()
        self.dir = "LEFT"


class Symbol(Cell):
    def __init__(self, x, y, width, height, batch, isVisible, inputSymbol, spriteImage):
        super().__init__(x, y, width, height, batch, isVisible, spriteImage)
        self.isSymbol = True
        self.symbol = inputSymbol

    def move(self, direction):
        worldMap.put(self.x, self.y, None)
        if direction == "UP":
            self.y = self.y + self.height if (self.y + self.height) < worldHeight else \
                (self.y + self.height) % worldHeight
        elif direction == "DOWN":
            self.y = self.y - self.height if (self.y - self.height) >= 0 else (self.y - self.height) % worldHeight
        elif direction == "RIGHT":
            self.x = self.x + self.width if (self.x + self.width) < worldWidth else (self.x + self.width) % worldWidth
        elif direction == "LEFT":
            self.x = self.x - self.width if (self.x - self.width) >= 0 else (self.x - self.width) % worldWidth
        self.dir = direction
        for i in symbolList:
            if i == self:
                pass
            elif i.x == self.x and i.y == self.y:
                i.move(self.dir)
        worldMap.put(self.x, self.y, self)
        self.draw()

class Number(Symbol):
    def __init__(self, x, y, width, height, batch, isVisible, inputSymbol, spriteImage):
        super().__init__(x, y, width, height, batch, isVisible, inputSymbol, spriteImage)
        self.isNumber = True
        self.number = str(inputSymbol)
        self.image = spriteImage

def evaluate_world() -> None:
    global worldMap, currentLevel
    executableStringsH = []
    executableStringsV = []
    appendableString = ''

    # Horizontal Evaluation
    for y in range(0, worldHeight + 1, 30):
        for x in range(0, worldWidth + 1, 30):
            item = worldMap.get(x, y)
            if (item is None) or (type(item) is Player):
                if appendableString != '':
                    executableStringsH.append(appendableString)
                appendableString = ''
            else:
                appendableString += str(item.symbol)

        if appendableString != '':
            executableStringsH.append(appendableString)
        appendableString = ''

    for index in range(len(executableStringsH)):
        executableStringsH[index] = executableStringsH[index].strip()

    # Vertical Evaluation
    for x in range(0, worldWidth + 1, 30):
        for y in range(worldHeight, 0, -30):
            item = worldMap.get(x, y)
            if item is None:
                if appendableString != '':
                    executableStringsV.append(appendableString)
                appendableString = ''
            elif (item is not None) and (type(item) is not Player):
                appendableString += str(item.symbol)

        if appendableString != '':
            executableStringsV.append(appendableString)
        appendableString = ''
    for index in range(len(executableStringsV)):
        executableStringsV[index] = executableStringsV[index].strip()

    # remove +3 from executableStrings
    finalH = []
    finalV = []
    for equation in executableStringsH:
        try:
            finalH.append(eval(equation))
        except SyntaxError:
            continue
    for equation in executableStringsV:
        try:
            finalV.append(eval(equation))
        except SyntaxError:
            continue
    """
    (Answer, Operator)
    If operator is None, only check rows and columns
    else apply operator
    """
    currentAnswer = levelData[currentLevel][0]
    currentSymbol = levelData[currentLevel][1]
    if currentSymbol is None:
        for x in finalH:
            if x == currentAnswer:
                currentLevel += 1
        for y in finalV:
            if y == currentAnswer:
                currentLevel += 1
    else:
        for x in finalH:
            for y in finalV:
                if eval(f'x {currentSymbol} y') == currentAnswer:
                    currentLevel += 1


# Drawing the text on the screen
def level_name_label_draw(labelText, x, y):
    levelTitle = pyglet.text.Label(labelText, font_name='Minecraft', font_size=60, x=x, y=y)
    levelTitle.draw()

def goal_label_draw(goalNumber):
    goalNumberLabel = pyglet.text.Label(str(goalNumber), font_name='Minecraft', font_size=18, x=485, y=120)
    goalNumberLabel.draw()

def world_multiplier_draw(multiplier):
    worldMultiplierLabel = pyglet.text.Label(multiplier, font_name='Minecraft', font_size=20, x=485, y=270)
    worldMultiplierLabel.draw()

# Answers of levels in format (Answer, World Symbol, Level Name)
levelData = [(0, 0, 'Title Screen'),
             (3, None, '1+2=?'),
             (9, None, 'Trinomial'),
             (9, None, 'Vinculum'),
             (6, '-', 'Complexity++'),
             (4, '-', 'Convergence'),
             (7, '/', 'Nice 7')]

# Update screen with current level
def call_level(levelNumber):
    global currentLevel, symbolList, worldMap
    if levelNumber == 0:
        symbolList = []
    elif levelNumber == 1:
        """
        1+2 = 3
        2+1 = 3
        """
        level_name_label_draw('1+2=?', 50, 375)
        goal_label_draw(3)
        playerLevel1.draw()
        plusSymbolLevel1.draw()
        oneLevel1.draw()
        twoLevel1.draw()
        symbolList = [plusSymbolLevel1, twoLevel1, oneLevel1]
    elif levelNumber == 2:
        """
        6-4+7 = 9
        7-4+6 = 9
        """
        level_name_label_draw('Trinomial', 50, 375)
        goal_label_draw(9)
        playerLevel2.draw()
        sixLevel2.draw()
        fourLevel2.draw()
        sevenLevel2.draw()
        minusSymbolLevel2.draw()
        plusSymbolLevel2.draw()
        symbolList = [plusSymbolLevel2, minusSymbolLevel2, sevenLevel2, fourLevel2, sixLevel2]
    elif levelNumber == 3:
        """
        27/3 = 9
        """
        level_name_label_draw("Vinculum", 50, 375)
        goal_label_draw(9)
        playerLevel3.draw()
        twoLevel3.draw()
        sevenLevel3.draw()
        threeLevel3.draw()
        divisionSymbolLevel3.draw()
        symbolList = [twoLevel3, sevenLevel3, threeLevel3, divisionSymbolLevel3]
    elif levelNumber == 4:
        """
        3-7+5*2 = 6
        5*2+3-7 = 6
        but '-' is more interesting =>
        5*2-7+3 = 6
        7+5-3*2 = 6
        """
        level_name_label_draw("Complexity++", 50, 375)
        goal_label_draw(6)
        world_multiplier_draw('-')
        playerLevel4.draw()
        fiveLevel4.draw()
        twoLevel4.draw()
        sevenLevel4.draw()
        threeLevel4.draw()
        plusSymbolLevel4.draw()
        multiplicationSymbolLevel4.draw()
        symbolList = [fiveLevel4, twoLevel4, sevenLevel4, threeLevel4, plusSymbolLevel4, multiplicationSymbolLevel4]
    elif levelNumber == 5:
        """
        5+2-3 = 4
        5-3+2 = 4
        7+2-5 = 4
        25-7*3 = 4
        5-7+2*3 = 4
        """
        level_name_label_draw("Convergence", 50, 375)
        goal_label_draw(4)
        world_multiplier_draw('-')
        playerLevel5.draw()
        fiveLevel5.draw()
        twoLevel5.draw()
        sevenLevel5.draw()
        threeLevel5.draw()
        plusSymbolLevel5.draw()
        multiplicationSymbolLevel5.draw()
        symbolList = [fiveLevel5, twoLevel5, sevenLevel5, threeLevel5, plusSymbolLevel5, multiplicationSymbolLevel5]

    elif levelNumber == 6:
        """
        6+9-4*2 = 7 <=
        9+6-2*4 = 7
        4-9+2*6 = 7 <=
        2*6+4-9 = 7 <=
        2*6-9+4 = 7
        9*2/6+4 = 7
        4+2/6*9 = 7
        2*9/6+4 = 7"""
        level_name_label_draw("Nice 7", 50, 375)
        goal_label_draw(7)
        world_multiplier_draw('÷')
        playerLevel6.draw()
        minusSymbolLevel6.draw()
        multiplicationSymbolLevel6.draw()
        sixLevel6.draw()
        nineLevel6.draw()
        fourLevel6.draw()
        twoLevel6.draw()
        symbolList = [sixLevel6, nineLevel6, fourLevel6, twoLevel6, minusSymbolLevel6, multiplicationSymbolLevel6]

    else:
        window.close()
        symbolList = []



groundBatch = pyglet.graphics.Batch()
for i in range(1, numberOfLevels + 1):
    exec(f"cellBatchLevel{i} = pyglet.graphics.Batch()")
userInterface = pyglet.graphics.Batch()

worldMap = List2D(worldWidth, worldHeight)
ground = pyglet.sprite.Sprite(backgroundImage, worldX, worldY, batch=groundBatch)

symbolList = []


playerLevel1 = Player(0, 0, 30, 30, cellBatchLevel1, True, playerImage)
plusSymbolLevel1 = Symbol(150, 120, 30, 30, cellBatchLevel1, True, '+', plusImage)
oneLevel1 = Number(120, 90, 30, 30, cellBatchLevel1, True, 1, oneImage)
twoLevel1 = Number(120, 150, 30, 30, cellBatchLevel1, True, 2, twoImage)

playerLevel2 = Player(0, 0, 30, 30, cellBatchLevel2, True, playerImage)
plusSymbolLevel2 = Symbol(60, 60, 30, 30, cellBatchLevel2, True, '+', plusImage)
minusSymbolLevel2 = Symbol(150, 150, 30, 30, cellBatchLevel2, True, '-', minusImage)
sixLevel2 = Number(60, 90, 30, 30, cellBatchLevel2, True, 6, sixImage)
fourLevel2 = Number(30, 60, 30, 30, cellBatchLevel2, True, 4, fourImage)
sevenLevel2 = Number(60, 30, 30, 30, cellBatchLevel2, True, 7, sevenImage)

playerLevel3 = Player(0, 0, 30, 30, cellBatchLevel3, True, playerImage)
divisionSymbolLevel3 = Symbol(90, 90, 30, 30, cellBatchLevel3, True, '/', divisionImage)
twoLevel3 = Number(60, 120, 30, 30, cellBatchLevel3, True, 2, twoImage)
sevenLevel3 = Number(180, 90, 30, 30, cellBatchLevel3, True, 7, sevenImage)
threeLevel3 = Number(120, 150, 30, 30, cellBatchLevel3, True, 3, threeImage)

playerLevel4 = Player(0, 0, 30, 30, cellBatchLevel4, True, playerImage)
multiplicationSymbolLevel4 = Symbol(30, 30, 30, 30, cellBatchLevel4, True, '*', multiplicationImage)
plusSymbolLevel4 = Symbol(60, 60, 30, 30, cellBatchLevel4, True, '+', plusImage)
fiveLevel4 = Number(120, 90, 30, 30, cellBatchLevel4, True, 5, fiveImage)
twoLevel4 = Number(30, 60, 30, 30, cellBatchLevel4, True, 2, twoImage)
sevenLevel4 = Number(90, 30, 30, 30, cellBatchLevel4, True, 7, sevenImage)
threeLevel4 = Number(90, 60, 30, 30, cellBatchLevel4, True, 3, threeImage)
playerLevel5 = Player(0, 0, 30, 30, cellBatchLevel5, True, playerImage)
multiplicationSymbolLevel5 = Symbol(60, 30, 30, 30, cellBatchLevel5, True, '*', multiplicationImage)
plusSymbolLevel5 = Symbol(120, 150, 30, 30, cellBatchLevel5, True, '+', plusImage)
fiveLevel5 = Number(30, 90, 30, 30, cellBatchLevel5, True, 5, fiveImage)
twoLevel5 = Number(90, 90, 30, 30, cellBatchLevel5, True, 2, twoImage)
sevenLevel5 = Number(150, 30, 30, 30, cellBatchLevel5, True, 7, sevenImage)
threeLevel5 = Number(30, 60, 30, 30, cellBatchLevel5, True, 3, threeImage)

playerLevel6 = Player(0, 0, 30, 30, cellBatchLevel6, True, playerImage)
multiplicationSymbolLevel6 = Symbol(30, 30, 30, 30, cellBatchLevel6, True, '*', multiplicationImage)
minusSymbolLevel6 = Symbol(60, 60, 30, 30, cellBatchLevel6, True, '-', minusImage)
sixLevel6 = Number(90, 90, 30, 30, cellBatchLevel6, True, 6, sixImage)
nineLevel6 = Number(120, 120, 30, 30, cellBatchLevel6, True, 9, nineImage)
fourLevel6 = Number(150, 150, 30, 30, cellBatchLevel6, True, 4, fourImage)
twoLevel6 = Number(30, 60, 30, 30, cellBatchLevel6, True, 2, twoImage)



@window.event
def on_draw():
    global currentLevel, symbolList
    window.clear()
    if currentLevel == 0:
        call_level(0)
        titleScreenLabel.draw()
        partLabel.draw()
        pressSpaceToContinueLabel.draw()
    elif currentLevel == numberOfLevels + 1:
        thankYouLabel.draw()
        creatorLabel.draw()
    else:
        call_level(currentLevel)
        groundBatch.draw()
        try:
            eval(f"cellBatchLevel{currentLevel}.draw()")
        except NameError:
            pass
        goalLabel.draw()
        worldOperatorLabel.draw()


@window.event
def on_key_press(symbol, modifiers):
    global currentLevel
    if symbol == key.ESCAPE:
        window.close()
    elif symbol == key.W or symbol == key.UP:
        eval(f"playerLevel{currentLevel}.move_up()")
    elif symbol == key.A or symbol == key.LEFT:
        eval(f"playerLevel{currentLevel}.move_left()")
    elif symbol == key.D or symbol == key.RIGHT:
        eval(f"playerLevel{currentLevel}.move_right()")
    elif symbol == key.S or symbol == key.DOWN:
        eval(f"playerLevel{currentLevel}.move_down()")
    elif symbol == key.SPACE:
        currentLevel += 1

    for symbolInWorld in symbolList:
        if symbolInWorld.x == eval(f"playerLevel{currentLevel}.x") and symbolInWorld.y == eval(
            f"playerLevel{currentLevel}.y"):
            symbolInWorld.move(eval(f"playerLevel{currentLevel}.dir"))


@window.event
def on_key_release(symbol, modifier):
    evaluate_world()



pyglet.app.run()

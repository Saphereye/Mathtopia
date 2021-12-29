import pyglet
from pyglet.window import key
import os

# region WorldInfo
cwd = os.getcwd()+'/'
window = pyglet.window.Window()
bgMusicPlayer = pyglet.media.Player()
bgMusic = pyglet.media.load(cwd+"Music/Vincent Rubinetti - Quaternions.mp3")
bgMusicPlayer.queue(bgMusic)
bgMusicPlayer.play()
bgMusicPlayer.loop = True

worldWidth = 300
worldHeight = 300
worldX = 50
worldY = 50

currentLevel = 0
levelNames = ["1+2=3"]

pyglet.font.add_file(cwd+'Font/Minecraft.ttf')
minecraftText = pyglet.font.load('Minecraft')



# endregion

# region Level Specific Content
titleScreenLabel = pyglet.text.Label('Mathtopia', font_name='Minecraft', font_size=72, x=100, y=225)
partLabel = pyglet.text.Label('The beginning', font_name='Minecraft', font_size=18, x=100, y=200)
pressSpaceToContinueLabel = pyglet.text.Label('Press SPACE to continue', font_name='Minecraft', font_size=18, x=162.5,
                                              y=100)
worldOperatorLabel = pyglet.text.Label('World Operator', font_name='Minecraft', font_size=20, x=412.5, y=300)
goalLabel = pyglet.text.Label('Goal', font_name='Minecraft', font_size=20, x=462.5, y=150)
# endregion

# region Loading Images
playerImage = pyglet.image.load(cwd+'Images/Player.png')

plusImage = pyglet.image.load(cwd+'Images/Plus.png')
minusImage = pyglet.image.load(cwd+'Images/Minus.png')
multiplicationImage = pyglet.image.load(cwd+'Images/Multiplication.png')
divisionImage = pyglet.image.load(cwd+'Images/Division.png')

oneImage = pyglet.image.load(cwd+'Images/One.png')
twoImage = pyglet.image.load(cwd+'Images/Two.png')
threeImage = pyglet.image.load(cwd+'Images/Three.png')
fourImage = pyglet.image.load(cwd+'Images/Four.png')
fiveImage = pyglet.image.load(cwd+'Images/Five.png')
sixImage = pyglet.image.load(cwd+'Images/Six.png')
sevenImage = pyglet.image.load(cwd+'Images/Seven.png')
eightImage = pyglet.image.load(cwd+'Images/Eight.png')
nineImage = pyglet.image.load(cwd+'Images/Nine.png')
zeroImage = pyglet.image.load(cwd+'Images/Zero.png')

backgroundImage = pyglet.image.load(cwd+'Images/Background.png')


# endregion

# region Classes
class List2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.value = [None for _ in range(width * height)]
        """
        (1,3) (2,3) (3,3)       6 7 8
        (1,2) (2,2) (3,2)   =>  3 4 5   => [0 1 2 3 4 5 6 7 8]
        (1,1) (2,1) (3,1)       0 1 2 
        """

    def Put(self, x, y, element):
        # x and y are inserted as 1...n
        self.value[(x - 1) + (y - 1) * self.width] = element

    def Get(self, x, y):
        return self.value[(x - 1) + (y - 1) * self.width]


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

    def Draw(self):
        if self.isVisible:
            worldMap.Put(self.x, self.y, self)
            self.obj = pyglet.sprite.Sprite(self.image, self.x + worldX, self.y + worldY, batch=self.batch)


class Player(Cell):
    global worldMap

    def __init__(self, x, y, width, height, batch, isVisible, spriteImage):
        super().__init__(x, y, width, height, batch, isVisible, spriteImage)

    def Move(self, x, y):
        worldMap.Put(self.x, self.y, None)
        self.x = x
        self.y = y
        worldMap.Put(self.x, self.y, self)
        self.Draw()

    def MoveUp(self):
        worldMap.Put(self.x, self.y, None)
        self.y = self.y + self.height if (self.y + self.height) < worldHeight else (self.y + self.height) % worldHeight
        worldMap.Put(self.x, self.y, self)
        self.Draw()
        self.dir = "UP"

    def MoveDown(self):
        worldMap.Put(self.x, self.y, None)
        self.y = self.y - self.height if (self.y - self.height) >= 0 else (self.y - self.height) % worldHeight
        worldMap.Put(self.x, self.y, self)
        self.Draw()
        self.dir = "DOWN"

    def MoveRight(self):
        worldMap.Put(self.x, self.y, None)
        self.x = self.x + self.width if (self.x + self.width) < worldWidth else (self.x + self.width) % worldWidth
        worldMap.Put(self.x, self.y, self)
        self.Draw()
        self.dir = "RIGHT"

    def MoveLeft(self):
        worldMap.Put(self.x, self.y, None)
        self.x = self.x - self.width if (self.x - self.width) >= 0 else (self.x - self.width) % worldWidth
        worldMap.Put(self.x, self.y, self)
        self.Draw()
        self.dir = "LEFT"


class Symbol(Cell):
    def __init__(self, x, y, width, height, batch, isVisible, inputSymbol, spriteImage):
        super().__init__(x, y, width, height, batch, isVisible, spriteImage)
        self.isSymbol = True
        self.symbol = inputSymbol

    def Move(self, direction):
        worldMap.Put(self.x, self.y, None)
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
                i.Move(self.dir)
        worldMap.Put(self.x, self.y, self)
        self.Draw()


class Number(Symbol):
    def __init__(self, x, y, width, height, batch, isVisible, inputSymbol, spriteImage):
        super().__init__(x, y, width, height, batch, isVisible, inputSymbol, spriteImage)
        self.isNumber = True
        self.number = str(inputSymbol)
        self.image = spriteImage


# endregion

# region Helper Functions
def EvaluateWorld():
    global worldMap, currentLevel
    executableStringsH = []
    executableStringsV = []
    appendableString = ''

    # Horizontal Evaluation
    for y in range(0, worldHeight + 1, 30):
        for x in range(0, worldWidth + 1, 30):
            item = worldMap.Get(x, y)
            if (item is None) or (type(item) is Player):
                if appendableString != '':
                    executableStringsH.append(appendableString)
                appendableString = ''
            else:
                appendableString += str(item.symbol)

        if appendableString != '':
            executableStringsH.append(appendableString)
        appendableString = ''
    for i in range(len(executableStringsH)):
        executableStringsH[i] = executableStringsH[i].strip()

    # Vertical Evaluation
    for x in range(0, worldWidth + 1, 30):
        for y in range(worldHeight, 0, -30):
            item = worldMap.Get(x, y)
            if item is None:
                if appendableString != '':
                    executableStringsV.append(appendableString)
                appendableString = ''
            elif (item is not None) and (type(item) is not Player):
                appendableString += str(item.symbol)

        if appendableString != '':
            executableStringsV.append(appendableString)
        appendableString = ''
    for i in range(len(executableStringsV)):
        executableStringsV[i] = executableStringsV[i].strip()

    # remove +3 from executableStrings
    finalH = []
    finalV = []
    for i in executableStringsH:
        try:
            finalH.append(eval(i))
        except SyntaxError:
            continue
    for i in executableStringsV:
        try:
            finalV.append(eval(i))
        except SyntaxError:
            continue
    # =================================CAUTION==========================================
    # As H and V both are traversed, current level CAN be increased twice in same level
    # =================================CAUTION==========================================
    if currentLevel == 1:
        for i in finalH:
            if i == 3:
                currentLevel = 2
        for i in finalV:
            if i == 3:
                currentLevel = 2
    elif currentLevel == 2:
        for i in finalH:
            if i == 9:
                currentLevel += 1
        for i in finalV:
            if i == 9:
                currentLevel += 1
    elif currentLevel == 3:
        for i in finalH:
            if i == 9:
                currentLevel += 1
        for i in finalV:
            if i == 9:
                currentLevel += 1


def LevelNameLabelDraw(labelText, x, y):
    levelTitle = pyglet.text.Label(labelText, font_name='Minecraft', font_size=60, x=x, y=y)
    levelTitle.draw()


def GoalLabelDraw(goalNumber):
    goalNumberLabel = pyglet.text.Label(str(goalNumber), font_name='Minecraft', font_size=18, x=485, y=120)
    goalNumberLabel.draw()


def CallLevel(levelNumber):
    global currentLevel, symbolList, worldMap
    if levelNumber == 0:
        symbolList = []
    elif levelNumber == 1:
        """
        1+2 = 3
        2+1 = 3
        """
        LevelNameLabelDraw('1+2=?', 50, 375)
        GoalLabelDraw(3)
        playerLevel1.Draw()
        plusSymbolLevel1.Draw()
        oneLevel1.Draw()
        twoLevel1.Draw()
        symbolList = [plusSymbolLevel1, twoLevel1, oneLevel1]
    elif levelNumber == 2:
        """
        6-4+7 = 9
        7-4+6 = 9
        """
        LevelNameLabelDraw('Trinomial', 50, 375)
        GoalLabelDraw(9)
        playerLevel2.Draw()
        sixLevel2.Draw()
        fourLevel2.Draw()
        sevenLevel2.Draw()
        minusSymbolLevel2.Draw()
        plusSymbolLevel2.Draw()
        symbolList = [plusSymbolLevel2, minusSymbolLevel2, sevenLevel2, fourLevel2, sixLevel2]
    elif levelNumber == 3:
        """
        27/3 = 9
        """
        LevelNameLabelDraw("Vinculum", 50, 375)
        GoalLabelDraw(9)
        playerLevel3.Draw()
        twoLevel3.Draw()
        sevenLevel3.Draw()
        threeLevel3.Draw()
        divisionSymbolLevel3.Draw()
        symbolList = [twoLevel3, sevenLevel3, threeLevel3, divisionSymbolLevel3]
    elif levelNumber == 4:
        """
        3-7+5*2 = 6
        5*2+3-7 = 6
        5*2-7+3 = 6
        7+5-3*2 = 6
        """
        LevelNameLabelDraw("Complexity++", 50, 375)
        GoalLabelDraw(6)
    elif levelNumber == 5:
        """
        5+2-3 = 4
        5-3+2 = 4
        7+2-5 = 4
        25-7*3 = 4
        5-7+2*3 = 4
        """
        LevelNameLabelDraw("BODMAS", 50, 375)
        GoalLabelDraw(4)
    elif levelNumber == 6:
        """
        31-24 = 7
        3*2+1 = 7
        2*4-1 = 7
        4*2-1 = 7
        1*4+3 = 7
        3*1+4 = 7
        4*1+3 = 7
        24/3-1 = 7
        3*4/2+1 = 7
        """
        LevelNameLabelDraw("Cartesian's 7", 50, 375)
        GoalLabelDraw(7)
    elif levelNumber == 7:
        """
        6+9-4*2 = 7 <=
        9+6-2*4 = 7
        4-9+2*6 = 7
        2*6+4-9 = 7
        2*6-9+4 = 7
        9*2/6+4 = 7
        4+2/6*9 = 7
        2*9/6+4 = 7"""
        LevelNameLabelDraw("Nice 7", 50, 375)
        GoalLabelDraw(7)
    elif levelNumber == 8:
        """
        9+7-5*3 = 1
        5-7+9/3 = 1
        9/3-7+5 = 1
        """
        LevelNameLabelDraw("Odd one out", 50, 375)
        GoalLabelDraw(1)
    else:
        titleScreenLabel.draw()


# endregion

# region Batches
groundBatch = pyglet.graphics.Batch()
cellBatchLevel1 = pyglet.graphics.Batch()
cellBatchLevel2 = pyglet.graphics.Batch()
cellBatchLevel3 = pyglet.graphics.Batch()
userInterface = pyglet.graphics.Batch()
# endregion

worldMap = List2D(worldWidth, worldHeight)
ground = pyglet.sprite.Sprite(backgroundImage, worldX, worldY, batch=groundBatch)

# region Symbols
symbolList = []

# region Level 1
playerLevel1 = Player(0, 0, 30, 30, cellBatchLevel1, True, playerImage)
plusSymbolLevel1 = Symbol(60, 60, 30, 30, cellBatchLevel1, True, '+', plusImage)
oneLevel1 = Number(30, 120, 30, 30, cellBatchLevel1, True, 1, oneImage)
twoLevel1 = Number(150, 150, 30, 30, cellBatchLevel1, True, 2, twoImage)
threeLevel1 = Number(60, 30, 30, 30, cellBatchLevel1, True, 3, threeImage)

# endregion
# region Level 2
playerLevel2 = Player(0, 0, 30, 30, cellBatchLevel2, True, playerImage)
plusSymbolLevel2 = Symbol(60, 60, 30, 30, cellBatchLevel2, True, '+', plusImage)
minusSymbolLevel2 = Symbol(90, 60, 30, 30, cellBatchLevel2, True, '-', minusImage)
sixLevel2 = Number(30, 120, 30, 30, cellBatchLevel2, True, 6, sixImage)
fourLevel2 = Number(150, 150, 30, 30, cellBatchLevel2, True, 4, fourImage)
sevenLevel2 = Number(60, 30, 30, 30, cellBatchLevel2, True, 7, sevenImage)

# endregion
# region Level 3
playerLevel3 = Player(0, 0, 30, 30, cellBatchLevel3, True, playerImage)
divisionSymbolLevel3 = Symbol(60, 60, 30, 30, cellBatchLevel3, True, '/', divisionImage)
twoLevel3 = Number(30, 210, 30, 30, cellBatchLevel3, True, 2, twoImage)
sevenLevel3 = Number(90, 120, 30, 30, cellBatchLevel3, True, 7, sevenImage)
threeLevel3 = Number(30, 120, 30, 30, cellBatchLevel3, True, 3, threeImage)


# endregion

# endregion

# region Events
@window.event
def on_draw():
    global currentLevel, symbolList
    window.clear()
    if currentLevel == 0:
        CallLevel(0)
        titleScreenLabel.draw()
        partLabel.draw()
        pressSpaceToContinueLabel.draw()
    else:
        CallLevel(currentLevel)
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
        eval(f"playerLevel{currentLevel}.MoveUp()")
    elif symbol == key.A or symbol == key.LEFT:
        eval(f"playerLevel{currentLevel}.MoveLeft()")
    elif symbol == key.D or symbol == key.RIGHT:
        eval(f"playerLevel{currentLevel}.MoveRight()")
    elif symbol == key.S or symbol == key.DOWN:
        eval(f"playerLevel{currentLevel}.MoveDown()")
    elif symbol == key.SPACE:
        currentLevel += 1

    for i in symbolList:
        if i.x == eval(f"playerLevel{currentLevel}.x") and i.y == eval(f"playerLevel{currentLevel}.y"):
            i.Move(eval(f"playerLevel{currentLevel}.dir"))


@window.event
def on_key_release(symbol, modifier):
    EvaluateWorld()


# endregion

pyglet.app.run()

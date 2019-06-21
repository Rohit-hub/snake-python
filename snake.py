from time import sleep
from random import randint
from pynput.keyboard import Key, Listener


class Game:
    # Create the board and snake
    def __init__(self, size, winCondition):
        # Create a square board that is size x size
        self.size = size
        self.board = Board(size,self)
        # Start with a score of 0
        self.score = 0
        # Set the score limit to winCondition
        self.winCondition = winCondition

        # Initialise the snake on the board
        self.snake = Snake(self.board, size)

        # Start the snake moving North
        self.storedDirection = "N"

        # 0: Loss, 1: Game in progress, 2: Won
        self.state = 1

    # Return the board object
    def getBoard(self):
        return self.board

    # Add to the score and return the new score
    def addScore(self, score=1):
        self.score += score
        return self.score

    # Check if the target score has been reached and return the new game state
    def checkWin(self):
        # If the target score has been reached
        if (self.score >= self.winCondition):
            self.setState(2) # State 2 = Win
        return self.getState()

    # Move the snake and check the win condition
    def tick(self):
        # Move the snake forward in the selected direction
        self.snake.update(self.storedDirection)
        # Check if the latest move caused the score limit to be reached
        self.checkWin()

        # Print the new board state
        self.board.printBoard()

    # Get the width of the board
    def getSize(self):
        return self.size

    # Get the current board state
    def getState(self):
        # 0: Game lost
        # 1: Game in progress
        # 2: Game won
        return self.state

    # Set the game state to 0, 1 or 2
    def setState(self, state):
        if (state in [0,1,2]):
            self.state = state

    # Place the first piece of fruit and display the board
    def start(self):
        self.placeFruit()
        self.board.printBoard() # TODO: Remove printBoard and create PyQt GUI

    # Place a fruit on a random free spot on the board
    def placeFruit(self):

        # Create an array that contains the coordinates of every empty spot on the board
        freeSpaces = []
        containedObj = None

        # For each column (Do self.size-2 to exclude the walls around the play area)
        for x in range(self.size-2):
            # For each row in the column
            for y in range(self.size-2):
                # Get the currently contained object in the current tile
                containedObj = self.board.getContains(x,y)

                # If the tile has nothing on it, add it to the list of free spaces
                if (containedObj == None):
                    freeSpaces.append({"x":x,"y":y})

        # If any free spaces exist
        if (len(freeSpaces)>0):
            # Pick a random space
            chosenSpace = randint(0,len(freeSpaces)-1)
            chosenSpace = freeSpaces[chosenSpace]

            # Add a fruit to the selected space
            self.board.setContains(chosenSpace["x"],chosenSpace["y"],Fruit())


    # Get keyboard input using Pynput
    def inputDir(self,inputKey):
        # Get the first snake segment
        head = self.snake.getBody()[0]
        # Get the direction that it is travelling
        oldDirection = head.getDir()
        newDirection = None

        # Translate keystrokes into desired compass directions
        if (inputKey == Key.up):
            newDirection = "N"
        elif (inputKey == Key.down):
            newDirection = "S"
        elif (inputKey == Key.left):
            newDirection = "W"
        elif (inputKey == Key.right):
            newDirection = "E"

        # Find out which direction is opposite to the chosen direction
        oppositeDirection = head.getOppositeDir(oldDirection)

        # Check if the new direction is valid
        if (newDirection in ["N","S","E","W"]):
            # Do not allow the snake to do a 180 degree turn
            if (newDirection != oppositeDirection):
                self.storedDirection = newDirection
        
            
            
    
# A tile that keeps track of what is on it (e.g a segment of the snake or a fruit)
class Tile:
    # Start empty
    def __init__(self):
        self.contains = None

    # Set the contents of the tile
    def setContains(self, obj):
        self.contains = obj

    # Get the contents of the tile
    def getContains(self):
        return self.contains

    # Clear the contents of the tile
    def emptyContains(self):
        self.contains = None


# The board keeps references to all of the tiles and their positions
class Board:
    def __init__(self,size,game):
        # Set the board to be a square of size x size
        self.size = size
        self.board = []
        self.game = game
        temp = []
        # For each row, do (size+2) to allow space for walls at either end
        for i in range(size+2):
            temp = []
            # For each column
            for k in range(size+2):
                # Create a tile for that spot
                temp.append(Tile())
                # If the tile exists at the edge of the board, place a wall in it
                if (k == 0 or k == size+1 or i == 0 or i == size+1):
                    temp[-1].setContains(Wall())
            self.board.append(temp)

    # Print the board to console
    def printBoard(self): # TODO: Replace with GUI
        printString = "\n\n\n\n\n\n\n\n\n"
        for row in self.board:
            for col in row:
                if (col.getContains() == None):
                    printString = printString + "  "
                elif (isinstance(col.getContains(),Segment)):
                    printString = printString + "x "
                elif (isinstance(col.getContains(),Wall)):
                    printString = printString + "+ "
                elif (isinstance(col.getContains(),Fruit)):
                    printString = printString + "# "
            printString = printString + "\n"
        print(printString)

    # Set the contents of a tile at a given set of coordinates
    def setContains(self,xCoord, yCoord, obj):
        self.board[yCoord][xCoord].setContains(obj)

    # Get the contents of a tile at a given set of coordinates
    def getContains(self,xCoord,yCoord):
        return self.board[yCoord][xCoord].getContains()

    # Clear the contents of a tile at a given set of coordinates
    def emptyContains(self, xCoord, yCoord):
        selfboard[yCoord][xCoord].emptyContains()

    # Get the width of the board
    def getSize(self):
        return self.game.getSize()

    # Get the board array
    def getBoard(self):
        return self.board

    # Get the game that this board was spawned by
    def getGame(self):
        return self.game

# A piece of the snake which tracks its coordinate and direction
class Segment:
    def __init__(self, xCoord, yCoord, goingTo, comingFrom, snake):
        # Instantiate a segment at the given coordinates with the given direction
        self.snake = snake
        self.x = xCoord
        self.y = yCoord
        self.goingTo = goingTo
        self.comingFrom = comingFrom

        # Hard-coded directions and their opposites to improve readability later on
        self.oppositeDirections = {"N":"S","S":"N","W":"E","E":"W"}

    # Get the opposite direction that this segment is going to
    def getOppositeDir(self, direction):
        return self.oppositeDirections[direction] # This is different from self.comingFrom as the segment should only be making 90 degree turns

    # Get the direction that this segment is travelling to
    def getDir(self):
        return self.goingTo

    # Set the direction that this segment is travelling to
    def setDir(self, newDir):
        self.goingTo = newDir

    # Get the direction that this segment came from
    def getComingFrom(self):
        return self.comingFrom

    # Move this segment forward by 1 space
    def move(self):
        if (self.goingTo == "N"):
            self.y -= 1
        elif (self.goingTo == "S"):
            self.y += 1
        elif (self.goingTo == "W"):
            self.x -= 1
        elif (self.goingTo == "E"):
            self.x += 1

        # After the segment moves, log the direction it came from
        self.comingFrom = self.oppositeDirections[self.goingTo]

        # Return the new coordinates of this segment
        return {"x":self.x,"y":self.y}

    # Get the coordinates of this segment
    def getPos(self):
        return {"x":self.x,"y":self.y}

    # Check that the tile in front of this segment is within the play area
    def canMove(self):
        # Get the size of the board
        size = self.snake.getBoardSize()

        # Get the coordinate that this segment would move to next
        tempY = self.y
        tempX = self.x
        if (self.goingTo == "N"):
            tempY -= 1
        elif (self.goingTo == "S"):
            tempY += 1
        elif (self.goingTo == "W"):
            tempX -= 1
        elif (self.goingTo == "E"):
            tempX += 1

        # If the snake would be moving out of bounds, return false
        if (tempY < 0 or tempX < 0):
            return False
        elif (tempX == size or tempY == size):
            return False
        # If the snake is still within the play area, return true
        else:
            return True

    def getNextCoord(self):
        pos = self.getPos()
        direction = self.getDir()

        if (direction == "N"):
            pos["y"] -= 1
        elif (direction == "S"):
            pos["y"] += 1
        elif (direction == "W"):
            pos["x"] -= 1
        elif (direction == "E"):
            pos["x"] += 1

        return pos

        
        
        
class Wall:
    def __init__(self):
        pass
    
class Fruit:
    def __init__(self, pointValue=1):
        self.value = pointValue
        

class Snake:
    def __init__(self, board, size):
        self.segments = []
        self.board = board
        self.size = size

        snakeOrigin = size//2 + 1
        startingSegment = Segment(snakeOrigin,snakeOrigin,"N","S",self)
        self.segments.append(startingSegment)
        self.segments.append(Segment(snakeOrigin,snakeOrigin+1,"N","S",self))
        self.segments.append(Segment(snakeOrigin,snakeOrigin+2,"N","S",self))

        self.updateBoardContains()
        

    def updateBoardContains(self):
        # Remove all segments from the board (but not the snake)
        for row in range(self.size):
            for col in range(self.size):
                if (isinstance(self.board.getContains(row,col),Segment)):
                    self.board.emptyContains(row,col)
                    
        # For each segment of the snake, add its position to the board
        coord = {}
        for segment in self.getBody():
            coord = segment.getPos()
            self.board.setContains(coord["x"],coord["y"],segment)

                
            
            
    # Return an array containing all of the snake segments
    def getBody(self):
        return self.segments

    # Move the snake
    def update(self,newDir):
        newCoord = {}
        oldCoord = {}

        # Get the coordinate that the head segment is about to move to
        head = self.segments[0]
        headPos = head.getPos()
        headDir = head.setDir(newDir)
        nextCoord = head.getNextCoord()
        nextY = nextCoord["y"]
        nextX = nextCoord["x"]

        # Check if the head is about to collide with something
        nextObject = board.getContains(nextX, nextY)

        # If the head has collided with a wall or part of itself
        if (isinstance(nextObject, Wall) or isinstance(nextObject, Segment)):
            # Set the game state to be a loss
            self.board.getGame().setState(0)
        # If the head has collided with a fruit
        elif (isinstance(nextObject, Fruit)):
            # Grow the snake
            self.grow()
            # Place a new piece of fruit
            self.board.getGame().placeFruit()
            # Increment the score
            self.board.getGame().addScore()

        # If the next tile is empty
        else:
            # Move the snake along
            self.moveSnake()
            
        
    # Move each segment of the snake
    def moveSnake(self):
        # Get the direction that the snake is about to move to
        previousDir = self.getBody()[0].getDir()
        tempDir = ""

        # For each snake segment
        for segment in self.getBody():
            # Get the coordinate it is currently at
            oldCoord = segment.getPos()
            # Get the coordinate it is moving to
            newCoord = segment.move()


            # Get the segments current direction
            tempDir = segment.getDir()

            # Set the segment to move in the direction that the previous segment was moving
            # This makes segments follow the path of the snake
            segment.setDir(previousDir)
            # Store the direction that this segment was previously going to, so that the following segment can be set to move in this direction
            previousDir = tempDir

            # Move the segment to its new location
            self.board.setContains(oldCoord["x"],oldCoord["y"],None)
            self.board.setContains(newCoord["x"],newCoord["y"],segment)

            
    # Return the width of the board
    def getBoardSize(self):
        return self.board.getSize()

    # Grow the snake by 1 piece
    def grow(self):
        # Get the read segment
        head = self.segments[0]
        # Get the coordinates of the head
        headPos = head.getPos()
        # Get the direction that the head is moving to
        headDir = head.getDir()
        oppositeDir = head.getOppositeDir(headDir)

        # Get the coordinate that the head is about to move to
        nextCoord = head.getNextCoord()
        nextY = nextCoord["y"]
        nextX = nextCoord["x"]

        # Create a new segment at those coordinates that is moving in the same direction as the old head was
        newHead = Segment(nextX, nextY, headDir, oppositeDir, self)

        # Add this new segment to the start of the body array (So it becomes the new head)
        self.segments.insert(0, newHead)
        # Set the contents of the next tile to the new segment
        self.board.setContains(nextX, nextY, newHead)

    # Return the board array
    def getBoard(self):
        return self.board
        
        
# Board size defaults to 11
s = 11

# Find out the maximum score possible (Where the snake will fill the entire play area, -3 due to the snake starting with 3 segments
winCond = ((s-2)**2)-3

# Create the game
game = Game(size = s, winCondition = winCond)
board = game.getBoard()

input("Press ENTER to begin...")

# Listen for keystrokes and report them to the game object
listener = Listener(on_press=game.inputDir)
listener.start()


# Place the first piece of fruit and print the board for the first time
game.start()
while (True):
    # Wait 0.2 seconds
    sleep(0.2)
    # Move the snake in the selected direction and place a new piece of fruit if required
    game.tick()
    # If the desired score has been reached
    if (game.getState() > 1):
        print("\n\n\nYou won the game!\n\n\n") # Display victory message TODO: No longer necessary when GUI is implemented
        sleep(0.5) # Block keyboard input for a moment so that the user does not accidentally scroll up in the console TODO: This is not necessary after a GUI is implemented
        input("Press ENTER to exit...") 
        break
    # If the game was lost
    elif (game.getState() == 0):
        print("\n\n\nSorry, game over...\n\n\n") # Display game over message TODO: No longer necessary when GUI is implemented
        sleep(0.5) # Block keyboard input for a moment so that the user does not accidentally scroll up in the console TODO: This is not necessary after a GUI is implemented
        input("Press ENTER to exit...")
        break
    

import pygame as pygame
import random

pygame.init()  # Initialises pygame

DisplayWidth = 520
DisplayHeight = 520
Display = pygame.display.set_mode((DisplayWidth, DisplayHeight))  # Sets display width * height

Clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game")

Red = (255, 0, 0)  # Various colour definitions
Green = (0, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)
Black = (0, 0, 0)


def DrawGrid():
    for Column in range(DisplayWidth):
        for Row in range(DisplayHeight):
            pygame.draw.rect(Display, White, [Column * ObjectSize, Row * ObjectSize, ObjectSize, ObjectSize], 1)


def GameLoop():
    class Snake(object):
        def DrawSegment(self, SnakeList):
            for a in SnakeList:
                pygame.draw.rect(Display, Green, [a[0], a[1], ObjectSize, ObjectSize])


    class Apple(object):

        def GenAppleX(self):
            XApple = random.randrange(0, DisplayWidth, ObjectSize)
            return XApple

        def GenAppleY(self):
            YApple = random.randrange(0, DisplayHeight, ObjectSize)
            return YApple

        def DrawApple(self, XApple, YApple):
            pygame.draw.rect(Display, Red,
                             [XApple, YApple, ObjectSize, ObjectSize])  # [StartingX, StartingY, Width, Height]

    def DrawGrid():
        for Column in range(DisplayWidth):
            for Row in range(DisplayHeight):
                pygame.draw.rect(Display, White, [Column * ObjectSize, Row * ObjectSize, ObjectSize, ObjectSize], 1)

    def GameOverMessage(msg,  # Function adapted from: https://www.edureka.co/blog/snake-game-with-pygame/#score
                        Colour):
        Display.blit(pygame.font.SysFont("bahnschrift", 25).render(msg, True, Colour),
                     [DisplayWidth / 12, DisplayHeight / 3])

    def ScoreMessage(Score):  # Function adapted from: https://www.edureka.co/blog/snake-game-with-pygame/#score
        Display.blit(pygame.font.SysFont("bahnschrift", 25).render("Your Score: " + str(Score), True, Red),
                     [DisplayWidth / 3, DisplayHeight / 2])

    def HighScoreMessage(HighScore):  # Function adapted from: https://www.edureka.co/blog/snake-game-with-pygame/#score
        Display.blit(pygame.font.SysFont("bahnschrift", 25).render("Highest Score: " + str(HighScore), True, Red),
                     [DisplayWidth / 3.5, DisplayHeight / 1.5])

    Snake = Snake()  # Instantiates a new Snake
    Apple = Apple()  # Instantiates a new Apple
    XCurrentSnake = DisplayWidth / 2  # Starting X position for the snake head
    YCurrentSnake = DisplayHeight / 2  # Starting Y position for the snake head
    XChange = 0
    YChange = 0
    ObjectSize = 20  # Size of both the Snake and the Apple
    XApple = Apple.GenAppleX()  # Calls method for initial random X-Coord of the Apple
    YApple = Apple.GenAppleY()  # Calls method for initial random Y-Coord of the Apple
    SnakeList = []  # Declares the SnakeList
    SnakeLength = 1  # Length of the Snake is initially 1

    pygame.display.update()
    GameOver = False
    GameClosed = False
    while not GameOver:

        while GameClosed:
            Display.fill(Black)
            with open("SnakeGameHighScores.txt") as ReadFile:
                ReadLines = []
                for NextLine in ReadFile:
                    ReadLines.append(int(NextLine))
            ReadLines.sort()
            GameOverMessage("You Lost! Press P:Play Again or Q:Quit", Red)
            ScoreMessage(SnakeLength - 1)  # Final Score is final length of the Snake, minus the initial Snake segment
            HighScore = ReadLines[-1]
            HighScoreMessage(HighScore)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the x button in the top right of the window is pressed, quit the game
                    GameOver = True  # Quits the game
                    GameClosed = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:

                        GameOver = True
                        GameClosed = False
                    if event.key == pygame.K_p:

                        GameLoop()

        Display.fill(Black)  # Sets background colour to Blue
        for event in pygame.event.get():  # Constantly getting all events in the game
            if event.type == pygame.QUIT:  # If the x button in the top right of the window is pressed, quit the game
                GameOver = True  # Quits the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    XChange = - ObjectSize
                    YChange = 0
                elif event.key == pygame.K_RIGHT:
                    XChange = ObjectSize
                    YChange = 0
                elif event.key == pygame.K_UP:
                    YChange = - ObjectSize
                    XChange = 0
                elif event.key == pygame.K_DOWN:
                    YChange = ObjectSize
                    XChange = 0

        XCurrentSnake += XChange
        YCurrentSnake += YChange

        Apple.DrawApple(XApple, YApple)  # Draws the next Apple

        if XCurrentSnake < 0:  # Code to make the snake wrap-around when it goes off screen
            XCurrentSnake += DisplayWidth + ObjectSize
        elif YCurrentSnake < 0:
            YCurrentSnake += DisplayHeight + ObjectSize
        elif XCurrentSnake > DisplayWidth - ObjectSize:
            XCurrentSnake -= DisplayWidth + ObjectSize
        elif YCurrentSnake > DisplayWidth - ObjectSize:
            YCurrentSnake -= DisplayWidth + ObjectSize

        SnakeHead = [XCurrentSnake, YCurrentSnake]  # Creates a list to track the path of the Snake's Head
        SnakeList.append(SnakeHead)

        if len(SnakeList) > SnakeLength:  # Deletes the position of the "old" SnakeHead so that the "new" position of the SnakeHead can be recorded
            del SnakeList[0]

        for x in SnakeList[:-1]:  # Iterates through the positions of each segment of the Snake's body
            if x == SnakeHead:  # If the position of the Snake's Head equals any of the segment positions, Game Over
                with open("SnakeGameHighScores.txt", "a") as HighScoresFile:
                    HighScoresFile.write(str(SnakeLength - 1) + "\n")
                GameClosed = True

        Snake.DrawSegment(SnakeList)  # Calls the method to draw the snake

        if (XCurrentSnake == XApple) and (YCurrentSnake == YApple):  # Logic for when the Snake eats an Apple
            XApple = Apple.GenAppleX()  # Calls method to randomly generate X-Coord for the Apple
            YApple = Apple.GenAppleY()  # Calls method to randomly generate Y-Coord for the Apple
            GenApplePassed = False
            while not GenApplePassed:
                for x in SnakeList:  # Iterates through SnakeList checking if the current Apple will be spawned on a position currently occupied by the Snake if it will be, the position of the next Apple is re-generated. If it won't be, spawn the Apple
                    if x == [XApple, YApple]:
                        XApple = Apple.GenAppleX()
                        YApple = Apple.GenAppleY()
                    else:
                        GenApplePassed = True
            SnakeLength += 1  # Length of the Snake + 1 when the Snake eats an Apple

        pygame.display.update()  # Updates surface to display changes
        Clock.tick(7)  # Max frame-rate for the game

    pygame.quit()  # Quits pygame
    quit()


GameLoop()

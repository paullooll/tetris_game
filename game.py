import tkinter
import mysql.connector
from tkinter import *
from tkinter import Entry
from tkinter import messagebox
from PIL import ImageTk
import database  # Assuming you have a database.py file with connection details
from mysql.connector import Error
import pygame  # Make sure pygame is installed: pip install pygame
import random
import math
import sys

conn = database.conn  # Assuming you have a database.py file with connection details

# --- Tkinter Login Form Code ---

form = tkinter.Tk()
bg_image = ImageTk.PhotoImage(file="bg.png")  # Replace with your actual background image
bg_label = Label(form, image=bg_image)
bg_label.grid(row=0, column=0)
form_width = 800
form_height = 600
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()
x = (screen_width / 2) - (form_width / 2)
y = (screen_height / 2) - (form_height / 2)

form.geometry("%dx%d+%d+%d" % (form_width, form_height, x, y))
form.title("User Login")

txt_username = Entry(form, width=25, font=("Consolas Bold", 16))
txt_username.place(x=330, y=180, height=35)

txt_password = Entry(form, width=20, font=("Consolas Bold", 16), show='*')
txt_password.place(x=390, y=230, height=35)


def check_login():
    global current_user  # Make current_user global to access it in other functions
    username = txt_username.get()
    password = txt_password.get()
    try:
        if conn.is_connected():
            pst = conn.cursor()
            sqlquery = 'SELECT * FROM user WHERE username=%s AND password=%s'
            pst.execute(sqlquery, (username, password))
            rs = pst.fetchone()
            if (username == "" and password == ""):
                messagebox.showinfo("Error", "Username and Password is required")
                return
            elif rs is None:
                messagebox.showinfo("", "Username and Password is Incorrect")
            else:
                messagebox.showinfo("", "Login Successfully")
                current_user = username  # Store the logged-in username
                form.destroy()  # Close the login window
                start_tetris_game()  # Start the Tetris game
    except Error as e:
        messagebox.showinfo("", "Connection Failed")


btn_login = Button(form, width=24, font=("Consolas Bold", 16), text="Login", command=check_login)
btn_login.place(x=250, y=300, height=50)
btn_login.configure(bg='green', fg='white')


# --- Registration Page Code ---

def open_registration_window():
    registration_window = Toplevel(form)
    registration_window.title("User Registration")

    # --- Copied design from login form ---

    bg_image_reg = ImageTk.PhotoImage(file="bg.png")  # Replace with your actual background image
    bg_label_reg = Label(registration_window, image=bg_image_reg)  # Use registration_window as parent
    bg_label_reg.grid(row=0, column=0)
    registration_window.geometry("%dx%d+%d+%d" % (form_width, form_height, x, y))  # Same size and position

    # --- Keep a reference to the image to prevent it from being garbage collected ---
    registration_window.bg_image_reg = bg_image_reg
    # --- End of correction ---

    # ... (Add username and password entry fields similar to login form) ...
    txt_username_reg = Entry(registration_window, width=25,
                             font=("Consolas Bold", 16))  # Use registration_window as parent
    txt_username_reg.place(x=330, y=180, height=35)

    txt_password_reg = Entry(registration_window, width=20, font=("Consolas Bold", 16),
                             show='*')  # Use registration_window as parent
    txt_password_reg.place(x=390, y=230, height=35)
    def register_user():
        username = txt_username_reg.get()  # Assuming you named the entry fields txt_username_reg and txt_password_reg
        password = txt_password_reg.get()

        try:
            if conn.is_connected():
                if (username == "" and password == ""):
                    messagebox.showinfo("Error", "Username and Password is required")
                    return
                else:
                    cursor = conn.cursor()
                    query = "INSERT INTO user (username, password) VALUES (%s, %s)"
                    cursor.execute(query, (username, password))
                    conn.commit()
                    messagebox.showinfo("", "Registration Successful")
                    registration_window.destroy()  # Close registration window
                    form.deiconify()  # Show the login window again
        except Error as e:
            messagebox.showinfo("", f"Registration Failed: {e}")

    btn_register = Button(registration_window, width=24, font=("Consolas Bold", 16), text="Register",
                          command=register_user)
    btn_register.place(x=250, y=300, height=50)  # Adjust position as needed
    btn_register.configure(bg='green', fg='white')


# --- Add the "New user? register here" text ---

lbl_register = Label(form, text="New user? register here", font=("Consolas Bold", 12), fg="blue", cursor="hand2")
lbl_register.place(x=280, y=360)  # Adjust position as needed
lbl_register.bind("<Button-1>", lambda e: [form.withdraw(), open_registration_window()])  # Hide login window and open registration

# --- Tetris Game Code ---

def start_tetris_game():
    global current_user

    pygame.init()
    pygame.font.init()

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    pieceNames = ('I', 'O', 'T', 'S', 'Z', 'J', 'L')

    STARTING_LEVEL = 0

    MOVE_PERIOD_INIT = 4

    CLEAR_ANI_PERIOD = 4
    SINE_ANI_PERIOD = 120

    SB_FONT_SIZE = 29
    FONT_SIZE_SMALL = 17
    PAUSE_FONT_SIZE = 66
    GAMEOVER_FONT_SIZE = 66
    TITLE_FONT_SIZE = 70
    VERSION_FONT_SIZE = 20

    fontSB = pygame.font.SysFont('agencyfb', SB_FONT_SIZE)
    fontSmall = pygame.font.SysFont('agencyfb', FONT_SIZE_SMALL)
    fontPAUSE = pygame.font.SysFont('agencyfb', PAUSE_FONT_SIZE)
    fontGAMEOVER = pygame.font.SysFont('agencyfb', GAMEOVER_FONT_SIZE)
    fontTitle = pygame.font.SysFont('agencyfb', TITLE_FONT_SIZE)
    fontVersion = pygame.font.SysFont('agencyfb', VERSION_FONT_SIZE)

    ROW = (0)
    COL = (1)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GRAY = (80, 80, 80)
    GRAY = (110, 110, 110)
    LIGHT_GRAY = (150, 150, 150)
    BORDER_COLOR = GRAY
    NUM_COLOR = WHITE
    TEXT_COLOR = GRAY

    blockColors = {
        'I': (19, 232, 232),
        'O': (236, 236, 14),
        'T': (126, 5, 126),
        'S': (0, 128, 0),
        'Z': (236, 14, 14),
        'J': (30, 30, 201),
        'L': (240, 110, 2)}

    pieceDefs = {
        'I': ((1, 0), (1, 1), (1, 2), (1, 3)),
        'O': ((0, 1), (0, 2), (1, 1), (1, 2)),
        'T': ((0, 1), (1, 0), (1, 1), (1, 2)),
        'S': ((0, 1), (0, 2), (1, 0), (1, 1)),
        'Z': ((0, 0), (0, 1), (1, 1), (1, 2)),
        'J': ((0, 0), (1, 0), (1, 1), (1, 2)),
        'L': ((0, 2), (1, 0), (1, 1), (1, 2))}

    directions = {
        'down': (1, 0),
        'right': (0, 1),
        'left': (0, -1),
        'downRight': (1, 1),
        'downLeft': (1, -1),
        'noMove': (0, 0)}

    levelSpeeds = (48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)

    baseLinePoints = (0, 40, 100, 300, 1200)

    class GameKeyInput:

        def __init__(self):
            self.xNav = self.KeyName('idle', False)
            self.down = self.KeyName('idle', False)
            self.rotate = self.KeyName('idle', False)
            self.cRotate = self.KeyName('idle', False)
            self.enter = self.KeyName('idle', False)
            self.pause = self.KeyName('idle', False)
            self.restart = self.KeyName('idle', False)

        class KeyName:

            def __init__(self, initStatus, initTrig):
                self.status = initStatus
                self.trig = initTrig

    class GameClock:

        def __init__(self):
            self.frameTick = 0
            self.pausedMoment = 0
            self.move = self.TimingType(MOVE_PERIOD_INIT)
            self.fall = self.TimingType(levelSpeeds[STARTING_LEVEL])
            self.clearAniStart = 0

        class TimingType:

            def __init__(self, framePeriod):
                self.preFrame = 0
                self.framePeriod = framePeriod

            def check(self, frameTick):
                if frameTick - self.preFrame > self.framePeriod - 1:
                    self.preFrame = frameTick
                    return True
                return False

        def pause(self):
            self.pausedMoment = self.frameTick

        def unpause(self):
            self.frameTick = self.pausedMoment

        def restart(self):
            self.frameTick = 0
            self.pausedMoment = 0
            self.move = self.TimingType(MOVE_PERIOD_INIT)
            self.fall = self.TimingType(levelSpeeds[STARTING_LEVEL])
            self.clearAniStart = 0

        def update(self):
            self.frameTick = self.frameTick + 1

    class MainBoard:

        def __init__(self, blockSize, xPos, yPos, colNum, rowNum, boardLineWidth, blockLineWidth, scoreBoardWidth):

            self.blockSize = blockSize
            self.xPos = xPos
            self.yPos = yPos
            self.colNum = colNum
            self.rowNum = rowNum
            self.boardLineWidth = boardLineWidth
            self.blockLineWidth = blockLineWidth
            self.scoreBoardWidth = scoreBoardWidth

            self.blockMat = [['empty'] * colNum for i in range(rowNum)]

            self.piece = MovingPiece(colNum, rowNum, 'uncreated')

            self.lineClearStatus = 'idle'
            self.clearedLines = [-1, -1, -1, -1]

            self.gameStatus = 'firstStart'
            self.gamePause = False
            self.nextPieces = ['I', 'I']

            self.score = 0
            self.level = STARTING_LEVEL
            self.lines = 0
            self.current_user = current_user

        def restart(self):
            self.update_score_in_database()  # Update score before restarting
            self.blockMat = [['empty'] * self.colNum for i in range(self.rowNum)]
            self.piece = MovingPiece(self.colNum, self.rowNum, 'uncreated')
            self.lineClearStatus = 'idle'
            self.clearedLines = [-1, -1, -1, -1]
            gameClock.fall.preFrame = gameClock.frameTick
            self.generateNextTwoPieces()
            self.gameStatus = 'running'
            self.gamePause = False
            self.score = 0
            self.level = STARTING_LEVEL
            self.lines = 0
            gameClock.restart()

        def erase_BLOCK(self, xRef, yRef, row, col):
            pygame.draw.rect(gameDisplay, BLACK,
                             [xRef + (col * self.blockSize), yRef + (row * self.blockSize), self.blockSize,
                              self.blockSize], 0)

        def draw_BLOCK(self, xRef, yRef, row, col, color):
            pygame.draw.rect(gameDisplay, BLACK,
                             [xRef + (col * self.blockSize), yRef + (row * self.blockSize), self.blockSize,
                              self.blockLineWidth], 0)
            pygame.draw.rect(gameDisplay, BLACK, [xRef + (col * self.blockSize) + self.blockSize - self.blockLineWidth,
                                                  yRef + (row * self.blockSize), self.blockLineWidth, self.blockSize],
                             0)
            pygame.draw.rect(gameDisplay, BLACK,
                             [xRef + (col * self.blockSize), yRef + (row * self.blockSize), self.blockLineWidth,
                              self.blockSize], 0)
            pygame.draw.rect(gameDisplay, BLACK, [xRef + (col * self.blockSize),
                                                  yRef + (row * self.blockSize) + self.blockSize - self.blockLineWidth,
                                                  self.blockSize, self.blockLineWidth], 0)
            pygame.draw.rect(gameDisplay, color, [xRef + (col * self.blockSize) + self.blockLineWidth,
                                                  yRef + (row * self.blockSize) + self.blockLineWidth,
                                                  self.blockSize - (2 * self.blockLineWidth),
                                                  self.blockSize - (2 * self.blockLineWidth)], 0)

        def draw_GAMEBOARD_BORDER(self):
            pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos - self.boardLineWidth - self.blockLineWidth,
                                                         self.yPos - self.boardLineWidth - self.blockLineWidth,
                                                         (self.blockSize * self.colNum) + (2 * self.boardLineWidth) + (
                                                                     2 * self.blockLineWidth), self.boardLineWidth], 0)
            pygame.draw.rect(gameDisplay, BORDER_COLOR,
                             [self.xPos + (self.blockSize * self.colNum) + self.blockLineWidth,
                              self.yPos - self.boardLineWidth - self.blockLineWidth, self.boardLineWidth,
                              (self.blockSize * self.rowNum) + (2 * self.boardLineWidth) + (2 * self.blockLineWidth)],
                             0)
            pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos - self.boardLineWidth - self.blockLineWidth,
                                                         self.yPos - self.boardLineWidth - self.blockLineWidth,
                                                         self.boardLineWidth,
                                                         (self.blockSize * self.rowNum) + (2 * self.boardLineWidth) + (
                                                                     2 * self.blockLineWidth)], 0)
            pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos - self.boardLineWidth - self.blockLineWidth,
                                                         self.yPos + (
                                                                     self.blockSize * self.rowNum) + self.blockLineWidth,
                                                         (self.blockSize * self.colNum) + (2 * self.boardLineWidth) + (
                                                                     2 * self.blockLineWidth), self.boardLineWidth], 0)

        def draw_GAMEBOARD_CONTENT(self):
            if self.gameStatus == 'firstStart':
                titleText = fontTitle.render('TETRIS', False, WHITE)
                gameDisplay.blit(titleText, (self.xPos + +0.1 * self.blockSize, self.yPos + 8 * self.blockSize))
            else:
                for row in range(0, self.rowNum):
                    for col in range(0, self.colNum):
                        if self.blockMat[row][col] == 'empty':
                            self.erase_BLOCK(self.xPos, self.yPos, row, col)
                        else:
                            self.draw_BLOCK(self.xPos, self.yPos, row, col, blockColors[self.blockMat[row][col]])

                if self.piece.status == 'moving':
                    for i in range(0, 4):
                        self.draw_BLOCK(self.xPos, self.yPos, self.piece.blocks[i].currentPos.row,
                                        self.piece.blocks[i].currentPos.col, blockColors[self.piece.type])

                if self.gamePause == True:
                    pygame.draw.rect(gameDisplay, DARK_GRAY,
                                     [self.xPos + 1 * self.blockSize, self.yPos + 8 * self.blockSize,
                                      8 * self.blockSize, 4 * self.blockSize], 0)
                    pauseText = fontPAUSE.render('PAUSE', False, BLACK)
                    gameDisplay.blit(pauseText, (self.xPos + +1.65 * self.blockSize, self.yPos + 8 * self.blockSize))

                if self.gameStatus == 'gameOver':
                    pygame.draw.rect(gameDisplay, LIGHT_GRAY,
                                     [self.xPos + 1 * self.blockSize, self.yPos + 8 * self.blockSize,
                                      8 * self.blockSize, 8 * self.blockSize], 0)
                    gameOverText0 = fontGAMEOVER.render('GAME', False, BLACK)
                    gameDisplay.blit(gameOverText0, (self.xPos + +2.2 * self.blockSize, self.yPos + 8 * self.blockSize))
                    gameOverText1 = fontGAMEOVER.render('OVER', False, BLACK)
                    gameDisplay.blit(gameOverText1,
                                     (self.xPos + +2.35 * self.blockSize, self.yPos + 12 * self.blockSize))

        def draw_SCOREBOARD_BORDER(self):
            pygame.draw.rect(gameDisplay, BORDER_COLOR,
                             [self.xPos + (self.blockSize * self.colNum) + self.blockLineWidth,
                              self.yPos - self.boardLineWidth - self.blockLineWidth,
                              self.scoreBoardWidth + self.boardLineWidth, self.boardLineWidth], 0)
            pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos + (
                    self.blockSize * self.colNum) + self.boardLineWidth + self.blockLineWidth + self.scoreBoardWidth,
                                                         self.yPos - self.boardLineWidth - self.blockLineWidth,
                                                         self.boardLineWidth,
                                                         # Removed the extra parentheses and calculation here
                                                         (self.blockSize * self.rowNum) + (2 * self.boardLineWidth) + (
                                                                 2 * self.blockLineWidth)], 0)
            pygame.draw.rect(gameDisplay, BORDER_COLOR,
                             [self.xPos + (self.blockSize * self.colNum) + self.blockLineWidth,
                              self.yPos + (self.blockSize * self.rowNum) + self.blockLineWidth,
                              self.scoreBoardWidth + self.boardLineWidth, self.boardLineWidth], 0)

        def draw_SCOREBOARD_CONTENT(self):

            xPosRef = self.xPos + (self.blockSize * self.colNum) + self.boardLineWidth + self.blockLineWidth
            yPosRef = self.yPos
            yLastBlock = self.yPos + (self.blockSize * self.rowNum)

            if self.gameStatus == 'running':
                nextPieceText = fontSB.render('next:', False, TEXT_COLOR)
                gameDisplay.blit(nextPieceText, (xPosRef + self.blockSize, self.yPos))

                blocks = [[0, 0], [0, 0], [0, 0], [0, 0]]
                origin = [0, 0]
                for i in range(0, 4):
                    blocks[i][ROW] = origin[ROW] + pieceDefs[self.nextPieces[1]][i][ROW]
                    blocks[i][COL] = origin[COL] + pieceDefs[self.nextPieces[1]][i][COL]

                    if self.nextPieces[1] == 'O':
                        self.draw_BLOCK(xPosRef + 0.5 * self.blockSize, yPosRef + 2.25 * self.blockSize, blocks[i][ROW],
                                        blocks[i][COL], blockColors[self.nextPieces[1]])
                    elif self.nextPieces[1] == 'I':
                        self.draw_BLOCK(xPosRef + 0.5 * self.blockSize, yPosRef + 1.65 * self.blockSize, blocks[i][ROW],
                                        blocks[i][COL], blockColors[self.nextPieces[1]])
                    else:
                        self.draw_BLOCK(xPosRef + 1 * self.blockSize, yPosRef + 2.25 * self.blockSize, blocks[i][ROW],
                                        blocks[i][COL], blockColors[self.nextPieces[1]])

                if self.gamePause == False:
                    pauseText = fontSmall.render('P -> pause', False, WHITE)
                    gameDisplay.blit(pauseText, (xPosRef + 1 * self.blockSize, yLastBlock - 15 * self.blockSize))
                else:
                    unpauseText = fontSmall.render('P -> unpause', False, self.whiteSineAnimation())
                    gameDisplay.blit(unpauseText, (xPosRef + 1 * self.blockSize, yLastBlock - 15 * self.blockSize))

                restartText = fontSmall.render('R -> restart', False, WHITE)
                gameDisplay.blit(restartText, (xPosRef + 1 * self.blockSize, yLastBlock - 14 * self.blockSize))

            else:

                yBlockRef = 0.3
                text0 = fontSB.render('press', False, self.whiteSineAnimation())
                gameDisplay.blit(text0, (xPosRef + self.blockSize, self.yPos + yBlockRef * self.blockSize))
                text1 = fontSB.render('enter', False, self.whiteSineAnimation())
                gameDisplay.blit(text1, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 1.5) * self.blockSize))
                text2 = fontSB.render('to', False, self.whiteSineAnimation())
                gameDisplay.blit(text2, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 3) * self.blockSize))
                if self.gameStatus == 'firstStart':
                    text3 = fontSB.render('start', False, self.whiteSineAnimation())
                    gameDisplay.blit(text3, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 4.5) * self.blockSize))
                else:
                    text3 = fontSB.render('restart', False, self.whiteSineAnimation())
                    gameDisplay.blit(text3, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 4.5) * self.blockSize))

            pygame.draw.rect(gameDisplay, BORDER_COLOR,
                             [xPosRef, yLastBlock - 12.5 * self.blockSize, self.scoreBoardWidth, self.boardLineWidth],
                             0)

            scoreText = fontSB.render('score:', False, TEXT_COLOR)
            gameDisplay.blit(scoreText, (xPosRef + self.blockSize, yLastBlock - 12 * self.blockSize))
            scoreNumText = fontSB.render(str(self.score), False, NUM_COLOR)
            gameDisplay.blit(scoreNumText, (xPosRef + self.blockSize, yLastBlock - 10 * self.blockSize))

            levelText = fontSB.render('level:', False, TEXT_COLOR)
            gameDisplay.blit(levelText, (xPosRef + self.blockSize, yLastBlock - 8 * self.blockSize))
            levelNumText = fontSB.render(str(self.level), False, NUM_COLOR)
            gameDisplay.blit(levelNumText, (xPosRef + self.blockSize, yLastBlock - 6 * self.blockSize))

            linesText = fontSB.render('lines:', False, TEXT_COLOR)
            gameDisplay.blit(linesText, (xPosRef + self.blockSize, yLastBlock - 4 * self.blockSize))
            linesNumText = fontSB.render(str(self.lines), False, NUM_COLOR)
            gameDisplay.blit(linesNumText, (xPosRef + self.blockSize, yLastBlock - 2 * self.blockSize))

        def whiteSineAnimation(self):
            sine = math.floor(255 * math.fabs(math.sin(2 * math.pi * (gameClock.frameTick / (SINE_ANI_PERIOD * 2)))))
            sineEffect = [sine, sine, sine]
            return sineEffect

        def lineClearAnimation(self):
            clearAniStage = math.floor((gameClock.frameTick - gameClock.clearAniStart) / CLEAR_ANI_PERIOD)
            halfCol = math.floor(self.colNum / 2)
            if clearAniStage < halfCol:
                for i in range(0, 4):
                    if self.clearedLines[i] >= 0:
                        self.blockMat[self.clearedLines[i]][(halfCol) + clearAniStage] = 'empty'
                        self.blockMat[self.clearedLines[i]][(halfCol - 1) - clearAniStage] = 'empty'
            else:
                self.lineClearStatus = 'cleared'

        def dropFreeBlocks(self):
            for cLIndex in range(0, 4):
                if self.clearedLines[cLIndex] >= 0:
                    for rowIndex in range(self.clearedLines[cLIndex], 0, -1):
                        for colIndex in range(0, self.colNum):
                            self.blockMat[rowIndex + cLIndex][colIndex] = self.blockMat[rowIndex + cLIndex - 1][
                                colIndex]
                    for colIndex in range(0, self.colNum):
                        self.blockMat[0][colIndex] = 'empty'

        def getCompleteLines(self):
            clearedLines = [-1, -1, -1, -1]
            cLIndex = -1
            rowIndex = self.rowNum - 1
            while rowIndex >= 0:
                for colIndex in range(0, self.colNum):
                    if self.blockMat[rowIndex][colIndex] == 'empty':
                        rowIndex = rowIndex - 1
                        break
                    if colIndex == self.colNum - 1:
                        cLIndex = cLIndex + 1
                        clearedLines[cLIndex] = rowIndex
                        rowIndex = rowIndex - 1
            if cLIndex >= 0:
                gameClock.clearAniStart = gameClock.frameTick
                self.lineClearStatus = 'clearRunning'
            else:
                self.prepareNextSpawn()
            return clearedLines

        def prepareNextSpawn(self):
            self.generateNextPiece()
            self.lineClearStatus = 'idle'
            self.piece.status = 'uncreated'

        def generateNextTwoPieces(self):
            self.nextPieces[0] = pieceNames[random.randint(0, 6)]
            self.nextPieces[1] = pieceNames[random.randint(0, 6)]
            self.piece.type = self.nextPieces[0]

        def generateNextPiece(self):
            self.nextPieces[0] = self.nextPieces[1]
            self.nextPieces[1] = pieceNames[random.randint(0, 6)]
            self.piece.type = self.nextPieces[0]

        def checkAndApplyGameOver(self):
            if self.piece.gameOverCondition == True:
                self.gameStatus = 'gameOver'
                for i in range(0, 4):
                    if self.piece.blocks[i].currentPos.row >= 0 and self.piece.blocks[i].currentPos.col >= 0:
                        self.blockMat[self.piece.blocks[i].currentPos.row][
                            self.piece.blocks[i].currentPos.col] = self.piece.type

        def updateScores(self):
            clearedLinesNum = 0
            for i in range(0, 4):
                if self.clearedLines[i] > -1:
                    clearedLinesNum = clearedLinesNum + 1
            self.score = self.score + (self.level + 1) * baseLinePoints[clearedLinesNum] + self.piece.dropScore
            if self.score > 999999:
                self.score = 999999
            self.lines = self.lines + clearedLinesNum
            self.level = STARTING_LEVEL + math.floor(self.lines / 10)
            if self.level > 99:
                self.level = 99

        def updateSpeed(self):
            if self.level < 29:
                gameClock.fall.framePeriod = levelSpeeds[self.level]
            else:
                gameClock.fall.framePeriod = 1
            if gameClock.fall.framePeriod < 4:
                gameClock.fall.framePeriod = gameClock.move.framePeriod

        def gameAction(self):
            if self.gameStatus == 'firstStart':
                if key.enter.status == 'pressed':
                    self.restart()
            elif self.gameStatus == 'running':
                if key.restart.trig == True:
                    self.restart()
                    key.restart.trig = False
                if self.gamePause == False:
                    self.piece.move(self.blockMat)
                    self.checkAndApplyGameOver()
                    if key.pause.trig == True:
                        gameClock.pause()
                        self.gamePause = True
                        key.pause.trig = False
                    if self.gameStatus != 'gameOver':
                        if self.piece.status == 'moving':
                            if key.rotate.trig == True:
                                self.piece.rotate('CW')
                                key.rotate.trig = False
                            if key.cRotate.trig == True:
                                self.piece.rotate('cCW')
                                key.cRotate.trig = False
                        elif self.piece.status == 'collided':
                            if self.lineClearStatus == 'idle':
                                for i in range(0, 4):
                                    self.blockMat[self.piece.blocks[i].currentPos.row][
                                        self.piece.blocks[i].currentPos.col] = self.piece.type
                                self.clearedLines = self.getCompleteLines()
                                self.updateScores()
                                self.updateSpeed()
                            elif self.lineClearStatus == 'clearRunning':
                                self.lineClearAnimation()
                            else:  # 'clearFin'
                                self.dropFreeBlocks()
                                self.prepareNextSpawn()
                else:  # self.gamePause = False
                    if key.pause.trig == True:
                        gameClock.unpause()
                        self.gamePause = False
                        key.pause.trig = False
            else:  # 'gameOver'
                if key.enter.status == 'pressed':
                    self.restart()

        def draw_LEFT_PANEL(self):
            if self.gameStatus == 'running':
                xPosRef = self.xPos - self.scoreBoardWidth * 3.5  # Moved further left (adjust the multiplier as needed)
                yPosRef = self.yPos
                try:
                    if conn.is_connected():
                        cursor = conn.cursor()

                        # Fetch user's score
                        query = "SELECT score FROM user WHERE username = %s"
                        cursor.execute(query, (self.current_user,))
                        user_score = cursor.fetchone()[0]

                        # Display user's name and score
                        font_user_score = pygame.font.SysFont('agencyfb', SB_FONT_SIZE * 15)  # 3 times bigger font
                        name_text = fontSB.render(f"{self.current_user}: {user_score}", False, TEXT_COLOR)
                        gameDisplay.blit(name_text, (xPosRef + self.blockSize, yPosRef + 1 * self.blockSize))

                        # Fetch leaderboard data (top 5 scores)
                        query = "SELECT username, score FROM user ORDER BY score DESC LIMIT 5"
                        cursor.execute(query)
                        leaderboard_data = cursor.fetchall()

                        # Display leaderboard
                        font_leaderboard = pygame.font.SysFont('agencyfb', SB_FONT_SIZE * 1)  # 2 times bigger font
                        leaderboard_text = fontSB.render("Leaderboard:", False, TEXT_COLOR)
                        gameDisplay.blit(leaderboard_text, (xPosRef + self.blockSize, yPosRef + 4 * self.blockSize))

                        y_offset = 6
                        font_leaderboard_entry = pygame.font.SysFont('agencyfb',
                                                                     FONT_SIZE_SMALL * 2)  # 3 times bigger font
                        for i, (username, score) in enumerate(leaderboard_data):
                            entry_text = font_leaderboard_entry.render(f"{i + 1}. {username}: {score}", False, WHITE)
                            gameDisplay.blit(entry_text, (xPosRef + self.blockSize, yPosRef + (
                                        y_offset + i * 2) * self.blockSize))  # Adjusted spacing

                except Error as e:
                    print(e)

        def update_score_in_database(self):
            try:
                if conn.is_connected():
                    cursor = conn.cursor()

                    # Fetch user's previous score
                    query = "SELECT score FROM user WHERE username = %s"
                    cursor.execute(query, (self.current_user,))
                    previous_score = cursor.fetchone()[0]

                    # Update score if the new score is higher
                    if self.score > previous_score:
                        query = "UPDATE user SET score = %s WHERE username = %s"
                        cursor.execute(query, (self.score, self.current_user))
                        conn.commit()
            except Error as e:
                print(e)

        def draw(self):
            self.draw_GAMEBOARD_BORDER()
            self.draw_SCOREBOARD_BORDER()
            self.draw_GAMEBOARD_CONTENT()
            self.draw_SCOREBOARD_CONTENT()
            self.draw_LEFT_PANEL()  # Draw the left panel

    class MovingPiece:

        def __init__(self, colNum, rowNum, status):

            self.colNum = colNum
            self.rowNum = rowNum

            self.blockMat = [['empty'] * colNum for i in range(rowNum)]

            self.blocks = []
            for i in range(0, 4):
                self.blocks.append(MovingBlock())

            self.currentDef = [[0] * 2 for i in range(4)]
            self.status = status
            self.type = 'I'

            self.gameOverCondition = False

            self.dropScore = 0
            self.lastMoveType = 'noMove'

        def applyNextMove(self):
            for i in range(0, 4):
                self.blocks[i].currentPos.col = self.blocks[i].nextPos.col
                self.blocks[i].currentPos.row = self.blocks[i].nextPos.row

        def applyFastMove(self):

            if gameClock.move.check(gameClock.frameTick) == True:
                if self.lastMoveType == 'downRight' or self.lastMoveType == 'downLeft' or self.lastMoveType == 'down':
                    self.dropScore = self.dropScore + 1
                self.applyNextMove()

        def slowMoveAction(self):

            if gameClock.fall.check(gameClock.frameTick) == True:
                if self.movCollisionCheck('down') == True:
                    self.createNextMove('noMove')
                    self.status = 'collided'
                else:
                    self.createNextMove('down')
                    self.applyNextMove()

        def createNextMove(self, moveType):
            self.lastMoveType = moveType
            for i in range(0, 4):
                self.blocks[i].nextPos.row = self.blocks[i].currentPos.row + directions[moveType][ROW]
                self.blocks[i].nextPos.col = self.blocks[i].currentPos.col + directions[moveType][COL]  # Corrected line

        def movCollisionCheck_BLOCK(self, dirType, blockIndex):
            if dirType == 'down':
                if (self.blocks[blockIndex].currentPos.row + 1 > self.rowNum - 1) or \
                        self.blockMat[self.blocks[blockIndex].currentPos.row + directions[dirType][ROW]][
                            self.blocks[blockIndex].currentPos.col + directions[dirType][COL]] != 'empty':
                    return True
            else:
                if (((directions[dirType][COL]) * (
                        self.blocks[blockIndex].currentPos.col + directions[dirType][COL])) > (
                        ((self.colNum - 1) + (directions[dirType][COL]) * (self.colNum - 1)) / 2) or
                        self.blockMat[self.blocks[blockIndex].currentPos.row + directions[dirType][ROW]][
                            self.blocks[blockIndex].currentPos.col + directions[dirType][COL]] != 'empty'):
                    return True
            return False

        def movCollisionCheck(self, dirType):
            for i in range(0, 4):
                if self.movCollisionCheck_BLOCK(dirType, i) == True:
                    return True
            return False

        def rotCollisionCheck_BLOCK(self, blockCoor):
            if (blockCoor[ROW] > self.rowNum - 1 or blockCoor[ROW] < 0 or blockCoor[COL] > self.colNum - 1 or blockCoor[
                COL] < 0 or self.blockMat[blockCoor[ROW]][blockCoor[COL]] != 'empty'):
                return True
            return False

        def rotCollisionCheck(self, blockCoorList):
            for i in range(0, 4):
                if self.rotCollisionCheck_BLOCK(blockCoorList[i]) == True:
                    return True
            return False

        def spawnCollisionCheck(self, origin):

            for i in range(0, 4):
                spawnRow = origin[ROW] + pieceDefs[self.type][i][ROW]
                spawnCol = origin[COL] + pieceDefs[self.type][i][COL]
                if spawnRow >= 0 and spawnCol >= 0:
                    if self.blockMat[spawnRow][spawnCol] != 'empty':
                        return True
            return False

        def findOrigin(self):

            origin = [0, 0]
            origin[ROW] = self.blocks[0].currentPos.row - self.currentDef[0][ROW]
            origin[COL] = self.blocks[0].currentPos.col - self.currentDef[0][COL]
            return origin

        def rotate(self, rotationType):

            if self.type != 'O':
                tempBlocks = [[0] * 2 for i in range(4)]
                origin = self.findOrigin()

                if self.type == 'I':
                    pieceMatSize = 4
                else:
                    pieceMatSize = 3

                for i in range(0, 4):
                    if rotationType == 'CW':
                        tempBlocks[i][ROW] = origin[ROW] + self.currentDef[i][COL]
                        tempBlocks[i][COL] = origin[COL] + (pieceMatSize - 1) - self.currentDef[i][ROW]
                    else:
                        tempBlocks[i][COL] = origin[COL] + self.currentDef[i][ROW]
                        tempBlocks[i][ROW] = origin[ROW] + (pieceMatSize - 1) - self.currentDef[i][COL]

                if self.rotCollisionCheck(tempBlocks) == False:
                    for i in range(0, 4):
                        self.blocks[i].currentPos.row = tempBlocks[i][ROW]
                        self.blocks[i].currentPos.col = tempBlocks[i][COL]
                        self.currentDef[i][ROW] = self.blocks[i].currentPos.row - origin[ROW]
                        self.currentDef[i][COL] = self.blocks[i].currentPos.col - origin[COL]

        def spawn(self):

            self.dropScore = 0

            origin = [0, 3]

            for i in range(0, 4):
                self.currentDef[i] = list(pieceDefs[self.type][i])

            spawnTry = 0
            while spawnTry < 2:
                if self.spawnCollisionCheck(origin) == False:
                    break
                else:
                    spawnTry = spawnTry + 1
                    origin[ROW] = origin[ROW] - 1
                    self.gameOverCondition = True
                    self.status = 'collided'

            for i in range(0, 4):
                spawnRow = origin[ROW] + pieceDefs[self.type][i][ROW]
                spawnCol = origin[COL] + pieceDefs[self.type][i][COL]
                self.blocks[i].currentPos.row = spawnRow
                self.blocks[i].currentPos.col = spawnCol

        def move(self, lastBlockMat):

            if self.status == 'uncreated':
                self.status = 'moving'
                self.blockMat = lastBlockMat
                self.spawn()

            elif self.status == 'moving':

                if key.down.status == 'pressed':
                    if key.xNav.status == 'right':
                        if self.movCollisionCheck('down') == True:
                            self.createNextMove('noMove')
                            self.status = 'collided'
                        elif self.movCollisionCheck('downRight') == True:
                            self.createNextMove('down')
                        else:
                            self.createNextMove('downRight')

                    elif key.xNav.status == 'left':
                        if self.movCollisionCheck('down') == True:
                            self.createNextMove('noMove')
                            self.status = 'collided'
                        elif self.movCollisionCheck('downLeft') == True:
                            self.createNextMove('down')
                        else:
                            self.createNextMove('downLeft')

                    else:  # 'idle'
                        if self.movCollisionCheck('down') == True:
                            self.createNextMove('noMove')
                            self.status = 'collided'
                        else:
                            self.createNextMove('down')

                    self.applyFastMove()

                elif key.down.status == 'idle':
                    if key.xNav.status == 'right':
                        if self.movCollisionCheck('right') == True:
                            self.createNextMove('noMove')
                        else:
                            self.createNextMove('right')
                    elif key.xNav.status == 'left':
                        if self.movCollisionCheck('left') == True:
                            self.createNextMove('noMove')
                        else:
                            self.createNextMove('left')
                    else:
                        self.createNextMove('noMove')

                    self.applyFastMove()

                    self.slowMoveAction()

                else:  # 'released'
                    key.down.status = 'idle'

    class MovingBlock:

        def __init__(self):
            self.currentPos = self.CurrentPosClass(0, 0)
            self.nextPos = self.NextPosClass(0, 0)

        class CurrentPosClass:

            def __init__(self, row, col):
                self.row = row
                self.col = col

        class NextPosClass:

            def __init__(self, row, col):
                self.row = row
                self.col = col

    def gameLoop():

        blockSize = 20
        boardColNum = 10
        boardRowNum = 20
        boardLineWidth = 10
        blockLineWidth = 1
        scoreBoardWidth = blockSize * (boardColNum // 2)
        boardPosX = DISPLAY_WIDTH * 0.5  # Adjusted to move the game board to the right
        boardPosY = DISPLAY_HEIGHT * 0.15

        mainBoard = MainBoard(blockSize, boardPosX, boardPosY, boardColNum, boardRowNum, boardLineWidth, blockLineWidth,
                              scoreBoardWidth)

        xChange = 0

        gameExit = False

        while not gameExit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        xChange += -1
                    if event.key == pygame.K_RIGHT:
                        xChange += 1
                    if event.key == pygame.K_DOWN:
                        key.down.status = 'pressed'
                    if event.key == pygame.K_UP:
                        if key.rotate.status == 'idle':
                            key.rotate.trig = True
                            key.rotate.status = 'pressed'
                    if event.key == pygame.K_z:
                        if key.cRotate.status == 'idle':
                            key.cRotate.trig = True
                            key.cRotate.status = 'pressed'
                    if event.key == pygame.K_p:
                        if key.pause.status == 'idle':
                            key.pause.trig = True
                            key.pause.status = 'pressed'
                    if event.key == pygame.K_r:
                        if key.restart.status == 'idle':
                            key.restart.trig = True
                            key.restart.status = 'pressed'
                    if event.key == pygame.K_RETURN:
                        key.enter.status = 'pressed'

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        xChange += 1
                    if event.key == pygame.K_RIGHT:
                        xChange += -1
                    if event.key == pygame.K_DOWN:
                        key.down.status = 'released'
                    if event.key == pygame.K_UP:
                        key.rotate.status = 'idle'
                    if event.key == pygame.K_z:
                        key.cRotate.status = 'idle'
                    if event.key == pygame.K_p:
                        key.pause.status = 'idle'
                    if event.key == pygame.K_r:
                        key.restart.status = 'idle'
                    if event.key == pygame.K_RETURN:
                        key.enter.status = 'idle'

                if xChange > 0:
                    key.xNav.status = 'right'
                elif xChange < 0:
                    key.xNav.status = 'left'
                else:
                    key.xNav.status = 'idle'

            gameDisplay.fill(BLACK)

            mainBoard.gameAction()
            mainBoard.draw()
            gameClock.update()

            pygame.display.update()
            clock.tick(60)

    key = GameKeyInput()
    gameClock = GameClock()
    gameLoop()
    pygame.quit()
    sys.exit()

form.mainloop()
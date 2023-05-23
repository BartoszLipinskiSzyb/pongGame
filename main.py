import json
import os.path
import random

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
import sys
import pygame

class constants():
    colors = {
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "black": (0, 0, 0)
    }

    gameTitle = "Pong"

class graphics():
    def __init__(self, context):
        self.context = context

        pygame.display.set_caption(constants.gameTitle)

        self.screenDimension = (self.context.options.fieldsValue["width"], self.context.options.fieldsValue["height"])
        self.windowScreenDimension = self.screenDimension
        self.fps = self.context.options.fieldsValue["fps"]
        self.isFullscreen = self.context.options.fieldsValue["fullscreen"]
        self.isMouseVisible = self.context.options.fieldsValue["cursorVisible"]

    def toggleFullscreen(self):
        self.isFullscreen = not self.isFullscreen
        self.setFullscreen(self.isFullscreen)

    def setFullscreen(self, isFullscreen):
        if isFullscreen:
            self.context.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.context.screen = pygame.display.set_mode(self.windowScreenDimension)
        self.screenDimension = (pygame.display.Info().current_w, pygame.display.Info().current_h)

    def initWindow(self):
        self.setFullscreen(self.isFullscreen)
        pygame.mouse.set_visible(self.isMouseVisible)
        pygame.display.flip()

class ball():
    def __init__(self, context):
        self.context = context

        self.position = [self.context.graphics.screenDimension[0]/2, self.context.graphics.screenDimension[1]/2]
        self.size = (20, 20)
        self.speed = self.context.options.fieldsValue["ballSpeed"]
        self.direction = [[-1, 1][random.randint(0, 1)], [-1, 1][random.randint(0, 1)]]
        self.normalizeDirectionVector()

    def normalizeDirectionVector(self):
        directionVectorLength = pow(pow(self.direction[0], 2) + pow(self.direction[1], 2), 0.5)
        for i in range(2):
            self.direction[i] /= directionVectorLength

    def draw(self):
        self.context.drawRect(constants.colors["white"], self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2, self.size[0], self.size[1])

class images():
    path = "img/"
    def __init__(self):
        self.fastImg = pygame.image.load(self.path + "fast.png")
        self.numbers = []
        for i in range(10):
            self.numbers.append(pygame.image.load(self.path + str(i) + ".png"))

class game():
    def __init__(self, context):
        self.context = context

        self.running = True

        self.options = options(self)

        self.graphics = graphics(self)
        self.images = images()

        self.ball = ball(self)

        self.points = [0, 0]

        self.timeMultiplier = 1
        self.speedZone = 300
        self.speedUpTolerance = 0.3

        self.boardsPosition = [self.graphics.screenDimension[1] / 2, self.graphics.screenDimension[1] / 2]
        self.boardsSize = (20, 100)
        self.boardsMargin = 20
        self.boardsSpeed = self.context.options.fieldsValue["boardsSpeed"]
        self.boardsDirection = [0, 0]
        self.boardsSpinMultiplier = [1, 1]

        self.graphics.initWindow()
        self.gameLoop()

    def drawRect(self, color, x, y, w, h):
        pygame.draw.rect(surface=self.screen, color=color, rect=pygame.Rect(x, y, w, h))

    def drawBoards(self):
        self.drawRect(constants.colors["white"], self.boardsMargin, self.boardsPosition[0] - self.boardsSize[1]/2, self.boardsSize[0], self.boardsSize[1])
        self.drawRect(constants.colors["white"], self.graphics.screenDimension[0] - self.boardsMargin - self.boardsSize[0], self.boardsPosition[1] - self.boardsSize[1]/2, self.boardsSize[0], self.boardsSize[1])

    def drawPoints(self):
        self.screen.blit(self.images.numbers[self.points[0]], (self.graphics.screenDimension[0] / 2 - 160, 20))
        self.screen.blit(self.images.numbers[self.points[1]], (self.graphics.screenDimension[0] / 2, 20))

    def drawScreen(self):
        self.screen.fill(color=constants.colors["black"])
        self.drawBoards()
        self.ball.draw()
        if self.timeMultiplier > 2:
            self.screen.blit(self.images.fastImg, (20, 20))
        #self.drawRect(constants.colors["red"], self.ball.position[0], self.ball.position[1], 1, 1)
        self.drawPoints()
        pygame.display.update()

    def updatePositions(self, dt):
        dt *= self.timeMultiplier
        # update both boards positions
        for i in range(2):
            self.boardsPosition[i] += self.boardsSpeed * self.boardsDirection[i] * dt

            # limiting boards to the screen
            if self.boardsPosition[i] < self.boardsSize[1] / 2:
                self.boardsPosition[i] = self.boardsSize[1] / 2
            if self.boardsPosition[i] > self.graphics.screenDimension[1] - (self.boardsSize[1] / 2):
                self.boardsPosition[i] = self.graphics.screenDimension[1] - (self.boardsSize[1] / 2)

        # vertical ball collision with wall
        if (self.ball.position[1] < self.ball.size[1]/2 and self.ball.direction[1] < 0) or (self.ball.position[1] > self.graphics.screenDimension[1] - self.ball.size[1]/2 and self.ball.direction[1] > 0):
            self.ball.direction[1] *= -1

        # horizontal ball collision with left board
        if self.ball.position[0] - self.ball.size[0]/2 <= self.boardsMargin + self.boardsSize[0] and self.ball.direction[0] < 0 and abs(self.ball.position[1] - self.boardsPosition[0]) < self.boardsSize[1]/2:
            self.ball.direction[0] *= -1
            self.ball.direction[1] += self.boardsDirection[0] * self.boardsSpinMultiplier[0]
            self.ball.normalizeDirectionVector()
        # horizontal ball collision with right board
        if self.ball.position[0] + self.ball.size[0]/2 >= self.graphics.screenDimension[0] - (self.boardsMargin + self.boardsSize[0]) and self.ball.direction[0] > 0 and abs(self.ball.position[1] - self.boardsPosition[1]) < self.boardsSize[1]/2:
            self.ball.direction[0] *= -1
            self.ball.direction[1] += self.boardsDirection[1] * self.boardsSpinMultiplier[1]
            self.ball.normalizeDirectionVector()

        # update ball position
        for i in range(2):
            self.ball.position[i] += self.ball.direction[i] * self.ball.speed * dt

        if self.ball.position[0] < self.boardsMargin + self.boardsSize[0]:
            self.points[1] += 1
            self.ball = ball(self)

        if self.ball.position[0] > self.graphics.screenDimension[0] - (self.boardsMargin + self.boardsSize[0]):
            self.points[0] += 1
            self.ball = ball(self)

        if self.context.options.fieldsValue["speedUp"]:
            if self.speedZone < self.ball.position[0] < self.graphics.screenDimension[0] - self.speedZone and abs(self.ball.direction[0]) < self.speedUpTolerance:
                self.timeMultiplier = 3
            else:
                self.timeMultiplier = 1

    def gameLoop(self):
        clock = pygame.time.Clock()
        while self.running == True:
            dt = clock.tick(self.graphics.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.boardsDirection[1] += -1
                    if event.key == pygame.K_DOWN:
                        self.boardsDirection[1] += 1

                    if event.key == pygame.K_w:
                        self.boardsDirection[0] += -1
                    if event.key == pygame.K_s:
                        self.boardsDirection[0] += 1

                    if event.key == pygame.K_F11:
                        self.graphics.toggleFullscreen()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.boardsDirection[1] += 1
                    if event.key == pygame.K_DOWN:
                        self.boardsDirection[1] += -1

                    if event.key == pygame.K_w:
                        self.boardsDirection[0] += 1
                    if event.key == pygame.K_s:
                        self.boardsDirection[0] += -1

            self.updatePositions(dt)
            self.drawScreen()

        pygame.display.quit()
        pygame.quit()
        del self

class options(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context

        self.fieldsType = {
            "Graphics": None,
            "fps": int,
            "width": int,
            "height": int,
            "fullscreen": bool,
            "cursorVisible": bool,
            "ballSpeed": float,
            "boardsSpeed": float,
            "speedUp": bool
        }

        # default values
        self.fieldsValue = {
            "Graphics": None,
            "fps": 60,
            "width": 1000,
            "height": 800,
            "fullscreen": False,
            "cursorVisible": False,
            "Game": None,
            "ballSpeed": 0.4,
            "boardsSpeed": 0.5,
            "speedUp": False
        }

        self.fieldsValueDefault = self.fieldsValue

        self.labels = {}
        self.lineEdits = {}

        self.initUI()

    def writeToFile(self, dict):
        file = open("settings.json", "w")
        file.write(json.dumps(dict))
        file.close()

    def loadSettings(self):
        if not os.path.isfile("settings.json"):
            self.writeToFile(self.fieldsValue)

        file = open("settings.json", "r")
        self.fieldsValue = json.load(file)

        if not len(self.fieldsValue) == len(self.fieldsValueDefault):
            self.writeToFile(self.fieldsValueDefault)
            self.loadSettings()

        file.close()

    def saveSetting(self, close):
        for i in self.lineEdits:
            # parsing dynamically to type from fieldsType
            if self.fieldsType[i] == bool:
                # TODO: make fields' qt inputs dependent on a type, e.g. checkbox for bool
                self.fieldsValue[i] = self.lineEdits[i].text().lower() == "true"
            else:
                try:
                    self.fieldsValue[i] = self.fieldsType[i](self.lineEdits[i].text())
                except ValueError:
                    self.fieldsValue[i] = self.fieldsValueDefault[i]

        self.writeToFile(self.fieldsValue)

        if close:
            self.close()

    def initUI(self):
        self.dispWidth = 400
        self.dispHeight = 800
        self.resize(self.dispWidth, self.dispHeight)

        self.loadSettings()

        heightPointer = 10
        for i in self.fieldsValue:
            if i[0].isupper():
                self.labels[i] = QLabel(self)
                self.labels[i].setGeometry(10, heightPointer, 300, 60)
                self.labels[i].setFont(QFont("Courier", 30))
                self.labels[i].setText(i)
                heightPointer += 20
            else:
                self.labels[i] = QLabel(self)
                self.labels[i].setGeometry(10, heightPointer, 100, 30)
                self.labels[i].setText(i)

                self.lineEdits[i] = QLineEdit(self)
                self.lineEdits[i].setGeometry(120, heightPointer, 100, 30)
                if self.fieldsValue[i] is not None:
                    self.lineEdits[i].setText(str(self.fieldsValue[i]))

            heightPointer += 30

        self.btnSave = QPushButton(self)
        self.btnSave.setText("Zapisz")
        self.btnSave.setGeometry(10, self.dispHeight - 200, 100, 30)
        self.btnSave.clicked.connect(lambda : self.saveSetting(False))

        self.btnSaveNExit = QPushButton(self)
        self.btnSaveNExit.setText("Zapisz i wyjdź")
        self.btnSaveNExit.setGeometry(120, self.dispHeight - 200, 150, 30)
        self.btnSaveNExit.clicked.connect(lambda : self.saveSetting(True))


class launcher(QWidget):
    (width, height) = (300, 200)

    def __init__(self):
        super().__init__()

        self.options = options(self)

        self.initUI()
        self.show()

    def openOptions(self):
        self.options = options(self)
        self.options.show()

    def startGame(self):
        self.winner = QLabel(self)
        self.winner.setGeometry(10, 50, 50, 30)

        self.game = game(self)

    def initUI(self):
        self.resize(self.width,self.height)
        self.setWindowTitle(constants.gameTitle)

        self.btnPlay = QPushButton(self)
        self.btnPlay.setGeometry(10, 10, 100, 30)
        self.btnPlay.setText("Graj")
        self.btnPlay.clicked.connect(self.startGame)

        self.btnOptions = QPushButton(self)
        self.btnOptions.setGeometry(10, 50, 100, 30)
        self.btnOptions.setText("Ustawienia")
        self.btnOptions.clicked.connect(self.openOptions)

def main():
    app = QApplication(sys.argv)
    ex = launcher()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
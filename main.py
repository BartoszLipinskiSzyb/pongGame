import random

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
import sys
import pygame

class constants():
    colors = {
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "black": (0, 0, 0)
    }

class graphics():
    def __init__(self, context):
        self.context = context

        self.screenDimension = (1000, 800)
        self.windowScreenDimension = (1000, 800)
        self.fps = 120
        self.isFullscreen = False
        self.isMouseVisible = False

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
        self.speed = 0.4
        self.direction = [[-1, 1][random.randint(0, 1)], [-1, 1][random.randint(0, 1)]]
        self.normalizeDirectionVector()

    def normalizeDirectionVector(self):
        directionVectorLength = pow(pow(self.direction[0], 2) + pow(self.direction[1], 2), 0.5)
        for i in range(2):
            self.direction[i] /= directionVectorLength

    def draw(self):
        self.context.drawRect(constants.colors["white"], self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2, self.size[0], self.size[1])

class game():
    def __init__(self, context):
        self.context = context

        self.running = True

        self.graphics = graphics(self)
        self.constants = constants()

        self.ball = ball(self)

        self.points = [0, 0]

        self.timeMultiplier = 1
        self.speedZone = 300
        self.speedUpTolerance = 0.3

        self.boardsPosition = [self.graphics.screenDimension[1] / 2, self.graphics.screenDimension[1] / 2]
        self.boardsSize = (20, 100)
        self.boardsMargin = 20
        self.boardsSpeed = 0.3
        self.boardsDirection = [0, 0]
        self.boardsSpinMultiplier = [1, 1]

        self.fastImg = pygame.image.load("fast.png")

        self.graphics.initWindow()
        self.gameLoop()

    def drawRect(self, color, x, y, w, h):
        pygame.draw.rect(surface=self.screen, color=color, rect=pygame.Rect(x, y, w, h))

    def drawBoards(self):
        self.drawRect(constants.colors["white"], self.boardsMargin, self.boardsPosition[0] - self.boardsSize[1]/2, self.boardsSize[0], self.boardsSize[1])
        self.drawRect(constants.colors["white"], self.graphics.screenDimension[0] - self.boardsMargin - self.boardsSize[0], self.boardsPosition[1] - self.boardsSize[1]/2, self.boardsSize[0], self.boardsSize[1])

    def drawScreen(self):
        self.screen.fill(color=constants.colors["black"])
        self.drawBoards()
        self.ball.draw()
        if self.timeMultiplier > 2:
            self.screen.blit(self.fastImg, (20, 20))
        #self.drawRect(constants.colors["red"], self.ball.position[0], self.ball.position[1], 1, 1)
        pygame.display.update()

    def updatePositions(self, dt):
        dt *= self.timeMultiplier
        # update both boards positions
        for i in range(2):
            self.boardsPosition[i] += self.boardsSpeed * self.boardsDirection[i] * dt

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
            print(self.points)

        if self.ball.position[0] > self.graphics.screenDimension[0] - (self.boardsMargin + self.boardsSize[0]):
            self.points[0] += 1
            self.ball = ball(self)
            print(self.points)

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

class launcher(QWidget):
    (width, height) = (300, 200)

    def __init__(self):
        super().__init__()
        self.initUI()

    def startGame(self):
        self.winner = QLabel(self)
        self.winner.setGeometry(10, 50, 50, 30)

        self.game = game(self)

    def initUI(self):
        self.setGeometry(100,100,self.width,self.height)

        self.btnPlay = QPushButton(self)
        self.btnPlay.setGeometry(10, 10, 50, 30)
        self.btnPlay.setText("Graj")
        self.btnPlay.clicked.connect(self.startGame)

        self.show()

def main():
    app = QApplication(sys.argv)
    ex = launcher()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys
import pygame

class constants():
    colors = {
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "black": (0, 0, 0)
    }

class graphics():
    def __init__(self):
        self.screenDimension = (1000, 800)
        self.windowScreenDimension = (1000, 800)
        self.fps = 120
        self.isFullscreen = False
        self.isMouseVisible = False

class game():
    def __init__(self):
        self.running = True

        self.graphics = graphics()
        self.constants = constants()

        self.boardsPosition = [self.graphics.screenDimension[1] / 2, self.graphics.screenDimension[1] / 2]
        self.boardsSize = (20, 100)
        self.boardsMargin = 20
        self.boardsSpeed = 0.3
        self.boardsDirection = [0, 0]
        self.boardsSpinMultiplier = [1, 1]

        self.ballPosition = [500, 500]
        self.ballSize = (20, 20)
        self.ballSpeed = 0.4
        self.ballDirection = [-1, 1]

        self.initWindow()
        self.gameLoop()

    def initWindow(self):
        self.setFullscreen(self.graphics.isFullscreen)
        pygame.mouse.set_visible(self.graphics.isMouseVisible)
        pygame.display.flip()

    def drawRect(self, color, x, y, w, h):
        pygame.draw.rect(surface=self.screen, color=color, rect=pygame.Rect(x, y, w, h))

    def drawBoards(self):
        self.drawRect(constants.colors["white"], self.boardsMargin, self.boardsPosition[0] - self.boardsSize[1]/2, self.boardsSize[0], self.boardsSize[1])
        self.drawRect(constants.colors["white"], self.graphics.screenDimension[0] - self.boardsMargin - self.boardsSize[0], self.boardsPosition[1] - self.boardsSize[1]/2, self.boardsSize[0], self.boardsSize[1])

    def drawBall(self):
        self.drawRect(constants.colors["white"], self.ballPosition[0] - self.ballSize[0]/2, self.ballPosition[1] - self.ballSize[1]/2, self.ballSize[0], self.ballSize[1])

    def drawScreen(self):
        self.screen.fill(color=constants.colors["black"])
        self.drawBoards()
        self.drawBall()
        #self.drawRect(constants.colors["red"], self.ballPosition[0], self.ballPosition[1], 1, 1)
        pygame.display.update()

    def updatePositions(self, dt):
        # update both boards positions
        for i in range(2):
            self.boardsPosition[i] += self.boardsSpeed * self.boardsDirection[i] * dt

        # vertical ball collision with wall
        if (self.ballPosition[1] < self.ballSize[1]/2 and self.ballDirection[1] < 0) or (self.ballPosition[1] > self.graphics.screenDimension[1] - self.ballSize[1]/2 and self.ballDirection[1] > 0):
            self.ballDirection[1] *= -1

        # horizontal ball collision with left board
        if self.ballPosition[0] - self.ballSize[0]/2 <= self.boardsMargin + self.boardsSize[0] and self.ballDirection[0] < 0 and abs(self.ballPosition[1] - self.boardsPosition[0]) < self.boardsSize[1]/2:
            self.ballDirection[0] *= -1
            self.ballDirection[1] += self.boardsDirection[0] * self.boardsSpinMultiplier[0]
        # horizontal ball collision with right board
        if self.ballPosition[0] + self.ballSize[0]/2 >= self.graphics.screenDimension[0] - (self.boardsMargin + self.boardsSize[0]) and self.ballDirection[0] > 0 and abs(self.ballPosition[1] - self.boardsPosition[1]) < self.boardsSize[1]/2:
            self.ballDirection[0] *= -1
            self.ballDirection[1] += self.boardsDirection[1] * self.boardsSpinMultiplier[1]

        # direction vector normalization
        directionVectorLength = pow(pow(self.ballDirection[0], 2) + pow(self.ballDirection[1], 2), 0.5)
        for i in range(2):
            self.ballDirection[i] /= directionVectorLength

        # update ball position
        for i in range(2):
            self.ballPosition[i] += self.ballDirection[i] * self.ballSpeed * dt

    def setFullscreen(self, isFullscreen):
        if isFullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.graphics.windowScreenDimension)
        self.graphics.screenDimension = (pygame.display.Info().current_w, pygame.display.Info().current_h)

    def toggleFullscreen(self):
        self.graphics.isFullscreen = not self.graphics.isFullscreen
        self.setFullscreen(self.graphics.isFullscreen)

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
                        self.toggleFullscreen()

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
    def initUI(self):
        self.setGeometry(100,100,self.width,self.height)

        self.btnPlay = QPushButton(self)
        self.btnPlay.setGeometry(10, 10, 50, 30)
        self.btnPlay.setText("Graj")
        self.btnPlay.clicked.connect(lambda : game())

        self.show()

def main():
    app = QApplication(sys.argv)
    ex = launcher()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
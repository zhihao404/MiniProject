import pyxel
import random
import time

animal_files = {
    'pig': 'assets/pig.png',
    'sheep': 'assets/sheep.png',
    'hamster': 'assets/hamster.png',
    'tanuki': 'assets/tanuki.png',
}

background_file = 'assets/kusa.png'
cursor_file = 'assets/ami.png'
saku_file = 'assets/saku.png'

class Animal:
    def __init__(self, image_bank, image_x, image_y, width, height):
        self.image_bank = image_bank
        self.image_x = image_x
        self.image_y = image_y
        self.width = width
        self.height = height
        self.restart()

    def restart(self):
        self.x = random.randint(10, 190)
        self.y = random.randint(10, 190)
        angle = random.uniform(0, 360)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def update(self):
        self.x += self.vx * 3
        self.y += self.vy * 3
        if self.x < 0 or self.x >= 200 - self.width:
            self.vx = -self.vx
        if self.y < 0 or self.y >= 200 - self.height:
            self.vy = -self.vy

    def draw(self):
        pyxel.blt(self.x, self.y, self.image_bank, self.image_x, self.image_y, self.width, self.height, pyxel.COLOR_BLACK)

    def is_clicked(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

def load_images():
    pyxel.images[0].load(0, 0, animal_files['pig'])
    pyxel.images[0].load(16, 0, animal_files['sheep'])
    pyxel.images[0].load(32, 0, animal_files['hamster'])
    pyxel.images[0].load(48, 0, animal_files['tanuki'])
    pyxel.images[1].load(0, 0, background_file)
    pyxel.images[2].load(0, 0, cursor_file)
    pyxel.images[1].load(64, 0, saku_file)

class Game:
    def __init__(self):
        self.animals = [
            Animal(0, 0, 0, 16, 16),
            Animal(0, 16, 0, 16, 16),
            Animal(0, 32, 0, 16, 16),
            Animal(0, 48, 0, 16, 16),
            Animal(0, 0, 0, 16, 16),
            Animal(0, 16, 0, 16, 16),
            Animal(0, 32, 0, 16, 16),
            Animal(0, 48, 0, 16, 16),
            Animal(0, 0, 0, 16, 16),
            Animal(0, 16, 0, 16, 16),
            Animal(0, 32, 0, 16, 16),
            Animal(0, 48, 0, 16, 16),
        ]
        self.start_time = time.time()
        self.score = 0
        self.time_up = False

    def restart(self):
        self.start_time = time.time()
        self.score = 0
        self.time_up = False
        for animal in self.animals:
            animal.restart()

    def update(self):
        if not self.time_up:
            if time.time() - self.start_time >= 10:
                self.time_up = True
            else:
                for animal in self.animals:
                    animal.update()
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    mx, my = pyxel.mouse_x, pyxel.mouse_y
                    for animal in self.animals:
                        if animal.is_clicked(mx, my):
                            self.score += 1
                            animal.restart()
        else:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.restart()

    def draw(self):
        pyxel.cls(0)
        pyxel.mouse(False)
        for x in range(0, 200, 16):
            for y in range(0, 200, 16):
                pyxel.blt(x, y, 1, 0, 0, 16, 16)
        for x in range(0, 200, 16):
            pyxel.blt(x, 0, 1, 64, 0, 16, 16, pyxel.COLOR_BLACK)
            pyxel.blt(x, 184, 1, 64, 0, 16, 16, pyxel.COLOR_BLACK)
        for animal in self.animals:
            animal.draw()
        pyxel.rect(0, 0, 50, 10, pyxel.COLOR_ORANGE)
        pyxel.text(5, 3, f"Score: {self.score}", pyxel.COLOR_WHITE)
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)

        if self.time_up:
            pyxel.rect(50, 70, 80, 40, pyxel.COLOR_ORANGE)
            pyxel.text(60, 80, f"Time Up!!", pyxel.COLOR_WHITE)
            pyxel.text(60, 90, f"Score: {self.score}", pyxel.COLOR_WHITE)
            pyxel.text(60, 100, f"Click to Restart", pyxel.COLOR_BROWN)
            if 50 <= pyxel.mouse_x <= 130 and 70 <= pyxel.mouse_y <= 110:
                pyxel.mouse(True)

pyxel.init(200, 200)
load_images()

game = Game()

pyxel.run(game.update, game.draw)

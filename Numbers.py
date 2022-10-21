from ctypes.wintypes import WIN32_FIND_DATAA
import pygame as pg
import random
import time

pg.init()

SCREENWIDTH = 1000
SCREENHEIGHT = 700

SHOWN = (140, 140, 220)
WRITE = (220, 140, 140)
EMPTY = (170,170,170)
BACKGROUND = (255,255,255)
FONT = pg.font.SysFont("timesnewroman.ttf", 72)
WIN = (40,200,40)
LOSS = (200,40,40)
TEXT = (20, 20, 20)

class Game:
    def __init__(self, screenwidth = 1000, screenheight = 700):
        self.screen = pg.display.set_mode((screenwidth, screenheight))
        self.height = screenheight
        self.width = screenwidth
        self.score = 0
        self.state = "End" #View, Play, Correct, End
        self.number = None #Number to repeat
        self.input = None #Inputted number
    
    def generate_number(self):
        self.number = random.randint(10**self.score, 10**(self.score+1)-1)
        
    def update(self):
        self.screen.fill(EMPTY)
        if self.state == "View":
            text = FONT.render(f"{self.number}", True, TEXT)
            text_rect = text.get_rect(center=(self.width/2, self.height/2))
            self.screen.blit(text, text_rect)
        elif self.state == "Play" and self.input != None:
            text = FONT.render(f"{self.input}", True, TEXT)
            text_rect = text.get_rect(center=(self.width/2, self.height/2))
            self.screen.blit(text, text_rect)
        elif self.state == "Correct":
            if self.input == self.number:
                text1 = FONT.render(f"{self.number}", True, WIN)
                text2 = FONT.render(f"{self.input}", True, WIN)
            else:
                text1 = FONT.render(f"{self.number}", True, LOSS)
                text2 = FONT.render(f"{self.input}", True, LOSS)
            text_rect1 = text1.get_rect(center=(self.width/2, self.height/2 - text1.get_height()))
            text_rect2 = text2.get_rect(center=(self.width/2, self.height/2 + text2.get_height()))
            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
        pg.display.update()

    def countdown(self, count, color):
        pg.draw.rect(self.screen, color, (0,0,self.width, self.height//10))
        pg.display.update()
        for i in range(self.width):
            time.sleep(round(count/self.width, 3))
            pg.draw.rect(self.screen, EMPTY, (self.width - i, 0, self.width, self.height//10))
            pg.display.update()

    def play(self):
        self.score = 0
        self.input = None
        while self.state != "End":
            self.input = None
            self.generate_number()
            self.update()
            self.countdown(self.score + 1, WIN)
            start = time.time()
            self.state = "Play"
            self.input = None
            self.update()
            while self.state == "Play":
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        pg.quit()
                    elif event.type == pg.KEYDOWN and event.key in {pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9, pg.K_BACKSPACE}:
                        if not self.input and event.key != pg.K_BACKSPACE and time.time() - start > 0.05:
                            self.input = event.key - pg.K_0
                            self.update()
                        elif event.key == pg.K_BACKSPACE:
                            self.input //= 10
                            self.update()
                        elif self.input: 
                            self.input = self.input*10 + event.key - pg.K_0
                            self.update()
                    elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN and self.input and self.state == "Play":
                        self.state = "Correct"
                        self.update()
                        self.countdown(1.5, SHOWN)
                        if self.input == self.number:
                            self.score += 1
                            self.state = "View"
                        else:
                            self.state = "End"
                    pg.event.clear(pg.KEYDOWN)

    def menu(self):
        self.screen.fill(BACKGROUND)
        pressspace = FONT.render("Press space to play", True, TEXT)
        if self.score > 1:
            scorecount = FONT.render(f'Score: {self.score}', True, TEXT)
            self.screen.blit(scorecount, (10, 10))
        self.screen.blit(pressspace, (10, 10 + pressspace.get_height()))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.state = "View"

    def run(self):
        while True:
            if self.state == "View" or self.state == "Play":
                self.play()
            elif self.state == "End":
                self.menu()
                

def main():
    game = Game(SCREENWIDTH, SCREENHEIGHT)
    game.run()


if __name__ == "__main__":
    main()

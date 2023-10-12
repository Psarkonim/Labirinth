from pygame import *

init()
mixer.init()
font.init()

window = display.set_mode((700, 500))
display.set_caption('Labirinth')

clock = time.Clock()
bg = transform.scale(image.load('background.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, img: str, speed: int):
        super().__init__()
        self.img = transform.scale(image.load(img), (width, height))
        self.rect = self.img.get_rect() 
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class Wall(sprite.Sprite):
    def __init__(self, x:int, y:int, color: tuple, width: int, height: int):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x , self.rect.y))


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        
        if key_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def set_direction(self, direction: bool):
        self.direction = direction

    def update(self):
        if self.rect.x < 300:
            self.direction = 1
            
        elif self.rect.x > 600:
            self.direction = 0
        
        if self.direction:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
            


mixer.music.load('jungles.ogg')
mixer.music.play()

win_sound = mixer.Sound('kick.ogg')
lose_sound = mixer.Sound('money.ogg')

wall_color = (200, 50, 50)

hero = Player(100, 100, 75, 75, 'hero.png', 5)
enemy = Enemy(300, 100, 75, 75, 'cyborg.png', 5)
enemy.set_direction(0)
wall_1 = Wall(20, 20, wall_color, 680, 15)
wall_2 = Wall(20, 20, wall_color, 15, 300)
wall_3 = Wall(350, 300, wall_color, 250, 15)
wall_4 = Wall(350, 300, wall_color, 15, 250)
wall_5 = Wall(200, 200, wall_color, 15, 350)  
wall_6 = Wall(600, 450, wall_color, 15, 50)
treasure = GameSprite(400, 350, 100, 100, 'treasure.png', 0)
font = font.SysFont('Arial', 100)
font_lose = font.render('YOU LOSE!', True, (255, 0, 15))
font_win = font.render('YOU WIN!', True, (20, 200, 20))
game = True
finish = False
walls = [wall_1, wall_2, wall_3, wall_4, wall_5, wall_6] 

while game:
    for evnt in event.get():
        if evnt.type == QUIT:
            game = False
    
    if not finish:
        window.blit(bg, (0, 0)) 
        
        hero.update()
        enemy.update()
        
        for wall in walls:
            wall.draw()

        hero.draw()
        enemy.draw()
        treasure.draw()

        if sprite.collide_rect(hero, enemy):
            finish = True
            lose_sound.play()
            window.blit(font_lose, (150, 250))

        for wall in walls:
            if sprite.collide_rect(hero, wall):
                finish = True
                lose_sound.play()
                window.blit(font_lose, (150, 250))
        
        if sprite.collide_rect(hero, treasure):
            finish = True
            win_sound.play()
            window.blit(font_win, (150, 250))

        display.update()
        clock.tick(60)
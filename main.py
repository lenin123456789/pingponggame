from pygame import *
import time as timer

win_height = 500
win_width = 600

window = display.set_mode((win_width, win_height))
background_color = (200, 255, 255)
window.fill(background_color)


class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, width, height, speed):
        self.image = transform.scale(image.load(player_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < win_height - self.height:
            self.rect.y += self.speed
            
    def update_r(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < win_height - self.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def reset_ball(self, angle):
        rotate_ball = transform.rotate(self.image, angle)
        window.blit(rotate_ball, (self.rect.x, self.rect.y))


paddle_1 = Player("racket.png", 10, 200, 50, 150, 4)
paddle_2 = Player("racket.png", win_width - 60, 200, 50, 150, 4)
ball = Ball("tenis_ball.png", 200, 200, 50, 50, 4)

font.init()
font_1 = font.Font(None, 84)
pause_text = font_1.render("PAUSED", 1, (00,0,0))

starting_text = font_1.render("Choose set pont.",1, (0,0,0))
endeing_text = font_1.render("GAME OVER!",1, (0,0,0))

list_setpoints = [1, 5,10,1000000000]

font_2 = font.Font(None, 32)








choosen_point = 0
game_over = False
FPS = 500
finish = False
game_status = None
clock = time.Clock()
dx = ball.speed
dy = ball.speed
angle = 0 
point_l = 0
point_r = 0
turn_dir = 1

while not game_over:
    for e in event.get():
        if e.type == QUIT:
            game_over = True

        if e.type == KEYDOWN:
            if e.key == K_p:
                if game_status == None:
                    game_status = "pause"

                elif game_status == "pause":
                    game_status = None

            if e.key == K_1 and choosen_point == 0:
                choosen_point = list_setpoints[0]

            if e.key == K_2 and choosen_point == 0:
                choosen_point = list_setpoints[1]

            if e.key == K_3 and choosen_point == 0:
                choosen_point = list_setpoints[2]

            if e.key == K_4 and choosen_point == 0:
                choosen_point = list_setpoints[3]

    if not finish:
        if choosen_point == 0:
            text_y = 250
            window.blit(starting_text, (100,200))
            for point in list_setpoints:
                point_choise = font_2.render(f"{point} points", 1, (0,0,0))
                window.blit(point_choise, (180, text_y))
                text_y += 25
  




        if game_status == None and choosen_point != 0:
            
            angle += turn_dir

            ball.rect.x += dx
            ball.rect.y += dy

            if sprite.collide_rect(ball, paddle_1):
                dx *= -1.01
                turn_dir *= -1.01
            if sprite.collide_rect(ball, paddle_2):
                dx *= -1.01
                turn_dir *= -1.01
            if ball.rect.y > win_height - 50 or ball.rect.y < 0:
                dy *= -1.01
                turn_dir *= -1.01

            if ball.rect.x > win_width - 50 :
                point_l += 1
                

            if ball.rect.x < 0:
                point_r += 1 
                


            if ball.rect.x < 0 or ball.rect.x > win_width - 50:
                ball.rect.x = 200
                ball.rect.y = 200
                # timer.sleep(0.5)
                dx = ball.speed
                dy = ball.speed
                turn_dir = 1
                dx *= -1
            if point_l == choosen_point or point_r == choosen_point:
                game_status = "ended"
            window.fill(background_color)
            point_text_l = font_2.render(f"point: {point_l}", 1,(0,0,0))
            point_text_r = font_2.render(f"point: {point_r}", 1,(0,0,0))
            window.blit(point_text_l, (50,50))
            window.blit(point_text_r, (450,50))
            paddle_1.update_l()
            paddle_2.update_r()
            ball.reset_ball(angle)
            paddle_1.reset()
            paddle_2.reset()
        elif game_status == "pause":
            window.fill(background_color)
            window.blit(pause_text, (175,200))
        elif game_status == "ended":
            window.fill(background_color)
            window.blit(endeing_text, (180,200))
            if point_r > point_l:
                winner = font_2.render("Player 2 win the game", 1, (0,0,0))
            if point_r > point_r:
                winner = font_2.render("Player 1 win the game", 1, (0,0,0))

    display.update()
    clock.tick(FPS)
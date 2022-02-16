import pygame
import time
import random
pygame.init()
pygame.mouse.get_visible()
#cheats
speed_faster = False

hard_mode = False

up_down = False

start_laser = False

infinet_laser = True

infinet_chest = False

infinet_lives = False

limited_laser = False

control_ball = False
#sound
music = False

sound = False

background = random.randint(1,8)
OG_background = background
background_color = pygame.image.load(f"{background}_background.png")
game_over = False
level_win = False
shots = 3
infinet_chest_count = 20
o = 0
level = 1
score = 0
if hard_mode:
    lives = 1
else:
    lives = 3
BLANK_ROWS = 2
if speed_faster:
    FPS = 100
else:
    FPS = 70
BLUE = (0 , 0, 255)
BRICKS_PER_ROW = 10
NUM_ROWS = 5
WHITE = (255, 255, 255)
square_color = (255, 0, 0)
screen = pygame.display.set_mode((600, 800))
t_bricks = BRICKS_PER_ROW * NUM_ROWS
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
if infinet_laser and limited_laser:
    limited_laser = False
if start_laser and infinet_laser:
    start_laser = False
if infinet_lives:
    lives = 999999999999999999
if music == True:
    #songs
    song = random.randint(1,4)
    pygame.mixer.music.load(f"main song {song}.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    og_song = song

def draw_text(surface, text, pos=(0, 0), color=WHITE, font_size=20, anchor="topleft"):
    arial = pygame.font.match_font("arial")
    font = pygame.font.Font(arial, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, anchor, pos)
    surface.blit(text_surface, text_rect)
    
class Brick(pygame.sprite.Sprite):
    def __init__(self, row, col, brick_color):
        super().__init__()
        brick_image = pygame.image.load(f"{brick_color}_brick.png").convert_alpha()
# calculate new size based on BRICKS_PER_ROW
        brick_width = round(screen_rect.width / BRICKS_PER_ROW)
        orig_size = brick_image.get_rect()
        scale_factor = (brick_width / orig_size.width)
        brick_height = round(orig_size.height * scale_factor)
        new_size = (brick_width, brick_height)
        
        # scale the image
        self.image = pygame.transform.scale(brick_image, new_size)
        self.rect = self.image.get_rect()
        
        # position the brick
        row += BLANK_ROWS
        self.rect.x = col * brick_width
        self.rect.y = row * brick_height
        
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ball_color = random.randint(1,2)
        ball_image = pygame.image.load(f"{ball_color}_ball.png").convert_alpha()
        self.image = pygame.transform.scale(ball_image, (20, 20))
        if sound == True:
            self.bounce_sound = pygame.mixer.Sound("paddle sound.wav")
            self.wall_sound = pygame.mixer.Sound("wall sound.wav")
            self.break_sound = pygame.mixer.Sound("break.wav")
        self.rect = self.image.get_rect()
        self.reset()
        
    def reset(self):
        
        self.rect.center = screen_rect.center
        self.x_speed = random.choice((5, -5))
        self.y_speed = 5
        self.lost = False
        
    def update(self):
        #update code goes here
        if control_ball:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.rect.x += 15
            elif keys[pygame.K_a]:
                self.rect.x -= 15
            elif keys[pygame.K_s]:
                self.rect.y += 15
            elif keys[pygame.K_w]:
                self.rect.y -= 15

        if self.rect.right >= screen_rect.right:
            if sound == True:
                self.wall_sound.play()
            self.x_speed = -5
        if self.rect.left <= screen_rect.left:
            if sound == True:
                self.wall_sound.play()
            self.x_speed = 5
        if self.rect.top <= screen_rect.top:
            if sound == True:
                self.wall_sound.play()
            self.y_speed = 5
        if self.rect.bottom >= screen_rect.bottom:
            self.lost = True

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        paddle_color = random.randint(1,2)
        paddle_image = pygame.image.load(f"{paddle_color}_paddle.png").convert_alpha()
        self.image = pygame.transform.scale(paddle_image, (125, 20))
        self.rect = self.image.get_rect()
        self.rect.center = screen_rect.center
        self.rect.bottom = screen_rect.bottom - 10
        
    def update(self):
        keys = pygame.key.get_pressed()
        
        #pause
        if keys[pygame.K_p]:
            while True:
                time.sleep(0.1)
                resume = input("to resume type start or to stop type stop: ")
                if resume == "start" or resume == "START" or resume == "Start":
                    time.sleep(1)
                    print("3")
                    time.sleep(1)
                    print("2")
                    time.sleep(1)
                    print("1")
                    break
                if resume == "Stop" or resume == "stop" or resume == "STOP":
                    pygame.quit()
                    break


        if up_down == True:
            if keys[pygame.K_RIGHT]:
                self.rect.x += 15
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 15
            if not control_ball:
                if keys[pygame.K_a]:
                    self.rect.x -= 15
                elif keys[pygame.K_d]:
                    self.rect.x += 15
            if keys[pygame.K_UP]:
                self.rect.y -= 15
            elif keys[pygame.K_DOWN]:
                self.rect.y += 15
            if not control_ball:
                if keys[pygame.K_s]:
                    self.rect.y += 15
                elif keys[pygame.K_w]:
                    self.rect.y -= 15
        else:
            if keys[pygame.K_RIGHT]:
                self.rect.x += 13
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 13
            if not control_ball:
                if keys[pygame.K_a]:
                    self.rect.x -= 13
                elif keys[pygame.K_d]:
                    self.rect.x += 13

        if self.rect.right >= screen_rect.right:
            self.rect.right = screen_rect.right
        if self.rect.left <= screen_rect.left:
            self.rect.left = screen_rect.left
            
class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        box_image = pygame.image.load("box.png").convert_alpha()
        self.image = pygame.transform.scale(box_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = screen_rect.center
        self.rect.top = screen_rect.top + 5


class Laser(pygame.sprite.Sprite):
    def __init__(self, laser_color):
        super().__init__()
        laser_image = pygame.image.load(f"{laser_color}_laser.png").convert_alpha()
        self.image = pygame.transform.scale(laser_image, (40, 100))
        self.rect = self.image.get_rect()
        self.rect.center = screen_rect.center
        self.rect.bottom = screen_rect.bottom - 5
        self.laser_mover = True
        if sound == True:
            self.break_sound = pygame.mixer.Sound("break.wav")
            
    def update(self):
        #update code goes here
        keys = pygame.key.get_pressed()
        
                
                
        if not up_down:
            if control_ball:
                if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                    self.laser_mover = False
            else:
                if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]:
                    self.laser_mover = False            
        else:
            if keys[pygame.K_SPACE]:
                self.laser_mover = False
        if not self.laser_mover:
            self.rect.y -= 15               
        if self.laser_mover:
            keys = pygame.key.get_pressed()
            if up_down == True:
                if keys[pygame.K_RIGHT]:
                    self.rect.x += 15
                elif keys[pygame.K_LEFT]:
                    self.rect.x -= 15
                if not control_ball:
                    if keys[pygame.K_a]:
                        self.rect.x -= 15
                    elif keys[pygame.K_d]:
                        self.rect.x += 15
                if keys[pygame.K_UP]:
                    self.rect.y -= 15
                elif keys[pygame.K_DOWN]:
                    self.rect.y += 15
                if not control_ball:
                    if keys[pygame.K_s]:
                        self.rect.y += 15
                    elif keys[pygame.K_w]:
                        self.rect.y -= 15
            else:
                if keys[pygame.K_RIGHT]:
                    self.rect.x += 13
                elif keys[pygame.K_LEFT]:
                    self.rect.x -= 13
                if not control_ball:
                    if keys[pygame.K_a]:
                        self.rect.x -= 13
                    elif keys[pygame.K_d]:
                        self.rect.x += 13

            if self.rect.right >= screen_rect.right:
                self.rect.right = screen_rect.right
            if self.rect.left <= screen_rect.left:
                self.rect.left = screen_rect.left
                
laser_color = random.randint(1,3)
box = Box()
box_group = pygame.sprite.Group()                
laser = Laser(laser_color)
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
ball = Ball()
all_sprites.add(ball)
paddle = Paddle()
all_sprites.add(paddle)
if start_laser or infinet_laser or limited_laser:
    all_sprites.add(laser)
if infinet_chest:
    box_group.add(box)
    all_sprites.add(box)
else:
    power_box = random.randint(1,4)
    if power_box == 1:
        box_group.add(box)
        all_sprites.add(box)
brick_color = random.randint(1,6)
for row in range(0, NUM_ROWS):
    for col in range(0, BRICKS_PER_ROW):
        brick = Brick(row, col, brick_color)
        all_sprites.add(brick)
        bricks.add(brick)
og_brick_color = brick_color

running = True
while running:
    if infinet_chest:
        infinet_chest_count += 1
    if infinet_laser or limited_laser:
        if infinet_laser or shots > 0:
            if laser.rect.bottom <= screen_rect.top:
                if shots == 1:
                    shots -= 1
                if not shots <= 1:
                    laser.rect.center = paddle.rect.center
                    laser.rect.bottom = paddle.rect.bottom
                    laser.laser_mover = True
                    if limited_laser:
                        shots -= 1
            
    screen.blit(background_color,(0,0))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if level_win:
        if limited_laser:
            shots = 6
        if not infinet_chest:
            power_box = random.randint(1,4)
            if power_box == 1:
                box_group.add(box)
                all_sprites.add(box)
        if speed_faster:
            FPS += 50
        else:
            FPS += 10
        level += 1
        ball.reset()
        brick_color = random.randint(1,6)
        for row in range(0, NUM_ROWS):
            for col in range(0, BRICKS_PER_ROW):
                while True:
                    if brick_color == og_brick_color:
                        brick_color = random.randint(1,6)
                    else:
                        break
                brick = Brick(row, col, brick_color)
                all_sprites.add(brick)
                bricks.add(brick)
        og_brick_color = brick_color
        background = random.randint(1,8)
        while True:
            if background == OG_background:
                background = random.randint(1,8)
            else:
                break
        background_color = pygame.image.load(f"{background}_background.png")
        background = OG_background
        if music == True:
            while True:
                if song == og_song:
                    song = random.randint(1,4)
                else:
                    break
            pygame.mixer.music.load(f"main song {song}.wav")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops=-1)
        if infinet_lives:
            if lives < 999999999999999999:
                lives = 999999999999999999
        else:
            if lives < 3:
                lives = 3
        level_win = False
    if game_over:
        if o == 0:
            over = random.randint(1,4)
        background_color = pygame.image.load(f"game_over {over}.png")
        draw_text(screen, f"GAME OVER YOUR SCORE WAS {score}", screen_rect.center, font_size=40, anchor="center")
        o += 1
    else:
        all_sprites.update()
     # Check for paddle / ball collision
        if pygame.sprite.collide_rect(ball, paddle):
            if sound == True:
                ball.bounce_sound.play()
            ball.y_speed = -5
            if ball.rect.centerx < paddle.rect.centerx:
                ball.x_speed = -5
            else:
                ball.x_speed = 5
    if ball.lost:
        lives -= 1
        if lives == 0:
            game_over = True
        ball.reset()

    all_sprites.draw(screen)
    if limited_laser:
        score_text = f"Score: {score} / Lives: {lives}/ Speed: {FPS}/level: {level}/shots {shots}"
    else:
        score_text = f"Score: {score} / Lives: {lives}/ Speed: {FPS}/level {level}"
    draw_text(screen, score_text, (8, 8))
    
    pygame.display.flip()
    # Check for ball / brick collision
    collided_brick = pygame.sprite.spritecollideany(ball, bricks)
    collided_brick_laser = pygame.sprite.spritecollideany(laser, bricks)
    collided_box = pygame.sprite.spritecollideany(ball, box_group)
    collided_box_laser = pygame.sprite.spritecollideany(laser, box_group)
    if collided_brick or collided_brick_laser:
        score += 1
        if sound == True:
            ball.break_sound.play()
        if collided_brick_laser:
            collided_brick_laser.kill()
        elif collided_brick:
            collided_brick.kill()
            ball.y_speed *= -1
        if score % t_bricks == 0:
            level_win = True
            if infinet_laser:
                laser.rect.center = paddle.rect.center
                laser.rect.bottom = paddle.rect.bottom
                laser.laser_mover = True
    if collided_box or collided_box_laser:
        if collided_box:
            collided_box.kill()
        elif collided_box_laser:
            collided_box_laser.kill()
        power_up = random.randint(1,2)
        if infinet_laser:
            power_up = 2
        if power_up == 1:
            laser.rect.center = paddle.rect.center
            laser.rect.bottom = paddle.rect.bottom
            laser.laser_mover = True
        elif power_up == 2:
            lives += 1
    if infinet_chest:
        if infinet_chest_count >= 53:
            box_group.add(box)
            all_sprites.add(box)
            infinet_chest_count = 0
    pygame.display.flip()
pygame.quit()

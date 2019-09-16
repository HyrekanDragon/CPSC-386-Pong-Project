import pygame
import pygame.math
import sys
import time
import random
from pygame.locals import *

# Set up pygame
pygame.init()

# Set up window
W_WIDTH = 600
W_HEIGHT = 600
ws = pygame.display.set_mode((W_WIDTH, W_HEIGHT), 0, 32)

# Set up the fonts
font = pygame.font.SysFont(None, 48)
font2 = pygame.font.SysFont(None, 32)

# Set up Colors
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the game speed
SPEED = 5

# Set sounds
bounce_sound = pygame.mixer.Sound('pong.wav')
match_win = pygame.mixer.Sound('match win.wav')
match_lost = pygame.mixer.Sound('match lost.wav')
game_win = pygame.mixer.Sound('game win.wav')
game_lost = pygame.mixer.Sound('game lost.wav')


def vector2(velocity):
    v = pygame.Vector2()
    v[0] = velocity[0]
    v[1] = velocity[1]
    return v


class Paddle:
    def __init__(self, rect, clr, orientation, velocity=(0, 0)):
        self.rect_ = pygame.Rect(rect)
        self.color_ = Color(clr)
        self.orientation_ = orientation
        self.velocity_ = vector2(velocity)

    def __str__(self):
        return 'Box: clr={}, rect={}'.format(self.color_, self.rect_)

    def get_color(self):
        return self.color_

    def get_rect(self):
        return self.rect_

    def get_orientation(self):
        return self.orientation_

    def get_velocity(self):
        return self.velocity_

    def move_rect_v(self, velocity):
        self.rect_.top += velocity

    def move_rect_h(self, velocity):
        self.rect_.left += velocity


class Ball:
    def __init__(self, x_center, y_center, clr, velocity):
        self.circle_rect_ = pygame.draw.circle(ws, Color(clr), (x_center, y_center), 10, 0)
        self.center_ = [x_center, y_center]
        self.color_ = Color(clr)
        self.velocity_ = vector2(velocity)

    def get_color(self):
        return self.color_

    def get_rect(self):
        return self.circle_rect_

    def get_velocity(self):
        return self.velocity_

    def get_center(self):
        return self.center_

    def move_rect(self, velocity):
        self.circle_rect_.top += velocity


class Score:
    def __init__(self, score=0):
        self.score_ = score

    def get_score(self):
        return self.score_

    def increment(self):
        self.score_ += 1

    def reset(self):
        self.score_ = 0


p1 = Paddle(rect=(10, 250, 10, 100), clr='#FF0000', orientation='vertical')
p3 = Paddle(rect=(125, 10, 100, 10), clr='#FF0000', orientation='horizontal')
p5 = Paddle(rect=(125, 580, 100, 10), clr='#FF0000', orientation='horizontal')

p2 = Paddle(rect=(580, 250, 10, 100), clr='#0000FF', orientation='vertical')
p4 = Paddle(rect=(375, 10, 100, 10), clr='#0000FF', orientation='horizontal')
p6 = Paddle(rect=(375, 580, 100, 10), clr='#0000FF', orientation='horizontal')

players = (p1, p2, p3, p4, p5, p6)

ball = Ball(x_center=300, y_center=300, clr='#FFFFFF', velocity=(random.randint(1, 5), random.randint(1, 5)))

# Get paddle images
player_paddle_image = pygame.image.load('blue paddle.png')
player_stretched_image_h = pygame.transform.scale(player_paddle_image, (p4.get_rect().width, p4.get_rect().height))
player_stretched_image_v = pygame.transform.scale(player_paddle_image, (p2.get_rect().width, p2.get_rect().height))

computer_paddle_image = pygame.image.load('red paddle.png')
computer_stretched_image_h = pygame.transform.scale(computer_paddle_image, (p3.get_rect().width, p3.get_rect().height))
computer_stretched_image_v = pygame.transform.scale(computer_paddle_image, (p1.get_rect().width, p1.get_rect().height))

# Create Scores
c_score = Score()
c_win = Score()
p_score = Score()
p_win = Score()


def play():
    player_move_up = False
    player_move_down = False
    player_move_left = False
    player_move_right = False
    # Game Variables

    while True:
        p_won = False
        c_won = False
        answer = True
        # Check for the QUIT event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Check for players input
            if event.type == KEYDOWN:
                # Change the keyboard variables
                if event.key == K_w or event.key == K_UP:
                    player_move_down = False
                    player_move_up = True
                if event.key == K_s or event.key == K_DOWN:
                    player_move_up = False
                    player_move_down = True
                if event.key == K_a or event.key == K_LEFT:
                    player_move_right = False
                    player_move_left = True
                if event.key == K_d or event.key == K_RIGHT:
                    player_move_left = False
                    player_move_right = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_w or event.key == K_UP:
                    player_move_up = False
                if event.key == K_s or event.key == K_DOWN:
                    player_move_down = False
                if event.key == K_a or event.key == K_LEFT:
                    player_move_left = False
                if event.key == K_d or event.key == K_RIGHT:
                    player_move_right = False

        # Determine how computer will move
        br = ball.get_rect()
        c1 = p1.get_rect()
        c2 = p3.get_rect()

        if br.left > c2.left + 50:
            computer_move_right = True
            computer_move_left = False
        elif br.left < c2.left + 50:
            computer_move_right = False
            computer_move_left = True
        else:
            computer_move_right = False
            computer_move_left = False
        if br.top > c1.top:
            computer_move_down = True
            computer_move_up = False
        elif br.top < c1.top:
            computer_move_down = False
            computer_move_up = True
        else:
            computer_move_down = False
            computer_move_up = False

        # Draw the white background onto the surface.
        ws.fill(BACKGROUND)

        # Draw Net
        for x in range(0, W_HEIGHT, 10):
            pygame.draw.rect(ws, WHITE, pygame.Rect(299, x, 2, 5))

        r1 = p2.get_rect()
        r2 = p4.get_rect()

        # Move the Players
        if player_move_down and r1.bottom < W_HEIGHT:
            p2.move_rect_v(SPEED * 1.5)
        if player_move_up and r1.top > 0:
            p2.move_rect_v(-SPEED * 1.5)
        if player_move_right and r2.right < W_HEIGHT:
            p4.move_rect_h(SPEED)
            p6.move_rect_h(SPEED)
        if player_move_left and r2.left > 300:
            p4.move_rect_h(-SPEED)
            p6.move_rect_h(-SPEED)

        # Move the Computer
        if computer_move_down and c1.bottom < W_HEIGHT:
            p1.move_rect_v(SPEED/3)
        if computer_move_up and c1.top > 0:
            p1.move_rect_v(-SPEED/3)
        if computer_move_right and c2.right < 300:
            p3.move_rect_h(SPEED/4)
            p5.move_rect_h(SPEED/4)
        if computer_move_left and c2.left > 0:
            p3.move_rect_h(-SPEED/4)
            p5.move_rect_h(-SPEED/4)

        # Update players position
        for p in players:
            r = p.get_rect()
            c = p.get_color()
            pygame.draw.rect(ws, c, r)

        ws.blit(player_stretched_image_v, p2.get_rect())
        ws.blit(player_stretched_image_h, p4.get_rect())
        ws.blit(player_stretched_image_h, p6.get_rect())
        ws.blit(computer_stretched_image_v, p1.get_rect())
        ws.blit(computer_stretched_image_h, p3.get_rect())
        ws.blit(computer_stretched_image_h, p5.get_rect())

        # Move the ball
        bc = ball.get_color()
        bv = ball.get_velocity()
        bcenter = ball.get_center()

        bcenter[0] += bv[0]
        bcenter[1] += bv[1]
        br.left += bv[0]
        br.top += bv[1]

        # Collision detection
        if br.left < 0 or br.right > W_WIDTH:
            if br.left < 0:
                p_score.increment()
            else:
                c_score.increment()
            br.top = 295
            br.left = 295
            bcenter[0] = 300
            bcenter[1] = 300
            bv[0] = random.randint(-5, 5)
            bv[1] = random.randint(-5, 5)
        if br.top < 0 or br.bottom > W_HEIGHT:
            if bcenter[0] < 300:
                p_score.increment()
            else:
                c_score.increment()
            br.top = 295
            br.left = 295
            bcenter[0] = 300
            bcenter[1] = 300
            bv[0] = random.randint(-5, 5)
            bv[1] = random.randint(-5, 5)
        if bv[0] and bv[1] == 0:
            bv[0] = random.randint(-5, 5)
            bv[1] = random.randint(-5, 5)
        if bv[0] == 0 and bv[1] == 0:
            bv[0] = random.randint(-5, 5)
            bv[1] = random.randint(-5, 5)

        for p in players:
            r = p.get_rect()
            if br.colliderect(r):
                bounce_sound.play()
                if p.get_orientation() == 'vertical':
                    bv[0] *= -1
                    if bv[1] > 0:
                        bv[1] = random.randint(1, 5)
                    else:
                        bv[1] = random.randint(-5, -1)
                else:
                    bv[1] *= -1
                    if bv[0] > 0:
                        bv[0] = random.randint(1, 5)
                    else:
                        bv[0] = random.randint(-5, -1)

        # Check  if match won
        if p_score.get_score() >= 11 or c_score.get_score() >= 11:
            if p_score.get_score() - c_score.get_score() >= 2:
                match_win.play()
                p_score.reset()
                c_score.reset()
                p_win.increment()
            elif p_score.get_score() - c_score.get_score() <= -2:
                match_lost.play()
                p_score.reset()
                c_score.reset()
                c_win.increment()

        # Update ball position
        pygame.draw.circle(ws, bc, (int(bcenter[0]), int(bcenter[1])), 10, 0)

        # Check if game won:
        if p_win.get_score() == 3:
            p_won = True
            game_win.play()
        if c_win.get_score() == 3:
            c_won = True
            game_lost.play()

        # Draw Score Text
        textobj1 = font.render('%s-%s' % (c_score.get_score(), c_win.get_score()), 1, WHITE)
        textrect1 = textobj1.get_rect()
        textrect1.topleft = (0, 0)
        ws.blit(textobj1, textrect1)

        textobj2 = font.render('%s-%s' % (p_score.get_score(), p_win.get_score()), 1, WHITE)
        textrect2 = textobj2.get_rect()
        textrect2.topleft = (W_WIDTH-70, 0)
        ws.blit(textobj2, textrect2)

        if c_won or p_won:
            while answer:
                for event2 in pygame.event.get():
                    if event2.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event2.type == KEYDOWN:
                        if event2.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event2.key == K_y:
                            p_score.reset()
                            c_score.reset()
                            p_win.reset()
                            c_win.reset()
                            answer = False
                        if event2.key == K_n:
                            pygame.quit()
                            sys.exit()

                if p_won:
                    win_message = font2.render('YOU WON, CONGRATULATIONS', 1, WHITE)
                    win_rect = win_message.get_rect()
                    win_rect.topleft = (150, 200)
                    ws.blit(win_message, win_rect)
                elif c_won:
                    lose_message = font2.render('YOU LOST, PLEASE TRY AGAIN', 1, WHITE)
                    lose_rect = lose_message.get_rect()
                    lose_rect.topleft = (150, 200)
                    ws.blit(lose_message, lose_rect)

                play_again = font2.render('DO YOU WANT TO PLAY AGAIN? PRESS Y/N', 1, WHITE)
                play_rect = play_again.get_rect()
                play_rect.topleft = (75, 300)
                ws.blit(play_again, play_rect)

                pygame.display.update()
                time.sleep(0.01)

        pygame.display.update()
        time.sleep(0.01)


play()

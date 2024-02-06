# Importing all necessary modules
import pygame
from sys import exit
import random


# Creating Classes for the objects present in the game
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            'Game photos/playerplane.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 600))
        self.rectx = self.rect.x
        self.recty = self.rect.y
        self.r_c = 0
        self.l_c = 0
        self.shoot_sound = pygame.mixer.Sound('Game Audio/Player_shot.mp3')

    def render(self, h, k):
        wn.blit(self.image, (h, k))

    def movement(self, x, y):
        self.r_c = x
        self.l_c = y

    def shoot(self):
        self.shoot_sound.play()
        return Bullet('Game photos/bullet.png', self.rect.center[0], self.rect.center[1])

    def update(self):
        if self.rect.right <= 700:
            self.rect.right += self.r_c
        if self.rect.left >= 100:
            self.rect.left += self.l_c

    def restart(self):
        self.rect.right = 450


class Bot(pygame.sprite.Sprite):
    def __init__(self, pic, posx, posy):
        super().__init__()
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect(center=(posx, posy))
        self.shot_sound = pygame.mixer.Sound('Game Audio/Bot_shot.mp3')

    def create_bullet(self):
        self.shot_sound.play()
        return Bullet('Game photos/bullet_2.png', self.rect.center[0], self.rect.center[1])

    def destroy(self):
        self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture, px, py):
        super().__init__()
        self.image = pygame.image.load(picture).convert_alpha()
        self.rect = self.image.get_rect(center=(px, py))

    def update(self, tpe):
        self.rect.y += tpe

        if self.rect.y <= 50 or self.rect.y >= 700:
            self.kill()


class Button:
    def __init__(self, width, height, position):
        self.pressed = False

        self.rect = pygame.Rect(position, (width, height))
        self.top_colour = (209, 255, 0)

        self.text_surface = text_font3.render('Replay', True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.click_sound = pygame.mixer.Sound('Game Audio/click.mp3')

    def draw(self):
        pygame.draw.rect(wn, self.top_colour, self.rect, border_radius=12)
        wn.blit(self.text_surface, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.top_colour = (209, 241, 154)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.click_sound.play()
                    self.pressed = False
                    return True
        else:
            self.top_colour = (209, 255, 0)


# Functions necessary for game running
def display_score():
    score = pygame.time.get_ticks() - start_time
    score_surf = text_font2.render(
        f'Score: {score//1000}', False, (255, 255, 255))
    score_surf_rect = score_surf.get_rect(center=(90, 100))
    wn.blit(score_surf, score_surf_rect)
    return score


def collision_detect():
    pygame.sprite.groupcollide(bot_group, bullet_group, True, True)
    pygame.sprite.groupcollide(player_group, evil_bullet_group, True, False)


def game_state():
    if pygame.sprite.spritecollide(player, evil_bullet_group, False):
        game_over_sound.play()
        bot_group.empty()
        evil_bullet_group.empty()
        bullet_group.empty()
        player_group.add(player)
        return False
    else:
        return True


# Initialising Pygame and setting up the screen
pygame.init()
wn = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Space Invaders 2")
bg_surface = pygame.image.load('Game photos/bg.jpg').convert()

# Core attributes used in game
clk = pygame.time.Clock()
game_active = True
text_font2 = pygame.font.Font(None, 40)
text_font3 = pygame.font.Font(None, 50)
game_over_sound = pygame.mixer.Sound('Game Audio/game_over.mp3')
start_time = 0

# List of all bot types
bots = ['Game photos/bot_1.png', 'Game photos/bot_2.png',
        'Game photos/bot_3.png', 'Game photos/bot_4.png']

# Creating Title of Game
text_font = pygame.font.Font('game_font.otf', 60)
game_name = text_font.render('Space Invaders 2', False, (125, 253, 13))
game_name_rect = game_name.get_rect(center=(400, 40))

# Initialising the instance of the player
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

# Creating a group to store all instances of bots
bot_group = pygame.sprite.Group()

# Creating a group to store all instances of bullets
bullet_group = pygame.sprite.Group()
evil_bullet_group = pygame.sprite.Group()

# Instance of Replay button
game_button = Button(200, 50, (310, 550))

# Creating Custom events to make things take place at regular intervals
bot_gen_event = pygame.USEREVENT + 1
bot_shoot_event = pygame.USEREVENT + 2

pygame.time.set_timer(bot_gen_event, 2000)
pygame.time.set_timer(bot_shoot_event, 3500)

# Actual Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.movement(5, 0)
                elif event.key == pygame.K_LEFT:
                    player.movement(0, -5)
                elif event.key == pygame.K_SPACE:
                    bullet_group.add(player.shoot())
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.movement(0, 0)
                elif event.key == pygame.K_LEFT:
                    player.movement(0, 0)
            elif event.type == bot_gen_event:
                if len(bot_group) <= 6:
                    bot_group.add(Bot(random.choice(bots), random.randint(
                        100, 625), random.randint(200, 500)))
            elif event.type == bot_shoot_event:
                for bot in bot_group:
                    evil_bullet_group.add(bot.create_bullet())

        else:
            if game_button.check_click():
                game_active = True
                start_time = pygame.time.get_ticks()
                player.restart()

    if game_active:
        wn.blit(bg_surface, (0, 0))
        wn.blit(game_name, game_name_rect)

        bullet_group.draw(wn)
        bullet_group.update(-5)

        player_group.draw(wn)
        player_group.update()

        bot_group.draw(wn)
        bot_group.update()

        evil_bullet_group.draw(wn)
        evil_bullet_group.update(3)

        display_score()
        collision_detect()
        game_active = game_state()
        current_score = display_score()

    else:
        wn.blit(bg_surface, (0, 0))

        game_over_title = text_font.render('GAME OVER', False, (125, 253, 13))
        game_over_title_rect = game_over_title.get_rect(center=(400, 40))
        wn.blit(game_over_title, game_over_title_rect)

        final_message = text_font3.render(
            f'Score: {current_score//1000}', False, (255, 255, 255))
        final_message_rect = final_message.get_rect(center=(400, 300))
        wn.blit(final_message, final_message_rect)

        game_button.draw()

    pygame.display.update()
    clk.tick(60)

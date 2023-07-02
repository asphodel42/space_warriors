import pygame
import time
import emoji
from random import randint


class GameSprite(pygame.sprite.Sprite):
    """Main class for sprites"""
    def __init__(self, player_image, player_x, player_y, width, height, speed):  # Initialization
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load(
            player_image), (width, height))  # Sprite object

        self.speed = speed  # Speed

        # Object's hitbox
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # Draw a sprite 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    
class Player(GameSprite):
    # controls
    def update(self):
        global ammo_count
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < window_width - 105:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y > 600:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < window_height - 105:
            self.rect.y += self.speed
        if keys[pygame.K_r]:
            ammo_count = 6


    # Create a bullet that's moving up
    def fire(self):
        bullet = Bullet(image_bullet, self.rect.centerx, self.rect.y, 10, 60, 20)
        return bullet
    


class Alien(GameSprite):
    def update(self):
        global missed_aliens, finish, current_lives
        self.rect.y += self.speed
        # Disapear if crossed the edge of window
        if self.rect.y > window_height:
            self.rect.x = randint(100, window_width - 100)
            self.rect.y = 0
            missed_aliens += 1

        if self.rect.colliderect(ship.rect):
            current_lives -= 1
            print(current_lives)
            self.rect.x = randint(80, window_width-80)
            self.rect.y = -40
            

    def collision(self):
        global score_points
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                explosion_sound.play()
                bullet.kill()
                self.rect.x = randint(80, window_width-80)
                self.rect.y = -40
                score_points += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -100:
            self.kill()
        

# Assets
image_background = 'assets/background/galaxy.jpg'  # Background
image_ship = 'assets/sprites/space_ship_state.png'  # Player
image_bullet = 'assets/sprites/laser.png'  # Bullets
image_alien = 'assets/sprites/alien.png'  # Enemy
sound_music = 'assets/music/space.ogg'  # Music
sound_shoot = 'assets/music/shoot_sound.ogg'
sound_explosion = 'assets/music/explosion.ogg'  # Explosion
image_icon = 'assets/background/icon.png'  # Icon
font_name = "assets/font/Starjout.ttf"  # Font

# Vars
score_points = 0
missed_aliens = 0
ammo_count = 6
current_lives = 3  # Number of HP

finish = False
game = True

# Create a window
window_width, window_height = 1300, 800
pygame.display.set_caption("Space War")
pygame.display.set_icon(pygame.image.load(image_icon))
window = pygame.display.set_mode((window_width, window_height))

# Creating background
background = pygame.transform.scale(pygame.image.load(image_background), (window_width, window_height))

# Creating star ship
ship = Player(image_ship, 5, window_height-100, 120, 100, 15)
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()

# Creating aliens
for i in range(1, 6):
    alien = Alien(image_alien, randint(100, window_width-100), -40, 100, 100, randint(1, 4))
    aliens.add(alien)

# Music
pygame.mixer.init()
pygame.mixer.music.load(sound_music)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play()
shoot_sound = pygame.mixer.Sound(sound_shoot)
shoot_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(sound_explosion)
explosion_sound.set_volume(0.1)

# Label
pygame.font.init()
font = pygame.font.Font(font_name, 25)
font_finish = pygame.font.Font(None, 100)
lost = font_finish.render('YOU LOST', True, (120, 13, 31))
win = font_finish.render('YOU WIN', True, (32, 252, 3))


while game:  # Game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN and ammo_count > 0:
            ammo_count -= 1
            bullets.add(ship.fire())
            shoot_sound.play()

    
    if not finish:
        # Render fonts
        score = font.render(f'Score: {score_points}', True, (255, 232, 31))
        missed = font.render(f'Missed: {missed_aliens}', True, (255, 232, 31))
        ammo = font.render(f'Ammo: {int(ammo_count)}', True, (255, 232, 31))
        hp = font.render(f'{current_lives}', True, (255, 232, 31))
        
        # Update background
        window.blit(background, (0,0))  # Background
        window.blit(score, (10, 0))  # Score label
        window.blit(missed, (10, 25))  # Missed label
        window.blit(ammo, (window_width - 150, window_height - 50))  # Ammo label
        window.blit(hp, (window_width - 50, 15))  # HP Label

        # Update movement
        for alien in aliens:
            alien.collision()

        bullets.update()
        aliens.update()
        ship.update()

        # Sprites draw
        bullets.draw(window)
        aliens.draw(window)
        ship.reset()

        # Losing
        if current_lives <= 0:
            finish = True
            window.blit(lost, (450, 450))
        if missed_aliens >= 6:
            finish = True
            window.blit(lost, (450, 450))

        # Winning
        if score_points >= 30:
            finish = True
            window.blit(win, (500, 400))
    
    pygame.display.update()

    pygame.time.delay(30)
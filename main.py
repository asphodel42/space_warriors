import pygame

# Main class for sprites
class GameSprite(pygame.sprite.Sprite):
    # Initialization
    def __init__(self, player_image, player_x, player_y, width, height, speed):
        pygame.sprite.Sprite.__init__(self)

        # Sprite object
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))

        # Speed
        self.speed = speed

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < window_width - 80:
            self.rect.x += self.speed

    # Create a bullet that's moving up
    def fire(self):
        pass


# Pictures
image_background = 'assets/background/galaxy.jpg'  # Background
image_ship = 'assets/sprites/rocket.png'  # Player

font_name = "assets/font/Starjout.ttf"

# Create a window
window_width, window_height = 700, 500
pygame.display.set_caption("Space War")
window = pygame.display.set_mode((window_width, window_height))

# Creating background
background = pygame.transform.scale(pygame.image.load(image_background), (window_width, window_height))

# Creating star ship
ship = Player(image_ship, 5, window_height-100, 80, 100, 10)


finish = False
game = True
score = 0
missed = 0

# Music
pygame.mixer.init()
pygame.mixer.music.load("assets/music/space.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound("assets/music/fire.ogg")

# Label
pygame.font.init()
font = pygame.font.Font(font_name, 25)
score = font.render(f'Score: {score}', True, (255, 232, 31))
missed = font.render(f'Missed: {missed}', True, (255, 232, 31))

while game:  # Game loop
    # 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if not finish:
        # Update background
        window.blit(background, (0,0))
        window.blit(score, (10, 0))
        window.blit(missed, (10, 25))

        # Sprites movement
        ship.update()

        # Update movement
        ship.reset()

        pygame.display.update()

    pygame.time.delay(30)
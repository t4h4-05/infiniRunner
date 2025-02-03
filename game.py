import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Procedural Generation")

class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT // 2 - self.height // 2
        self.base_speed = 1
        self.speed_multiplier = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def move(self, keys):
        current_speed = self.base_speed * self.speed_multiplier
        
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= current_speed
        if keys[pygame.K_RIGHT] and self.x < WINDOW_WIDTH - self.width:
            self.x += current_speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= current_speed
        if keys[pygame.K_DOWN] and self.y < WINDOW_HEIGHT - self.height:
            self.y += current_speed
            
        # Speed control with SHIFT and CTRL
        if keys[pygame.K_LSHIFT]:
            self.speed_multiplier = 2.0
        elif keys[pygame.K_LCTRL]:
            self.speed_multiplier = 0.5
        else:
            self.speed_multiplier = 1.0
        
        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def collides_with(self, platform):
        return self.rect.colliderect(platform.rect)

class Platform:
    def __init__(self, y):
        self.width = random.randint(100, 300)
        self.height = 20
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = y
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

# Initialize font for distance display
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

# Game objects
player = Player()
platforms = []
platform_spacing = 200  # Increased initial spacing
scroll_speed = 0.2  # Slower initial speed
distance = 0
base_platform_count = 4  # Fewer initial platforms

def reset_game():
    # Reset game objects and variables
    player = Player()
    platforms = []
    for i in range(0, WINDOW_HEIGHT + platform_spacing, platform_spacing):
        platforms.append(Platform(i))
    return player, platforms, 0.2, 0  # Returns player, platforms, scroll_speed, distance

# Game loop
running = True
game_over = False
player, platforms, scroll_speed, distance = reset_game()

while running:
    scroll_speed *= 1.000001  # Gradually increase speed
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keyboard input and move player
    keys = pygame.key.get_pressed()
    
    # Check for restart
    if game_over or keys[pygame.K_r]:
        game_over = False
        player, platforms, scroll_speed, distance = reset_game()
        continue
        
    player.move(keys)
    
    # Update platforms and distance
    distance += scroll_speed
    extra_platforms = int(distance // 1000)  # Add a platform every 1000 pixels
    desired_platform_count = extra_platforms
    
    # Update platforms
    for platform in platforms:
        platform.y += scroll_speed
        if platform.y > WINDOW_HEIGHT:
            # Reset platform to top when it goes below screen
            platform.y = -platform.height
            platform.x = random.randint(0, WINDOW_WIDTH - platform.width)
            platform.width = random.randint(100, 300)
        
        # Check for collision with player
        if player.collides_with(platform):
            game_over = True
    
    # Add more platforms if needed
    while len(platforms) < desired_platform_count:
        # Find highest platform
        highest_y = min(p.y for p in platforms)
        # Add new platform above it
        platforms.append(Platform(highest_y - platform_spacing))
    
    # Clear the screen
    screen.fill((0, 0, 0))  # Black background
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen)
    
    # Draw the player
    player.draw(screen)
    
    # Draw distance counter
    distance_text = font.render(f'Distance: {int(distance*0.1)}', True, (255, 255, 255))
    screen.blit(distance_text, (WINDOW_WIDTH - 200, 10))
    
    # Draw game over text if game is over
    if game_over:
        game_over_text = font.render('Game Over! Press R to restart', True, (255, 0, 0))
        screen.blit(game_over_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2))
    
    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()

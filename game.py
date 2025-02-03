import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Procedural Generation with Restart Button")

# Initialize font for distance display and button text
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

class Player:
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height
        # Start in the center of the window
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT // 2 - self.height // 2
        self.base_speed = 1  # Movement speed set to 1
        self.speed_multiplier = 1.0
        # Create a surface with per-pixel alpha and fill with light blue
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((173, 216, 230))  # Light blue color
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self, keys):
        current_speed = self.base_speed * self.speed_multiplier

        # Basic movement with boundary checks
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= current_speed
        if keys[pygame.K_RIGHT] and self.x < WINDOW_WIDTH - self.width:
            self.x += current_speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= current_speed
        if keys[pygame.K_DOWN] and self.y < WINDOW_HEIGHT - self.height:
            self.y += current_speed

        # Speed modification: LEFT SHIFT to speed up, LEFT CTRL to slow down
        if keys[pygame.K_LSHIFT]:
            self.speed_multiplier = 2.0
        elif keys[pygame.K_LCTRL]:
            self.speed_multiplier = 0.5
        else:
            self.speed_multiplier = 1.0

        # Update the player's rectangle position
        self.rect.topleft = (self.x, self.y)
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def collides_with(self, platform):
        # Calculate the offset between the player and platform masks
        offset = (int(platform.x - self.x), int(platform.y - self.y))
        return self.mask.overlap(platform.mask, offset) is not None

class Platform:
    def __init__(self, y):
        # Randomize width and height for an irregular look
        self.width = random.randint(100, 300)
        self.height = random.randint(15, 40)
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = y
        self.color = (255, 105, 180)  # Pink color
        # Random border radius for rounded corners
        self.border_radius = random.randint(5, self.height // 2)
        # Create a surface with per-pixel alpha
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), border_radius=self.border_radius)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
    
    def draw(self, screen):
        # Draw the platform onto the screen and update its rectangle position
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

# Global parameters for initial difficulty settings
platform_spacing = 200      # Spacing between platforms
initial_scroll_speed = 0.1  # Slower starting scroll speed
base_platform_count = 4     # Spawn 4 obstacles immediately

def reset_game():
    """Reset and return the initial game objects and variables."""
    player = Player(width=50, height=50)
    # Define a safe zone around the player's spawn so obstacles don't appear there
    safe_zone = player.rect.inflate(100, 100)
    platforms = []
    # Spawn obstacles immediately across the vertical span
    for i in range(-platform_spacing, WINDOW_HEIGHT, platform_spacing):
        plat = Platform(i)
        # Only adjust platforms in the visible region
        if plat.y >= 0 and plat.rect.colliderect(safe_zone):
            attempts = 0
            # Reposition horizontally until it no longer collides with the safe zone.
            while plat.rect.colliderect(safe_zone) and attempts < 10:
                plat.x = random.randint(0, WINDOW_WIDTH - plat.width)
                plat.rect.x = plat.x
                attempts += 1
            # If still colliding after several attempts, reposition vertically away from the player's safe zone.
            if plat.rect.colliderect(safe_zone):
                plat.y = safe_zone.bottom + random.randint(10, 50)
                plat.rect.y = plat.y
        platforms.append(plat)
    scroll_speed = initial_scroll_speed
    distance = 0
    return player, platforms, scroll_speed, distance

# Variables for restart delay handling (in milliseconds)
RESTART_DELAY = 500
last_restart_time = 0

running = True
game_over = False
player, platforms, scroll_speed, distance = reset_game()

while running:
    # Gradually increase the scroll speed if the game is active
    if not game_over:
        scroll_speed *= 1.00001

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Only allow restart actions when the game is over
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_restart_time >= RESTART_DELAY:
                        player, platforms, scroll_speed, distance = reset_game()
                        game_over = False
                        last_restart_time = current_time
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = event.pos
                    restart_button_rect = pygame.Rect(WINDOW_WIDTH - 150, 10, 140, 40)
                    if restart_button_rect.collidepoint(mouse_pos):
                        current_time = pygame.time.get_ticks()
                        if current_time - last_restart_time >= RESTART_DELAY:
                            player, platforms, scroll_speed, distance = reset_game()
                            game_over = False
                            last_restart_time = current_time

    keys = pygame.key.get_pressed()
    if not game_over:
        player.move(keys)

        # Update platforms and the distance counter
        distance += scroll_speed
        # Increase obstacles every 100 units of distance (first extra obstacle appears when displayed distance > 10)
        extra_platforms = int(distance // 100)
        desired_platform_count = base_platform_count + extra_platforms

        for platform in platforms:
            platform.y += scroll_speed
            if platform.y > WINDOW_HEIGHT:
                # Recycle the platform: spawn it well above view so it scrolls in gradually.
                platform.y = -platform.height - random.randint(20, 100)
                platform.x = random.randint(0, WINDOW_WIDTH - platform.width)
                platform.width = random.randint(100, 300)
                platform.height = random.randint(15, 40)
                platform.border_radius = random.randint(5, platform.height // 2)
                platform.image = pygame.Surface((platform.width, platform.height), pygame.SRCALPHA)
                pygame.draw.rect(platform.image, platform.color, (0, 0, platform.width, platform.height), border_radius=platform.border_radius)
                platform.mask = pygame.mask.from_surface(platform.image)
                platform.rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
            
            # Collision detection using pixel-perfect mask overlap
            if player.collides_with(platform):
                game_over = True

        # Add new platforms if needed based on distance traveled
        while len(platforms) < desired_platform_count:
            if platforms:
                highest_y = min(p.y for p in platforms)
            else:
                highest_y = -platform_spacing  # Fallback base if no platforms exist
            platforms.append(Platform(highest_y - platform_spacing))

    # Set a white background
    screen.fill((255, 255, 255))
    
    # Draw obstacles and the player
    for platform in platforms:
        platform.draw(screen)
    player.draw(screen)
    
    # Display the distance counter in the top right (in black)
    distance_text = font.render(f'Distance: {int(distance*0.01)}', True, (0, 0, 0))
    screen.blit(distance_text, (WINDOW_WIDTH - 220, 10))
    
    # Only display the restart button when the game is over
    if game_over:
        restart_button_rect = pygame.Rect(WINDOW_WIDTH - 150, 10, 140, 40)
        pygame.draw.rect(screen, (200, 200, 200), restart_button_rect)
        button_text = font.render("Restart", True, (0, 0, 0))
        text_rect = button_text.get_rect(center=restart_button_rect.center)
        screen.blit(button_text, text_rect)
        # Display game over text as well
        game_over_text = font.render("Game Over! Press R to restart", True, (255, 0, 0))
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 170, WINDOW_HEIGHT // 2))
    
    pygame.display.flip()

pygame.quit()

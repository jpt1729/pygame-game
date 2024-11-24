import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 854
SCREEN_HEIGHT = 480

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame RPG")

# Load assets
map_image = pygame.image.load("assets/map.png")
main_character_image = pygame.image.load("assets/char.png")
main_character_image = pygame.transform.scale(main_character_image, (50, 50))  # Resize if needed

# Character class
class NPC:
    def __init__(self, x, y, image_path, dialog):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize NPC
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dialog = dialog

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def interact(self):
        # Display the dialog
        return self.dialog

# Create an NPC
npc = NPC(400, 300, "assets/npc.png", "Hello, adventurer! Welcome to the world of Pygame.")

# Main character setup
main_character = main_character_image
main_character_rect = main_character.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
character_speed = 5

# Dialog system
def display_dialog(surface, text):
    font = pygame.font.Font(None, 36)
    dialog_box = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 50)
    pygame.draw.rect(surface, WHITE, dialog_box)
    pygame.draw.rect(surface, BLACK, dialog_box, 2)
    text_surface = font.render(text, True, BLACK)
    surface.blit(text_surface, (dialog_box.x + 10, dialog_box.y + 10))

# Game loop
clock = pygame.time.Clock()
running = True
show_dialog = False
dialog_text = ""

while running:
    screen.fill(WHITE)
    screen.blit(map_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and show_dialog:
            # Close dialog on space press
            show_dialog = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        main_character_rect.y -= character_speed
    if keys[pygame.K_DOWN]:
        main_character_rect.y += character_speed
    if keys[pygame.K_LEFT]:
        main_character_rect.x -= character_speed
    if keys[pygame.K_RIGHT]:
        main_character_rect.x += character_speed

    # Interaction detection
    if main_character_rect.colliderect(npc.rect):
        show_dialog = True
        dialog_text = npc.interact()

    # Draw everything
    screen.blit(main_character, main_character_rect)
    npc.draw(screen)

    if show_dialog:
        display_dialog(screen, dialog_text)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

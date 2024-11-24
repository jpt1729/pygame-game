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
map_image = pygame.image.load("map.png")
main_character_image = pygame.image.load("main_character.png")
main_character_image = pygame.transform.scale(main_character_image, (50, 50))  # Resize if needed

# Character class
class NPC:
    def __init__(self, x, y, image_path, dialog, responses):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize NPC
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dialog = dialog
        self.responses = responses  # A list of responses for the player

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def interact(self):
        return self.dialog, self.responses

# Create an NPC
npc = NPC(400, 300, "npc.png", "Hello, adventurer! What brings you here?", [
    "1. I'm here to explore the world.",
    "2. I'm looking for treasure hidden in the forest.",
    "3. Just passing by. Nice to meet you!"
])

# Main character setup
main_character = main_character_image
main_character_rect = main_character.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
character_speed = 5

# Dialog system
def display_dialog(surface, text, options, font):
    dialog_box = pygame.Rect(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 150)
    pygame.draw.rect(surface, WHITE, dialog_box)
    pygame.draw.rect(surface, BLACK, dialog_box, 2)

    # Render dialog text with wrapping
    wrapped_text = wrap_text(text, font, dialog_box.width - 20)
    for i, line in enumerate(wrapped_text):
        text_surface = font.render(line, True, BLACK)
        surface.blit(text_surface, (dialog_box.x + 10, dialog_box.y + 10 + i * 30))

    # Render response options
    for i, option in enumerate(options):
        option_surface = font.render(option, True, BLACK)
        surface.blit(option_surface, (dialog_box.x + 10, dialog_box.y + 70 + len(wrapped_text) * 30 + i * 30))

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# Game loop
clock = pygame.time.Clock()
running = True
show_dialog = False
dialog_text = ""
dialog_options = []
player_response = ""
response_action = None

font = pygame.font.Font(None, 28)  # Font for dialog

while running:
    screen.fill(WHITE)
    screen.blit(map_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if show_dialog:
                # Handle dialog options
                if event.key == pygame.K_1 and len(dialog_options) > 0:
                    player_response = dialog_options[0]
                    response_action = "exploring"
                elif event.key == pygame.K_2 and len(dialog_options) > 1:
                    player_response = dialog_options[1]
                    response_action = "treasure hunting"
                elif event.key == pygame.K_3 and len(dialog_options) > 2:
                    player_response = dialog_options[2]
                    response_action = "just passing"

                # Close dialog when Enter is pressed
                if event.key == pygame.K_RETURN:
                    show_dialog = False
                    player_response = ""  # Reset player response
            elif event.key == pygame.K_RETURN and not show_dialog:
                # Close player response display
                player_response = ""

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
    if main_character_rect.colliderect(npc.rect) and not show_dialog:
        show_dialog = True
        dialog_text, dialog_options = npc.interact()

    # Draw everything
    screen.blit(main_character, main_character_rect)
    npc.draw(screen)

    if show_dialog:
        display_dialog(screen, dialog_text, dialog_options, font)
    elif player_response:
        # Display the player's chosen response and trigger an action
        response_box = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 50)
        pygame.draw.rect(screen, WHITE, response_box)
        pygame.draw.rect(screen, BLACK, response_box, 2)
        response_surface = font.render(f"You chose: {player_response} ({response_action})", True, BLACK)
        screen.blit(response_surface, (response_box.x + 10, response_box.y + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

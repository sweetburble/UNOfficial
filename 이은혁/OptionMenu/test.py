import pygame

# Define the actions and their default keys
actions = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Configure Keys")

# Set up the font
font = pygame.font.SysFont(None, 25)

# Define a function to display the current key for each action
def display_keys():
    y = 50
    for action, key in actions.items():
        text = font.render(f"{action}: {pygame.key.name(key)}", True, (255, 255, 255))
        gameDisplay.blit(text, (50, y))
        y += 25

# Define a function to update the key for an action
def update_key(action):
    updating = True
    while updating:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                actions[action] = event.key
                updating = False

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            # Update the key for the corresponding action
            if event.key == pygame.K_u:
                update_key("up")
            elif event.key == pygame.K_d:
                update_key("down")
            elif event.key == pygame.K_l:
                update_key("left")
            elif event.key == pygame.K_r:
                update_key("right")

    # Display the current keys
    gameDisplay.fill((0, 0, 0))
    display_keys()
    pygame.display.update()

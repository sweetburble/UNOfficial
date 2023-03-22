import pygame
pygame.init()

# Set up display
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Settings Menu")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Define fonts
font = pygame.font.SysFont("Arial", 30)

# Define menu items
menu_items = ["Resolution", "Fullscreen", "Volume", "Back"]
selected_item = 0

# Main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                if selected_item == 0:
                    # Resolution menu
                    pass
                elif selected_item == 1:
                    # Fullscreen menu
                    pass
                elif selected_item == 2:
                    # Volume menu
                    pass
                elif selected_item == 3:
                    # Back to main menu
                    running = False

    # Clear screen
    screen.fill(white)

    # Render menu items
    for i, item in enumerate(menu_items):
        text = font.render(item, True, black if i != selected_item else gray)
        text_rect = text.get_rect()
        text_rect.center = (screen_width / 2, screen_height / 2 - len(menu_items) * 15 + i * 30)
        screen.blit(text, text_rect)

    # Update display
    pygame.display.flip()

# Clean up
pygame.quit()
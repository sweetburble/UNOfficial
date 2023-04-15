import pygame
import time

pygame.init()

# Set up the timer font
font = pygame.font.SysFont("Arial", 50)

# Set up the timer variables
start_time = time.time()
elapsed_time = 0
max_time = 10 # maximum time in seconds

# Set up the Pygame window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("UNO Timer")

# Main game loop
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate elapsed time and update the timer text
    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(str(max_time - elapsed_time), True, (255, 255, 255))

    # Draw the timer text on the screen
    screen.fill((0, 0, 0))
    screen.blit(timer_text, (350, 250))

    # Check if the time has run out
    if elapsed_time > max_time:
        running = False

    # Update the display
    pygame.display.flip()

# End of game loop
pygame.quit()
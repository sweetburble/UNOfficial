import pygame

# def move_image(screen, image, background_image, start_pos, end_pos, duration, background=None):
#     """
#     Move an image from start_pos to end_pos with animation
#     :param screen: Pygame screen object
#     :param image: Pygame surface object representing the image to be moved
#     :param start_pos: Tuple representing the starting position of the image (x, y)
#     :param end_pos: Tuple representing the ending position of the image (x, y)
#     :param duration: Duration of the animation in milliseconds
#     :param background: Optional Pygame surface object representing the background image of the screen
#     """
#     # Calculate the distance to move in each frame
#     distance_x = (end_pos[0] - start_pos[0]) / duration
#     distance_y = (end_pos[1] - start_pos[1]) / duration

#     # Get the current time
#     start_time = pygame.time.get_ticks()

#     # Loop until the duration has elapsed
#     while pygame.time.get_ticks() - start_time < duration:
#         # Create a new background surface with the same size as the screen
#         if background is None:
#             background = pygame.Surface(screen.get_size())
#             background.fill((0, 0, 0))

#         # Blit the background image to the background surface
#         background.blit(background_image, (0, 0))

#         # Calculate the position of the image in this frame
#         elapsed_time = pygame.time.get_ticks() - start_time
#         current_pos_x = int(start_pos[0] + (elapsed_time * distance_x))
#         current_pos_y = int(start_pos[1] + (elapsed_time * distance_y))

#         # Blit the moving image to the background surface at the current position
#         background.blit(image, (current_pos_x, current_pos_y))

#         # Blit the entire background surface to the screen
#         screen.blit(background, (0, 0))

#         # Update the screen
#         pygame.display.flip()

#         # Wait for a short amount of time to control the animation speed
#         pygame.time.wait(10)

# def move_image(screen, image, start_pos, end_pos, duration):
#     """
#     Move an image from start_pos to end_pos with animation
#     :param screen: Pygame screen object
#     :param image: Pygame surface object representing the image to be moved
#     :param start_pos: Tuple representing the starting position of the image (x, y)
#     :param end_pos: Tuple representing the ending position of the image (x, y)
#     :param duration: Duration of the animation in milliseconds
#     """
#     # Calculate the distance to move in each frame
#     distance_x = (end_pos[0] - start_pos[0]) / duration
#     distance_y = (end_pos[1] - start_pos[1]) / duration

#     # Get the current time
#     start_time = pygame.time.get_ticks()

#     # Store the current position of the image
#     current_pos = start_pos

#     # Loop until the duration has elapsed
#     while pygame.time.get_ticks() - start_time < duration:
#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return
#             elif event.type == pygame.MOUSEMOTION:
#                 # Get the position of the mouse cursor
#                 mouse_pos = pygame.mouse.get_pos()
#                 # Check if the mouse is inside the bounds of the image
#                 if image.get_rect().move(current_pos).collidepoint(mouse_pos):
#                     # Move the image to the current position of the mouse cursor
#                     current_pos = (mouse_pos[0] - image.get_width() / 2, mouse_pos[1] - image.get_height() / 2)

#         # Reset the current position of the image if the mouse is not hovering over it
#         if not image.get_rect().move(current_pos).collidepoint(pygame.mouse.get_pos()):
#             current_pos = start_pos

#         # Clear the screen
#         screen.fill((0, 0, 0))

#         # Calculate the position of the image in this frame
#         elapsed_time = pygame.time.get_ticks() - start_time
#         current_pos_x = int(current_pos[0])
#         current_pos_y = int(current_pos[1])

#         # Blit the moving image to the screen at the current position
#         screen.blit(image, (current_pos_x, current_pos_y))

#         # Update the screen
#         pygame.display.flip()

#         # Wait for a short amount of time to control the animation speed
#         pygame.time.wait(10)d

# Initialize Pygame
pygame.init()

# Set the screen size
screen_size = (800, 600)

# Create the Pygame screen
screen = pygame.display.set_mode(screen_size)

# Load the image to be moved
image = pygame.image.load("./images/Back_inverted.png")
background_image = pygame.image.load("./images/background.png")


# Set the starting and ending positions of the image
start_pos = (100, 100)
end_pos = (500, 400)

# Set the duration of the animation in milliseconds
duration = 2000

# Call the move_image function to move the image
move_image(screen, image, start_pos, end_pos, duration)

# Quit Pygame when finished
pygame.quit()
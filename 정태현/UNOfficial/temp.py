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
#     # distance_x = (end_pos[0] - start_pos[0]) / duration
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
#         current_pos_x = int(start_pos[0])
#         current_pos_y = int(start_pos[1] + (elapsed_time * distance_y))

#         # Blit the moving image to the background surface at the current position
#         background.blit(image, (current_pos_x, current_pos_y))

#         # Blit the entire background surface to the screen
#         screen.blit(background, (0, 0))

#         # Update the screen
#         pygame.display.flip()

#         # Wait for a short amount of time to control the animation speed
#         pygame.time.wait(10)

# # Initialize Pygame
# pygame.init()

# # Set the screen size
# screen_size = (1000, 600)

# # Create the Pygame screen
# screen = pygame.display.set_mode(screen_size)

# # Load the image to be moved
# image = pygame.image.load("./images/Back_inverted.png")
# background_image = pygame.image.load("./images/background.png")


# # Set the starting and ending positions of the image
# start_pos = (100, 400)
# end_pos = (100, 300)

# # Set the duration of the animation in milliseconds
# duration = 500

# print(pygame.time.get_ticks())
# print(pygame.time.Clock())

# # Call the move_image function to move the image
# move_image(screen, image, background_image, start_pos, end_pos, duration)

# # Quit Pygame when finished
# pygame.quit()


# ============================================================
def move_card(ess, uno, img, card, screen, image, background_image, duration):
    """
    Move an image from start_pos to end_pos with animation
    :param screen: Pygame screen object
    :param image: Pygame surface object representing the image to be moved
    :param start_pos: Tuple representing the starting position of the image (x, y)
    :param end_pos: Tuple representing the ending position of the image (x, y)
    :param duration: Duration of the animation in milliseconds
    :param background: Optional Pygame surface object representing the background image of the screen
    """
    # Calculate the distance to move in each frame
    # distance_x = (end_pos[0] - start_pos[0]) / duration
    # distance_y = (end_pos[1] - start_pos[1]) / duration
    distance_y = 100 / duration

    # Get the current time
    start_time = pygame.time.get_ticks()

    # while 시작에서 500 tick이 지나면 while 종료
    while pygame.time.get_ticks() - start_time < duration:
        # Create a new background surface with the same size as the screen
        if background is None:
            background = pygame.Surface(screen.get_size())
            background.fill((0, 0, 0))

        # Blit the background image to the background surface
        background.blit(background_image, (0, 0))

        # Calculate the position of the image in this frame
        elapsed_time = pygame.time.get_ticks() - start_time
        current_pos_x = int(start_pos[0])
        current_pos_y = int(start_pos[1] + (elapsed_time * distance_y))

        # Blit the moving image to the background surface at the current position
        background.blit(image, (current_pos_x, current_pos_y))

        # Blit the entire background surface to the screen
        screen.blit(background, (0, 0))

        # Update the screen
        pygame.display.u()

        # Wait for a short amount of time to control the animation speed
        pygame.time.wait(10)
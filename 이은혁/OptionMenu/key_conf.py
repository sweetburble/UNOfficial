import pygame

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up fonts
font = pygame.font.Font(None, 36)
longerfonts=pygame.font.Font(None,26)

# Define menu items
setting_items = {"size":0,
                 "color_change":0,
                 "up":0,
                 "down":0,
                 "right":0,
                 "left":0,
                 "select":0}

with open('save.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(':')
        if key in setting_items:
            setting_items[key] = value
        else:
            pass


# Set up the screen
if setting_items["size"] == 'large':
    screen_width = 1400
    screen_height = 900
    screen = pygame.display.set_mode([screen_width, screen_height])
elif setting_items["size"] == 'medium':
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode([screen_width, screen_height])
elif setting_items["size"] == 'small':
    screen_width = 700
    screen_height = 500
    screen = pygame.display.set_mode([screen_width, screen_height])
   

pygame.display.set_caption("Game Settings Menu")

#현재 어떤 옵션을 선택했는지
selected_item = 0

# Set up text objects
title_text = font.render("Key Configure", True, WHITE)
title_rect = title_text.get_rect(center=(screen_width//2, screen_height//7))

up_text = font.render("UP", True, WHITE)
up_rect = up_text.get_rect(center=(screen_width//2, 2*screen_height//7))

left_text = font.render("LEFT", True, WHITE)
left_rect = left_text.get_rect(center=(screen_width//3, 3*screen_height//7))

right_text = font.render("RIGHT", True, WHITE)
right_rect = right_text.get_rect(center=(2*screen_width//3, 3*screen_height//7))

down_text = font.render("DOWN", True, WHITE)
down_rect = down_text.get_rect(center=(screen_width//2, 4*screen_height//7))

select_text = font.render("ENTER",True,WHITE)
select_rect = select_text.get_rect(center=(screen_width//3,5*screen_height//7))

mouse_text = font.render("Enable Mouse",True,WHITE)
mouse_rect = mouse_text.get_rect(center=(2*screen_width//3,5*screen_height//7))

back_text = font.render("Back", True, WHITE)
back_rect = back_text.get_rect(center=(screen_width//3, 6*screen_height//7))

main_text = font.render("Main Menu",True,WHITE)
main_rect = main_text.get_rect(center=(2*screen_width//3,6*screen_height//7))


# Game loop
done = False
with open('save.txt','r') as f:
    saves=f.readlines()
with open('default.txt','r')as fdef:
    defaults=fdef.readlines()
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type==pygame.KEYDOWN:    
            if event.key==pygame.K_RETURN: #결정의 경우
                pass                    
            else: #옮기기의 경우
                if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                    if selected_item==2 or selected_item==6 or selected_item==8:
                        selected_item+=1
                    elif selected_item==3 or selected_item==7 or selected_item==9:
                        selected_item-=1
                else:
                    if event.key==pygame.K_DOWN:
                        if selected_item>=8:
                            selected_item=0
                        elif selected_item==3:
                            selected_item+=1
                        else:
                            selected_item+=2
                    elif event.key==pygame.K_UP:
                        if selected_item==0:
                            selected_item=8
                        elif selected_item==3 or selected_item==7:
                            selected_item-=3
                        else:
                            selected_item-=2
                
    # Fill the screen
    screen.fill(BLACK)
    
    # Draw text objects
    screen.blit(title_text, title_rect)
    screen.blit(up_text, up_rect)
    screen.blit(left_text, left_rect)
    screen.blit(right_text, right_rect)
    screen.blit(down_text, down_rect)
    screen.blit(select_text, select_rect)
    screen.blit(mouse_text,mouse_rect)
    screen.blit(back_text,back_rect)
    screen.blit(main_text,main_rect)

    # Highlight selected difficulty
    if selected_item==0:
        pygame.draw.rect(screen, WHITE, up_rect, 3)
    elif selected_item==2:
        pygame.draw.rect(screen, WHITE, left_rect, 3)
    elif selected_item==3:
        pygame.draw.rect(screen, WHITE, right_rect, 3)
    elif selected_item==4:
        pygame.draw.rect(screen, WHITE, down_rect, 3)    
    elif selected_item==6:
        pygame.draw.rect(screen, WHITE, select_rect, 3)
    elif selected_item==7:
        pygame.draw.rect(screen, WHITE, mouse_rect, 3)
    elif selected_item==8:
        pygame.draw.rect(screen, WHITE, back_rect, 3)
    elif selected_item==9:
        pygame.draw.rect(screen, WHITE, main_rect, 3)    
    # Update the screen
    pygame.display.update()  
    
    

# Quit pygame
pygame.quit()
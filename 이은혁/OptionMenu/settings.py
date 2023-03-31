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
title_text = font.render("Game Settings", True, WHITE)
title_rect = title_text.get_rect(center=(screen_width//2, screen_height//7))

screensize_text = font.render("Size of Screen:", True, WHITE)
screensize_rect = screensize_text.get_rect(center=(screen_width//5, 2*screen_height//7))

small_text = font.render("Small", True, WHITE)
small_rect = small_text.get_rect(center=(2*screen_width//5, 2*screen_height//7))

medium_text = font.render("Medium", True, WHITE)
medium_rect = medium_text.get_rect(center=(3*screen_width//5, 2*screen_height//7))

large_text = font.render("Large", True, WHITE)
large_rect = large_text.get_rect(center=(4*screen_width//5, 2*screen_height//7))

keycon_text = font.render("Key Configuration",True,WHITE)
keycon_rect = keycon_text.get_rect(center=(screen_width//2,3*screen_height//7))

altcol_text = font.render("Alternative Colors",True,WHITE)
altcol_rect=altcol_text.get_rect(center=(screen_width//2,4*screen_height//7))

reset_text = font.render("RESET ALL SETTINGS",True,WHITE)
reset_rect = reset_text.get_rect(center=(screen_width//2,5*screen_height//7))

back_text = font.render("Back", True, WHITE)
back_rect = back_text.get_rect(center=(screen_width//2, 6*screen_height//7))

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
                if selected_item==0:
                    saves[0]='small\n'
                    #만약 즉시 적용으로 수정할 거라면 if event.type == pygame.VIDEORESIZE: 를 좀 사용해보면 좋겠다.
                elif selected_item==0.1:
                    saves[0]='medium\n'
                elif selected_item==0.2:
                    saves[0]='large\n'
                elif selected_item==1:
                    #keyconfiguration으로 들어감
                    pass
                elif selected_item==2:
                    if saves[1].startswith('original'):
                        saves[1]='alternative\n'
                    else:
                        saves[1]='original\n'
                elif selected_item==3:
                    with open('save.txt','w')as f:
                        f.writelines(defaults)
                    saves=defaults
                elif selected_item==4:
                    with open('save.txt', 'r') as file:
                        for line in file:
                            key, value = line.strip().split(':')
                            setting_items[key] = saves#여기 아직 안됨 ㅅㅂ
                    done=True                      
            else: #옮기기의 경우
                if selected_item<1:
                    if event.key==pygame.K_RIGHT:
                        if selected_item==0.2:
                            selected_item=0
                        else:
                            selected_item+=0.1
                    elif event.key==pygame.K_LEFT: 
                        if selected_item==0:
                            selected_item=0.2
                        else:
                            selected_item-=0.1
                    elif event.key==pygame.K_DOWN:
                            selected_item=1
                    elif event.key==pygame.K_UP:
                            selected_item=4
                else:
                    if event.key==pygame.K_DOWN:
                        if selected_item==4:
                            selected_item=0
                        else:
                            selected_item+=1
                    elif event.key==pygame.K_UP:
                        if selected_item==0:
                            selected_item=4
                        else:
                            selected_item-=1
                
    # Fill the screen
    screen.fill(BLACK)
    
    # Draw text objects
    screen.blit(title_text, title_rect)
    screen.blit(screensize_text, screensize_rect)
    screen.blit(small_text, small_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(large_text, large_rect)
    screen.blit(keycon_text,keycon_rect)
    screen.blit(altcol_text,altcol_rect)
    screen.blit(reset_text,reset_rect)
    screen.blit(back_text, back_rect)
    
    # Highlight selected difficulty
    if selected_item==0:
        pygame.draw.rect(screen, WHITE, small_rect, 3)
    elif selected_item==0.1:
        pygame.draw.rect(screen, WHITE, medium_rect, 3)
    elif selected_item==0.2:
        pygame.draw.rect(screen, WHITE, large_rect, 3)
    elif selected_item==1:
        pygame.draw.rect(screen, WHITE, keycon_rect, 3)    
    elif selected_item==2:
        pygame.draw.rect(screen, WHITE, altcol_rect, 3)
    elif selected_item==3:
        pygame.draw.rect(screen, WHITE, reset_rect, 3)
    elif selected_item==4:
        pygame.draw.rect(screen, WHITE, back_rect, 3)
    # Update the screen
    pygame.display.update()  
    
    

# Quit pygame
pygame.quit()
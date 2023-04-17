import pygame

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up fonts
font = pygame.font.Font(None, 36)
longerfonts=pygame.font.Font(None,26)

# Define menu items
saves = {}
configured={}

with open('save.txt', 'r') as f:
    lines = f.readlines()
    settings = lines[:3]
    settings2 = lines[3:8]
for line in settings:
    key, value = line.strip().split(':')
    saves[key]=value
for line in settings2:
    action, key_name = line.strip().split(':')
    key = int(key_name)
    saves[action] = key

configured = saves#지금 이 configured 가 개 쓸모가 없는 그건거 같은데 나중에 refactoring 할때 이거 위주로 보자. 돌아가긴 함.

#키 설정을 위한 함수
def update_key(something):
    updating = True
    while updating:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = event.key
                configured[something] = key_name
                updating = False

# Set up the screen
if saves["size"] == 'large':
    screen_width = 1400
    screen_height = 900
    screen = pygame.display.set_mode([screen_width, screen_height])
elif saves["size"] == 'medium':
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode([screen_width, screen_height])
elif saves["size"] == 'small':
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
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type==pygame.KEYDOWN:    
            if event.key==saves["select"]: 
                if selected_item==0:
                    update_key("up")
                elif selected_item==2:
                    update_key("left")
                elif selected_item==3:
                    update_key("right")
                elif selected_item==4:
                    update_key("down")
                elif selected_item==6:
                    update_key("select")
                elif selected_item==8:
                    with open('save.txt', 'w') as file:
                        for key,value in configured.items():
                            file.write(f"{key}:{value}\n")
                        done=True    
                elif selected_item==9:  
                    with open('save.txt', 'w') as file:
                        for key,value in configured.items():
                            file.write(f"{key}:{value}\n")
                        done=True                     
            else: #옮기기의 경우
                if event.key==saves["right"] or event.key==saves["left"]:
                    if selected_item==2 or selected_item==6 or selected_item==8:
                        selected_item+=1
                    elif selected_item==3 or selected_item==7 or selected_item==9:
                        selected_item-=1
                else:
                    if event.key==saves["down"]:
                        if selected_item>=8:
                            selected_item=0
                        elif selected_item==3:
                            selected_item+=1
                        else:
                            selected_item+=2
                    elif event.key==saves["up"]:
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
import pygame
import sys
from pygame.locals import *

selected_item = 0 # 설정 창에서 쓰는 선택 바

""" keyconfigure 에서 쓰는 키보드 설정을 바꾸는 update 함수 """
def update_key(saves, something):
    updating = True
    while updating:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = event.key
                saves[something] = key_name
                updating = False

""" 효과음의 볼륨을 조절하는 함수 """
def volumesetting(sound, value):
    sound.click.set_volume(value)
    sound.card_drawn.set_volume(value)
    sound.card_played.set_volume(value)
    sound.shuffled.set_volume(value)
    sound.uno.set_volume(value)
    sound.victory.set_volume(value)

""" 호출한 딕셔너리를 default.txt로 초기화하는 함수 """
def return_default_setting():
    default_setting = {}
    with open('default.txt', 'r') as f: 
        lines = f.readlines()
        settings = lines[:3]
        settings2 = lines[3:8]
        settings3 = lines[8:]
    for line in settings:
        key, value = line.strip().split(':')
        default_setting[key] = value
    for line in settings2:
        action, key_name = line.strip().split(':')
        key = int(key_name)
        default_setting[action] = key
    for line in settings3:
        action, key_name = line.strip().split(':')
        key = float(key_name)
        default_setting[action] = key
    return default_setting

""" 일반 설정 화면 """
def load_setting(ess, uno, PM, FONT, saves):
    width, height = uno.screen_width, uno.screen_height
    global selected_item

    font = pygame.font.Font(FONT.joe_fin, 36)
    smallfont = pygame.font.Font(FONT.joe_fin,28)

    # 텍스트 객체와 박스 생성
    title_text = font.render("Game Settings", True, (255,255,255))
    title_rect = title_text.get_rect(center=(width//2, height//7))
    
    if saves["size"] == 'small':
        screensize_text = smallfont.render("Size of Screen:", True, (255,255,255))
    else:
        screensize_text = font.render("Size of Screen:", True, (255,255,255))
    screensize_rect = screensize_text.get_rect(center=(width//5, 2*height//7))
    small_text = font.render("Small", True, (255,255,255))
    small_rect = small_text.get_rect(center=(2*width//5, 2*height//7))
    medium_text = font.render("Medium", True, (255,255,255))
    medium_rect = medium_text.get_rect(center=(3*width//5, 2*height//7))
    large_text = font.render("Large", True, (255,255,255))
    large_rect = large_text.get_rect(center=(4*width//5, 2*height//7))
    keycon_text = font.render("Key Config & Sounds",True,(255,255,255))
    keycon_rect = keycon_text.get_rect(center=(width//2,3*height//7))
    altcol_text = font.render("Alternative Colors",True,(255,255,255))
    altcol_rect=altcol_text.get_rect(center=(width//2,4*height//7))
    reset_text = font.render("RESET ALL SETTINGS",True,(255,255,255))
    reset_rect = reset_text.get_rect(center=(width//2,5*height//7))
    back_text = font.render("Back", True, (255,255,255))
    back_rect = back_text.get_rect(center=(width//2, 6*height//7))

    # 텍스트 객체를 그린다
    uno.screen.blit(title_text, title_rect)
    uno.screen.blit(screensize_text, screensize_rect)
    uno.screen.blit(small_text, small_rect)
    uno.screen.blit(medium_text, medium_rect)
    uno.screen.blit(large_text, large_rect)
    uno.screen.blit(keycon_text, keycon_rect)
    uno.screen.blit(altcol_text, altcol_rect)
    uno.screen.blit(reset_text, reset_rect)
    uno.screen.blit(back_text, back_rect)
    
    # 선택된 텍스트에 박스 그리기
    if selected_item == 0:
        pygame.draw.rect(uno.screen, (255,255,255), small_rect, 3)
    elif selected_item == 0.1:
        pygame.draw.rect(uno.screen, (255,255,255), medium_rect, 3)
    elif selected_item == 0.2:
        pygame.draw.rect(uno.screen, (255,255,255), large_rect, 3)
    elif selected_item == 1:
        pygame.draw.rect(uno.screen, (255,255,255), keycon_rect, 3)    
    elif selected_item == 2:
        pygame.draw.rect(uno.screen, (255,255,255), altcol_rect, 3)
    elif selected_item == 3:
        pygame.draw.rect(uno.screen, (255,255,255), reset_rect, 3)
    elif selected_item == 4:
        pygame.draw.rect(uno.screen, (255,255,255), back_rect, 3)

    for event in pygame.event.get():
        if event.type == QUIT:
            with open('save.txt', 'w') as file:
                for key,value in saves.items():
                    file.write(f"{key}:{value}\n")
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if small_rect.collidepoint(mouse_pos):
                selected_item = 0
                saves["size"] ='small'
            elif medium_rect.collidepoint(mouse_pos):
                selected_item = 0.1
                saves["size"] ='medium'
            elif large_rect.collidepoint(mouse_pos):
                selected_item = 0.2
                saves["size"] ='large'
            elif keycon_rect.collidepoint(mouse_pos): # key configuration으로 들어감
                selected_item = 1
                with open('save.txt', 'w') as file:
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                selected_item = 0        
                ess.play_mode = PM.key
                break
            elif altcol_rect.collidepoint(mouse_pos): # 색약 모드
                selected_item = 2
                if saves["color_change"].startswith('original'):
                    saves["color_change"] = 'alternative'
                else:
                    saves["color_change"] = 'original'
            elif reset_rect.collidepoint(mouse_pos): # 리셋 버튼
                selected_item = 3
                return True
            elif back_rect.collidepoint(mouse_pos): # 시작화면으로 돌아가기
                with open('save.txt', 'w') as file:
                    for key, value in saves.items():
                        file.write(f"{key}:{value}\n")
                selected_item = 0
                uno.background = pygame.image.load('./images/Main_background.png')
                uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                uno.screen.blit(uno.background, (-30, -30))
                ess.play_mode = PM.load
                break 
        if event.type == pygame.KEYDOWN:    
            if event.key == saves["select"]: # 결정의 경우
                if selected_item == 0:
                    saves["size"] = 'small'
                elif selected_item == 0.1:
                    saves["size"] ='medium'
                elif selected_item == 0.2:
                    saves["size"] ='large'
                elif selected_item == 1:
                    with open('save.txt', 'w') as file: # key configuration 설정으로 들어간다
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                    selected_item = 0        
                    ess.play_mode = PM.key
                    break
                elif selected_item == 2: # 색약 모드
                    if saves["color_change"].startswith('original'):
                        saves["color_change"] = 'alternative'
                    else:
                        saves["color_change"] = 'original'
                elif selected_item == 3: # 리셋 버튼
                    return True
                elif selected_item == 4: # 시작화면으로 돌아가기
                    with open('save.txt', 'w') as file:
                        for key, value in saves.items():
                            file.write(f"{key}:{value}\n")
                    selected_item = 0
                    uno.background = pygame.image.load('./images/Main_background.png')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                    uno.screen.blit(uno.background, (-30, -30))
                    ess.play_mode = PM.load
                    break                   
            else: # 키보드로 메뉴를 이동하는 경우
                if selected_item < 1:
                    if event.key == saves["right"]:
                        if selected_item == 0.2:
                            selected_item = 0
                        else:
                            selected_item += 0.1
                    elif event.key == saves["left"]: 
                        if selected_item == 0:
                            selected_item = 0.2
                        else:
                            selected_item -= 0.1
                    elif event.key == saves["down"]:
                            selected_item = 1
                    elif event.key == saves["up"]:
                            selected_item = 4
                else:
                    if event.key == saves['down']:
                        if selected_item == 4:
                            selected_item = 0
                        else:
                            selected_item += 1
                    elif event.key == saves['up']:
                        if selected_item == 0:
                            selected_item = 4
                        else:
                            selected_item -= 1


""" 키 설정 화면 """
def load_key_config(ess, uno, PM, FONT, saves):
    font = pygame.font.Font(FONT.joe_fin, 36)
    width, height = uno.screen_width, uno.screen_height
    global selected_item

    title_text = font.render("Key Config & Sounds", True, (255,255,255))
    title_rect = title_text.get_rect(center=(width//2, height//7))
    up_text = font.render("UP", True, (255,255,255))
    up_rect = up_text.get_rect(center=(width//2, 2*height//7))
    left_text = font.render("LEFT", True, (255,255,255))
    left_rect = left_text.get_rect(center=(width//3, 3*height//7))
    right_text = font.render("RIGHT", True, (255,255,255))
    right_rect = right_text.get_rect(center=(2*width//3, 3*height//7))
    down_text = font.render("DOWN", True, (255,255,255))
    down_rect = down_text.get_rect(center=(width//2, 4*height//7))
    select_text = font.render("ENTER",True,(255,255,255))
    select_rect = select_text.get_rect(center=(width//3,5*height//7))
    sound_text = font.render("Sound",True,(255,255,255))
    sound_rect = sound_text.get_rect(center=(2*width//3,5*height//7))
    back_text = font.render("Back", True, (255,255,255))
    back_rect = back_text.get_rect(center=(width//3, 6*height//7))
    main_text = font.render("Main Menu",True,(255,255,255))
    main_rect = main_text.get_rect(center=(2*width//3,6*height//7))

    # 텍스트 객체를 그린다
    uno.screen.blit(title_text, title_rect)
    uno.screen.blit(up_text, up_rect)
    uno.screen.blit(left_text, left_rect)
    uno.screen.blit(right_text, right_rect)
    uno.screen.blit(down_text, down_rect)
    uno.screen.blit(select_text, select_rect)
    uno.screen.blit(sound_text,sound_rect)
    uno.screen.blit(back_text,back_rect)
    uno.screen.blit(main_text,main_rect)

    # 선택된 글자를 하이라이트 한다
    if selected_item == 0:
        pygame.draw.rect(uno.screen, (255,255,255), up_rect, 3)
    elif selected_item == 2:
        pygame.draw.rect(uno.screen, (255,255,255), left_rect, 3)
    elif selected_item == 3:
        pygame.draw.rect(uno.screen, (255,255,255), right_rect, 3)
    elif selected_item == 4:
        pygame.draw.rect(uno.screen, (255,255,255), down_rect, 3)    
    elif selected_item == 6:
        pygame.draw.rect(uno.screen, (255,255,255), select_rect, 3)
    elif selected_item == 7:
        pygame.draw.rect(uno.screen, (255,255,255), sound_rect, 3)
    elif selected_item == 8:
        pygame.draw.rect(uno.screen, (255,255,255), back_rect, 3)
    elif selected_item == 9:
        pygame.draw.rect(uno.screen, (255,255,255), main_rect, 3)

    for event in pygame.event.get():
        if event.type == QUIT:
            with open('save.txt', 'w') as file:
                for key,value in saves.items():
                    file.write(f"{key}:{value}\n")
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if up_rect.collidepoint(mouse_pos):
                selected_item = 0
                update_key(saves, "up")
            elif left_rect.collidepoint(mouse_pos):
                selected_item = 2
                update_key(saves, "left")
            elif right_rect.collidepoint(mouse_pos):
                selected_item = 3
                update_key(saves, "right")
            elif down_rect.collidepoint(mouse_pos):
                selected_item = 4
                update_key(saves, "down")
            elif select_rect.collidepoint(mouse_pos):
                selected_item = 6
                update_key(saves, "select")
            elif sound_rect.collidepoint(mouse_pos): # 사운드 설정으로 이동
                selected_item = 7
                with open('save.txt', 'w') as file:
                        for key, value in saves.items():
                            file.write(f"{key}:{value}\n")
                selected_item = 0
                ess.play_mode = PM.volume
                break
            elif back_rect.collidepoint(mouse_pos): # 설정 화면으로 돌아가기
                selected_item = 8
                with open('save.txt', 'w') as file:
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                selected_item = 0
                ess.play_mode = PM.setting
                break 
            elif main_rect.collidepoint(mouse_pos): # 시작 화면으로 돌아가기
                selected_item = 9
                with open('save.txt', 'w') as file:
                    for key,value in saves.items():
                        file.write(f"{key}:{value}\n")
                selected_item = 0
                uno.background = pygame.image.load('./images/Main_background.png')
                uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                uno.screen.blit(uno.background, (-30, -30))
                ess.play_mode = PM.load
                break
        
        if event.type == pygame.KEYDOWN:    
            if event.key == saves["select"]: 
                if selected_item == 0:
                    update_key(saves, "up")
                elif selected_item == 2:
                    update_key(saves, "left")
                elif selected_item == 3:
                    update_key(saves, "right")
                elif selected_item == 4:
                    update_key(saves, "down")
                elif selected_item == 6:
                    update_key(saves, "select")
                elif selected_item == 7:  # 사운드 설정으로 이동
                    with open('save.txt', 'w') as file:
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                    selected_item = 0
                    ess.play_mode = PM.volume
                    break
                elif selected_item == 8:
                    with open('save.txt', 'w') as file: # 설정 화면으로 돌아가기
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                    selected_item = 0
                    ess.play_mode = PM.setting
                    break  
                elif selected_item == 9:  
                    with open('save.txt', 'w') as file: # 시작 화면으로 돌아가기
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                        selected_item = 0
                        uno.background = pygame.image.load('./images/Main_background.png')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                        uno.screen.blit(uno.background, (-30, -30))
                        ess.play_mode = PM.load
                        break
            else: # 키보드로 메뉴를 이동하는 경우
                if event.key == saves["right"] or event.key == saves["left"]:
                    if selected_item == 2 or selected_item == 6 or selected_item == 8:
                        selected_item += 1
                    elif selected_item == 3 or selected_item == 7 or selected_item == 9:
                        selected_item -= 1
                else:
                    if event.key == saves["down"]:
                        if selected_item >= 8:
                            selected_item = 0
                        elif selected_item == 3:
                            selected_item += 1
                        else:
                            selected_item += 2
                    elif event.key == saves["up"]:
                        if selected_item == 0:
                            selected_item = 8
                        elif selected_item == 3 or selected_item == 7:
                            selected_item -= 3
                        else:
                            selected_item -= 2


""" 볼륨 설정 화면 """
def load_volume_config(ess, uno, sound, PM, FONT, saves):
    font = pygame.font.Font(FONT.joe_fin, 36)
    width, height = uno.screen_width, uno.screen_height
    global selected_item
    
    title_text = font.render("Volume Configure", True, (255,255,255))
    title_rect = title_text.get_rect(center=(width//2, height//6))
    master_text = font.render("Master:", True, (255,255,255))
    master_rect = master_text.get_rect(center=(width//5, 2*height//6))
    msmall_text = font.render("Small", True, (255,255,255))
    msmall_rect = msmall_text.get_rect(center=(2*width//5, 2*height//6))
    mmedium_text = font.render("Medium", True, (255,255,255))
    mmedium_rect = mmedium_text.get_rect(center=(3*width//5, 2*height//6))
    mlarge_text = font.render("Large", True, (255,255,255))
    mlarge_rect = mlarge_text.get_rect(center=(4*width//5, 2*height//6))
    backmusic_text = font.render("BGM:", True, (255,255,255))
    backmusic_rect = backmusic_text.get_rect(center=(width//5, 3*height//6))
    bsmall_text = font.render("Small", True, (255,255,255))
    bsmall_rect = bsmall_text.get_rect(center=(2*width//5, 3*height//6))
    bmedium_text = font.render("Medium", True, (255,255,255))
    bmedium_rect = bmedium_text.get_rect(center=(3*width//5, 3*height//6))
    blarge_text = font.render("Large", True, (255,255,255))
    blarge_rect = blarge_text.get_rect(center=(4*width//5, 3*height//6))
    effect_text = font.render("Effects:", True, (255,255,255))
    effect_rect = effect_text.get_rect(center=(width//5, 4*height//6))
    esmall_text = font.render("Small", True, (255,255,255))
    esmall_rect = esmall_text.get_rect(center=(2*width//5, 4*height//6))
    emedium_text = font.render("Medium", True, (255,255,255))
    emedium_rect = emedium_text.get_rect(center=(3*width//5, 4*height//6))
    elarge_text = font.render("Large", True, (255,255,255))
    elarge_rect = elarge_text.get_rect(center=(4*width//5, 4*height//6))
    back_text = font.render("Back", True, (255,255,255))
    back_rect = back_text.get_rect(center=(width//3, 5*height//6))
    main_text = font.render("Main Menu",True,(255,255,255))
    main_rect = main_text.get_rect(center=(2*width//3,5*height//6))

    # 텍스트 객체를 그린다
    uno.screen.blit(title_text, title_rect)
    uno.screen.blit(master_text, master_rect)
    uno.screen.blit(msmall_text, msmall_rect)
    uno.screen.blit(mmedium_text, mmedium_rect)
    uno.screen.blit(mlarge_text, mlarge_rect)
    uno.screen.blit(backmusic_text, backmusic_rect)
    uno.screen.blit(bsmall_text,bsmall_rect)
    uno.screen.blit(bmedium_text, bmedium_rect)
    uno.screen.blit(blarge_text, blarge_rect)
    uno.screen.blit(effect_text, effect_rect)
    uno.screen.blit(esmall_text,esmall_rect)
    uno.screen.blit(emedium_text, emedium_rect)
    uno.screen.blit(elarge_text, elarge_rect)
    uno.screen.blit(back_text, back_rect)
    uno.screen.blit(main_text, main_rect)


    # 선택된 글자를 하이라이트 한다
    if selected_item == 0:
        pygame.draw.rect(uno.screen, (255,255,255), msmall_rect, 3)
    elif selected_item == 1:
        pygame.draw.rect(uno.screen, (255,255,255), mmedium_rect, 3)
    elif selected_item == 2:
        pygame.draw.rect(uno.screen, (255,255,255), mlarge_rect, 3)
    elif selected_item == 3:
        pygame.draw.rect(uno.screen, (255,255,255), bsmall_rect, 3)    
    elif selected_item == 4:
        pygame.draw.rect(uno.screen, (255,255,255), bmedium_rect, 3)
    elif selected_item == 5:
        pygame.draw.rect(uno.screen, (255,255,255), blarge_rect, 3)
    elif selected_item == 6:
        pygame.draw.rect(uno.screen, (255,255,255), esmall_rect, 3)
    elif selected_item == 7:
        pygame.draw.rect(uno.screen, (255,255,255), emedium_rect, 3)
    elif selected_item == 8:
        pygame.draw.rect(uno.screen, (255,255,255), elarge_rect, 3)
    elif selected_item == 9:
        pygame.draw.rect(uno.screen, (255,255,255), back_rect, 3)
    elif selected_item == 10:
        pygame.draw.rect(uno.screen, (255,255,255), main_rect, 3)    
    

    for event in pygame.event.get():
        if event.type == QUIT:
            with open('save.txt', 'w') as file:
                for key,value in saves.items():
                    file.write(f"{key}:{value}\n")
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN: # 마우스 클릭
            mouse_pos = pygame.mouse.get_pos()
            if msmall_rect.collidepoint(mouse_pos): # 전체 소리 조절
                selected_item = 0
                saves["background"] = 0.1
                saves["effects"] = 0.1
                pygame.mixer.music.set_volume(saves["background"])
                volumesetting(sound, saves["effects"])
            elif mmedium_rect.collidepoint(mouse_pos):
                selected_item = 1
                saves["background"] = 0.3
                saves["effects"] = 0.5
                pygame.mixer.music.set_volume(saves["background"])
                volumesetting(sound, saves["effects"])
            elif mlarge_rect.collidepoint(mouse_pos):
                selected_item = 2
                saves["background"] = 0.5
                saves["effects"] = 0.7
                pygame.mixer.music.set_volume(saves["background"])
                volumesetting(sound, saves["effects"])
            elif bsmall_rect.collidepoint(mouse_pos): # 배경음악 크기 조절
                selected_item = 3
                saves["background"] = 0.1
                pygame.mixer.music.set_volume(saves["background"])
            elif bmedium_rect.collidepoint(mouse_pos): 
                selected_item = 4
                saves["background"] = 0.3
                pygame.mixer.music.set_volume(saves["background"])
            elif blarge_rect.collidepoint(mouse_pos):
                selected_item = 5
                saves["background"] = 0.5
                pygame.mixer.music.set_volume(saves["background"])
            elif esmall_rect.collidepoint(mouse_pos): # 효과음 크기 조절
                selected_item = 6
                saves["effects"] = 0.1
                volumesetting(sound, saves["effects"])
            elif emedium_rect.collidepoint(mouse_pos):
                selected_item = 7
                saves["effects"] = 0.5
                volumesetting(sound, saves["effects"])
            elif elarge_rect.collidepoint(mouse_pos):
                selected_item = 8
                saves["effects"] = 0.7
                volumesetting(sound, saves["effects"])
            elif back_rect.collidepoint(mouse_pos): # Key configuration으로 돌아가기
                selected_item = 9
                with open('save.txt', 'w') as file:
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                selected_item = 0
                ess.play_mode = PM.key
                break
            elif main_rect.collidepoint(mouse_pos): # 시작 화면으로 돌아가기
                selected_item = 10
                with open('save.txt', 'w') as file:
                    for key,value in saves.items():
                        file.write(f"{key}:{value}\n")
                selected_item = 0
                uno.background = pygame.image.load('./images/Main_background.png')
                uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                uno.screen.blit(uno.background, (-30, -30))
                ess.play_mode = PM.load
                break

        if event.type == pygame.KEYDOWN:    
            if event.key == saves["select"]: 
                if selected_item == 0:          # 전체 소리 조절
                    saves["background"] = 0.1
                    saves["effects"] = 0.1
                    pygame.mixer.music.set_volume(saves["background"])
                    volumesetting(sound, saves["effects"])
                elif selected_item == 1:
                    saves["background"] = 0.3
                    saves["effects"] = 0.5
                    pygame.mixer.music.set_volume(saves["background"])
                    volumesetting(sound, saves["effects"])
                elif selected_item == 2:
                    saves["background"] = 0.5
                    saves["effects"] = 0.7
                    pygame.mixer.music.set_volume(saves["background"])
                    volumesetting(sound, saves["effects"])
                elif selected_item == 3:             # 배경음악 크기 조절
                    saves["background"] = 0.1
                    pygame.mixer.music.set_volume(saves["background"])
                elif selected_item == 4:
                    saves["background"] = 0.3
                    pygame.mixer.music.set_volume(saves["background"])
                elif selected_item == 5:
                    saves["background"] = 0.5
                    pygame.mixer.music.set_volume(saves["background"])
                elif selected_item == 6:           # 효과음 크기 조절
                    saves["effects"] = 0.1
                    volumesetting(sound, saves["effects"])
                elif selected_item == 7:
                    saves["effects"] = 0.5
                    volumesetting(sound, saves["effects"])
                elif selected_item == 8:
                    saves["effects"] = 0.7
                    volumesetting(sound, saves["effects"])
                elif selected_item == 9:                      # Key configuration으로 돌아가기
                    with open('save.txt', 'w') as file:
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                    selected_item = 0
                    ess.play_mode = PM.key
                    break
                elif selected_item == 10:                     # 시작 화면으로 돌아가기
                    with open('save.txt', 'w') as file:
                        for key,value in saves.items():
                            file.write(f"{key}:{value}\n")
                        selected_item = 0
                        uno.background = pygame.image.load('./images/Main_background.png')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                        uno.screen.blit(uno.background, (-30, -30))
                        ess.play_mode = PM.load
                        break
            else: # 키보드로 메뉴를 이동하는 경우
                if event.key == saves["right"]:
                    if selected_item == 9:
                        selected_item += 1
                    elif selected_item == 10:
                        selected_item -= 1
                    elif (selected_item+1) % 3 != 0:
                        selected_item += 1
                    else:
                        selected_item -= 2
                elif event.key == saves["left"]:
                    if selected_item == 10:
                        selected_item -= 1
                    elif selected_item == 9:
                        selected_item += 1
                    elif selected_item % 3 != 0:
                        selected_item -= 1
                    else:
                        selected_item += 2
                else:
                    if event.key == saves["down"]:
                        if (selected_item+3) < 9:
                            selected_item += 3
                        elif selected_item == 9:
                            selected_item = 0
                        elif selected_item == 10:
                            selected_item = 2
                        elif selected_item == 6:
                            selected_item = 9
                        else:
                            selected_item = 10    
                    elif event.key == saves["up"]:
                        if (selected_item-3) >= 0:
                            selected_item -= 3
                        elif selected_item == 9:
                            selected_item = 6
                        elif selected_item == 10:
                            selected_item = 8
                        elif selected_item == 0:
                            selected_item = 9
                        else:
                            selected_item = 10
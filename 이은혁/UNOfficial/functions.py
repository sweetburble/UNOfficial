import itertools
import random
import pygame
import sys
import pygame_gui
from pygame.locals import *

KEYS = {} # 키 설정이 저장된 딕셔너리
""" functions.py에서 사용할 키 설정을 불러온다 """
def function_key_config(KEYS):
    with open('save.txt', 'r') as f:
        lines = f.readlines()
        settings = lines[:3]
        settings2 = lines[3:8]
        settings3 = lines[8:]
    for line in settings:
        key, value = line.strip().split(':')
        KEYS[key] = value
    for line in settings2:
        action, key_name = line.strip().split(':')
        key = int(key_name)
        KEYS[action] = key
    for line in settings3:
        action, key_name = line.strip().split(':')
        key = float(key_name)
        KEYS[action] = key

""" 기타 설정이 저장되어 있는 saves를 업데이트 한다 """
def update_saves(saves):
    with open('save.txt', 'r') as f:
        lines = f.readlines()
        settings = lines[:3]
        settings2 = lines[3:8]
        settings3 = lines[8:]
    for line in settings:
        key, value = line.strip().split(':')
        saves[key] = value
    for line in settings2:
        action, key_name = line.strip().split(':')
        key = int(key_name)
        saves[action] = key
    for line in settings3:
        action, key_name = line.strip().split(':')
        key = float(key_name)
        saves[action] = key

# =================================================================
""" 선택하는 객체가 아니라 그냥 텍스트만 화면에 출력하고 싶을 때 사용하는 함수 """
def draw_text(uno, text, text_size, text_col, x, y):
    font = pygame.font.Font('./fonts/JosefinSans-Bold.ttf', text_size)
    img = font.render(text, True, text_col)
    uno.screen.blit(img, (x, y))

def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.SysFont(textFont, textSize)
    newText = newFont.render(message, True, textColor)
    return newText

""" 시작 화면 """
def main_menu(ob, uno, STORY):
    selected = 1

    start_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.3), 200, 50)
    story_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.4), 200, 50)
    setting_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.5), 200, 50)
    multiplay_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.6), 200, 50)
    achievement_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.7), 200, 50)
    quit_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.8), 200, 50)

    while True:
        pygame.init()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEYS["up"]:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == KEYS["down"]:
                    if selected >= 6:
                        selected = 6
                    else:
                        selected = selected + 1
                if event.key == KEYS["select"]: # K_RETURN은 엔터키
                    if selected <= 1: # 게임 시작 버튼
                        ob.play_mode = set_start(ob, uno)
                        if (ob.play_mode == "IN GAME"):
                            return
                        uno.screen.blit(uno.background, (-30, -30))
                    elif selected == 2: # 스토리 모드 버튼
                        ob.play_mode = story_mode(ob, uno, STORY)
                        uno.screen.blit(uno.background, (-30, -30))
                        return
                    elif selected == 3: # 설정 버튼
                        ob.play_mode = "SETTING"
                        return
                    elif selected == 4: # 멀티플레이 버튼
                        ob.play_mode = "MULTIPLAY"
                        return
                    elif selected == 5: # 업적 버튼
                        # ob.play_mode = "ACHIEVEMENT"
                        return
                    elif selected >= 6: # 종료 버튼
                        pygame.quit()
                        sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos): # 게임 시작 버튼
                    selected = 1
                    ob.play_mode = set_start(ob, uno)
                    uno.screen.blit(uno.background, (-30, -30))
                    return
                elif story_rect.collidepoint(mouse_pos): # 스토리 모드 버튼
                    selected = 2
                    ob.play_mode = story_mode(ob, uno, STORY)
                    uno.screen.blit(uno.background, (-30, -30))
                    return
                elif setting_rect.collidepoint(mouse_pos): # 설정 버튼
                    selected = 3
                    ob.play_mode = "SETTING"
                    return
                elif multiplay_rect.collidepoint(mouse_pos): # 멀티플레이 버튼
                    selected = 4
                    ob.play_mode = "MULTIPLAY"
                    return
                elif achievement_rect.collidepoint(mouse_pos): # 업적 버튼
                    selected = 5
                    # ob.play_mode = "ACHIEVEMENT"
                    return
                elif quit_rect.collidepoint(mouse_pos): # 종료 버튼
                    pygame.quit()
                    sys.exit()

        if selected == 1:
            text_start = text_format("START", uno.font, 50, (0,0,0))
        else:
            text_start = text_format("START", uno.font, 50, (255, 255, 255))

        if selected == 2:
            text_story = text_format("STORY MOD", uno.font, 50, (0,0,0))
        else:
            text_story= text_format("STORY MOD", uno.font, 50, (255, 255, 255))

        if selected == 3:
            text_setting = text_format("SETTING", uno.font, 50, (0,0,0))
        else:
            text_setting = text_format("SETTING", uno.font, 50, (255, 255, 255))

        if selected == 4:
            text_multiplay = text_format("MULTIPLAY", uno.font, 50, (0,0,0))
        else:
            text_multiplay = text_format("MULTIPLAY", uno.font, 50, (255, 255, 255))

        if selected == 5:
            text_achievement = text_format("ACHIEVEMENT", uno.font, 50, (0,0,0))
        else:
            text_achievement = text_format("ACHIEVEMENT", uno.font, 50, (255, 255, 255))

        if selected == 6:
            text_quit = text_format("QUIT", uno.font, 50, (0,0,0))
        else:
            text_quit = text_format("QUIT", uno.font, 50, (255, 255, 255))

        # 시작 화면에 사용할 수 있는 키 표시
        text_up = text_format("UP:",uno.font,30,(255,255,255))
        text_left = text_format("LEFT:",uno.font,30,(255,255,255))
        text_right = text_format("RIGHT:",uno.font,30,(255,255,255))
        text_down = text_format("DOWN:",uno.font,30,(255,255,255))
        text_enter = text_format("ENTER:",uno.font,30,(255,255,255))
        text_ups = text_format(pygame.key.name(KEYS["up"]),uno.font,30,(255,255,255))
        text_lefts = text_format(pygame.key.name(KEYS["left"]),uno.font,30,(255,255,255))
        text_rights = text_format(pygame.key.name(KEYS["right"]),uno.font,30,(255,255,255))
        text_downs = text_format(pygame.key.name(KEYS["down"]),uno.font,30,(255,255,255))
        text_enters = text_format(pygame.key.name(KEYS["select"]),uno.font,30,(255,255,255))

        start_rect = text_start.get_rect()
        story_rect = text_story.get_rect()
        setting_rect = text_setting.get_rect()
        multiplay_rect = text_multiplay.get_rect()
        achievement_rect = text_achievement.get_rect()
        quit_rect = text_quit.get_rect()

        # 시작 화면에 사용할 수 있는 키 표시
        up_rect = text_up.get_rect()
        left_rect = text_left.get_rect()
        right_rect = text_right.get_rect()
        down_rect = text_down.get_rect()
        enter_rect = text_enter.get_rect()
        ups_rect = text_ups.get_rect()
        lefts_rect = text_lefts.get_rect()
        rights_rect = text_rights.get_rect()
        downs_rect = text_downs.get_rect()
        enters_rect = text_enters.get_rect()

        # 시작 화면의 메뉴들을 출력한다
        start_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.3), 200, 50)
        story_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.4), 200, 50)          
        setting_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.5), 200, 50)
        multiplay_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.6), 200, 50)
        achievement_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.7), 200, 50)
        quit_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.8), 200, 50)

        # 시작 화면에 사용할 수 있는 키 표시
        up_rect = pygame.Rect(int(uno.screen_width*0.01), int(uno.screen_height*0.01),100,25)
        ups_rect = pygame.Rect(int(uno.screen_width*0.01)+50, int(uno.screen_height*0.01),200,50)
        left_rect = pygame.Rect(int(uno.screen_width*0.01), int(uno.screen_height*0.01)+30,100,25)
        lefts_rect = pygame.Rect(int(uno.screen_width*0.01)+70, int(uno.screen_height*0.01)+30,200,50)
        right_rect = pygame.Rect(int(uno.screen_width*0.01), int(uno.screen_height*0.01)+60,100,25)
        rights_rect = pygame.Rect(int(uno.screen_width*0.01)+90, int(uno.screen_height*0.01)+60,200,50)
        down_rect = pygame.Rect(int(uno.screen_width*0.01), int(uno.screen_height*0.01)+90,100,25)
        downs_rect = pygame.Rect(int(uno.screen_width*0.01)+100, int(uno.screen_height*0.01)+90,200,50)
        enter_rect = pygame.Rect(int(uno.screen_width*0.01), int(uno.screen_height*0.01)+120,100,25)
        enters_rect = pygame.Rect(int(uno.screen_width*0.01)+95, int(uno.screen_height*0.01)+120,200,50)

        uno.screen.blit(text_start, start_rect)
        uno.screen.blit(text_story, story_rect)
        uno.screen.blit(text_setting, setting_rect)
        uno.screen.blit(text_multiplay, multiplay_rect)
        uno.screen.blit(text_achievement, achievement_rect)
        uno.screen.blit(text_quit, quit_rect)
        uno.screen.blit(text_up, up_rect)
        uno.screen.blit(text_ups, ups_rect)
        uno.screen.blit(text_left, left_rect)
        uno.screen.blit(text_lefts, lefts_rect)
        uno.screen.blit(text_right, right_rect)
        uno.screen.blit(text_rights, rights_rect)
        uno.screen.blit(text_down, down_rect)
        uno.screen.blit(text_downs, downs_rect)
        uno.screen.blit(text_enter, enter_rect)
        uno.screen.blit(text_enters, enters_rect)

        pygame.display.update()

""" 게임 시작 전, 로비 화면 """
def set_start(ob, uno):
    pygame.init()
    uno.background = pygame.image.load('./images/default.png')
    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
    uno.screen.blit(uno.background, (-100, -70))
    selected = 1

    while True:
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEYS["up"]:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == KEYS["down"]:
                    if selected >= 6:
                        selected = 6
                    else:
                        selected = selected + 1
                if event.key == KEYS["select"]:
                    if selected <= 1:
                        uno.player_num = 2
                        # 카드 덱을 세팅하고, 버려진 카드덱에 카드를 한장 놓고, 플레이어들에게 카드를 배분한다
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 2:
                        uno.player_num = 3
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 3:
                        uno.player_num = 4
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 4:
                        uno.player_num = 5
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 5:
                        uno.player_num = 6
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected >= 6: # 시작화면으로 돌아감
                        uno.background = pygame.image.load('./images/Main_background.png')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                        return "START SCREEN"
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if two_rect.collidepoint(mouse_pos):
                    uno.player_num = 2
                    selected = 1
                    return set_players(ob, uno, uno.player_num)
                elif three_rect.collidepoint(mouse_pos):
                    uno.player_num = 3
                    selected = 2
                    return set_players(ob, uno, uno.player_num)
                elif four_rect.collidepoint(mouse_pos):
                    uno.player_num = 4
                    selected = 3
                    return set_players(ob, uno, uno.player_num)
                elif five_rect.collidepoint(mouse_pos):
                    uno.player_num = 5
                    selected = 4
                    return set_players(ob, uno, uno.player_num)
                elif six_rect.collidepoint(mouse_pos):
                    uno.player_num = 6
                    selected = 5
                    return set_players(ob, uno, uno.player_num)
                elif quit_rect.collidepoint(mouse_pos): # 시작화면으로 돌아감
                    selected = 5
                    uno.background = pygame.image.load('./images/Main_background.png')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                    return "START SCREEN"
        
        # 선택한 글자의 색을 빨간색으로 표시      
        if selected == 1:
            text_two = text_format("2 PLAYERS", uno.font, 50, (255,24,0))
        else:
            text_two = text_format("2 PLAYERS", uno.font, 50, (0,0,0))
        if selected == 2:
            text_three = text_format("3 PLAYERS", uno.font, 50, (255,24,0))
        else:
            text_three = text_format("3 PLAYERS", uno.font, 50, (0,0,0))
        if selected == 3:
            text_four = text_format("4 PLAYERS", uno.font, 50, (255,24,0))
        else:
            text_four = text_format("4 PLAYERS", uno.font, 50, (0,0,0))                
        if selected == 4:
            text_five = text_format("5 PLAYERS", uno.font, 50, (255,24,0))
        else:
            text_five = text_format("5 PLAYERS", uno.font, 50, (0,0,0))
        if selected == 5:
            text_six = text_format("6 PLAYERS", uno.font, 50, (255,24,0))
        else:
            text_six = text_format("6 PLAYERS", uno.font, 50, (0,0,0))
        if selected == 6:
            text_quit = text_format("BACK", uno.font, 50, (255,24,0))
        else:
            text_quit = text_format("BACK", uno.font, 50, (0,0,0))

        two_rect = text_two.get_rect()
        three_rect = text_three.get_rect()
        four_rect = text_four.get_rect()
        five_rect = text_five.get_rect()
        six_rect = text_six.get_rect()
        quit_rect = text_quit.get_rect()

        two_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(150/600)), 200, 50)
        three_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(210/600)), 200, 50)
        four_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(270/600)), 200, 50)
        five_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(330/600)), 200, 50)
        six_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(390/600)), 200, 50)
        quit_rect = pygame.Rect(int(uno.screen_width*(325/800)), int(uno.screen_height*(450/600)), 200, 50)

        uno.screen.blit(text_two, two_rect)
        uno.screen.blit(text_three, three_rect)
        uno.screen.blit(text_four, four_rect)
        uno.screen.blit(text_five, five_rect)
        uno.screen.blit(text_six, six_rect)
        uno.screen.blit(text_quit, quit_rect)
        pygame.display.update()


""" 싱글 플레이어 모드 컴퓨터 이름 변경 화면 """
def set_players(ob, uno, player_num):
    pygame.init()
    uno.background = pygame.image.load('./images/default.png')
    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
    uno.player_num = player_num
    uno.screen.blit(uno.background, (-100, -70))
    selected = 1

    MANAGER = pygame_gui.UIManager((uno.screen_width, uno.screen_height))

    if uno.player_num >= 2:
        TEXT_INPUT_MY = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(420/600))), (200, 50)), manager = MANAGER, object_id="#my_text_entry")
        TEXT_INPUT1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(120/600))), (200, 50)), manager = MANAGER, object_id="#com1_text_entry")
        if uno.player_num >= 3:
            TEXT_INPUT2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(180/600))), (200, 50)), manager = MANAGER, object_id="#com2_text_entry")
            if uno.player_num >= 4:
                TEXT_INPUT3 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(240/600))), (200, 50)), manager = MANAGER, object_id="#com3_text_entry")
                if uno.player_num >= 5:
                    TEXT_INPUT4 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(300/600))), (200, 50)), manager = MANAGER, object_id="#com4_text_entry")
                    if uno.player_num == 6:
                        TEXT_INPUT5 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(360/600))), (200, 50)), manager = MANAGER, object_id="#com5_text_entry")

    while True:
        pygame.mixer.pre_init(44100, -16, 1, 512)
        
        for event in pygame.event.get():
            MANAGER.process_events(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEYS["up"]:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == KEYS["down"]:
                    if selected >= uno.player_num:
                        selected = uno.player_num
                    else:
                        selected = selected + 1
                if event.key == KEYS["select"]:
                    if selected == uno.player_num:
                        return "IN GAME"
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if one_rect.collidepoint(mouse_pos):
                    selected = 1
                elif two_rect.collidepoint(mouse_pos):
                    selected = 2
                elif three_rect.collidepoint(mouse_pos):
                    selected = 3
                elif four_rect.collidepoint(mouse_pos):
                    selected = 4
                elif five_rect.collidepoint(mouse_pos):
                    selected = 5
                elif start_rect.collidepoint(mouse_pos):
                    selected = uno.player_num
                    return "IN GAME"                
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#com1_text_entry":
                ob.bot_map[1] = event.text                
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#com2_text_entry":                
                ob.bot_map[2] = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#com3_text_entry":
                ob.bot_map[3] = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#com4_text_entry":
                ob.bot_map[4] = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#com5_text_entry":
                ob.bot_map[5] = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#my_text_entry":
                ob.bot_map[6] = event.text

        # 선택한 글자의 색을 빨간색으로 표시      
        if selected == 1:
            text_one = text_format("COM 1", uno.font, 50, (255,24,0))
        else:
            text_one = text_format("COM 1", uno.font, 50, (0,0,0))
        if selected == 2:
            text_two = text_format("COM 2", uno.font, 50, (255,24,0))
        else:
            text_two = text_format("COM 2", uno.font, 50, (0,0,0))
        if selected == 3:
            text_three = text_format("COM 3", uno.font, 50, (255,24,0))
        else:
            text_three = text_format("COM 3", uno.font, 50, (0,0,0))                
        if selected == 4:
            text_four = text_format("COM 4", uno.font, 50, (255,24,0))
        else:
            text_four = text_format("COM 4", uno.font, 50, (0,0,0))
        if selected == 5:
            text_five = text_format("COM 5", uno.font, 50, (255,24,0))
        else:
            text_five = text_format("COM 5", uno.font, 50, (0,0,0))
        if selected == uno.player_num:
            text_start = text_format("START", uno.font, 50, (255,24,0))
        else:
            text_start = text_format("START", uno.font, 50, (0,0,0))

        one_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(120/600)), 200, 50)
        two_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(180/600)), 200, 50)
        three_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(240/600)), 200, 50)
        four_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(300/600)), 200, 50)
        five_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(360/600)), 200, 50)
        start_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(420/600)), 200, 50)

        if uno.player_num == 2:
            uno.screen.blit(text_one, one_rect)
            uno.screen.blit(text_start, start_rect)
        elif uno.player_num == 3:
            uno.screen.blit(text_one, one_rect)
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_start, start_rect)
        elif uno.player_num == 4:
            uno.screen.blit(text_one, one_rect)
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_three, three_rect)
            uno.screen.blit(text_start, start_rect)
        elif uno.player_num == 5:
            uno.screen.blit(text_one, one_rect)
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_three, three_rect)
            uno.screen.blit(text_four, four_rect)
            uno.screen.blit(text_start, start_rect)
        elif uno.player_num == 6:
            uno.screen.blit(text_one, one_rect)
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_three, three_rect)
            uno.screen.blit(text_four, four_rect)
            uno.screen.blit(text_five, five_rect)
            uno.screen.blit(text_start, start_rect)

        MANAGER.update(60)
        MANAGER.draw_ui(uno.screen)
        pygame.display.update()


# =====================================================================
""" 스토리 모드 선택 화면 """
def story_mode(ob, uno, STORY):
    pygame.init()
    uno.background = pygame.image.load('./images/Story map.jpg')
    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/930, uno.screen_height/690))
    uno.screen.blit(uno.background, (-10, -10))

    selected = 1
    while True:
        pygame.init()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == KEYS["down"] or event.key == KEYS["left"]:
                    if selected <= 0:
                        selected = 0
                    else:
                        selected = selected - 1
                elif event.key == KEYS["up"] or event.key == KEYS["right"]:
                    # 0 ~ 최대 4까지
                    if selected >= STORY.Is_story_passed + 1:
                        selected = STORY.Is_story_passed + 1
                    else:
                        selected = selected + 1
                if event.key == KEYS["select"]: # K_RETURN은 엔터키
                    if selected <= 0: # 시작 화면으로 돌아간다
                        uno.background = pygame.image.load('./images/Main_background.png')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                        return "START SCREEN"
                    if selected == 1:
                        return select_story(ob, uno, STORY, 1)
                    if selected == 2:
                        return select_story(ob, uno, STORY, 2)
                    if selected == 3:
                        return select_story(ob, uno, STORY, 3)
                    if selected >= 4:
                        return select_story(ob, uno, STORY, 4)

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos): # 시작 화면으로 돌아간다
                    selected = 0
                    uno.background = pygame.image.load('./images/Main_background.png')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                    return "START SCREEN"
                elif MAP1_rect.collidepoint(mouse_pos):
                    selected = 1
                    return select_story(ob, uno, STORY, 1)
                elif MAP2_rect.collidepoint(mouse_pos):
                    selected = 2
                    return select_story(ob, uno, STORY, 2)
                elif MAP3_rect.collidepoint(mouse_pos):
                    selected = 3
                    return select_story(ob, uno, STORY, 3)
                elif MAP4_rect.collidepoint(mouse_pos):
                    selected = 4
                    return select_story(ob, uno, STORY, 4)

        # 메인 화면으로 돌아가는 버튼은 항상 존재한다
        if selected == 0:
            back_text = text_format("BACK", uno.font, 20, (0,0,0))
        else:
            back_text = text_format("BACK", uno.font, 20, (255, 255, 255))
        back_rect = back_text.get_rect()
        back_rect = pygame.Rect(uno.screen_width/2-470, int(uno.screen_height*0.2-100), 200, 50)
        uno.screen.blit(back_text, back_rect)

        if selected == 1:
            text_MAP1 = text_format("CHALLENGE", uno.font, 50, (0,0,0))
        else:
            text_MAP1 = text_format("CHALLENGE", uno.font, 50, (255, 255, 255))

        if selected == 2:
            text_MAP2 = text_format("CHALLENGE", uno.font, 50, (0,0,0))
        else:
            text_MAP2= text_format("CHALLENGE", uno.font, 50, (255, 255, 255))

        if selected == 3:
            text_MAP3 = text_format("CHALLENGE", uno.font, 50, (0,0,0))
        else:
            text_MAP3 = text_format("CHALLENGE", uno.font, 50, (255, 255, 255))

        if selected == 4:
            text_MAP4 = text_format("CHALLENGE", uno.font, 50, (0,0,0))
        else:
            text_MAP4 = text_format("CHALLENGE", uno.font, 50, (255, 255, 255))
        
        # 글자 객체를 그린다
        MAP1_rect = text_MAP1.get_rect()
        MAP2_rect = text_MAP2.get_rect()
        MAP3_rect = text_MAP3.get_rect()
        MAP4_rect = text_MAP4.get_rect()

        MAP1_rect = pygame.Rect(uno.screen_width/2-275, int(uno.screen_height*0.8+20), 200, 50)
        MAP2_rect = pygame.Rect(uno.screen_width/2-245, int(uno.screen_height*0.2+20), 200, 50)          
        MAP3_rect = pygame.Rect(uno.screen_width/2-40, int(uno.screen_height*0.5-20), 200, 50)
        MAP4_rect = pygame.Rect(uno.screen_width/2+140, int(uno.screen_height*0.2-20), 200, 50)

        # 이전 스토리를 클리어하지 않은 경우, 다음 스토리는 선택할 수 없다
        if STORY.Is_story_passed >= 0:
            uno.screen.blit(text_MAP1, MAP1_rect)
            if STORY.Is_story_passed >= 1:
                uno.screen.blit(text_MAP2, MAP2_rect)
                if STORY.Is_story_passed >= 2:
                    uno.screen.blit(text_MAP3, MAP3_rect)
                    if STORY.Is_story_passed >= 3:
                        uno.screen.blit(text_MAP4, MAP4_rect)

        pygame.display.update()

""" 어떤 한 지역을 선택하면 설명을 보여주고 선택 여부를 묻는다 """
def select_story(ob, uno, STORY, stage):
    pygame.init()
    uno.background = pygame.image.load('./images/Story map.jpg')
    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/930, uno.screen_height/690))
    uno.screen.blit(uno.background, (-10, -10))

    select_yes_no = 0 # yes는 0, no는 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEYS["left"]:
                    select_yes_no = 0
                elif event.key == KEYS["right"]:
                    select_yes_no = 1
                elif event.key == KEYS["select"]:
                    if select_yes_no == 0:
                        if stage == 1:
                            STORY.Is_stage_on[0]=True
                            uno.player_num = 2
                            return "IN GAME"
                        elif stage == 2:
                            STORY.Is_stage_on[1]=True
                            uno.player_num = 3
                            return "IN GAME"
                        elif stage == 3:
                            STORY.Is_stage_on[2]=True
                            uno.player_num = 2
                            return "IN GAME"
                        elif stage == 4:
                            STORY.Is_stage_on[3]=True
                            uno.player_num = 2
                            return "IN GAME"
                    elif select_yes_no == 1: # no를 선택하면 다시 스토리 선택 화면으로 돌아간다
                        uno.background = pygame.image.load('./images/Story map.jpg')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/930, uno.screen_height/690))
                        uno.screen.blit(uno.background, (-10, -10))
                        return "STORY MODE"
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_rect.collidepoint(mouse_pos):
                    select_yes_no = 0
                    if stage == 1:
                        STORY.Is_stage_on[0]=True
                        uno.player_num = 2
                        return "IN GAME"
                    elif stage == 2:
                        STORY.Is_stage_on[1]=True
                        uno.player_num = 3
                        return "IN GAME"
                    elif stage == 3:
                        STORY.Is_stage_on[2]=True
                        uno.player_num = 2
                        return "IN GAME"
                    elif stage == 4:
                        STORY.Is_stage_on[3]=True
                        uno.player_num = 2
                        return "IN GAME"
                elif no_rect.collidepoint(mouse_pos):
                    select_yes_no = 1
                    uno.background = pygame.image.load('./images/Story map.jpg')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/930, uno.screen_height/690))
                    uno.screen.blit(uno.background, (-10, -10))
                    return "STORY MODE"

        if select_yes_no == 0: # yes가 선택되어 있는 경우
            text_yes = text_format("YES", uno.font, 50, (0, 0, 0))
            text_no = text_format("NO", uno.font, 50, (255, 255, 255))
        else: # no가 선택되어 있는 경우
            text_yes = text_format("YES", uno.font, 50, (255, 255, 255))
            text_no = text_format("NO", uno.font, 50, (0, 0, 0))
        
        yes_rect = pygame.Rect(int(uno.screen_width/2-100), int(uno.screen_height*0.8), 100, 40)
        no_rect = pygame.Rect(int(uno.screen_width/2+50), int(uno.screen_height*0.8), 100, 40)
        uno.screen.blit(text_yes, yes_rect)
        uno.screen.blit(text_no, no_rect)

        # 해당 스토리에 대한 설명
        draw_text(uno, "ARE YOU SURE?", 50, (255, 255, 255), uno.screen_width*(300/1000), int(uno.screen_height*0.1))
        if stage == 1:
            draw_text(uno, " - computer will get skill card 50% more at first", 30, (255, 255, 255), 0, int(uno.screen_height*0.3))
            draw_text(uno, " - computer use combo that use 2-3 or more cards at once", 30, (255, 255, 255), 0, int(uno.screen_height*0.4))
        elif stage == 2:
            draw_text(uno, " - play with 3 computers", 30, (255, 255, 255), 0, int(uno.screen_height*0.3))
            draw_text(uno, " - distribute all cards to the players equally, except first", 30, (255, 255, 255), 0, int(uno.screen_height*0.4))
        elif stage == 3:
            draw_text(uno, " - play with 2 computers", 30, (255, 255, 255), 0, int(uno.screen_height*0.3))
            draw_text(uno, " - every 5 turns, the color of the cards changes randomly", 30, (255, 255, 255), 0, int(uno.screen_height*0.4))
        elif stage == 4:
            draw_text(uno, " - play with 1 computers", 30, (255, 255, 255), 0, int(uno.screen_height*0.3))
            draw_text(uno, " - destroy a card of the computer each turn", 30, (255, 255, 255), 0, int(uno.screen_height*0.4))

        pygame.display.update()

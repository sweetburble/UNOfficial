import itertools
import random
import pygame
import sys
import pygame_gui
from pygame.locals import *

KEYS = {} # 키 설정이 저장된 딕셔너리
def function_key_config():
    """ functions.py에서 사용할 키 설정을 불러온다 """
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

def peek(s):
    """ Peek - 리스트에서 가장 마지막 원소를 리턴한다 """
    return s[-1]

# driver.py에서 1번째로 호출
def create(Object, uno):
    """ 카드를 생성하고, 분배한다 """
    for _ in range(uno.player_num):
        Object.player_list.append([]) # 플레이어 수만큼 2차원 리스트 생성 -> 플레이어들의 카드를 저장하기 위해서
    
    Object.shouted_uno = [False] * uno.player_num # 각 플레이어가 UNO를 외쳤는지 저장하는 플래그

    a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9',
            '+1', '+1', '+2', '+2', '+4', 'Skip', 'Skip', 'Reverse', 'Reverse') # 색깔 +1, +4 기술 카드 추가
    Object.deck1 = list(itertools.product(a, Object.color)) # 덱 생성
    for _ in range(4): # 덱에 와일드 카드 2종류 4장씩 추가
        Object.deck1.append(('Wild', 'Black'))
        Object.deck1.append(('+4', 'Black'))
    random.shuffle(Object.deck1) # 덱 셔플

    while peek(Object.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
                            ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
                            ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
                            ('+2', 'Blue'), ('+2', 'Yellow'), ('+1', 'Red'), ('+1', 'Green'),
                            ('+1', 'Blue'), ('+1', 'Yellow'), ('+4', 'Red'), ('+4', 'Green'),
                            ('+4', 'Blue'), ('+4', 'Yellow')]: # 첫 번째 카드는 기술카드가 아니어야 한다
        random.shuffle(Object.deck1)

    Object.deck2.append(Object.deck1.pop()) # 첫 번째 카드를 버려진 카드 덱(deck2)에 추가
    Object.current = peek(Object.deck2) # 버려진 카드 덱의 peek

    for j in range(uno.player_num):  # 모든 플레이어에게 카드를 7장씩 나누어 준다
        for _ in range(2):
            Object.player_list[j].append(Object.deck1.pop())

    # Object.player_list[0] = [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Reverse', 'Green'), ("+2", "Blue")]

# play_this_card에서 4번째로 호출
def set_curr_player(ob, uno, default): # (ob, uno, False)
    """ 다음 플레이어 결정 """
    if ob.current[0] == 'Reverse' and ob.special_check == 0:
        ob.direction_check *= -1  # 진행 방향 리버스
        ob.special_check = 1  # 기술 카드 상태 비활성화
        if uno.player_num == 2:
            ob.position = (ob.position + ob.direction_check) % 2
    
    if ob.current[0] == 'Skip' and ob.special_check == 0:
        ob.special_check = 1
        ob.position = (ob.position + ob.direction_check) % uno.player_num # 플레이 하는 플레이어 인덱스 (Playing player index)

    if default: # AI가 플레이 하는 경우 True, 유저인 경우 False
        ob.position = (ob.position + ob.direction_check) % uno.player_num # direction_check대로 진행한다

# driver.py에서 2번째로 호출
def re_initialize(ob, uno):
    """ 모든 게임 변수와 플래그를 초기화한다 """
    ob.message = "" # 메세지를 출력하기 위해서
    ob.winner = -1
    ob.player_playing = False
    ob.play_lag = -1
    ob.player_list = []
    ob.deck1 = list()
    ob.deck2 = list()
    ob.direction_check = 1  # 게임 플레이 방향 플래그
    ob.position = -1  # 위치 카운터
    ob.special_check = 0  # Flag to check status of special card
    ob.current = tuple()
    ob.drawn, ob.played, ob.choose_color = False, False, False
    ob.shouted_uno = [False] * 4

# driver.py에서 5번째로 호출
def take_from_stack(ob):
    """ 유저에 의해 덱에서 카드 한 장 드로우 """
    if not ob.drawn: # 이미 뽑은 상태가 아니면
        try: # 카드 덱이 비어있으면, 예외 처리
            ob.player_list[0].append(ob.deck1.pop())
        except:
            ob.deck1, ob.deck2 = ob.deck2, ob.deck1 # 카드 덱과 버려진 카드 덱을 바꾼다
            random.shuffle(ob.deck1)
            ob.player_list[0].append(ob.deck1.pop())
        finally:
            ob.drawn = True # 드로우 했나?를 True로 바꾼다

# driver.py에서 3번째로 호출
def play_this_card(ob, uno, card): # ob = ess, card = ess.player_list[0][int((625 - i) / 50)
    """ 유저에 의해 카드가 플레이 될 때 """
    if not ob.played:
        # ob.current = 버려진 카드 덱의 맨 위에 있는 카드
        # 숫자가 같거나, 색깔이 같거나, 와일드 카드가 아니면
        if (card[0] == ob.current[0] or card[1] == ob.current[1]) and (card[1] != 'Black'):
            ob.played, ob.drawn = True, True # 플레이 했나?, 드로우 했나?를 True로 바꾼다
            ob.deck2.append(card)
            ob.current = peek(ob.deck2)
            ob.player_list[0].remove(ob.current)
            ob.special_check = 0 # 기술 카드 상태 활성화 (만약 기술 카드를 냈으면 적용된다)
            set_curr_player(ob, uno, False)

        if card[1] == 'Black':
            ob.played, ob.drawn = True, True
            ob.choose_color = True # 와일드 카드는 모두 색깔을 선택하게 한다
            ob.player_list[0].remove(card)
            ob.deck2.append(card)

# driver.py에서 6번째로 호출
def play_this_card_2(ob, color): # color = "Red" or "Blue" or "Green" or "Yellow"가 들어간다
    """ 다음 색깔 선택 """
    ob.deck2[-1] = (ob.deck2[-1][0], color) # color에 맞는 이미지 파일(EX - Red.png)이 로딩될 것이다
    ob.current = peek(ob.deck2)
    ob.special_check = 0

# bot_action()에서 8번째로 호출
def handle24(ob, n): # (ob, int(ob.current[0][1]))
    """ +1, +2, +4 기술 카드를 처리한다 """
    for _ in range(n):
        try:
            ob.player_list[ob.position].append(ob.deck1.pop())
        except:
            ob.deck1, ob.deck2 = ob.deck2, ob.deck1
            random.shuffle(ob.deck1)
            ob.player_list[ob.position].append(ob.deck1.pop())
    ob.message = "%s Draws %d cards" % (ob.bot_map[ob.position], n)
    ob.special_check = 1 # 기술 카드 상태 비활성화

# bot_action()에서 10번째로 호출
def handle_black(ob, item):
    """ 와일드 카드를 처리한다 """
    ob.special_check = 0 # 기술 카드 상태 활성화
    ob.deck2.append(item)
    ob.current = peek(ob.deck2)
    
    d = dict()
    d['Blue'] = 0
    d['Green'] = 0
    d['Yellow'] = 0
    d['Red'] = 0
    d['Black'] = 0
    for _item in ob.player_list[ob.position]:
        d[_item[1]] += 1
    d = sorted(d.items(), key=lambda kv: (kv[1], kv[0]))
    new_color = d[-1][0] # AI가 가지고 있는 카드 중에서 가장 많은 색깔을 선택한다
    if new_color == 'Black':
        new_color = d[-2][0] # 그게 와일드 카드면, 두번째로 많은 색깔을 선택한다

    ob.message = "%s plays %s %s, new color is %s" % (ob.bot_map[ob.position], item[0], item[1], new_color)
    ob.current = (ob.current[0], new_color) # AI가 선택한 색깔로, 버려진 카드 덱에 이미지 파일(EX - Red.png)을 그린다

# bot_action()에서 9번째로 호출
def bot_play_card(ob, item):
    """ AI가 카드를 플레이한다 """
    ob.special_check = 0 # 기술 카드 상태 활성화
    ob.deck2.append(item)
    ob.current = peek(ob.deck2)
    ob.message = "%s plays card %s" % (ob.bot_map[ob.position], ob.current[1] + " " + ob.current[0])

# driver.py에서 7번째로 호출
def bot_action(ob, uno, sounds):
    """ AI 로직 구현 """
    ob.message = ""
    ob.shouted_uno[ob.position] = False # 플레이하는 AI의 UNO 외침 플래그를 초기화한다
    ob.played_check = 0 # ??

    # 버려진 카드 덱의 맨 위에 있는 기술 카드가 +2 또는 +4이고, 기술 카드 상태가 활성화 되었다면
    if (ob.current[0] == '+1' or ob.current[0] == '+2' or ob.current[0] == '+4') and ob.special_check == 0:
        handle24(ob, int(ob.current[0][1]))
        ob.played_check = 1

    else:
        if (ob.played_check != 1 and len(ob.player_list[ob.position]) == 2):
            pygame.mixer.pre_init(44100, -16, 1, 512)
            wait_time = random.randint(1000, 2000)
            pygame.time.delay(wait_time) # 1~2초 동안 기다린 다음, 우노를 외친다!
            sounds.uno.play()

            ob.shouted_uno[ob.position] = True
            ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]

        check = 0
        for item in ob.player_list[ob.position]: # AI가 가지고 있는 카드 중에서
            if ob.current[1] == item[1] or ob.current[0] == item[0]: # 색깔이나 숫자가 같은 카드가 있다면
                bot_play_card(ob, item)

                if item[1] == 'Black': # 그게 와일드 카드면
                    handle_black(ob, item)

                ob.player_list[ob.position].remove(item)

                set_curr_player(ob, uno, False)
                check = 1
                break

        if check == 0: # AI가 낼 수 있는 카드가 없다면
            black_check = 0
            for item in ob.player_list[ob.position]:
                if item[1] == 'Black': # 근데 와일드 카드가 있다면
                    ob.message = "%s plays %s" % (ob.bot_map[ob.position], item[0] + " " + item[1])
                    handle_black(ob, item)
                    ob.player_list[ob.position].remove(item)
                    black_check = 1
                    break
            if black_check == 0: # 와일드 카드도 없어서, 카드를 뽑아야 한다면
                try:
                    new_card = (ob.deck1.pop())
                except:
                    ob.deck1, ob.deck2 = ob.deck2, ob.deck1
                    random.shuffle(ob.deck1)
                    new_card = (ob.deck1.pop())

                ob.message = "%s draws a card" % ob.bot_map[ob.position]

                if new_card[1] == 'Black': # 뽑은 카드가 와일드 카드라면
                    ob.message = "%s plays %s" % (ob.bot_map[ob.position], new_card[0] + " " + new_card[1])
                    handle_black(ob, new_card) 
                elif new_card[1] == ob.current[1] or new_card[0] == ob.current[0]: # 뽑은 카드가 버려진 카드 덱의 맨 위에 있는 카드와 색깔이나 숫자가 같다면
                    bot_play_card(ob, new_card)
                else:
                    ob.player_list[ob.position].append(new_card)

# =================================================================
# 선택하는 객체가 아니라 그냥 텍스트만 화면에 출력하고 싶을 때 사용하세요
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
                        # ob.play_mode = "MULTIPLAY"
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
                    # ob.play_mode = "MULTIPLAY"
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
        uno.screen.blit(text_up,up_rect)
        uno.screen.blit(text_ups,ups_rect)
        uno.screen.blit(text_left,left_rect)
        uno.screen.blit(text_lefts,lefts_rect)
        uno.screen.blit(text_right,right_rect)
        uno.screen.blit(text_rights,rights_rect)
        uno.screen.blit(text_down,down_rect)
        uno.screen.blit(text_downs,downs_rect)
        uno.screen.blit(text_enter,enter_rect)
        uno.screen.blit(text_enters,enters_rect)

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
                        create(ob, uno)
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 2:
                        uno.player_num = 3
                        create(ob, uno)
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 3:
                        uno.player_num = 4
                        create(ob, uno)
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 4:
                        uno.player_num = 5
                        create(ob, uno)
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected == 5:
                        uno.player_num = 6
                        create(ob, uno)
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.player_num)
                    if selected >= 6: # 시작화면으로 돌아감
                        uno.background = pygame.image.load('./images/Main_background.png')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                        return "LOAD PAGE"
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if two_rect.collidepoint(mouse_pos):
                    uno.player_num = 2
                    create(ob, uno)
                    selected = 1
                    return set_players(ob, uno, uno.player_num)
                elif three_rect.collidepoint(mouse_pos):
                    uno.player_num = 3
                    create(ob, uno)
                    selected = 2
                    return set_players(ob, uno, uno.player_num)
                elif four_rect.collidepoint(mouse_pos):
                    uno.player_num = 4
                    create(ob, uno)
                    selected = 3
                    return set_players(ob, uno, uno.player_num)
                elif five_rect.collidepoint(mouse_pos):
                    uno.player_num = 5
                    create(ob, uno)
                    selected = 4
                    return set_players(ob, uno, uno.player_num)
                elif six_rect.collidepoint(mouse_pos):
                    uno.player_num = 6
                    create(ob, uno)
                    selected = 5
                    return set_players(ob, uno, uno.player_num)
                elif quit_rect.collidepoint(mouse_pos): # 시작화면으로 돌아감
                    selected = 5
                    uno.background = pygame.image.load('./images/Main_background.png')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                    return "LOAD PAGE"
        
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
        TEXT_INPUT_MY = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(420/600))), (200, 50)), manager=MANAGER, object_id="#my_text_entry")
        TEXT_INPUT1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(120/600))), (200, 50)), manager=MANAGER, object_id="#com1_text_entry")
        if uno.player_num >= 3:
            TEXT_INPUT2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(180/600))), (200, 50)), manager=MANAGER, object_id="#com2_text_entry")
            if uno.player_num >= 4:
                TEXT_INPUT3 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(240/600))), (200, 50)), manager=MANAGER, object_id="#com3_text_entry")
                if uno.player_num >= 5:
                    TEXT_INPUT4 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(300/600))), (200, 50)), manager=MANAGER, object_id="#com4_text_entry")
                    if uno.player_num == 6:
                        TEXT_INPUT5 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(uno.screen_width*(450/800)), int(uno.screen_height*(360/600))), (200, 50)), manager=MANAGER, object_id="#com5_text_entry")

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
                        return "LOAD PAGE"
                    if selected == 1:
                        select_story(ob, uno, STORY, 1)
                    if selected == 2:
                        select_story(ob, uno, STORY, 2)
                    if selected == 3:
                        select_story(ob, uno, STORY, 3)
                    if selected >= 4:
                        select_story(ob, uno, STORY, 4)

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos): # 시작 화면으로 돌아간다
                    selected = 0
                    uno.background = pygame.image.load('./images/Main_background.png')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                    return "LOAD PAGE"
                elif MAP1_rect.collidepoint(mouse_pos):
                    selected = 1
                    select_story(ob, uno, STORY, 1)
                elif MAP2_rect.collidepoint(mouse_pos):
                    selected = 2
                    select_story(ob, uno, STORY, 2)
                elif MAP3_rect.collidepoint(mouse_pos):
                    selected = 3
                    select_story(ob, uno, STORY, 3)
                elif MAP4_rect.collidepoint(mouse_pos):
                    selected = 4
                    select_story(ob, uno, STORY, 4)

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
                        pass
                    elif select_yes_no == 1: # no를 선택하면 다시 스토리 선택 화면으로 돌아간다
                        uno.background = pygame.image.load('./images/Story map.jpg')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/930, uno.screen_height/690))
                        uno.screen.blit(uno.background, (-10, -10))
                        return
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_rect.collidepoint(mouse_pos):
                    select_yes_no = 0
                    pass
                elif no_rect.collidepoint(mouse_pos):
                    select_yes_no = 1
                    uno.background = pygame.image.load('./images/Story map.jpg')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/930, uno.screen_height/690))
                    uno.screen.blit(uno.background, (-10, -10))
                    return

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

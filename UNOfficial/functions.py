import itertools
import random
import pygame
import sys
from pygame.locals import *

def peek(s):
    """ Peek - 리스트에서 가장 마지막 원소를 리턴한다 """
    return s[-1]

# driver.py에서 1번째로 호출
def create(Object):
    """ 카드들을 처리한다 """
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

    for j in range(4):  # 플레이어 4명에게 카드를 7장씩 나누어 준다
        for _ in range(7):
            Object.player_list[j].append(Object.deck1.pop())

    # Object.player_list[0] = [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Reverse', 'Green'), ("+2", "Blue")]

# play_this_card에서 4번째로 호출
def set_curr_player(ob, default): # (ob, False)
    """ 다음 플레이어 결정 """
    if ob.current[0] == 'Reverse' and ob.special_check == 0:
        ob.direction_check *= -1  # 진행 방향 리버스
        ob.special_check = 1  # 기술 카드 상태 비활성화
    
    if ob.current[0] == 'Skip' and ob.special_check == 0:
        ob.special_check = 1
        ob.position = (ob.position + ob.direction_check) % 4 # 플레이 하는 플레이어 인덱스 (Playing player index)

    if default: # AI가 플레이 하는 경우 True, 유저인 경우 False
        ob.position = (ob.position + ob.direction_check) % 4 # direction_check대로 진행한다

# driver.py에서 2번째로 호출
def re_initialize(ob):
    """ 모든 게임 변수와 플래그를 재초기화한다 """
    ob.message = "" # 메세지를 출력하기 위해서
    ob.winner = -1
    ob.player_playing = False
    ob.play_lag = -1
    ob.player_list = [[], [], [], []]
    ob.deck1 = list()
    ob.deck2 = list()
    ob.direction_check = 1  # Flag to check direction of play
    ob.position = -1  # 위치 카운터
    ob.special_check = 0  # Flag to check status of special card
    ob.current = tuple()
    ob.drawn, ob.played, ob.choose_color = False, False, False
    ob.uno = [True] * 4
    ob.easy = False

    # 카드 덱을 세팅하고, 버려진 카드덱에 카드 한장 놓았고, 플레이어들에게 카드를 배분한다
    create(ob)

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
def play_this_card(ob, card): # ob = ess, card = ess.player_list[0][int((625 - i) / 50)
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
            set_curr_player(ob, False)

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
    if not ob.easy:  # Color picker for hard mode, 하드 모드에서는 색깔을 선택한다
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
    else: 
        new_color = random.choice(ob.color) # 이지 모드에서는 랜덤으로 색깔을 선택한다
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
def bot_action(ob, sounds):
    """ AI 로직 구현 """
    ob.message = ""
    ob.uno[ob.position] = False # 플레이하는 AI의 UNO 외침 플래그를 초기화한다
    ob.played_check = 0 # ??
    
    # 버려진 카드 덱의 맨 위에 있는 기술 카드가 +2 또는 +4이고, 기술 카드 상태가 활성화 되었다면
    if (ob.current[0] == '+1' or ob.current[0] == '+2' or ob.current[0] == '+4') and ob.special_check == 0:
        handle24(ob, int(ob.current[0][1]))
        ob.played_check = 1

    else:
        check = 0
        for item in ob.player_list[ob.position]: # AI가 가지고 있는 카드 중에서
            if ob.current[1] == item[1] or ob.current[0] == item[0]: # 색깔이나 숫자가 같은 카드가 있다면
                bot_play_card(ob, item)

                if item[1] == 'Black': # 그게 와일드 카드면
                    handle_black(ob, item)

                ob.player_list[ob.position].remove(item)

                set_curr_player(ob, False)
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
        
        if len(ob.player_list[ob.position]) == 1:
            wait_time = random.randint(1000, 2000)
            if ob.easy and random.randint(0, 1): # 이지 모드에서는 1/2 확률로 UNO를 외친다
                pygame.time.delay(wait_time)
                ob.uno[ob.position] = True
                ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]
                sounds.uno.play()
            elif ob.easy == False: # 하드 모드는 무조건 UNO를 외친다
                pygame.time.delay(wait_time)
                ob.uno[ob.position] = True
                ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]
                sounds.uno.play()

# =====================================================================
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.SysFont(textFont, textSize)
    newText = newFont.render(message, True, textColor)
    return newText

""" 시작 화면 """
def main_menu(ob, uno):
    selected = 1

    start_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.4), 200, 50)
    story_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.5), 200, 50)
    setting_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.6), 200, 50)
    quit_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.7), 200, 50)

    while True:
        pygame.init()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == K_DOWN:
                    if selected >= 4:
                        selected = 4
                    else:
                        selected = selected + 1
                if event.key == K_RETURN: # K_RETURN은 엔터키
                    if selected <= 1: # 게임 시작 버튼
                        ob.play_mode = set_start(ob, uno)
                        if (ob.play_mode == "IN GAME"):
                            return
                        uno.screen.blit(uno.background, (-30, -30))
                    if selected == 2: # 스토리 모드 버튼
                        selected = 2
                        ob.play_mode = story_mode(ob, uno)
                        uno.screen.blit(uno.background, (-30, -30))
                        return
                    if selected == 3: # 설정 버튼
                        ob.play_mode = "SETTING"
                        return
                    if selected >= 4: # 종료 버튼
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
                    ob.play_mode = story_mode(ob, uno)
                    uno.screen.blit(uno.background, (-30, -30))
                    return
                elif setting_rect.collidepoint(mouse_pos): # 설정 버튼
                    selected = 3
                    ob.play_mode = "SETTING"
                    return
                elif quit_rect.collidepoint(mouse_pos): # 종료 버튼
                    text_quit = text_format("QUIT", uno.font, 50, (0,0,0))
                    uno.screen.blit(text_quit, quit_rect)
                    pygame.display.update()
                    pygame.time.delay(500)
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
            text_quit = text_format("QUIT", uno.font, 50, (0,0,0))
        else:
            text_quit = text_format("QUIT", uno.font, 50, (255, 255, 255))

        # 메뉴 아이템 표시
        start_rect = text_start.get_rect()
        story_rect = text_story.get_rect()
        setting_rect = text_setting.get_rect()
        quit_rect = text_quit.get_rect()

        start_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.4), 200, 50)
        story_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.5), 200, 50)          
        setting_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.6), 200, 50)
        quit_rect = pygame.Rect(uno.screen_width/2-50, int(uno.screen_height*0.7), 200, 50)

        uno.screen.blit(text_start, start_rect)
        uno.screen.blit(text_story, story_rect)
        uno.screen.blit(text_setting, setting_rect)
        uno.screen.blit(text_quit, quit_rect)

        pygame.display.update()
        pygame.display.set_caption("UNO!")

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
                if event.key == K_UP:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == K_DOWN:
                    if selected >= 5:
                        selected = 5
                    else:
                        selected = selected + 1
                if event.key == K_RETURN:
                    if selected <= 1:
                        uno.playernum = 2
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.playernum)
                    if selected == 2:
                        uno.playernum = 3
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.playernum)
                    if selected == 3:
                        uno.playernum = 4
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.playernum)
                    if selected == 4:
                        uno.playernum = 5
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return set_players(ob, uno, uno.playernum)
                    if selected >= 5:
                        uno.background = pygame.image.load('./images/Main_background.png')
                        return "LOAD PAGE"
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if two_rect.collidepoint(mouse_pos):
                    uno.playernum = 2
                    selected = 1
                    return set_players(ob, uno, uno.playernum)
                elif three_rect.collidepoint(mouse_pos):
                    uno.playernum = 3
                    selected = 2
                    return set_players(ob, uno, uno.playernum)
                elif four_rect.collidepoint(mouse_pos):
                    uno.playernum = 4
                    selected = 3
                    return set_players(ob, uno, uno.playernum)
                elif five_rect.collidepoint(mouse_pos):
                    uno.playernum = 5
                    selected = 4
                    return set_players(ob, uno, uno.playernum)
                elif quit_rect.collidepoint(mouse_pos):
                    selected = 5
                    uno.background = pygame.image.load('./images/Main_background.png')
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
            text_quit = text_format("BACK", uno.font, 50, (255,24,0))
        else:
            text_quit = text_format("BACK", uno.font, 50, (0,0,0))

        two_rect = text_two.get_rect()
        three_rect = text_three.get_rect()
        four_rect = text_four.get_rect()
        five_rect = text_five.get_rect()
        quit_rect = text_quit.get_rect()

        two_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(180/600)), 200, 50)
        three_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(240/600)), 200, 50)
        four_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(300/600)), 200, 50)
        five_rect = pygame.Rect(int(uno.screen_width*(275/800)), int(uno.screen_height*(360/600)), 200, 50)
        quit_rect = pygame.Rect(int(uno.screen_width*(325/800)), int(uno.screen_height*(420/600)), 200, 50)

        uno.screen.blit(text_two, two_rect)
        uno.screen.blit(text_three, three_rect)
        uno.screen.blit(text_four, four_rect)
        uno.screen.blit(text_five, five_rect)
        uno.screen.blit(text_quit, quit_rect)
        pygame.display.update()


""" 컴퓨터 플레이어 수 설정 """
def set_players(ob, uno, playernum):
    pygame.init()
    uno.background = pygame.image.load('./images/default.png')
    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
    uno.playernum = playernum
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
                if event.key == K_UP:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == K_DOWN:
                    if selected >= uno.playernum:
                        selected = uno.playernum
                    else:
                        selected = selected + 1
                if event.key == K_RETURN:
                    if selected == uno.playernum:
                        # ob.play_mode = "IN GAME"
                        return "IN GAME"
                    elif selected == 1:
                        uno.background = pygame.image.load('./images/Main_background.png')
                        pass
                    elif selected == 2:
                        uno.background = pygame.image.load('./images/Main_background.png')
                        pass
                    elif selected == 3:
                        uno.background = pygame.image.load('./images/Main_background.png')
                        pass
                    elif selected == 4:
                        uno.background = pygame.image.load('./images/Main_background.png')
                        pass
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if two_rect.collidepoint(mouse_pos):
                    selected = 1
                    pass
                elif three_rect.collidepoint(mouse_pos):
                    selected = 2
                    pass
                elif four_rect.collidepoint(mouse_pos):
                    selected = 3
                    pass
                elif five_rect.collidepoint(mouse_pos):
                    selected = 4
                    pass
                elif start_rect.collidepoint(mouse_pos):
                    selected = uno.playernum
                    # ob.play_mode = "IN GAME"
                    return "IN GAME"
        # 선택한 글자의 색을 빨간색으로 표시      
        if selected == 1:
            text_two = text_format("COM 1", uno.font, 50, (255,24,0))
        else:
            text_two = text_format("COM 1", uno.font, 50, (0,0,0))
        if selected == 2:
            text_three = text_format("COM 2", uno.font, 50, (255,24,0))
        else:
            text_three = text_format("COM 2", uno.font, 50, (0,0,0))
        if selected == 3:
            text_four = text_format("COM 3", uno.font, 50, (255,24,0))
        else:
            text_four = text_format("COM 3", uno.font, 50, (0,0,0))                
        if selected == 4:
            text_five = text_format("COM 4", uno.font, 50, (255,24,0))
        else:
            text_five = text_format("COM 4", uno.font, 50, (0,0,0))
        if selected == uno.playernum:
            text_start = text_format("START", uno.font, 50, (255,24,0))
        else:
            text_start = text_format("START", uno.font, 50, (0,0,0))

        two_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(150/600)), 200, 50)
        three_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(210/600)), 200, 50)
        four_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(270/600)), 200, 50)
        five_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(330/600)), 200, 50)
        start_rect = pygame.Rect(int(uno.screen_width*(320/800)), int(uno.screen_height*(390/600)), 200, 50)

        if uno.playernum == 2:
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_start, start_rect)
        elif uno.playernum == 3:
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_three, three_rect)
            uno.screen.blit(text_start, start_rect)
        elif uno.playernum == 4:
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_three, three_rect)
            uno.screen.blit(text_four, four_rect)
            uno.screen.blit(text_start, start_rect)
        elif uno.playernum == 5:
            uno.screen.blit(text_two, two_rect)
            uno.screen.blit(text_three, three_rect)
            uno.screen.blit(text_four, four_rect)
            uno.screen.blit(text_five, five_rect)
            uno.screen.blit(text_start, start_rect)

        pygame.display.update()


# =====================================================================
""" 스토리 모드 선택 """
def story_mode(ob, uno):
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
                if event.key == K_DOWN:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == K_UP:
                    if selected >= 5:
                        selected = 5
                    else:
                        selected = selected + 1
                if event.key == K_RETURN: # K_RETURN은 엔터키
                    if selected <= 1:
                        # 실행할 내용
                        pass
                    if selected == 2:
                        # 실행할 내용
                        pass
                    if selected == 3:
                        # 실행할 내용
                        pass
                    if selected == 4:
                        pass
                    if selected >= 5: # 시작 화면으로 돌아간다
                        uno.background = pygame.image.load('./images/Main_background.png')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                        return "LOAD PAGE"

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if MAP1_rect.collidepoint(mouse_pos):
                    selected = 1
                    pass
                elif MAP2_rect.collidepoint(mouse_pos):
                    selected = 2
                    pass
                elif MAP3_rect.collidepoint(mouse_pos):
                    selected = 3
                    pass
                elif MAP4_rect.collidepoint(mouse_pos):
                    selected = 4
                    pass
                elif back_rect.collidepoint(mouse_pos): # 시작 화면으로 돌아간다
                    selected = 5
                    uno.background = pygame.image.load('./images/Main_background.png')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                    return "LOAD PAGE"

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
        
        if selected == 5:
            back_text = text_format("BACK", uno.font, 20, (0,0,0))
        else:
            back_text = text_format("BACK", uno.font, 20, (255, 255, 255))

        # 글자 객체를 그린다
        back_rect = back_text.get_rect()
        MAP1_rect = text_MAP1.get_rect()
        MAP2_rect = text_MAP2.get_rect()
        MAP3_rect = text_MAP3.get_rect()
        MAP4_rect = text_MAP4.get_rect()

        back_rect = pygame.Rect(uno.screen_width/2-470, int(uno.screen_height*0.2-100), 200, 50)
        MAP1_rect = pygame.Rect(uno.screen_width/2-275, int(uno.screen_height*0.8+20), 200, 50)
        MAP2_rect = pygame.Rect(uno.screen_width/2-245, int(uno.screen_height*0.2+20), 200, 50)          
        MAP3_rect = pygame.Rect(uno.screen_width/2-40, int(uno.screen_height*0.5-20), 200, 50)
        MAP4_rect = pygame.Rect(uno.screen_width/2+140, int(uno.screen_height*0.2-20), 200, 50)

        uno.screen.blit(back_text, back_rect)
        uno.screen.blit(text_MAP1, MAP1_rect)
        uno.screen.blit(text_MAP2, MAP2_rect)
        uno.screen.blit(text_MAP3, MAP3_rect)
        uno.screen.blit(text_MAP4, MAP4_rect)

        pygame.display.update()
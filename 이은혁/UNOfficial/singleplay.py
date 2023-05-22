import pygame
import sys
import random
import itertools
from pygame.locals import *
from functions import KEYS, draw_text, text_format, function_key_config, update_saves # singleplay.py에서 사용할 키값들을 저장하는 딕셔너리
from settings import volumesetting, load_setting

def peek(s):
    """ Peek - 리스트에서 가장 마지막 원소를 리턴한다 """
    return s[-1]

# driver.py에서 1번째로 호출
def create(Object, uno, card_num):
    """ 카드를 생성하고, 분배한다 """
    for _ in range(uno.player_num):
        Object.player_list.append([]) # 플레이어 수만큼 2차원 리스트 생성 -> 플레이어들의 카드를 저장하기 위해서
    
    Object.shouted_uno = [False] * uno.player_num # 각 플레이어가 UNO를 외쳤는지 저장하는 플래그

    a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9',
            '+1', '+1', '+2', '+2', '+4', 'Skip', 'Skip', 'Reverse', 'Reverse') # 색깔 +1, +4 기술 카드 추가
    Object.deck1 = list(itertools.product(a, Object.color)) # 덱 생성 -> 총 120장
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
        for _ in range(card_num):
            Object.player_list[j].append(Object.deck1.pop())

    # Object.player_list[0] = [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Reverse', 'Green'), ("+2", "Blue")]

def stage1_al(Object, uno, card_num): #첫번째 스테이지 알고리즘
    Object.deck1.append(Object.deck2.pop()) # 버려진 카드 한장 있는걸 뽑을 덱으로 옮김
    for index,j in enumerate(Object.player_list):
        if index != 0:
            for i in range(card_num):
                Object.deck1.append(Object.player_list[index].pop())
    random.shuffle(Object.deck1)
    for index,j in enumerate(Object.player_list):
        if index == 0:
            continue
        for _ in range(card_num):  
            adding = random.randrange(1,10)
            for i in range(10):
                if adding >=5 or adding <= 10:
                    if i == 9:
                        Object.player_list[index].append(Object.deck1.pop())
                    else:
                        if peek(Object.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
                                        ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
                                        ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
                                        ('+2', 'Blue'), ('+2', 'Yellow'), ('+1', 'Red'), ('+1', 'Green'),
                                        ('+1', 'Blue'), ('+1', 'Yellow'), ('+4', 'Red'), ('+4', 'Green'),
                                        ('+4', 'Blue'), ('+4', 'Yellow')]:
                            Object.player_list[index].append(Object.deck1.pop())
                            break

                        else:
                            random.shuffle(Object.deck1)
                else:
                    if i == 9:
                        Object.player_list[index].append(Object.deck1.pop())
                    else:
                        if peek(Object.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
                                        ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
                                        ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
                                        ('+2', 'Blue'), ('+2', 'Yellow'), ('+1', 'Red'), ('+1', 'Green'),
                                        ('+1', 'Blue'), ('+1', 'Yellow'), ('+4', 'Red'), ('+4', 'Green'),
                                        ('+4', 'Blue'), ('+4', 'Yellow')]:
                            random.shuffle(Object.deck1)
                        else:
                            Object.player_list[index].append(Object.deck1.pop())
                            break
    
    while peek(Object.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
                            ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
                            ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
                            ('+2', 'Blue'), ('+2', 'Yellow'), ('+1', 'Red'), ('+1', 'Green'),
                            ('+1', 'Blue'), ('+1', 'Yellow'), ('+4', 'Red'), ('+4', 'Green'),
                            ('+4', 'Blue'), ('+4', 'Yellow')]: # 첫 번째 카드는 기술카드가 아니어야 한다
        random.shuffle(Object.deck1)
    Object.deck2.append(Object.deck1.pop())
    Object.current = peek(Object.deck2) # 버려진 카드 덱의 peek

def stage2_al(Object, uno, card_num): # 2번째 스테이지 알고리즘
    for i in range(card_num):
        popped_item = Object.player_list[0].pop()
        Object.deck2.append(popped_item)
        Object.deck1.append(popped_item)
    for i in range(1,len(Object.player_list)):
        for _ in range(card_num):
            Object.deck1.append(Object.player_list[i].pop())
    random.shuffle(Object.deck1)
    
    i=0
    for card in range(len(Object.deck1)):
        if i==0:
            Object.player_list[i].append(Object.deck1.pop())
            i+=1 
        elif i==1:
            Object.player_list[i].append(Object.deck1.pop())
            i+=1    
        elif i==2:
            if i == (len(Object.player_list)-1):
                Object.player_list[i].append(Object.deck1.pop())
                i=0
            else:
                Object.player_list[i].append(Object.deck1.pop())
                i+=1
        elif i==3:
            if i == (len(Object.player_list)-1):
                Object.player_list[i].append(Object.deck1.pop())
                i=0
            else:
                Object.player_list[i].append(Object.deck1.pop())
                i+=1
        elif i==4:
            if i == (len(Object.player_list)-1):
                Object.player_list[i].append(Object.deck1.pop())
                i=0
            else:
                Object.player_list[i].append(Object.deck1.pop())
                i+=1
        elif i==5:
            Object.player_list[i].append(Object.deck1.pop())
            i=0
                

def stage3_al(ob, uno): # 고쳐야할 것 한 3번째 턴에 바꾸는것. 블랙때 안바뀌는듯?
    changed = False
    if ob.current[1] == 'Black':
        target=random.randrange(1,5)
        if target == 1:
            change_card_color(ob, "Red")
        elif target == 2:
            change_card_color(ob, "Blue")
        elif target == 3:
            change_card_color(ob, "Green")
        elif target == 4:
            change_card_color(ob, "Yellow")
        changed = True

    else:
        for card in ob.deck2:
            if changed == False:#카드의 색이 바뀌었는지 플래그
                if card[0] == ob.current[0] and card[1]!= ob.current[1]:
                    #여기 고치는중    
                        ob.deck2.remove(card)
                        ob.deck2.append(card)
                        ob.current = peek(ob.deck2)
                        changed = True
            else:
                break
        for card in ob.deck1:
            if changed == False:#카드의 색이 바뀌었는지 플래그
                if card[0] == ob.current[0] and card[1]!= ob.current[1]:
                    #여기 고치는중    
                        ob.deck1.remove(card)
                        ob.deck1.append(card)
                        ob.current = peek(ob.deck1)
                        changed = True
            else:
                ob.current = peek(ob.deck2)
                break
        
    if changed == False:
        ob.current = peek(ob.deck2)
        pass#그 지랄을 했는데도 안변한경우

def stage4_al(ob,uno):#고쳐야할 것 들, 블랙카드 낼시 한장 안사라짐, 3장일때 하나 내고 uno 안함
    if ob.position !=0:
        ob.deck2.insert(0, ob.player_list[ob.position].pop(0))

# play_this_card에서 4번째로 호출
def set_curr_player(ob, uno, default): # (ob, uno, False)
    """ 다음 플레이어 결정 """
    ob.Turn_count += 1
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
    ob.Turn_count = 1

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
def play_this_card(ob, uno, card, AltCol_path): # ob = ess, card = ess.player_list[0][int((625 - i) / 50)
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
            move_card(ob, uno, "./images/"+ AltCol_path + str(card[1]) + str(card[0]) + ".png") # 카드를 냈으면, 카드를 옮긴다
            set_curr_player(ob, uno, False)

        if card[1] == 'Black':
            ob.played, ob.drawn = True, True
            ob.choose_color = True # 와일드 카드는 모두 색깔을 선택하게 한다
            ob.player_list[0].remove(card)
            ob.deck2.append(card)
            move_card(ob, uno, "./images/" + AltCol_path + str(card[1]) + str(card[0]) + ".png") # 카드를 냈으면, 카드를 옮긴다

# driver.py에서 6번째로 호출
def change_card_color(ob, color): # color = "Red" or "Blue" or "Green" or "Yellow"가 들어간다
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
def handle_black(ob, uno, item):
    """ 와일드 카드를 처리한다 """
    move_card(ob, uno, "./images/Back_computer.png")

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
def bot_play_card(ob, uno, item):
    """ AI가 카드를 플레이한다 """
    move_card(ob, uno, "./images/Back_computer.png")
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
                bot_play_card(ob, uno, item)

                if item[1] == 'Black': # 그게 와일드 카드면
                    handle_black(ob, uno, item)

                ob.player_list[ob.position].remove(item)

                set_curr_player(ob, uno, False)
                
                check = 1
                break

        if check == 0: # AI가 낼 수 있는 카드가 없다면
            black_check = 0
            for item in ob.player_list[ob.position]:
                if item[1] == 'Black': # 근데 와일드 카드가 있다면
                    ob.message = "%s plays %s" % (ob.bot_map[ob.position], item[0] + " " + item[1])
                    handle_black(ob, uno, item)
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
                    handle_black(ob, uno, new_card) 
                elif new_card[1] == ob.current[1] or new_card[0] == ob.current[0]: # 뽑은 카드가 버려진 카드 덱의 맨 위에 있는 카드와 색깔이나 숫자가 같다면
                    bot_play_card(ob, uno, new_card)
                else:
                    ob.player_list[ob.position].append(new_card)

# ============================================================================================================
""" x좌표, y좌표, 이미지의 원래 너비, 원래 높이를 받아서, 화면 크기에 맞게 조정한 뒤, pygame.Rect 객체를 반환 """
def Make_Rect(uno, x, y, w, h):
    return pygame.Rect(uno.screen_width*(x/1000), uno.screen_height*(y/600), uno.screen_width*(w/1000), uno.screen_height*(h/600))

""" 간단한 애니메이션 효과를 구현하는 함수 """
def move_card(ess, uno, img_path):
    width, height = uno.screen_width, uno.screen_height
    duration = 100 # 틱을 미리 정함
    card_img = pygame.image.load(img_path) # 입력받은 이미지 경로를 통해 이미지를 불러옴
    card_img = pygame.transform.scale_by(card_img, (uno.screen_width/1000, uno.screen_height/600))

    if ess.player_playing == False:
        distance_x = 200 / duration
        distance_y = 0
        start_pos = ((width*(800/1000)), height/600*(-110 + ess.position * 120))
    else:
        distance_x = 0
        distance_y = 200 / duration
        start_pos = (width*(490/1000), height*(380/600))

    # Get the current time
    start_time = pygame.time.get_ticks()

    # while 시작에서 500 tick이 지나면 while 종료
    while pygame.time.get_ticks() - start_time < duration:

        # Calculate the position of the image in this frame
        elapsed_time = pygame.time.get_ticks() - start_time
        current_pos_x = int(start_pos[0] - (elapsed_time * distance_x))
        current_pos_y = int(start_pos[1] - (elapsed_time * distance_y))

        # Blit the moving image to the background surface at the current position
        uno.screen.blit(card_img, (current_pos_x, current_pos_y))

        pygame.display.update()

        # Wait for a short amount of time to control the animation speed
        pygame.time.wait(10)
# ============================================================================================================
def game_screen(ess, uno, sound, img, PM, saves, STORY):
    pygame.init()
    create(ess, uno, 7)
    print(saves)
    if STORY.Is_stage_on[0] == True:
        stage1_al(ess, uno, 7)
    elif STORY.Is_stage_on[1] == True:
        stage2_al(ess, uno, 7)
    
    disp = False
    win_dec = False  # 승자가 선언되면 True
    pen_check = False  # UNO 페널티 체크 플래그

    # 타이머 변수 세팅
    max_time = 10 # 플레이어에게 10초의 시간을 주고, 그 시간 안에 카드를 내지 않으면 자동으로 턴이 넘어간다
    
    img_path = saves["color_change"]+"/"
    AltCol_path = saves["color_change"] + "/" # 이미지 경로
    joe_fin = "./fonts/JosefinSans-Bold.ttf"
    width, height = uno.screen_width, uno.screen_height # 화면 크기
    
    selected_card = 0 # 선택한 카드의 인덱스
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if ess.player_playing:
                    if event.key == KEYS["up"]: # 선택한 카드를 낸다
                        play_this_card(ess, uno, ess.player_list[0][selected_card], AltCol_path)
                        sound.card_played.play()
                        selected_card = 0 # 카드를 낸 뒤에는 선택한 카드를 초기화
                    elif event.key == KEYS["down"]: # 덱에서 카드 한장 드로우
                        take_from_stack(ess)
                        sound.card_drawn.play()
                    elif event.key == KEYS["select"]: # 턴을 넘긴다
                        sound.click.play()
                        ess.player_playing = False
                        ess.play_lag = 0
                if event.key == KEYS["left"]: # 왼쪽으로 카드 선택
                    if (selected_card >= len(ess.player_list[0]) - 1):
                        selected_card = 0
                    else:
                        selected_card += 1
                elif event.key == KEYS["right"]: # 오른쪽으로 카드 선택
                    if (selected_card <= 0):
                        selected_card = len(ess.player_list[0]) - 1
                    else:
                        selected_card -= 1
                elif event.key == K_ESCAPE: # ESC 버튼을 누르면 게임이 일시정지됨
                    sound.click.play()
                    ess.is_game_paused = True
                    paused_game(ess, uno, sound, PM, saves)
                    img_path = saves["color_change"] + "/" # 이미지 경로 갱신
            if event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if ess.player_playing:
                    # 1) 유저가 카드 위에 마우스를 올려놓았을 때
                    for i in range(int((width/1000)*410), int((width/1000)*410 - 30 * len(ess.player_list[0])), -30):
                        if i < mouse_pos[0] < (i + 30) and height*(520/600) < mouse_pos[1] < height*(590/600):
                            selected_card = int(((width/1000)*425 - i) / 30)
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ess.player_playing:  # 유저가 플레이 중일 때, 동작 로직
                    if uno_button_rect.collidepoint(mouse_pos): # 1) UNO 버튼을 클릭
                        sound.uno.play()
                        ess.shouted_uno[0] = True
                    if play_done_rect.collidepoint(mouse_pos): # 2) 턴 종료 버튼을 클릭
                        sound.click.play()
                        ess.player_playing = False
                        ess.play_lag = 0
                    # 3) 낼 카드가 없어 덱에서 카드를 뽑을 때
                    elif card_deck_rect.collidepoint(mouse_pos):
                        take_from_stack(ess)
                        sound.card_drawn.play()

                    # 4) 유저가 카드를 클릭했는지 감지
                    for i in range(int((width/1000)*410), int((width/1000)*410 - 30 * len(ess.player_list[0])), -30):
                        if i < mouse_pos[0] < (i + 30) and height*(520/600) < mouse_pos[1] < height*(590/600):
                            play_this_card(ess, uno, ess.player_list[0][int(((width/1000)*410 - i) / 30)], AltCol_path)
                            sound.card_played.play()
                            selected_card = 0 # 카드를 낸 뒤에는 선택한 카드를 초기화

                # 5) 이번 턴에 와일드 카드를 냈으면, 새로운 색깔 선택
                if ess.choose_color:
                    if width*(395/1000) < mouse_pos[0] < width*(440/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 빨간색 버튼
                        ess.choose_color = False
                        change_card_color(ess, "Red")
                        sound.click.play()
                    if width*(450/1000) < mouse_pos[0] < width*(495/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 초록색 버튼
                        ess.choose_color = False
                        change_card_color(ess, "Green")
                        sound.click.play()
                    if width*(505/1000) < mouse_pos[0] < width*(550/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 파란색 버튼
                        ess.choose_color = False
                        change_card_color(ess, "Blue")
                        sound.click.play()
                    if width*(560/1000) < mouse_pos[0] < width*(605/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 노란색 버튼
                        ess.choose_color = False
                        change_card_color(ess, "Yellow")
                        sound.click.play()
                
                if pause_button_rect.collidepoint(mouse_pos): # 일시 정지 버튼을 클릭
                    sound.click.play()
                    ess.is_game_paused = True
                    paused_game(ess, uno, sound, PM, saves)
                    img_path = saves["color_change"] + "/" # 이미지 경로 갱신

        # 처음 덱 섞는 소리
        if ess.play_lag == -1:
            sound.shuffled.play()

        # 승자가 생겼는지 체크
        for idx, item in enumerate(ess.player_list):
            if len(item) == 0: # 플레이어의 카드가 0장이면 게임에서 승리한다.
                win_dec = True
                ess.winner = idx # 승자의 인덱스 저장
                ess.play_mode = PM.win # 승리 모드로 전환
                return

        pause_button_rect = Make_Rect(uno, 10, 10, 32, 32)
        uno_button_rect = Make_Rect(uno, 640, 500, 64, 64)
        play_done_rect = Make_Rect(uno, 565, 505, 64, 64)
        card_deck_rect = Make_Rect(uno, 140, 140, 85, 115)
        
        # 필수적인 이미지 표현
        uno.screen.blit(img.bg, (0, 0)) # 배경 화면
        uno.screen.blit(img.pause, (width*(10/1000), height*(10/1000))) # 일시 정지 버튼
        uno.screen.blit(img.card_back, (width*(140/1000), height*(140/600))) # 카드 덱 이미지
        uno.screen.blit(img.uno_button, (width*(640/1000), height*(500/600))) # -> 일단 플레이어의 UNO 버튼은 항상 표시되게 함

        try: # 게임을 시작하면, 버려진 카드 덱에 놓이는 처음 카드 이미지를 표시한다
            uno.screen.blit(pygame.image.load("./images/" + img_path + ess.current[1] + str(ess.current[0]) + ".png"), (width*(380/1000), height*(140/600)))
        except:
            uno.screen.blit(pygame.image.load("./images/" + img_path + ess.current[1] + ".png"), (width*(380/1000), height*(140/600)))

        uno.screen.blit(img.p_user, (width*(475/1000), height*(490/600))) # 유저 플레이어 이미지
        
        text_user = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.bot_map[6], True, (255, 238, 46))
        uno.screen.blit(text_user, [width*(490/1000), height*(460/600)]) # 유저 이름 텍스트
        
        for i in range(len(ess.player_list[0])):
            x_diff = i % 10
            y_diff = i // 10
            if (selected_card == i): # 카드 선택 애니메이션 구현
                uno.screen.blit(pygame.image.load("./images/" + img_path + ess.player_list[0][i][1] + str(ess.player_list[0][i][0]) + ".png"), (width*((390 - 30 * x_diff)/1000), height*((480 - 80 * y_diff)/600)))
            else:
                uno.screen.blit(pygame.image.load("./images/" + img_path + ess.player_list[0][i][1] + str(ess.player_list[0][i][0]) + ".png"), (width*((390 - 30 * x_diff)/1000), height*((520 - 80 * y_diff)/600)))
        # 카드 선택의 가시성을 위해 선택된 카드를 한 번 다시 그렸다
        uno.screen.blit(pygame.image.load("./images/" + img_path + ess.player_list[0][selected_card][1] + str(ess.player_list[0][selected_card][0]) + ".png"), (width*((390 - 30 * (selected_card % 10))/1000), height*((480 - 80 * (selected_card // 10))/600)))
        
        text_p1 = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.bot_map[1], True, (255, 238, 46))
        text_p2 = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.bot_map[2], True, (255, 238, 46))
        text_p3 = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.bot_map[3], True, (255, 238, 46))
        text_p4 = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.bot_map[4], True, (255, 238, 46))
        text_p5 = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.bot_map[5], True, (255, 238, 46))

        # 컴퓨터 플레이어들의 초기 카드 이미지 표시 -> 컴퓨터의 카드가 11장 이상이면 카드 이미지 x 숫자로 표시
        if uno.player_num >= 2:
            uno.screen.blit(img.p1, (width*(940/1000), height*(10/600))) # JARVIS 이미지
            uno.screen.blit(text_p1, [width*(860/1000), height*(10/600)]) # JARVIS 텍스트 표시
            if len(ess.player_list[1]) >= 11: 
                uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(60/600)])
                draw_text(uno, ("x " + str(len(ess.player_list[1]))), 40, (0, 0, 255), width*(850/1000), height*(70/600))
            else:
                for i in range(len(ess.player_list[1])): # JARVIS의 카드 이미지
                    uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(60/600)))
            if uno.player_num >= 3:
                uno.screen.blit(img.p2, (width*(940/1000), height*(130/600))) # EDITH 이미지
                uno.screen.blit(text_p2, [width*(860/1000), height*(130/600)]) # EDITH 텍스트 표시
                if len(ess.player_list[2]) >= 11:
                    uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(180/600)])
                    draw_text(uno, ("x " + str(len(ess.player_list[2]))), 40, (0, 0, 255), width*(850/1000), height*(190/600))
                else:
                    for i in range(len(ess.player_list[2])): # EDITH의 카드 이미지
                        uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(180/600)))
                if uno.player_num >= 4:
                    uno.screen.blit(img.p3, (width*(940/1000), height*(250/600))) # FRIDAY 이미지
                    uno.screen.blit(text_p3, [width*(860/1000), height*(250/600)]) # FRIDAY 텍스트 표시
                    if len(ess.player_list[3]) >= 11:
                        uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(300/600)])
                        draw_text(uno, ("x " + str(len(ess.player_list[3]))), 40, (0, 0, 255), width*(850/1000), height*(310/600))
                    else:
                        for i in range(len(ess.player_list[3])): # FRIDAY의 카드 이미지
                            uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(300/600)))
                    if uno.player_num >= 5:
                        uno.screen.blit(img.p4, (width*(940/1000), height*(370/600))) # BRIAN 이미지
                        uno.screen.blit(text_p4, [width*(860/1000), height*(370/600)]) # BRIAN 텍스트 표시
                        if len(ess.player_list[4]) >= 11:
                            uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(420/600)])
                            draw_text(uno, ("x " + str(len(ess.player_list[4]))), 40, (0, 0, 255), width*(850/1000), height*(430/600))
                        else:
                            for i in range(len(ess.player_list[4])): # BRIAN의 카드 이미지
                                uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(420/600)))
                        if uno.player_num == 6:
                            uno.screen.blit(img.p5, (width*(940/1000), height*(490/600))) # SWIFT 이미지
                            uno.screen.blit(text_p5, [width*(860/1000), height*(490/600)]) # SWIFT 텍스트 표시
                            if len(ess.player_list[5]) >= 11:
                                uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(540/600)])
                                draw_text(uno, ("x " + str(len(ess.player_list[5]))), 40, (0, 0, 255), width*(850/1000), height*(550/600))
                            else:
                                for i in range(len(ess.player_list[5])): # SWIFT의 카드 이미지
                                    uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(540/600)))

        text = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.message, True, (255, 238, 46))
        uno.screen.blit(text, [width*(140/1000), height*(110/600)]) # 게임 진행 메시지

        if ess.choose_color: # 유저가 와일드 카드를 냈으면, 색깔을 선택할 수 있게 이미지를 표시한다
            uno.screen.blit(img.pick_red, (width*(395/1000), height*(390/600)))
            uno.screen.blit(img.pick_green, (width*(450/1000), height*(390/600)))
            uno.screen.blit(img.pick_blue, (width*(505/1000), height*(390/600)))
            uno.screen.blit(img.pick_yellow, (width*(560/1000), height*(390/600)))

        # 어떤 플레이어가 UNO를 외쳤다면, UNO 이미지를 표시한다
        if ess.shouted_uno[0] == True:
            uno.screen.blit(img.shouted, (width*(490/1000), height*(400/600)))
        for i in range(1, uno.player_num):
            if (ess.shouted_uno[i] == True):
                uno.screen.blit(img.shouted, (width*(800/1000), height*(120 * (i - 1)/600)))
        
        # Play Flow, 플레이 흐름
        if ess.player_playing: # 유저가 플레이하고 있으면 True, 아니면 False
            if ess.play_lag == 400: # 약 10초 타이머
                ess.player_playing = False
                if STORY.Is_stage_on[2] == True:
                    if ess.Turn_count%5 ==0:
                        stage3_al(ess, uno) #카드 색깔 랜덤 바꾸기
                ess.play_lag = 0
            else:
                text = pygame.font.Font(joe_fin, int(height*(20/600))).render(str(max_time - ess.play_lag//40), True, (255, 238, 46))
                uno.screen.blit(text, [width*(550/1000), height*(460/600)])
                
                if not ess.drawn and not ess.played:  # Checking for previous special card overheads, 이전에 기술 카드를 냈는지 확인
                    if ess.current[0] == '+1' and ess.special_check == 0:  # Draw 1
                        for _ in range(1):
                            try:
                                ess.player_list[0].append(ess.deck1.pop())
                            except:
                                ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                                random.shuffle(ess.deck1)
                                ess.player_list[0].append(ess.deck1.pop())
                        ess.special_check = 1
                        ess.shouted_uno[0] = False
                        ess.player_playing = False
                    
                    elif ess.current[0] == '+2' and ess.special_check == 0:  # Draw 2
                        for _ in range(2):
                            try:
                                ess.player_list[0].append(ess.deck1.pop())
                            except:
                                ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                                random.shuffle(ess.deck1)
                                ess.player_list[0].append(ess.deck1.pop())
                        ess.special_check = 1
                        ess.shouted_uno[0] = False
                        ess.player_playing = False

                    elif ess.current[0] == '+4' and ess.special_check == 0:  # Draw 4
                        for _ in range(4):
                            try:
                                ess.player_list[0].append(ess.deck1.pop())
                            except:
                                ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                                random.shuffle(ess.deck1)
                                ess.player_list[0].append(ess.deck1.pop())
                        ess.special_check = 1
                        ess.shouted_uno[0] = False
                        ess.player_playing = False
                    
                    if len(ess.player_list[0]) == 1 and ess.shouted_uno[0] == False:
                        # 이전 턴에 UNO를 외치지 않았는데, 카드가 1장 남았다면,
                        try: 
                            ess.player_list[0].append(ess.deck1.pop()) # 페널티로 덱에서 카드 한장을 뽑는다.
                        except:
                            ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                            random.shuffle(ess.deck1)
                            ess.player_list[0].append(ess.deck1.pop())
                        finally:
                            ess.message = "You didn't shout UNO! Penalty card drawn!"
                            penalty_text = pygame.font.Font(joe_fin, int(height*(20/600))).render(ess.message, True, (255, 238, 46))
                            uno.screen.blit(penalty_text, [width*(140/1000), height*(110/600)]) # 게임 진행 메시지

                # img.line은 현재 플레이 해야할 플레이어를 표시하고, 유저는 체크 버튼이 추가로 표시된다
                uno.screen.blit(img.line, (width*(482/1000), height*(550/600)))
                uno.screen.blit(img.done, (width*(565/1000), height*(505/600)))
                
                if not ess.is_game_paused: # 게임이 일시정지 상태가 아니면
                    ess.play_lag += 1 # 게임의 FPS마다 1씩 증가한다

        else: # AI가 플레이 중이면
            if ess.play_lag == 140:  # 플레이어 간의 행동 사이에 지연을 구현한다
                disp = False
                pen_check = False

                # 다음 플레이어를 결정한다
                set_curr_player(ess, uno, True)


                # 그게 유저의 턴이면
                if ess.position == 0:
                    # ess.shouted_uno[0] = False # 유저 플레이어가 UNO를 외쳤는지 저장하는 플래그를 초기화한다
                    ess.player_playing = True # 유저가 플레이 중임을 표시한다

                else: # 다음 플레이어가 AI라면
                    # 일단 유저의 플래그를 초기화한다
                    ess.played = False
                    ess.drawn = False

                    # 그 다음 AI의 행동을 결정한다
                    bot_action(ess, uno, sound)
                    if STORY.Is_stage_on[2] == True:
                        if ess.Turn_count%5 ==0:
                            stage3_al(ess, uno) #카드 색깔 랜덤 바꾸기
                    if STORY.Is_stage_on[3] == True:
                        stage4_al(ess,uno) #ai 꺼 한장씩 빼기

                ess.play_lag = 0  # 랙 리셋

            else: # 아직 1.4초 안 지났으면
                if win_dec and ess.play_lag == 70:  # 게임의 승자 선언을 0.7초 지연한다
                    ess.play_mode = PM.win

                if not pen_check: # 페널티 체크 플래그, 게임이 처음 시작할 때는 False였다
                    for i in range(1, uno.player_num):
                        if ess.position == i and len(ess.player_list[i]) == 1 and not ess.shouted_uno[i]: # 1장 남았는데, UNO를 외치지 않으면
                            try: 
                                ess.player_list[i].append(ess.deck1.pop()) # 페널티로 덱에서 카드 한장을 뽑는다.
                            except:
                                ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                                random.shuffle(ess.deck1)
                                ess.player_list[i].append(ess.deck1.pop())

                            ess.message = "UNO Penalty!"
                            pen_check = True
                if not ess.is_game_paused: # 게임이 일시정지 상태가 아니면
                    ess.play_lag += 1 # 게임의 FPS마다 1씩 증가한다

                if not disp: # disp을 True로 한다?
                    disp = True

                # 현재 턴인 컴퓨터 플레이어를 검정 선 이미지로 표시한다
                Flag_line = (ess.position + ess.direction_check) % uno.player_num
                for i in range(1, uno.player_num):
                    if Flag_line == i:
                        uno.screen.blit(img.line, (width*(860/1000), height*((-110 + i * 120)/600)))

        pygame.display.update()

""" 게임이 일시정지되었을때의 메뉴 선택 화면 """
def paused_game(ess, uno, sound, PM, saves):
    pygame.init()
    uno.background = pygame.image.load('./images/Pause_background.jpg')
    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/1000, uno.screen_height/600))
    uno.screen.blit(uno.background, (-10, -10))

    selected = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEYS["up"]:
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == KEYS["down"]:
                    if selected >= 4:
                        selected = 4
                    else:
                        selected = selected + 1
                elif event.key == KEYS["select"]:
                    if selected == 1: # 설정 메뉴
                        bg = pygame.image.load("./images/background.png")
                        bg = pygame.transform.scale_by(bg, (uno.screen_width/1000, uno.screen_height/600))
                        uno.screen.blit(bg,(0,0))
                        
                        load_setting(ess, uno, sound, PM, saves) # 처음 설정 화면을 불러온다
                        
                        function_key_config(KEYS) # 키 설정을 불러온다
                        update_saves(saves) # 기타 설정을 불러온다
                        pygame.mixer.music.set_volume(saves["background"]) # 설정에 맞게 소리를 조절한다
                        volumesetting(sound, saves["effects"])
                    elif selected == 2: # 업적 메뉴
                        pass
                    elif selected == 3: # 게임 재개
                        ess.is_game_paused = False

                        uno.background = pygame.image.load('./images/background.png')
                        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/1000, uno.screen_height/600))
                        uno.screen.blit(uno.background, (0, 0))
                        return
                    elif selected == 4:
                        pygame.quit()
                        sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos): # 설정 메뉴
                    selected = 1
                    bg = pygame.image.load("./images/background.png")
                    bg = pygame.transform.scale_by(bg, (uno.screen_width/1000, uno.screen_height/600))
                    uno.screen.blit(bg,(0,0))

                    load_setting(ess, uno, sound, PM, saves) # 처음 설정 화면을 불러온다
                    
                    function_key_config(KEYS) # 키 설정을 불러온다
                    update_saves(saves) # 기타 설정을 불러온다
                    pygame.mixer.music.set_volume(saves["background"]) # 설정에 맞게 소리를 조절한다
                    volumesetting(sound, saves["effects"])
                elif achievement_rect.collidepoint(mouse_pos): # 업적 메뉴
                    selected = 2
                elif resume_rect.collidepoint(mouse_pos): # 게임 재개
                    selected = 3
                    ess.is_game_paused = False
                    uno.background = pygame.image.load('./images/background.png')
                    uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/1000, uno.screen_height/600))
                    uno.screen.blit(uno.background, (0, 0))
                    return
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        uno.background = pygame.image.load('./images/Pause_background.jpg')
        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/1000, uno.screen_height/600))
        uno.screen.blit(uno.background, (-10, -10))

        text_option = text_format("OPTION", uno.font, 50, (255, 255, 255))
        text_achievement = text_format("ACHIEVEMENT", uno.font, 50, (255, 255, 255))
        text_resume = text_format("RESUME GAME", uno.font, 50, (255, 255, 255))
        text_quit = text_format("QUIT", uno.font, 50, (255, 255, 255))

        if selected == 1:
            text_option = text_format("OPTION", uno.font, 50, (0,0,0))
        elif selected == 2:
            text_achievement = text_format("ACHIEVEMENT", uno.font, 50, (0,0,0))
        elif selected == 3:
            text_resume = text_format("RESUME GAME", uno.font, 50, (0,0,0))
        elif selected == 4:
            text_quit = text_format("QUIT", uno.font, 50, (0,0,0))
        
        # 메뉴 객체 생성
        option_rect = pygame.Rect(uno.screen_width*(350/1000), int(uno.screen_height*0.4), 100, 40)
        achievement_rect = pygame.Rect(uno.screen_width*(350/1000), int(uno.screen_height*0.5), 100, 40)
        resume_rect = pygame.Rect(uno.screen_width*(350/1000), int(uno.screen_height*0.6), 100, 40)
        quit_rect = pygame.Rect(uno.screen_width*(350/1000), int(uno.screen_height*0.7), 100, 40)

        uno.screen.blit(text_option, option_rect)
        uno.screen.blit(text_achievement, achievement_rect)
        uno.screen.blit(text_resume, resume_rect)
        uno.screen.blit(text_quit, quit_rect)

        # 그냥 텍스트는 이렇게 출력
        draw_text(uno, "PAUSE", 50, (255, 255, 255), uno.screen_width*(350/1000), int(uno.screen_height*0.1))

        pygame.display.update()
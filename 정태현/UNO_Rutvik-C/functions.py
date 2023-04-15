import itertools
import random
import pygame

def peek(s):
    """ Peek - 리스트에서 가장 마지막 원소를 리턴한다 """
    return s[-1]

# driver.py에서 1번째로 호출
def create(Object):
    """ 카드들을 처리한다 """
    a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9',
        '+2', '+2', 'Skip', 'Skip', 'Reverse', 'Reverse')
    Object.deck1 = list(itertools.product(a, Object.color)) # 덱 생성
    for _ in range(4): # 덱에 와일드 카드 2종류 4장씩 추가
        Object.deck1.append(('Wild', 'Black'))
        Object.deck1.append(('+4', 'Black'))
    random.shuffle(Object.deck1) # 덱 셔플

    while peek(Object.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
                            ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
                            ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
                            ('+2', 'Blue'), ('+2', 'Yellow')]: # 첫번째 카드는 기술카드가 아니어야 한다
        random.shuffle(Object.deck1)

    Object.deck2.append(Object.deck1.pop()) # 첫 번째 카드를 버려진 카드 덱(deck2)에 추가
    Object.current = peek(Object.deck2) # 버려진 카드 덱의 peek

    for j in range(4):  # 플레이어 4명에게 카드를 나누어 준다
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

    if default: # 와일드 카드를 내지 않았으면 False, 냈으면 True
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
    ob.easy = True

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
        if (card[0] == ob.current[0] or card[1] == ob.current[1]) and (card[0] not in ('+4', 'Wild')):
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
    """ +2 / +4 카드를 처리한다 """
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
    """ 와일드 카드 처리 """
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
    if (ob.current[0] == '+2' or ob.current[0] == '+4') and ob.special_check == 0:
        handle24(ob, int(ob.current[0][1]))
        ob.played_check = 1

    else:
        check = 0
        for item in ob.player_list[ob.position]: # AI가 가지고 있는 카드 중에서
            if ob.current[1] in item or ob.current[0] in item: # 색깔이나 숫자가 같은 카드가 있다면
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
                if 'Black' in item: # 근데 와일드 카드가 있다면
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
            else: # 하드 모드는 무조건 UNO를 외친다
                pygame.time.delay(wait_time)
                ob.uno[ob.position] = True
                ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]
                sounds.uno.play()

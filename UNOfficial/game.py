import random
import time
import sys
import itertools
import pygame

from classes import Sound

pygame.init()
pygame.mixer.init()
multi_sound = Sound()


# 4인용 멀티 플레이 UNO 게임 클래스
class Multi_Uno:
    def __init__(self, id):
        self.id = id # 게임 방 번호
        self.ready = False # 게임이 시작되었는지 확인하는 플래그
        self.player_num = 4 # 플레이어 수

        self.player_list = []  # 2차원 리스트 생성 -> 플레이어들의 카드를 저장하기 위해서
        self.player_card_count = [0, 0, 0, 0]  # 플레이어들의 카드 수를 저장하는 리스트
        self.deck1 = list() # deck1 =  카드 덱
        self.deck2 = list() # deck2 =  버려진 카드 덱
        
        self.direction_check = 1  # 게임의 진행 방향, 1은 시계 방향, -1은 반시계 방향
        self.position = -1 # 플레이 하는 플레이어의 인덱스
        self.current = list() # 버려진 카드 덱의 맨 위에 있는 카드

        self.choose_colors = [False, False] # p1, p2

        self.p1_drawn = False  # 유저가 카드를 뽑았는지 확인하는 플래그
        self.p1_played = False # 유저가 카드를 플레이 했는지 확인하는 플래그
        self.p1_player_playing = False # 유저가 플레이하고 있으면 True, 아니면 False

        self.p2_draw = False # 플레이어 2가 카드를 뽑았는지 확인하는 플래그
        self.p2_played = False # 플레이어 2가 카드를 플레이 했는지 확인하는 플래그
        self.p2_player_playing = False # 플레이어 2가 플레이하고 있으면 True, 아니면 False
        
        self.winner = -1
        self.play_lag = -1
        self.play_mode = ""
        self.is_game_paused = False
        
        self.played_check = 0  # Play checker
        self.special_check = 0  # +1, +2, +4, skip으로 한 번 턴이 넘어갔는지 확인하는 플래그
        self.shouted_uno = [False] * 4  # 각 플레이어가 UNO를 외쳤는지 저장하는 플래그
        self.message = "DEALING THE CARDS"  # 인게임 메세지, 한글은 폰트 문제로 인해 사용 불가
        self.player_mapp = {0: "p1Name", 1: "p2Name", 2: "EDITH", 3: "FRIDAY"}  # 플레이어 인덱스를 이름으로 인덱싱
        self.color = ['Blue', 'Red', 'Green', 'Yellow']  # 카드 색깔들

        # self.path = path # 색약 모드를 위해 이미지 파일을 불러오는 경로
    
    # def peek(self, s):
    #     """ Peek - 리스트에서 가장 마지막 원소를 리턴 """
    #     return s[-1]

    # def get_player_card_num(self, player):
    #     """ 어떤 플레이어의 카드 개수를 반환하는 함수 """
    #     return len(self.player_list[player])
    
    def connected(self):
        """ 두 플레이어가 모두 연결되었는지 확인하는 함수 """
        return self.ready
    
    # def get_deck2(self):
    #     """ 버려진 카드 덱을 반환하는 함수 """
    #     return self.deck2

    # def create(self):
    #     """ 카드를 생성하고, 분배 """
    #     for _ in range(4):
    #         self.player_list.append([]) # 플레이어 수만큼 2차원 리스트 생성 -> 플레이어들의 카드를 저장하기 위해서
        
    #     self.shouted_uno = [False] * 4 # 각 플레이어가 UNO를 외쳤는지 저장하는 플래그

    #     a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9',
    #             '+1', '+1', '+2', '+2', '+4', 'Skip', 'Skip', 'Reverse', 'Reverse') # 색깔 +1, +4 특수 카드 추가
    #     self.deck1 = list(itertools.product(a, self.color)) # 덱 생성 -> 총 120장
    #     for _ in range(4): # 덱에 와일드 카드 2종류 4장씩 추가 
    #         self.deck1.append(('Wild', 'Black'))
    #         self.deck1.append(('+4', 'Black'))
    #     random.shuffle(self.deck1) # 덱 셔플
        
    #     while self.peek(self.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
    #                             ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
    #                             ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
    #                             ('+2', 'Blue'), ('+2', 'Yellow'), ('+1', 'Red'), ('+1', 'Green'),
    #                             ('+1', 'Blue'), ('+1', 'Yellow'), ('+4', 'Red'), ('+4', 'Green'),
    #                             ('+4', 'Blue'), ('+4', 'Yellow')]: # 첫 번째 카드는 특수카드가 아니어야 한다
    #         random.shuffle(self.deck1)

    #     self.deck2.append(self.deck1.pop()) # 첫 번째 카드를 버려진 카드 덱(deck2)에 추가
    #     self.current = self.peek(self.deck2) # 버려진 카드 덱의 self.peek

    #     for j in range(4):  # 모든 플레이어에게 카드를 7장씩 나누어 준다
    #         self.player_card_count[j] = 7
    #         for _ in range(7):
    #             self.player_list[j].append(self.deck1.pop())

    #     print(self.current)

    #     # Object.player_list[0] = [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Reverse', 'Green'), ("+2", "Blue")]
    
    # # driver.py에서 2번째로 호출
    # def re_initialize(self):
    #     """ 모든 게임 변수와 플래그를 초기화 """
    #     self.player_list = []
    #     self.player_card_count = [0] * 4
    #     self.deck1 = list()
    #     self.deck2 = list()


    #     self.direction_check = 1  # 게임 플레이 방향 플래그
    #     self.position = -1  # 위치 카운터
    #     self.current = list()

    #     self.p1_drawn, self.p1_played = False, False
    #     self.p2_drawn, self.p2_played = False, False
    #     self.p1_player_playing, self.p2_player_playing = False, False
    #     self.choose_colors = [False, False] # 색깔 선택 플래그

    #     self.winner = -1
    #     self.play_lag = -1
    #     self.is_game_paused = False

    #     self.played_check = 0  # Play checker
    #     self.special_check = 0  # 특수 카드 상태 활성화, 1은 비활성화
    #     self.shouted_uno = [False] * 4
    #     self.message = "" # 메세지를 출력하기 위해서


    # def shout_uno(self, player):
    #     """ UNO를 외치는 함수 """
    #     self.shouted_uno[player] = True


    # def play(self):
    #     """ 게임을 진행하는 로직 """
    #     if self.position == 0:
    #         self.check_uno_penalty(self)

    #         self.play_lag = 0
    #         self.p1_drawn = False
    #         self.p1_played = False
    #         self.choose_colors[0] = False
    #         self.p1_player_playing = True
    #     elif self.position == 1:
    #         self.check_uno_penalty(self)

    #         self.play_lag = 0
    #         self.p2drawn = False
    #         self.p2_played = False
    #         self.choose_colors[1] = False
    #         self.p2_player_playing = True
    #     else: # AI가 플레이하는 상황
    #         self.bot_action(self)


    # def check_winner(self):
    #     """ 플레이어 중에 게임 승리조건을 만족했는지 확인하는 함수 """
    #     try:
    #         for i in range(4):
    #             if len(self.player_list[i]) == 0:
    #                 self.winner = i
    #                 self.message = self.player_mapp[i] + " wins the game! Congratulations!"
    #                 return True
    #     except:
    #         return False


    # def check_uno_penalty(self):
    #     """ UNO 패널티를 확인하는 함수 """
    #     if len(self.player_list[self.position]) == 1 and not self.shouted_uno[self.position]:
    #         try: 
    #             self.player_list[self.position].append(self.deck1.pop()) # 페널티로 덱에서 카드 한장을 뽑는다.
    #         except:
    #             self.deck1, self.deck2 = self.deck2, self.deck1
    #             random.shuffle(self.deck1)
    #             self.player_list[self.position].append(self.deck1.pop())
    #         finally:
    #             self.message = "You didn't shout UNO! Penalty card drawn!"


    # def take_from_stack(self, num, player):
    #     """ 덱에서 카드 num 장 드로우 """
    #     if player == 0 and not self.p1_drawn:
    #         for _ in range(num):
    #             try: # 카드 덱이 비어있으면, 예외 처리
    #                 self.player_list[0].append(self.deck1.pop())
    #             except:
    #                 self.deck1, self.deck2 = self.deck2, self.deck1 # 카드 덱과 버려진 카드 덱을 바꾼다
    #                 random.shuffle(self.deck1)
    #                 self.player_list[0].append(self.deck1.pop())
    #         self.p1_drawn = True # 드로우 했나?를 True로 바꾼다
    #         self.p1_player_playing = False # 플레이어의 턴을 넘긴다
    #         self.message = "%s draws %d cards" % self.player_mapp[player], num

    #     elif player == 1 and not self.p2drawn:
    #         for _ in range(num):
    #             try: # 카드 덱이 비어있으면, 예외 처리
    #                 self.player_list[1].append(self.deck1.pop())
    #             except:
    #                 self.deck1, self.deck2 = self.deck2, self.deck1
    #                 random.shuffle(self.deck1)
    #                 self.player_list[1].append(self.deck1.pop())
    #         self.p2drawn = True
    #         self.p2_player_playing = False # 플레이어의 턴을 넘긴다
    #         self.message = "%s draws %d cards" % self.player_mapp[player], num
    #     elif player == 2 or player == 3: # AI가 드로우 하는 상황
    #         for _ in range(num):
    #             try: # 카드 덱이 비어있으면, 예외 처리
    #                 self.player_list[player].append(self.deck1.pop())
    #             except:
    #                 self.deck1, self.deck2 = self.deck2, self.deck1
    #                 random.shuffle(self.deck1)
    #                 self.player_list[player].append(self.deck1.pop())
    #         self.message = "%s draws %d cards" % self.player_mapp[player], num


    # # color = "Red" or "Blue" or "Green" or "Yellow"
    # def change_card_color(self, player, color): 
    #     """ 와일드카드 효과로 버려진 카드 덱의 마지막 카드의 색을 바꾼다 """
    #     if player == 0 and self.choose_colors[player] and self.p1_player_playing:
    #         self.deck2[-1] = (self.deck2[-1][0], color) # color에 맞는 이미지 파일(EX - Red2.png)이 로딩
    #         self.current = self.peek(self.deck2)
    #         self.special_check = 0 # 처음 냈으니까 활성화
    #         self.choose_colors[player] = False
    #         self.p1_player_playing = False # 플레이어의 턴을 넘긴다
    #     elif player == 1 and self.choose_colors[player] and self.p2_player_playing:
    #         self.deck2[-1] = (self.deck2[-1][0], color)
    #         self.current = self.peek(self.deck2)
    #         self.special_check = 0
    #         self.choose_colors[player] = False
    #         self.p2_player_playing = False # 플레이어의 턴을 넘긴다


    # def play_this_card(self, player, card): # card = "+4:Black"
    #     """ 클라이언트의 카드 제출 요청을 처리 """
    #     if player == 0 and not self.p1_played:
    #         card = tuple(card.split(":")) # card = ("+4", "Black")
            
    #         # self.current = 버려진 카드 덱의 맨 위에 있는 카드
    #         # 1) 숫자나 색깔이 같은데, 와일드 카드가 아니면
    #         if (card[0] == self.current[0] or card[1] == self.current[1]) and (card[1] != 'Black'):
    #             self.p1_played, self.p1_drawn = True, True # 플레이 했나?, 드로우 했나?를 True로 바꾼다
    #             self.p1_player_playing = False # 플레이어가 플레이 했으니까 False로 바꾼다

    #             self.deck2.append(card)
    #             self.current = self.peek(self.deck2)
    #             self.player_list[0].remove(self.current)
    #             self.special_check = 0 # 처음 냈으니까 활성화
                
    #             self.set_next_player(self)

    #         if card[1] == 'Black':
    #             self.p1_played, self.p1_drawn = True, True
    #             self.player_list[0].remove(card)
    #             self.deck2.append(card)
    #             self.choose_colors[0] = True # 모든 와일드 카드는 색깔을 선택하게 한다
    #     elif player == 1 and not self.p2_played:
    #         card = tuple(card.split(":")) # card = ("+4", "Black")
            
    #         if (card[0] == self.current[0] or card[1] == self.current[1]) and (card[1] != 'Black'):
    #             self.p2_played, self.p2_drawn = True, True
    #             self.p2_player_playing = False

    #             self.deck2.append(card)
    #             self.current = self.peek(self.deck2)
    #             self.player_list[1].remove(self.current)
    #             self.special_check = 0
                
    #             self.set_next_player(self)

    #         if card[1] == 'Black':
    #             self.p2_played, self.p2_drawn = True, True
    #             self.p2_player_playing = False
    #             self.player_list[1].remove(card)
    #             self.deck2.append(card)
    #             self.choose_colors[1] = True # 모든 와일드 카드는 색깔을 선택하게 한다

    # def set_next_player(self):
    #     """ 다음 플레이어를 결정하는 함수 """
    #     if self.current[0] == 'Reverse' and self.special_check == 0:
    #         self.direction_check *= -1  # 진행 방향 리버스
    #         self.special_check = 1  # 한 번 적용했으니까 특수 카드 비활성화
    #         if self.player_num == 2: # 두 명일때는 Skip처럼 작동
    #             self.position = (self.position + self.direction_check * 2) % 2
    #         else:
    #             self.position = (self.position + self.direction_check) % self.player_num
        
    #     elif self.current[0] == 'Skip' and self.special_check == 0:
    #         self.special_check = 1  # 한 번 적용했으니까 특수 카드 비활성화
    #         self.position = (self.position + self.direction_check * 2) % self.player_num # 플레이 하는 플레이어 인덱스

    #     elif self.current[0] == '+1' and self.special_check == 0:
    #         self.take_from_stack(self, 1, self.position + 1) # 다음 플레이어에게 카드 한 장 준다
    #         self.shouted_uno[self.position + 1] = False # 턴이 자동으로 넘어가니까 uno 플래그를 해제

    #         self.special_check = 1  # 한 번 적용했으니까 특수 카드 비활성화
    #         self.position = (self.position + self.direction_check * 2) % self.player_num

    #     elif self.current[0] == '+2' and self.special_check == 0:
    #         self.take_from_stack(self, 2, self.position + 1)
    #         self.shouted_uno[self.position + 1] = False # 턴이 자동으로 넘어가니까 uno 플래그를 해제
            
    #         self.special_check = 1
    #         self.position = (self.position + self.direction_check * 2) % self.player_num

    #     elif self.current[0] == '+4' and self.special_check == 0:
    #         self.take_from_stack(self, 4, self.position + 1)
    #         self.shouted_uno[self.position + 1] = False # 턴이 자동으로 넘어가니까 uno 플래그를 해제

    #         self.special_check = 1
    #         self.position = (self.position + self.direction_check * 2) % self.player_num

    #     else: # 일반적인 카드라면
    #         self.position = (self.position + self.direction_check) % self.player_num # direction_check대로 진행한다

    #     self.play(self) # 다음 플레이어를 결정했으면 플레이한다

    # def bot_action(self):
    #     """ AI 로직 구현 """
    #     time.sleep(1) # 1초 동안 기다린다

    #     self.message = ""
    #     self.shouted_uno[self.position] = False # 플레이하는 AI의 UNO 외침 플래그를 초기화한다
    #     self.played_check = 0 # ??

    #     if (self.played_check != 1 and len(self.player_list[self.position]) == 2):
    #         time.sleep(1) # 1초 동안 기다린다

    #         # pygame.mixer.pre_init(44100, -16, 1, 512)
    #         # wait_time = random.randint(1000, 2000)
    #         # pygame.time.delay(wait_time) # 1~2초 동안 기다린 다음, 우노를 외친다!
    #         # multi_sound.uno.play()

    #         self.shouted_uno[self.position] = True
    #         self.message = "%s shouted UNO!" % self.bot_map[self.position]

    #     check = 0
    #     for item in self.player_list[self.position]: # AI가 가지고 있는 카드 중에서 -> item = ("+4", "Red")
    #         if item[1] == 'Black':
    #             self.bot_handle_black(self, item)
    #             self.bot_play_card(self, item)
            
    #             self.player_list[self.position].remove(item)
    #             self.set_next_player(self)
    #             check = 1
    #             break

    #         elif self.current[1] == item[1] or self.current[0] == item[0]: # 색깔이나 숫자가 같은 카드가 있다면
    #             self.bot_play_card(self, item)

    #             self.player_list[self.position].remove(item)
    #             self.set_next_player(self)
    #             check = 1
    #             break

    #     if check == 0: # AI가 낼 수 있는 카드가 없다면
    #         self.take_from_stack(self, 1, self.position) # 카드를 한 장 뽑고 턴 종료
    #         self.set_next_player(self)
    
    # def bot_play_card(self, item):
    #     """ AI가 카드를 냈을 때의 처리 """
    #     self.special_check = 0 # 특수 카드 활성화
    #     self.deck2.append(item)
    #     self.current = self.peek(self.deck2)
    #     self.message = "%s plays card %s" % (self.player_mapp[self.position], self.item[1] + " " + self.item[0])


    # def bot_handle_black(self, item):
    #     """ AI가 와일드 카드를 냈을 때 행동 구현 """
    #     self.special_check = 0 # 특수 카드 활성화

    #     self.deck2.append(item)
    #     self.current = self.peek(self.deck2)

    #     d = dict()
    #     d['Blue'] = 0
    #     d['Green'] = 0
    #     d['Yellow'] = 0
    #     d['Red'] = 0
    #     d['Black'] = 0
    #     for _item in self.player_list[self.position]:
    #         d[_item[1]] += 1
    #     d = sorted(d.items(), key=lambda kv: (kv[1], kv[0]))
    #     new_color = d[-1][0] # AI가 가지고 있는 카드 중에서 가장 많은 색깔을 선택한다
    #     if new_color == 'Black':
    #         new_color = d[-2][0] # 그게 와일드 카드면, 두번째로 많은 색깔을 선택한다

    #     self.message = "%s plays %s %s, new color is %s" % (self.player_mapp[self.position], item[0], item[1], new_color)
    #     self.current = (self.current[0], new_color) # AI가 선택한 색깔로, 버려진 카드 덱에 이미지 파일(EX - Red.png)을 그린다


# ===================================================================================================================================================
def peek(s):
    """ Peek - 리스트에서 가장 마지막 원소를 리턴 """
    return s[-1]

def get_player_card_num(Multi_Uno, player):
    """ 어떤 플레이어의 카드 개수를 반환하는 함수 """
    return len(Multi_Uno.player_list[player])

# def connected(Multi_Uno):
#     """ 두 플레이어가 모두 연결되었는지 확인하는 함수 """
#     return Multi_Uno.ready

def get_deck2(Multi_Uno):
    """ 버려진 카드 덱을 반환하는 함수 """
    return Multi_Uno.deck2

def create(Multi_Uno):
    """ 카드를 생성하고, 분배 """
    for _ in range(4):
        Multi_Uno.player_list.append([]) # 플레이어 수만큼 2차원 리스트 생성 -> 플레이어들의 카드를 저장하기 위해서
    
    Multi_Uno.shouted_uno = [False] * 4 # 각 플레이어가 UNO를 외쳤는지 저장하는 플래그

    a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9',
            '+1', '+1', '+2', '+2', '+4', 'Skip', 'Skip', 'Reverse', 'Reverse') # 색깔 +1, +4 특수 카드 추가
    Multi_Uno.deck1 = list(itertools.product(a, Multi_Uno.color)) # 덱 생성 -> 총 120장
    for _ in range(4): # 덱에 와일드 카드 2종류 4장씩 추가 
        Multi_Uno.deck1.append(('Wild', 'Black'))
        Multi_Uno.deck1.append(('+4', 'Black'))
    random.shuffle(Multi_Uno.deck1) # 덱 셔플
    
    while peek(Multi_Uno.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
                            ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
                            ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
                            ('+2', 'Blue'), ('+2', 'Yellow'), ('+1', 'Red'), ('+1', 'Green'),
                            ('+1', 'Blue'), ('+1', 'Yellow'), ('+4', 'Red'), ('+4', 'Green'),
                            ('+4', 'Blue'), ('+4', 'Yellow')]: # 첫 번째 카드는 특수카드가 아니어야 한다
        random.shuffle(Multi_Uno.deck1)

    Multi_Uno.deck2.append(Multi_Uno.deck1.pop()) # 첫 번째 카드를 버려진 카드 덱(deck2)에 추가
    Multi_Uno.current = peek(Multi_Uno.deck2) # 버려진 카드 덱의 peek

    for j in range(4):  # 모든 플레이어에게 카드를 7장씩 나누어 준다
        Multi_Uno.player_card_count[j] = 7
        for _ in range(7):
            Multi_Uno.player_list[j].append(Multi_Uno.deck1.pop())

    print(Multi_Uno.current)
    Multi_Uno.position = 0 # 플레이어 위치 카운터
    Multi_Uno.play_lag = 0
    Multi_Uno.p1_drawn = False
    Multi_Uno.p1_played = False
    Multi_Uno.choose_colors[0] = False
    Multi_Uno.p1_player_playing = True

    # Object.player_list[0] = [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Reverse', 'Green'), ("+2", "Blue")]

def re_initialize(Multi_Uno):
    """ 모든 게임 변수와 플래그를 초기화 """
    Multi_Uno.player_list = []
    Multi_Uno.player_card_count = [0] * 4
    Multi_Uno.deck1 = list()
    Multi_Uno.deck2 = list()


    Multi_Uno.direction_check = 1  # 게임 플레이 방향 플래그
    Multi_Uno.position = -1  # 위치 카운터
    Multi_Uno.current = list()

    Multi_Uno.p1_drawn, Multi_Uno.p1_played = False, False
    Multi_Uno.p2_drawn, Multi_Uno.p2_played = False, False
    Multi_Uno.p1_player_playing, Multi_Uno.p2_player_playing = False, False
    Multi_Uno.choose_colors = [False, False] # 색깔 선택 플래그

    Multi_Uno.winner = -1
    Multi_Uno.play_lag = -1
    Multi_Uno.is_game_paused = False

    Multi_Uno.played_check = 0  # Play checker
    Multi_Uno.special_check = 0  # 특수 카드 상태 활성화, 1은 비활성화
    Multi_Uno.shouted_uno = [False] * 4
    Multi_Uno.message = "" # 메세지를 출력하기 위해서


def shout_uno(Multi_Uno, player):
    """ UNO를 외치는 함수 """
    Multi_Uno.shouted_uno[player] = True


def play(Multi_Uno):
    """ 게임을 진행하는 로직 """
    print("Play: ", end="")
    print(Multi_Uno)
    
    if Multi_Uno.position == 0:
        check_uno_penalty(Multi_Uno)

        Multi_Uno.play_lag = 0
        Multi_Uno.p1_drawn = False
        Multi_Uno.p1_played = False
        Multi_Uno.choose_colors[0] = False
        Multi_Uno.p1_player_playing = True
    
    elif Multi_Uno.position == 1:
        check_uno_penalty(Multi_Uno)

        Multi_Uno.play_lag = 0
        Multi_Uno.p2drawn = False
        Multi_Uno.p2_played = False
        Multi_Uno.choose_colors[1] = False
        Multi_Uno.p2_player_playing = True
    
    else: # AI가 플레이하는 상황
        bot_action(Multi_Uno)


def check_winner(Multi_Uno):
    """ 플레이어 중에 게임 승리조건을 만족했는지 확인하는 함수 """
    try:
        for i in range(4):
            if len(Multi_Uno.player_list[i]) == 0:
                Multi_Uno.winner = i
                Multi_Uno.message = Multi_Uno.player_mapp[i] + " wins the game! Congratulations!"
                return True
    except:
        return False


def check_uno_penalty(Multi_Uno):
    """ UNO 패널티를 확인하는 함수 """
    if len(Multi_Uno.player_list[Multi_Uno.position]) == 1 and not Multi_Uno.shouted_uno[Multi_Uno.position]:
        try: 
            Multi_Uno.player_list[Multi_Uno.position].append(Multi_Uno.deck1.pop()) # 페널티로 덱에서 카드 한장을 뽑는다.
        except:
            Multi_Uno.deck1, Multi_Uno.deck2 = Multi_Uno.deck2, Multi_Uno.deck1
            random.shuffle(Multi_Uno.deck1)
            Multi_Uno.player_list[Multi_Uno.position].append(Multi_Uno.deck1.pop())
        finally:
            Multi_Uno.message = "You didn't shout UNO! Penalty card drawn!"


def take_from_stack(Multi_Uno, num, player):
    """ 덱에서 카드 num 장 드로우 """
    print("take_from_stack: ", end="")
    print(Multi_Uno)

    if player == 0 and not Multi_Uno.p1_drawn:
        for _ in range(num):
            try: # 카드 덱이 비어있으면, 예외 처리
                Multi_Uno.player_list[0].append(Multi_Uno.deck1.pop())
            except:
                Multi_Uno.deck1, Multi_Uno.deck2 = Multi_Uno.deck2, Multi_Uno.deck1 # 카드 덱과 버려진 카드 덱을 바꾼다
                random.shuffle(Multi_Uno.deck1)
                Multi_Uno.player_list[0].append(Multi_Uno.deck1.pop())
        Multi_Uno.p1_drawn = True # 드로우 했나?를 True로 바꾼다
        Multi_Uno.p1_player_playing = False # 플레이어의 턴을 넘긴다
        Multi_Uno.message = "%s draws %d cards" % Multi_Uno.player_mapp[player], num

    elif player == 1 and not Multi_Uno.p2drawn:
        for _ in range(num):
            try: # 카드 덱이 비어있으면, 예외 처리
                Multi_Uno.player_list[1].append(Multi_Uno.deck1.pop())
            except:
                Multi_Uno.deck1, Multi_Uno.deck2 = Multi_Uno.deck2, Multi_Uno.deck1
                random.shuffle(Multi_Uno.deck1)
                Multi_Uno.player_list[1].append(Multi_Uno.deck1.pop())
        Multi_Uno.p2drawn = True
        Multi_Uno.p2_player_playing = False # 플레이어의 턴을 넘긴다
        Multi_Uno.message = "%s draws %d cards" % Multi_Uno.player_mapp[player], num

    elif player == 2 or player == 3: # AI가 드로우 하는 상황
        for _ in range(num):
            try: # 카드 덱이 비어있으면, 예외 처리
                Multi_Uno.player_list[player].append(Multi_Uno.deck1.pop())
            except:
                Multi_Uno.deck1, Multi_Uno.deck2 = Multi_Uno.deck2, Multi_Uno.deck1
                random.shuffle(Multi_Uno.deck1)
                Multi_Uno.player_list[player].append(Multi_Uno.deck1.pop())
        Multi_Uno.message = "%s draws %d cards" % Multi_Uno.player_mapp[player], num


# color = "Red" or "Blue" or "Green" or "Yellow"
def change_card_color(Multi_Uno, player, color): 
    """ 와일드카드 효과로 버려진 카드 덱의 마지막 카드의 색을 바꾼다 """
    if player == 0 and Multi_Uno.choose_colors[player] and Multi_Uno.p1_player_playing:
        Multi_Uno.deck2[-1] = (Multi_Uno.deck2[-1][0], color) # color에 맞는 이미지 파일(EX - Red2.png)이 로딩
        Multi_Uno.current = peek(Multi_Uno.deck2)
        Multi_Uno.special_check = 0 # 처음 냈으니까 활성화
        Multi_Uno.choose_colors[player] = False
        Multi_Uno.p1_player_playing = False # 플레이어의 턴을 넘긴다
    elif player == 1 and Multi_Uno.choose_colors[player] and Multi_Uno.p2_player_playing:
        Multi_Uno.deck2[-1] = (Multi_Uno.deck2[-1][0], color)
        Multi_Uno.current = peek(Multi_Uno.deck2)
        Multi_Uno.special_check = 0
        Multi_Uno.choose_colors[player] = False
        Multi_Uno.p2_player_playing = False # 플레이어의 턴을 넘긴다


def play_this_card(Multi_Uno, player, card): # card = "+4:Black"
    """ 클라이언트의 카드 제출 요청을 처리 """
    if player == 0 and not Multi_Uno.p1_played:
        card = tuple(card.split(":")) # card = ("+4", "Black")
        
        # Multi_Uno.current = 버려진 카드 덱의 맨 위에 있는 카드
        # 1) 숫자나 색깔이 같은데, 와일드 카드가 아니면
        if (card[0] == Multi_Uno.current[0] or card[1] == Multi_Uno.current[1]) and (card[1] != 'Black'):
            Multi_Uno.p1_played, Multi_Uno.p1_drawn = True, True # 플레이 했나?, 드로우 했나?를 True로 바꾼다
            # Multi_Uno.p1_player_playing = False # 플레이어가 플레이 했으니까 False로 바꾼다

            Multi_Uno.deck2.append(card)
            Multi_Uno.current = peek(Multi_Uno.deck2)
            Multi_Uno.player_list[0].remove(Multi_Uno.current)
            Multi_Uno.special_check = 0 # 처음 냈으니까 활성화
            
            # set_next_player(Multi_Uno)

        if card[1] == 'Black':
            Multi_Uno.p1_played, Multi_Uno.p1_drawn = True, True
            Multi_Uno.player_list[0].remove(card)
            Multi_Uno.deck2.append(card)
            Multi_Uno.choose_colors[0] = True # 모든 와일드 카드는 색깔을 선택하게 한다
    
    elif player == 1 and not Multi_Uno.p2_played:
        card = tuple(card.split(":")) # card = ("+4", "Black")
        
        if (card[0] == Multi_Uno.current[0] or card[1] == Multi_Uno.current[1]) and (card[1] != 'Black'):
            Multi_Uno.p2_played, Multi_Uno.p2_drawn = True, True
            # Multi_Uno.p2_player_playing = False

            Multi_Uno.deck2.append(card)
            Multi_Uno.current = peek(Multi_Uno.deck2)
            Multi_Uno.player_list[1].remove(Multi_Uno.current)
            Multi_Uno.special_check = 0
            
            # set_next_player(Multi_Uno)

        if card[1] == 'Black':
            Multi_Uno.p2_played, Multi_Uno.p2_drawn = True, True
            Multi_Uno.player_list[1].remove(card)
            Multi_Uno.deck2.append(card)
            Multi_Uno.choose_colors[1] = True # 모든 와일드 카드는 색깔을 선택하게 한다

def set_next_player(Multi_Uno):
    """ 다음 플레이어를 결정하는 함수 """
    print("set_next_player: ", end="")
    print(Multi_Uno)
    
    
    if Multi_Uno.current[0] == 'Reverse' and Multi_Uno.special_check == 0:
        Multi_Uno.direction_check *= -1  # 진행 방향 리버스
        Multi_Uno.special_check = 1  # 한 번 적용했으니까 특수 카드 비활성화
        if Multi_Uno.player_num == 2: # 두 명일때는 Skip처럼 작동
            Multi_Uno.position = (Multi_Uno.position + Multi_Uno.direction_check * 2) % 2
        else:
            Multi_Uno.position = (Multi_Uno.position + Multi_Uno.direction_check) % Multi_Uno.player_num
    
    elif Multi_Uno.current[0] == 'Skip' and Multi_Uno.special_check == 0:
        Multi_Uno.special_check = 1  # 한 번 적용했으니까 특수 카드 비활성화
        Multi_Uno.position = (Multi_Uno.position + Multi_Uno.direction_check * 2) % Multi_Uno.player_num # 플레이 하는 플레이어 인덱스

    elif Multi_Uno.current[0] == '+1' and Multi_Uno.special_check == 0:
        take_from_stack(Multi_Uno, 1, Multi_Uno.position + 1) # 다음 플레이어에게 카드 한 장 준다
        Multi_Uno.shouted_uno[Multi_Uno.position + 1] = False # 턴이 자동으로 넘어가니까 uno 플래그를 해제

        Multi_Uno.special_check = 1  # 한 번 적용했으니까 특수 카드 비활성화
        Multi_Uno.position = (Multi_Uno.position + Multi_Uno.direction_check * 2) % Multi_Uno.player_num

    elif Multi_Uno.current[0] == '+2' and Multi_Uno.special_check == 0:
        take_from_stack(Multi_Uno, 2, Multi_Uno.position + 1)
        Multi_Uno.shouted_uno[Multi_Uno.position + 1] = False # 턴이 자동으로 넘어가니까 uno 플래그를 해제
        
        Multi_Uno.special_check = 1
        Multi_Uno.position = (Multi_Uno.position + Multi_Uno.direction_check * 2) % Multi_Uno.player_num

    elif Multi_Uno.current[0] == '+4' and Multi_Uno.special_check == 0:
        take_from_stack(Multi_Uno, 4, Multi_Uno.position + 1)
        Multi_Uno.shouted_uno[Multi_Uno.position + 1] = False # 턴이 자동으로 넘어가니까 uno 플래그를 해제

        Multi_Uno.special_check = 1
        Multi_Uno.position = (Multi_Uno.position + Multi_Uno.direction_check * 2) % Multi_Uno.player_num

    else: # 일반적인 카드라면
        Multi_Uno.position = (Multi_Uno.position + Multi_Uno.direction_check) % Multi_Uno.player_num # direction_check대로 진행한다

    play(Multi_Uno) # 다음 플레이어를 결정했으면 플레이한다

def bot_action(Multi_Uno):
    """ AI 로직 구현 """
    time.sleep(1) # 1초 동안 기다린다

    Multi_Uno.message = ""
    Multi_Uno.shouted_uno[Multi_Uno.position] = False # 플레이하는 AI의 UNO 외침 플래그를 초기화한다
    Multi_Uno.played_check = 0 # ??

    if (Multi_Uno.played_check != 1 and len(Multi_Uno.player_list[Multi_Uno.position]) == 2):
        time.sleep(1) # 1초 동안 기다린다

        # pygame.mixer.pre_init(44100, -16, 1, 512)
        # wait_time = random.randint(1000, 2000)
        # pygame.time.delay(wait_time) # 1~2초 동안 기다린 다음, 우노를 외친다!
        # multi_sound.uno.play()

        Multi_Uno.shouted_uno[Multi_Uno.position] = True
        Multi_Uno.message = "%s shouted UNO!" % Multi_Uno.bot_map[Multi_Uno.position]

    check = 0
    for item in Multi_Uno.player_list[Multi_Uno.position]: # AI가 가지고 있는 카드 중에서 -> item = ("+4", "Red")
        if item[1] == 'Black':
            bot_handle_black(Multi_Uno, item)
            bot_play_card(Multi_Uno, item)
        
            Multi_Uno.player_list[Multi_Uno.position].remove(item)
            set_next_player(Multi_Uno)
            check = 1
            break

        elif Multi_Uno.current[1] == item[1] or Multi_Uno.current[0] == item[0]: # 색깔이나 숫자가 같은 카드가 있다면
            bot_play_card(Multi_Uno, item)

            Multi_Uno.player_list[Multi_Uno.position].remove(item)
            set_next_player(Multi_Uno)
            check = 1
            break

    if check == 0: # AI가 낼 수 있는 카드가 없다면
        take_from_stack(Multi_Uno, 1, Multi_Uno.position) # 카드를 한 장 뽑고 턴 종료
        set_next_player(Multi_Uno)

def bot_play_card(Multi_Uno, item):
    """ AI가 카드를 냈을 때의 처리 """
    Multi_Uno.special_check = 0 # 특수 카드 활성화
    Multi_Uno.deck2.append(item)
    Multi_Uno.current = peek(Multi_Uno.deck2)
    Multi_Uno.message = "%s plays card %s" % (Multi_Uno.player_mapp[Multi_Uno.position], Multi_Uno.item[1] + " " + Multi_Uno.item[0])


def bot_handle_black(Multi_Uno, item):
    """ AI가 와일드 카드를 냈을 때 행동 구현 """
    Multi_Uno.special_check = 0 # 특수 카드 활성화

    Multi_Uno.deck2.append(item)
    Multi_Uno.current = peek(Multi_Uno.deck2)

    d = dict()
    d['Blue'] = 0
    d['Green'] = 0
    d['Yellow'] = 0
    d['Red'] = 0
    d['Black'] = 0
    for _item in Multi_Uno.player_list[Multi_Uno.position]:
        d[_item[1]] += 1
    d = sorted(d.items(), key=lambda kv: (kv[1], kv[0]))
    new_color = d[-1][0] # AI가 가지고 있는 카드 중에서 가장 많은 색깔을 선택한다
    if new_color == 'Black':
        new_color = d[-2][0] # 그게 와일드 카드면, 두번째로 많은 색깔을 선택한다

    Multi_Uno.message = "%s plays %s %s, new color is %s" % (Multi_Uno.player_mapp[Multi_Uno.position], item[0], item[1], new_color)
    Multi_Uno.current = (Multi_Uno.current[0], new_color) # AI가 선택한 색깔로, 버려진 카드 덱에 이미지 파일(EX - Red.png)을 그린다
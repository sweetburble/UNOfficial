import sys
import random
import pygame
from pygame.locals import *
import loadcard
import popup
import AI

class game():
    def __init__(self, playernum, difficulty):
        self.playernum = playernum
        self.difficulty = difficulty
        self.background = pygame.image.load('./img/default.png')
        self.screen = pygame.display.set_mode((800, 700))
        self.screen.blit(self.background, (-100, -70))
        self.color = {1:'RED', 2:'YELLOW', 3:'GREEN', 4:'BLUE', 5:'BLACK'}
        self.skill = {11:'_SKILL_0', 12:'_SKILL_1', 13:'_SKILL_2', 14:'_SKILL_3', 15:'_SKILL_4'}
        self.card_deck = []
        self.player = [[0] for i in range (0, self.playernum)]
        self.waste_group = pygame.sprite.RenderPlain()
        self.rotate = 0
        self.uno = 0
        pygame.display.update()

    def text_format(self, message, textFont, textSize, textColor):
        newFont = pygame.font.SysFont(textFont, textSize)
        newText = newFont.render(message, K_0, textColor)
        return newText

    # set_window()가 3번째로 호출
    def set_deck(self): # 덱은 총 108장의 카드로 이루어진다.
        for color_idx in range(1,5):
            card = self.color[color_idx]
            now_card = card + '_0'
            self.card_deck.append(now_card) # 숫자 0 카드는 한장만 들어간다. 총 4장
            for card_number in range(1, 10): # 숫자 1~9까지는 카드가 2장씩 들어간다. 총 72장
                now_card = card + "_" + str(card_number)
                iterate = 0
                while iterate != 2:
                    self.card_deck.append(now_card)
                    iterate += 1
            for card_number in range(11, 14): # 빨강, 노랑, 초록, 파랑 4가지 기본 카드는 스킬 카드가 3종류 2장씩이다. 순서 리버스, 다음 차례 건너뛰기, 다음 차례 카드 2장 추가
                now_card = card + self.skill[card_number]
                iterate = 0
                while iterate != 2:
                    self.card_deck.append(now_card)
                    iterate += 1
        card = 'BLACK' # 블랙은 무색 카드이다. 숫자 카드는 없고 기술카드만 2종류 4장씩 있다. 4장 추가, 원하는 색으로 바꾸기
        for card_number in range(14, 16):
            now_card = card + self.skill[card_number]
            iterate = 0
            while iterate != 4:
                self.card_deck.append(now_card)
                iterate += 1
        random.shuffle(self.card_deck) # random 모듈이 리스트의 원소(덱의 모든 카드들)를 섞어준다.
    
    # startgame()이 2번째로 호출
    def set_window(self):
        self.set_deck()
        for player in range(0, self.playernum):
            card = []
            for number in range(0, 7): # 한 플레이당 카드를 7장씩 주는 것이다.
                temp = self.card_deck.pop(number) # 리스트의 마지막 원소(카드)를 리턴하고, 삭제한다.
                card.append(temp)
            self.player[player] = card # self.player[?]에게 7장의 카드가 담긴 리스트를 할당한다.
        deck = loadcard.Card('BACK', (350, 300)) # 게임 화면 가운데에 덱을 그렸다.
        self.deck_group = pygame.sprite.RenderPlain(deck)

        player_deck = self.player[0] # 유저 플레이어는 무조건 있다.
        init_card = []
        for item in player_deck:
            cards = loadcard.Card(item, (400, 300)) # 플레이어가 처음 발급받은 카드를 하나씩 Card 객체로 생성하고, init_card 리스트에 넣었다.
            init_card.append(cards)

        for i in range(0, len(self.player)):
            player_deck = self.player[i]
            if i == 0:
                user_card = []
                for item in player_deck:
                    cards = loadcard.Card(item, (400, 300))
                    user_card.append(cards)
            elif i == 1:
                self.com1_card = [] # computer 1의 카드
                for item in player_deck:
                    cards = loadcard.Card('BACK', (400, 300)) # Card 객체를 생성하지만, 이미지는 안보여야 하니까 뒤집힌 카드로 한다.
                    cards.rotation(180) # 반대편에 있어야 하니까 180도 회전
                    self.com1_card.append(cards)
            elif i == 2:
                self.com2_card = []
                for item in player_deck:
                    cards = loadcard.Card('BACK', (400, 300))
                    cards.rotation(270) # 왼쪽에 있어야 하니까 시계 방향으로 90도 회전
                    self.com2_card.append(cards)
            else:
                self.com3_card = []
                for item in player_deck:
                    cards = loadcard.Card('BACK', (400, 300))
                    cards.rotation(90) # 오른쪽에 있어야 하니까 시계 방향으로 270도 회전
                    self.com3_card.append(cards)
        setting = True
        settinguser = 1; settingcom1 = 1; settingcom3 = 1; settingcom2 = 1
        if self.playernum == 3:
            settingcom3 = 0
        if self.playernum == 2:
            settingcom3 = 0
            settingcom2 = 0

        while setting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            i = 0
            temp_list = []
            
            for item in user_card: # 내 카드들
                item.update((200 + 70*i, 500)) # 카드들을 간격에 맞게 배치한다.
                temp_list.append(item)
                i += 1
            # 스프라이트 그룹 = 전체 스프라이트 객체를 갖는다
            self.user_group = pygame.sprite.RenderPlain(*temp_list) # 나중에 한번에 카드들을 draw()로 스크린에 스프라이트로 그리기 위해서 RenderPlain 그룹을 이미지, 위치등이 담긴 스프라이트 객체 리스트를 넣어서 생성한다.

            self.lastcard0 = temp_list[-1].getposition() # 마지막 카드의 위치를 얻어서, 카드가 증가하면 그 다음에 배치하도록 한다.
            if self.lastcard0 == (200 + 70*(len(temp_list)-1), 500):
                settinguser = 0

            i = 0
            temp_list = []
            setting = True
            for item in self.com1_card:
                item.update((270 + 40*i, 100))
                temp_list.append(item)
                i += 1
            self.com1_group = pygame.sprite.RenderPlain(*temp_list)
            self.lastcard1 = temp_list[-1].getposition()
            if self.lastcard1 == (270 + 40*(len(temp_list)-1), 100):
                settingcom1 = 0


            if self.playernum >= 3:
                i = 0
                temp_list = []
                setting = True
                for item in self.com2_card:
                    item.update((80, 170+40*i))
                    temp_list.append(item)
                    i += 1
                self.com2_group = pygame.sprite.RenderPlain(*temp_list)
                self.lastcard2 = temp_list[-1].getposition()
                if self.lastcard2 == (80, 170 + 40*(len(temp_list)-1)): # 3번째 컴퓨터는 왼쪽에 위치하니까 종렬로 깔아두었다.
                    settingcom2 = 0

            if self.playernum == 4:
                i = 0
                temp_list = []
                setting = True
                for item in self.com3_card:
                    item.update((710, 170 + 40*i))
                    temp_list.append(item)
                    i +=1
                self.com3_group = pygame.sprite.RenderPlain(*temp_list)
                self.lastcard3 = temp_list[-1].getposition()
                if self.lastcard3 == (710, 170 + 40*(len(temp_list)-1)):
                    settingcom3 = 0
            
            
            if settinguser == 0 and settingcom1 == 0 and settingcom2 == 0 and settingcom3 == 0:
                setting = False

            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            card = pygame.mixer.Sound('./sound/card.wav')
            for i in range(0,7):
                card.play()
            self.printwindow()
            pygame.display.update()

    # playgame()이 15번째로 호출했다
    def next_turn(self, now_turn):
        # 즉, 노란색으로 표시했던 이름을, 턴이 끝났으니 다시 검은색으로 복원시킨다.
        if now_turn == 0:
            user_text = self.text_format("ME", 'Berlin Sans FB', 30, (0,0,0))
            self.screen.blit(user_text, (165, 420))
        elif now_turn == 1:
            com1_text = self.text_format("COM1", 'Berlin Sans FB', 30, (0,0,0))
            self.screen.blit(com1_text, (235, 18))
        elif now_turn == 2:
            com2_text = self.text_format("COM2", 'Berlin Sans FB', 30, (0,0,0))
            self.screen.blit(com2_text, (45, 100))
        elif now_turn == 3:
            com3_text = self.text_format("COM3", 'Berlin Sans FB', 30, (0,0,0))
            self.screen.blit(com3_text, (675, 100))
        
        temp = self.get_next_player(now_turn)
        return temp
    
    # playgame()이 중급 AI를 위해 9번째로 호출
    def get_next_player(self, now_turn):
        # self.rotate는 초기에 0으로 초기화 되어있다.
        # rotate = 0은 나 -> com1 -> com2 -> com3 순이고,
        # rotate = 1은 리버스 카드등으로 인해 순서가 반대이다.
        if self.rotate == 0 and now_turn + 1 == self.playernum: 
            return 0 
        elif self.rotate == 1 and now_turn - 1 < 0: 
            return self.playernum - 1
        else: 
            if self.rotate == 0: 
                return now_turn + 1
            elif self.rotate == 1: 
                return now_turn - 1
        return 0

    # playgame()이 7번째로 호출하는 함수
    def select_player(self, now_turn): # now_turn의 처음 기본값은 0이다.
        # 누군가의 차례가 되면 그 이름이 노란색으로 바뀐다.
        if now_turn == 0:
            user_text = self.text_format("ME", 'Berlin Sans FB', 30, (255,242,0))
            self.screen.blit(user_text, (165, 420))
        elif now_turn == 1:
            com1_text = self.text_format("COM1", 'Berlin Sans FB', 30, (255,242,0))
            self.screen.blit(com1_text, (235, 18))
        elif now_turn == 2:
            com2_text = self.text_format("COM2", 'Berlin Sans FB', 30, (255,242,0))
            self.screen.blit(com2_text, (45, 100))
        else:
            com3_text = self.text_format("COM3", 'Berlin Sans FB', 30, (255,242,0))
            self.screen.blit(com3_text, (675, 100))
        pygame.display.update()
    
    # set_window()가 5번째로 호출
    def printwindow(self):
        self.screen.blit(self.background, (-100, -70))
        # 아까 set_window()에서 만든 스프라이트 그룹들을 draw()로 한번에 스크린에 그린다.
        self.deck_group.draw(self.screen)
        self.user_group.draw(self.screen)   
        self.com1_group.draw(self.screen)
        if self.playernum >= 3:
            self.com2_group.draw(self.screen)
            com2_text = self.text_format("COM2", 'Berlin Sans FB', 30, (0,0,0))
            self.screen.blit(com2_text, (45, 100))
        if self.playernum == 4:
            self.com3_group.draw(self.screen)
            com3_text = self.text_format("COM3", 'Berlin Sans FB', 30, (0,0,0))
            self.screen.blit(com3_text, (675, 100))

        user_text = self.text_format("ME", 'Berlin Sans FB', 30, (0,0,0))
        self.screen.blit(user_text, (165, 420))
        com1_text = self.text_format("COM1", 'Berlin Sans FB', 30, (0,0,0))
        self.screen.blit(com1_text, (235, 18))

        self.waste_group.draw(self.screen)

    # playgame()이 22번째로 호출
    def check_card(self, sprite): # sprite in self.user_group
        if len(self.waste_card) == 0: # 가장 처음은 플레이어가 카드를 낼 수 있다.
            return True
        else:
            name = sprite.get_name()
            name = name.split('_') # ["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
            w_name = self.waste_card[-1]
            w_name = w_name.split('_') # 게임판에 마지막으로 낸 카드
            if w_name[0] == 'BLACK' : return True
            if name[0] == 'BLACK' : return True
            if len(name) < 3 or len(w_name) < 3: # 어느 한쪽이 숫자 카드인데
                if w_name[0] == name[0]: return True # 색이 같거나
                if len(name) > 1 and len(w_name) > 1: 
                    if w_name[1] == name[1]: return True # 숫자나 스킬이 같으면 가능               
            else: # 둘 다 스킬 카드이면, 색이나 스킬 종류가 같아야 한다
                if w_name[0] == name[0]: return True
                if w_name[2] == name[2] : return True

        return False

    # playgame()이 17번째로 호출
    def card_skill(self, sprite): # sprite = t_card = loadcard.Card(temp, (430, 300))
        name = sprite.get_name()
        name = name.split('_')
        if name[1] == 'SKILL': # SKILL_0, 1, 2는 색깔 카드, SKILL_3, 4는 와일드 카드
            if name[2] == '0': # 다음 차례 스킵 스킬 카드
                pygame.time.wait(500)
                self.now_turn = self.next_turn(self.now_turn)
            elif name[2] == '1':
                if self.playernum == 2: # 리버스는 2명이면 어차피 똑같다
                    pygame.time.wait(500)
                    self.now_turn = self.next_turn(self.now_turn)
                else:
                    if self.rotate == 0: 
                        self.rotate = 1
                    else: 
                        self.rotate = 0
            elif name[2] == '2': # 두 장 추가 색깔 카드
                pygame.time.wait(500)
                self.give_card(2)
                self.now_turn = self.next_turn(self.now_turn)
            
            elif name[2] == '3': # 카드 색깔 바꾸기
                pygame.mixer.pre_init(44100, -16, 1, 512)
                pygame.init()
                select = pygame.mixer.Sound('./sound/select.wav')
                select.play()
                if self.now_turn == 0:
                    self.pick_color()
                elif self.now_turn == 1:
                    pygame.time.wait(500)
                    self.most_num_color(self.player[1])
                elif self.now_turn == 2:
                    pygame.time.wait(500)
                    self.most_num_color(self.player[2])
                elif self.now_turn == 3:
                    pygame.time.wait(500)
                    self.most_num_color(self.player[3])
            elif name[2] == '4': # 4장 추가 와일드 카드
                pygame.mixer.pre_init(44100, -16, 1, 512)
                pygame.init()
                select = pygame.mixer.Sound('./sound/select.wav')
                select.play()
                self.give_card(4)
                if self.now_turn == 0:
                    self.pick_color()
                elif self.now_turn == 1:
                    pygame.time.wait(500)
                    self.most_num_color(self.player[1])
                elif self.now_turn == 2:
                    pygame.time.wait(500)
                    self.most_num_color(self.player[2])
                elif self.now_turn == 3:
                    pygame.time.wait(500)
                    self.most_num_color(self.player[3])
        return True

    # card_skill()이 21번째로 호출, 
    # 즉 AI가 가지고 있는 카드 중에 가장 많은 색깔을 찾아서 그 색으로 선택한다
    def most_num_color(self, card_deck):
        r = 0; y = 0; g = 0; b = 0
        for item in card_deck:
            card = item.split('_')
            if card[0] == 'RED': r += 1
            if card[0] == 'YELLOW': y += 1
            if card[0] == 'GREEN': g += 1
            if card[0] == 'BLUE': b += 1
        a = [r, y, g, b]
        index = a.index(max(a))
        if index == 0 : temp_name = 'RED'
        if index == 1 : temp_name = 'YELLOW'
        if index == 2 : temp_name = 'GREEN'
        if index == 3 : temp_name = 'BLUE'
        temp = loadcard.Card(temp_name, (430, 300))
        self.waste_card.append(temp_name)
        self.waste_group.add(temp)
        self.printwindow()

    # card_skill()이 19번째로 호출
    def pick_color(self):
        color_popup = popup.Popup('pickcolor', (400, 300))
        popup_group = pygame.sprite.RenderPlain(color_popup)
        red = popup.Popup('RED', (306, 320))
        yellow = popup.Popup('YELLOW', (368, 320))
        green = popup.Popup('GREEN', (432, 320))
        blue = popup.Popup('BLUE', (494, 320))
        colors = [red, yellow, green, blue]
        color_group = pygame.sprite.RenderPlain(*colors) 
        # 컬러를 선택하는 팝업을 스프라이트 그룹으로 만들어서 한번에 그렸다.

        loop = True
        while loop:
            popup_group.draw(self.screen)
            color_group.draw(self.screen)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in color_group:
                        if sprite.get_rect().collidepoint(mouse_pos):
                            temp_name = sprite.get_name()
                            temp = loadcard.Card(temp_name, (430, 300))
                            self.waste_card.append(temp_name)
                            self.waste_group.add(temp)
                            self.printwindow() # 그냥 색깔 카드만 추가해서 낸다.
                            loop = False
        return 0

    # card_skill()이 18번째로 호출, 다음 차례인 플레이어를 불러와서 카드를 준다
    def give_card(self, card_num):
        dest_player = self.get_next_player(self.now_turn)
        for i in range(0, card_num):
            self.get_from_deck(dest_player)

    # 게임이 누군가의 승리로 끝나면 작동되는 함수, 게임을 다시 시작하기 위한 준비를 한다.
    def restart(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        win = pygame.mixer.Sound('./sound/win.wav')
        lose = pygame.mixer.Sound('./sound/lose.wav')
        pygame.draw.rect(self.screen, (255, 51, 0), pygame.Rect(200, 200, 400, 200))
        pygame.draw.rect(self.screen, (255, 180, 0), pygame.Rect(210, 210, 380, 180))

        if len(self.user_group) == 0: # 내가 이겼으면
            win.play()
            close_text = self.text_format("YOU WIN!", 'Berlin Sans FB', 80, (255,51,0))
            press_text = self.text_format("Press SPACE to REPLAY", 'Berlin Sans FB', 35, (255,51,0))
            self.screen.blit(close_text, (230, 220))
        else: # 컴퓨터가 이겼으면
            lose.play()
            close_text = self.text_format("YOU LOSE!", 'Berlin Sans FB', 80, (255,51,0))
            press_text = self.text_format("Press SPACE to REPLAY", 'Berlin Sans FB', 35, (255,51,0))
            self.screen.blit(close_text, (212, 220))
        
        self.screen.blit(press_text, (228, 330))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE: # SPACE BAR를 누르면 다시 시작한다.
                        self.startgame()
                        return
        return 0

    # UNO.py에서 1번째로 호출
    def startgame(self):
        self.card_deck.clear()
        self.player = [[0] for i in range (0, self.playernum)]
        self.waste_group = pygame.sprite.RenderPlain()
        self.rotate = 0
        self.set_window()
        self.playgame()

    # startgame()이 6번째로 호출
    def playgame(self):
        self.now_turn = 0
        self.waste_card = [] # 남은 카드 리스트
        while True:
            if len(self.user_group) == 0: # 내 카드가 0장이면 == 내가 이겼으면 다시 시작한다.
                self.restart()
                return
            elif self.playernum == 4:
                if len(self.player[1]) == 0 or len(self.player[2]) == 0 or len(self.player[2]) == 0:
                    self.restart()
                    return
            elif self.playernum == 3:
                if len(self.player[1]) == 0 or len(self.player[2]) == 0:
                    self.restart()
                    return
            elif self.playernum == 2:
                if len(self.player[1]) == 0:
                    self.restart()
                    return
            # 만약 카드 덱이 다 떨어졌으면, 다시 덱을 추가한다.
            if len(self.card_deck) == 0:
                self.set_deck()

            self.select_player(self.now_turn) # now_turn = 0부터 시작한다.
            
            # 1번 컴퓨터의 턴이면
            if self.now_turn == 1:
                self.select_player(self.now_turn)
                pygame.time.wait(700) # 0.7초 기다린다. 

                # self.player[1]에는 1번 컴퓨터가 현재 가진 카드들의의 리스트가 들어있다.
                ai = AI.AI(2, self.player[1], self.waste_card) # 1번 컴퓨터의 AI 객체를 생성한다.

                # 선택한 난이도에 따라 다른 행동을 취하는 함수를 부른다.
                if self.difficulty == 1:
                    temp = ai.basicplay()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0 : next_ = self.user_group # 다음 차례가 플레이어 차례이면
                    else : next_ = self.player[next] # 컴퓨터 차례이면
                    temp = ai.advancedplay(next_)
                
                if temp == 0 or temp == None: # AI가 낼 카드를 못 찾았으면
                    self.get_from_deck(1) # 덱에서 카드를 한 장 가져온다.
                    self.printwindow()
                    self.now_turn = self.next_turn(self.now_turn) # 다음 턴을 받아온다
                    pygame.display.update()
                else: # AI가 낼 카드가 있으면
                    pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com1_group:
                        if sprite.getposition() == self.lastcard1: # 위치가 같은 카드를 remove
                            self.com1_group.remove(sprite)
                    self.player[1].remove(temp) # AI가 가진 카드 리스트에서도 전부 remove
                    self.set_lastcard(self.lastcard1, (0,0))
                    card.play()
                    
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (430, 300))
                    self.waste_group.add(t_card) # 게임판에 낸 카드에 추가하고 표시한다
                    self.printwindow()
                    pygame.display.update()

                    self.card_skill(t_card) # 낸 카드가 스킬 카드면 스킬을 적용한다.
                    self.printwindow()

                    self.now_turn = self.next_turn(self.now_turn) 
                    pygame.display.update()
                
            elif self.now_turn == 2:
                self.select_player(self.now_turn)
                pygame.time.wait(700)
                ai = AI.AI(3, self.player[2], self.waste_card)
                if self.difficulty == 1:
                    temp = ai.basicplay()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0 : next_ = self.user_group
                    else : next_ = self.player[next]
                    temp = ai.advancedplay(next_)
                if temp == 0 or temp == None:
                    self.get_from_deck(2)
                    self.printwindow()
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()
                else:
                    pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com2_group:
                        if sprite.getposition() == self.lastcard2:
                            self.com2_group.remove(sprite)
                    self.player[2].remove(temp)
                    self.set_lastcard(self.lastcard2, (0,0))
                    card.play()
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (430, 300))
                    self.waste_group.add(t_card)
                    self.printwindow()
                    pygame.display.update()
                    self.card_skill(t_card)
                    self.printwindow()
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()
            
            elif self.now_turn == 3:
                self.select_player(self.now_turn)
                pygame.time.wait(700)
                ai = AI.AI(4, self.player[3], self.waste_card)
                if self.difficulty == 1:
                    temp = ai.basicplay()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0 : next_ = self.user_group
                    else : next_ = self.player[next]
                    temp = ai.advancedplay(next_)
                if temp == 0 or temp == None:
                    self.get_from_deck(3)
                    self.printwindow()
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()
                else:
                    pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com3_group:
                        if sprite.getposition() == self.lastcard3:
                            self.com3_group.remove(sprite)
                    self.player[3].remove(temp)
                    self.set_lastcard(self.lastcard3, (0,0))
                    card.play()
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (430, 300))
                    self.waste_group.add(t_card)
                    self.printwindow()
                    pygame.display.update()
                    self.card_skill(t_card)
                    self.printwindow()
                    
                    print("computer lastcard", self.lastcard3)
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()

            for event in pygame.event.get(): # 플레이어 턴이면 작동하는 이벤트 핸들러
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return

                if event.type == MOUSEBUTTONUP:
                    if self.now_turn == 0:
                        self.select_player(self.now_turn)
                        mouse_pos = pygame.mouse.get_pos()
                        for sprite in self.user_group:
                            if sprite.get_rect().collidepoint(mouse_pos):
                                if self.check_card(sprite): # 플레이어가 낼 수 있는 지 판단
                                    pygame.mixer.pre_init(44100, -16, 1, 512)
                                    pygame.init()
                                    card = pygame.mixer.Sound('./sound/deal_card.wav')
                                    self.user_group.remove(sprite)
                                    for temp in self.user_group:
                                        temp.move(sprite.getposition())
                                    sprite.setposition(430, 300)
                                    card.play()

                                    self.put_waste_group(sprite) # 낸 카드를 게임판에 처리
                                    self.card_skill(sprite)
                                    self.now_turn = self.next_turn(self.now_turn)
                                    break
                        for sprite in self.deck_group:
                            if sprite.get_rect().collidepoint(mouse_pos):
                                self.get_from_deck(self.now_turn)
                                self.now_turn = self.next_turn(self.now_turn)
                                break
            pygame.display.update()
    
    # playgame()이 14번째로 호출했다, 덱에서 카드를 한 장 가져오는 함수
    def get_from_deck(self, now_turn): 
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        deck = pygame.mixer.Sound('./sound/from_deck.wav')
        item = self.card_deck.pop(0) # 카드 덱의 첫번째 카드를 가져온다
        deck.play()
        if now_turn == 0: # 플레이어의 턴이면
            temp = loadcard.Card(item, (400, 300))
            current_pos = self.lastcard0
            if current_pos[0] >= 620: # 카드가 10장? 이상이면 2번째 줄에 배치
                y = current_pos[1] + 80
                x = 200
            else:
                y = current_pos[1]
                x = current_pos[0] + 70      
            temp.setposition(x, y)
            self.lastcard0 = (x, y)
            self.user_group.add(temp) # 스프라이트 그룹에 카드 객체 추가
        elif now_turn == 1:
            temp = loadcard.Card('BACK', (350, 300))
            temp.rotation(180)
            current_pos = self.lastcard1
            if current_pos[0] >= 510:
                y = current_pos[1] + 40
                x = 270
            else:
                y = current_pos[1]
                x = current_pos[0] + 40
            temp.setposition(x, y)
            self.lastcard1 = (x, y)
            self.com1_group.add(temp)
            self.player[1].append(item)
        elif now_turn == 2:
            temp = loadcard.Card('BACK', (350, 300))
            current_pos = self.lastcard2
            temp.rotation(90)
            if current_pos[1] >= 410:
                y = 170
                x = current_pos[0] + 40
            else:
                y = current_pos[1] + 40
                x = current_pos[0]
            temp.setposition(x, y)
            self.lastcard2 = (x, y)
            self.com2_group.add(temp)
            self.player[2].append(item)
        elif now_turn == 3:
            temp = loadcard.Card('BACK', (350, 300))
            current_pos = self.lastcard3
            temp.rotation(270)
            if current_pos[1] >= 410:
                y = 170
                x = current_pos[0] + 40
            else:
                y = current_pos[1] + 40
                x = current_pos[0]
            temp.setposition(x, y)
            self.lastcard3 = (x, y)
            self.com3_group.add(temp)
            self.player[3].append(item)
        self.printwindow()

    # playgame()이 16번째로 호출, 마지막 카드의 위치를 지정하는 함수
    def set_lastcard(self, lastcard, compare_pos): # self.lastcard1, (0,0)
        x = lastcard[0]
        y = lastcard[1]

        i_x = compare_pos[0]
        i_y = compare_pos[1]

        if self.now_turn == 0: # 플레이어의 턴이면
            if x >= i_x+60 and y == i_y:
                x -= 70

            elif y > i_y:
                if x <= 200:
                    x = 620
                    y = y - 80
                else:
                    x -= 70
            self.lastcard0 = (x, y)
        elif self.now_turn == 1:
            if y > 100 and x == 270:
                y -= 40
                x = 510
            else:
                x -= 40
            self.lastcard1 = (x, y)
        elif self.now_turn == 2:
            if x > 80 and y == 170:
                x -= 40
                y = 410
            else:
                y -= 40
            self.lastcard2 = (x, y)
        elif self.now_turn == 3:
            if x > 710 and y == 170:
                x -= 40
                y = 410
            else:
                y -= 40
            self.lastcard3 = (x, y)

    # playgame()이 23번째로 호출
    def put_waste_group(self, sprite): # for sprite in self.user_group
        self.waste_group.add(sprite)
        self.waste_card.append(sprite.get_name())
        self.set_lastcard(self.lastcard0, sprite.getposition())
        self.printwindow()
        # 낸 카드 그룹과 리스트에 추가하고, 위치 조정하고, 표시하는 함수
import pygame
from pygame.locals import *

temp = []

# playgame()이 8번째로 호출
class AI():
    def __init__(self, playernum, playerdeck, wastecard): # wastecard = 게임에서 제출된(버려진) 카드
        print(playerdeck)
        self.playernum = playernum
        self.playerdeck = playerdeck
        self.nowcard = wastecard[-1] # 게임에서 낸 카드들 중에 가장 마지막 카드 -> 가장 위에 카드 (색이나 번호를 일치시켜야 하는)
        self.wastes = wastecard

    # self.difficulty = 1일때 AI가 취하는 행동
    def basicplay(self):
        now = self.nowcard.split('_') # now = ["카드 색깔", "스킬 카드면 SKILL", "카드 번호"] 가 들어간다.
        
        # self.playerdeck에는 플레이어의 남은 카드가 들어가 있다.
        for item in self.playerdeck:
            card = item.split('_')
            if now[0] == 'BLACK' : return item # 가장 위에 카드가 블랙이면 아무 색이나 되니까 바로 내라.
            
            if len(now) == 1: # 낸 카드가 없을 때는, 아무 카드나 내려 놓을 수 있다.
                if card[0] == now[0]: return item
            
            # 숫자 카드일 때는 색이 일치하거나, 번호가 일치하면 내라
            elif len(card) < 3 or len(now) < 3:
                if card[0] == now[0]: return item
                elif card[1] == now[1]: return item
            
            # 기술 카드일 때는 인덱스가 2번으로 바뀜
            else:
                if card[0] == now[0]: return item
                elif card[2] == now[2]: return item
        # 내가 가진 카드가 블랙이면 그 카드를 내라.
        for item in self.playerdeck:
            card = item.split('_')
            if card[0] == 'BLACK' : return item
        return 0

    # self.difficulty = 2일때 AI가 취하는 행동
    # playgame()이 10번째로 호출
    def advancedplay(self, next_user): # self.user_group이나 self.player[next]이 들어가 있다
        now = self.nowcard.split('_') # now는 마지막으로 낸 카드 = ["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
        solution = []

        # self.playerdeck에는 AI의 남은 카드가 들어가 있다
        for item in self.playerdeck:
            card = item.split('_')
            if len(next_user) < 3:
                if len(card) == 3: # ["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
                    if card[2] == 4 : return item # 4장 추가 와일드 카드면, 그거 내라
                    elif card[2] == 2 : return item # 색깔 2장 추가 카드면, 그거 내라
        
        if len(self.playerdeck) == 1: # AI의 카드가 1장 남으면 그거 내면 된다
            return self.playerdeck[0]
        
        result = self.find_solution(now)
        if result == None: # 만약, 낼 카드를 못 찾았으면
            for item in self.playerdeck:
                card = item.split('_')
                if card[0] == 'BLACK': # 한번 더 와일드 카드가 있는 지 확인하고, 리턴한다
                    result = item
            return result
        else: return result # result는 0이거나 None일 수 있다

    # advanceplay()가 11번째로 호출
    def find_solution(self, now): # now는 게임판에 마지막으로 낸 카드 = ["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
        temp = []
        for item in self.playerdeck:
            item_ = item.split('_') # item_["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
            if len(item_) == 2: # 내 카드가 숫자 카드면
                if len(now) == 1:
                    if item_[0] == now[0]: temp.append(item)
                if len(now) == 2: # now가 숫자 카드면
                    if item_[0] == now[0]: temp.append(item)
                    elif item_[1] == now[1]: temp.append(item)
                if len(now) == 3: # now가 기술 카드면
                    if item_[0] == now[0]: temp.append(item)
            
            if len(item_) == 3: # 내 카드가 기술 카드면
                if item_[0] != 'BLACK': # 그 중, 색깔 기술 카드면
                    if item_[0] == now[0]: # 낼 수 있으면
                        if self.playernum == 2: # 게임이 2인용이면, 2장 연속으로 낼 수 있어야 이 카드를 사용한다
                            if self.check_same_color(item_[0]): temp.append(item)
                        else: temp.append(item)
                    if len(now) == 3: # now가 기술 카드인데, 내 카드가 같은 기술 카드면
                        if item_[2] == now[2]: 
                            if self.playernum == 2:
                                if self.check_same_color(item_[0]): temp.append(item)
                            else: temp.append(item)
                elif item_[0] == 'BLACK':
                    temp.append(item)
        
        if len(temp) == 1: # 이번 턴에 낼 수 있는 카드가 1장이면
            return temp[0]
        
        if len(temp) > 1: # 1장 이상이면
            before = temp[0]
            check = 0
            for i in range(1, len(temp)):
                before_ = before.split('_') # before_["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
                card = temp[i]
                card_ = card.split('_')
                if before_[0] == card_[0]: # 낼 수 있는 카드 중에 0번 카드와 색이 같은 카드를 찾으면
                    before = card
                else: check = 1

            if check == 1: # 0번 카드와 색이 같은 카드를 못 찾았으면
                result = self.calculate_p(temp) # 여태까지 가장 많이 제출된 카드의 색깔을 우선으로 낸다
            else:
                result = temp[0]
                for card in temp:
                    card_ = card.split('_')
                    if len(card_) == 3:
                        result = card # 색이 같은 카드를 찾았으면 기술 카드부터 낸다
            return result 

    # find_solution()이 12번째로 호출
    def check_same_color(self, color): # color에는 블랙이 아닌 4가지 색깔 문자열이 들어가 있다.
        sum = 0
        for item in self.playerdeck:
            item_ = item.split('_')
            if item_[0] == color:
                sum = sum + 1
        if sum > 1: return True # 즉, now에 있는 같은 색의 카드가 2장 이상 있는지 확인한다
        else: return False

    # find_solution()이 13번째로 호출
    def calculate_p(self, result): # result에는 이번 턴에 낼 수 있는 카드의 리스트들이 들어가있다
        red = 0; yellow = 0; green = 0; blue = 0

        # 즉, 게임에서 낸 모든 카드들의 색을 카운트한다
        for card in self.wastes: # self.wastes = 게임에서 제출된(버려진) 카드
            card_ = card.split('_') # card_["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
            if len(card_) != 1:
                if card_[0] == 'RED' : red += 1.0
                elif card_[0] == 'YELLOW' : yellow += 1.0
                elif card_[0] == 'GREEN' : green += 1.0
                elif card_[0] == 'BLUE' : blue += 1.0

        temp = [red, yellow, green, blue]
        if 0 in temp:
            temp.remove(0) # 한 번도 나오지 않은 카드 색깔은 버린다
        temp.sort(reverse=True) # 역순 = 많이 나온 카드 색깔 순으로 정렬
        c_temp = []
        for p in temp:
            if p == red: c_temp.append('RED')
            elif p == yellow: c_temp.append('YELLOW')
            elif p == green: c_temp.append('GREEN')
            elif p == blue: c_temp.append('BLUE')

        for c in c_temp:
            for i in result: # result에는 이번 턴에 낼 수 있는 카드의 리스트들이 들어가있다
                card = i.split('_') # card["카드 색깔", "스킬 카드면 SKILL", "카드 번호"]
                if card[0] == c : return i
        
        return result[0]
    
    # 결론은 여태까지 많이 제출한 카드 색깔을 우선으로 한다.
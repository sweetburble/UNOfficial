from functions import *
from classes import *
import pytest
import pygame

# with pytest.raises(TypeError):
    # TypeError가 발생해야 함

@pytest.fixture
def ess():
    # essential 클래스를 생성한다
    return Essentials()

@pytest.fixture
def sound():
    # essential 클래스를 생성한다
    pygame.init()
    pygame.mixer.music.set_volume(-1)
    return Sound()

""" peek() 함수 테스트 """
def test_peek():
    deck = ['a', 'b', 'c']
    assert peek(deck) == 'c'
    assert deck == ['a', 'b', 'c']

""" create() 함수 테스트 """
def test_create(ess):
    create(ess)
    assert len(ess.deck1) == 91
    assert len(ess.deck2) == 1
    assert len(ess.player_list) == 4
    assert len(ess.player_list[0]) == 7
    assert len(ess.player_list[1]) == 7
    assert len(ess.player_list[2]) == 7
    assert len(ess.player_list[3]) == 7

""" re_initialize() 함수 테스트 """
def test_re_initialize(ess):
    re_initialize(ess)
    assert ess.message == ""
    assert ess.winner == -1
    assert ess.player_playing == False
    assert ess.play_lag == -1
    assert ess.direction_check == 1 
    assert ess.position == -1  
    assert ess.special_check == 0  
    assert (ess.drawn, ess.played, ess.choose_color) == (False, False, False)
    assert ess.uno == [True] * 4
    assert ess.easy == True

""" play_this_card() 함수 테스트 """
def test_play_this_card(ess):
    ess.player_list[0] = [('1', 'Blue'), ('9', 'Blue'), ('+4', 'Black')]
    ess.deck2 = [('1', 'Red')]
    ess.current = peek(ess.deck2)

    play_this_card(ess, ('1', 'Blue')) # 숫자가 같으면 낼 수 있음
    assert (ess.played, ess.drawn) == (True, True)
    assert peek(ess.deck2) == ('1', 'Blue')
    (ess.played, ess.drawn) = (False, False)

    play_this_card(ess, ('9', 'Blue')) # 색깔이 같으면 낼 수 있음
    assert (ess.played, ess.drawn) == (True, True)
    assert peek(ess.deck2) == ('9', 'Blue')
    (ess.played, ess.drawn) = (False, False)

    play_this_card(ess, ('+4', 'Black')) # 와일드카드는 그냥 낼 수 있음
    assert ess.choose_color == True
    assert peek(ess.deck2) == ('+4', 'Black')

""" set_curr_player() 함수 테스트 """
def test_set_curr_player(ess):
    ess.player_playing = True
    ess.current = ('1', 'Red') # 현재 버려진 카드 덱의 맨 위 카드

    ess.position = 0
    ess.direction_check = 1
    set_curr_player(ess, True)
    assert ess.position == 1 # 정상적으로 다음 플레이어로 넘어감

    ess.position = 3
    ess.direction_check = -1 # 반대 방향으로 플레이어가 돌아가야 함
    set_curr_player(ess, True)
    assert ess.position == 2

    ess.current = ('Reverse', 'Red') # Reverse 카드를 냈을 때, direction_check가 바뀌어야 함
    ess.special_check = 0
    set_curr_player(ess, False)
    assert ess.direction_check == 1

    ess.current = ('Skip', 'Red') # Skip 카드를 냈을 때, 다음 플레이어로 넘어가야 함
    ess.special_check = 0
    set_curr_player(ess, False)
    assert ess.position == 3
    assert ess.special_check == 1

""" take_from_stack() 함수 테스트 """
def test_take_from_stack(ess):
    ess.deck1 = [('4', 'Yellow')]
    ess.deck2 = [('1', 'Blue'), ('Reverse', 'Red'), ('+2', 'Red'), ('+4', 'Black')]
    ess.player_list[0] = []
    ess.drawn = False

    take_from_stack(ess)
    assert len(ess.player_list[0]) == 1
    assert ess.drawn == True
    assert len(ess.deck1) == 0

    ess.drawn = False
    take_from_stack(ess)
    assert len(ess.deck1) == 3
    assert len(ess.player_list[0]) == 2

""" play_this_card_2() 함수 테스트 """
def test_play_this_card_2(ess):
    ess.special_check = 1
    ess.deck2 = [('1', 'Red'), ('7', 'Green')]

    play_this_card_2(ess, 'Blue')
    assert ess.deck2[-1] == ('7', 'Blue')
    assert ess.current == ('7', 'Blue')
    assert ess.special_check == 0

""" handle24() 함수 테스트 """
def test_handle24(ess):
    ess.bot_map = {1: "FRIDAY", 2: "EDITH", 3: "JARVIS"}
    ess.deck1 = [('1', 'Red'), ('7', 'Green'), ('+2', 'Red'), ('+4', 'Black')]
    ess.special_check = 0
    ess.position = 0
    ess.player_list[1] = [('2', 'Blue')]
    ess.player_list[2] = [('9', 'Yellow')]
    ess.player_list[3] = [('Wild', 'Black')]
    
    ess.position = 1
    handle24(ess, 1)
    assert len(ess.player_list[1]) == 2
    assert ess.special_check == 1
    assert ess.message == "FRIDAY Draws 1 cards"

    ess.position = 2
    handle24(ess, 2)
    assert len(ess.player_list[2]) == 3
    assert ess.message == "EDITH Draws 2 cards"
    
    ess.position = 3
    handle24(ess, 0)
    assert len(ess.player_list[3]) == 1

def test_bot_play_card(ess):
    ess.player_list[1] = [('5', 'Green')]
    ess.player_list[3] = [('+2', 'Blue')]
    ess.deck2 = [('6', 'Red')]
    ess.special_check = 1
    
    ess.position = 1
    bot_play_card(ess, ess.player_list[1][0])
    assert len(ess.deck2) == 2
    assert ess.current == ('5', 'Green')
    assert ess.message == "FRIDAY plays card Green 5"

    ess.position = 3
    bot_play_card(ess, ess.player_list[3][0])
    assert len(ess.deck2) == 3
    assert ess.current == ('+2', 'Blue')
    assert ess.message == "JARVIS plays card Blue +2"

""" handle_black() 함수 테스트 """
def test_handle_black(ess):
    ess.player_list[1] = [('Wild', 'Black'), ('Wild', 'Black'), ('+4', 'Black'), ('+2', 'Green'), ('5', 'Green'), ('1', 'Red')]
    ess.deck2 = [('3', 'Blue')]
    ess.position = 1
    ess.special_check = 1
    
    ess.easy = False
    handle_black(ess, ('Wild', 'Black'))
    assert len(ess.deck2) == 2
    assert ess.message == "FRIDAY plays Wild Black, new color is Green"
    assert ess.current == ('Wild', 'Green')

    # 컴퓨터가 easy모드일 때는, AssertionError가 발생해야 함
    ess.easy = True
    with pytest.raises(AssertionError):
        for i in range(4):
            handle_black(ess, ('+4', 'Black'))
            assert len(ess.deck2) == (3 + i)
            assert ess.message == "FRIDAY plays +4 Black, new color is Green"
            assert ess.current == ('+4', 'Green')

""" bot_action() 함수 테스트 """
def test_bot_action(ess, sound):
    # 1. 전 플레이어가 +1, +2, +4 카드를 냈다면, 카드를 받고 그냥 턴을 넘긴다
    ess.position = 1
    ess.current = ('+1', 'Red')
    ess.special_check = 0
    ess.deck1 = [('1', 'Red'), ('7', 'Green'), ('+2', 'Red'), ('+4', 'Black')]
    ess.player_list[1] = [('5', 'Green'), ('+2', 'Blue')]
    
    bot_action(ess, sound)
    assert len(ess.player_list[1]) == 3
    assert ess.played_check == 1

    # 2. AI가 가지고 있는 카드 중에서 색깔이나 숫자가 같은 카드가 있다면
    ess.current = ('6', 'Yellow')
    ess.player_list[1] = [('9', 'Yellow'), ('8', 'Blue'), ('+2', 'Blue')]

    bot_action(ess, sound)
    assert ess.player_list[1] == [('8', 'Blue'), ('+2', 'Blue')]

    # 3. 색깔이나 숫자가 같은 카드가 없는데, 와일드 카드가 있다면
    ess.current = ('6', 'Red')
    ess.player_list[1] = [('Wild', 'Black'), ('8', 'Blue'), ('7', 'Blue')]
    
    bot_action(ess, sound)
    assert ess.player_list[1] == [('8', 'Blue'), ('7', 'Blue')]

    # 4. 색깔이나 숫자가 같은 카드가 없고, 와일드 카드도 없다면
    ess.deck1 = [('1', 'Blue'), ('7', 'Green')]
    ess.current = ('4', 'Blue')
    ess.player_list[1] = [('9', 'Red'), ('8', 'Red')]
    
    bot_action(ess, sound)
    assert ess.deck1 == [('1', 'Blue')]
    assert ess.player_list[1] == [('9', 'Red'), ('8', 'Red'), ('7', 'Green')]
    assert ess.message == "FRIDAY draws a card"

    # 4-2. 덱에서 뽑은 카드를 낼 수 있다면
    bot_action(ess, sound)
    assert ess.deck1 == []
    assert ess.player_list[1] == [('9', 'Red'), ('8', 'Red'), ('7', 'Green')]

    # 5. 남은 카드가 2장인데, 이번 턴에 낼 수 있다면 UNO를 외친다
    ess.easy = False
    ess.current = ('4', 'Blue')
    ess.player_list[1] = [('9', 'Red'), ('8', 'Blue')]

    bot_action(ess, sound)
    assert ess.uno[1] == True
    assert ess.message == "FRIDAY shouted UNO!"

    # 5-2. easy 모드는 1/2 확률로 UNO를 외친다
    ess.easy = True
    with pytest.raises(AssertionError):
        for _ in range(5):
            ess.uno[1] = False
            ess.current = ('4', 'Blue')
            ess.player_list[1] = [('9', 'Red'), ('8', 'Blue')]
            bot_action(ess, sound)
            assert ess.uno[1] == True # 안 외칠수도 있기 때문에, False일 수도 있다
            assert ess.message == "FRIDAY shouted UNO!"
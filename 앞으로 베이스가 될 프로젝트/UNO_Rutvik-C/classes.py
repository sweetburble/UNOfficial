import pygame


class Essentials(object):
    def __init__(self):
        self.player_list = [[], [], [], []]  # 2차원 리스트 생성 -> 플레이어들의 카드를 저장하기 위해서
        self.deck1 = list() # deck1 =  카드 덱
        self.deck2 = list() # deck2 =  버려진 카드 덱
        
        self.direction_check = 1  # 게임의 진행 방향, 1은 시계 방향, -1은 반시계 방향
        self.position = -1  # 플레이 하는 플레이어 인덱스 (Playing player index)
        self.current = list()  # Current card on top of stack, 버려진 카드 덱의 맨 위에 있는 카드

        self.drawn = False  # 유저 플레이 플래그 (User play flags)
        self.played = False # 유저가 카드를 플레이 했는지 확인하는 플래그
        self.choose_color = False
        self.player_playing = False # 유저가 플레이하고 있으면 True, 아니면 False
        self.winner = -1
        self.play_lag = -1
        self.play_mode = ""

        self.played_check = 0  # Play checker
        self.special_check = 0  # 기술 카드 상태 활성화, 1은 비활성화
        self.uno = [True] * 4  # 각 플레이어가 UNO를 외쳤는지 저장하는 플래그
        self.message = "DEALING THE CARDS"  # 인게임 메세지, 한글은 폰트 문제로 인해 사용 불가
        self.easy = True  # 게임 난이도
        self.bot_map = {1: "FRIDAY", 2: "EDITH", 3: "JARVIS"}  # AI 인덱스를 이름으로 인덱싱
        self.color = ['Blue', 'Red', 'Green', 'Yellow']  # 카드 색깔들


class PlayMode(object):
    def __init__(self):
        # 다양한 플레이 모드를 선언했다 (Declaring various playing modes)
        self.load = "LOAD PAGE"
        self.in_game = "IN GAME"
        self.info = "INFO PAGE"
        self.win = "WINNER"


class Image(object):
    def __init__(self):
        # 필요한 이미지 파일 로딩
        self.icon = pygame.image.load("./images/icon.png")
        self.load = pygame.image.load("./images/uno_load.png")
        self.bg = pygame.image.load("./images/background.png")
        self.back = pygame.image.load("./images/return-button.png")
        self.mute = pygame.image.load("./images/mute.png")
        self.unmute = pygame.image.load("./images/unmute.png")
        self.p1 = pygame.image.load("./images/woman.png")
        self.p2 = pygame.image.load("./images/man.png")
        self.p3 = pygame.image.load("./images/woman (1).png")
        self.p4 = pygame.image.load("./images/man (1).png")
        self.card_back = pygame.image.load("./images/Back.png")
        self.card_back_l = pygame.image.load("./images/Back_left.png")
        self.card_back_r = pygame.image.load("./images/Back_right.png")
        self.card_back_i = pygame.image.load("./images/Back_inverted.png")
        self.done = pygame.image.load("./images/checked.png")
        self.line = pygame.image.load("./images/minus-line.png")
        self.help = pygame.image.load("./images/help.png")
        self.win = pygame.image.load("./images/winner.png")
        self.pick_color = pygame.image.load("./images/microsoft.png")
        self.uno = pygame.image.load("./images/UNO.png")
        self.uno_button = pygame.image.load("./images/UNOButton.png")
        self.red = pygame.image.load("./images/SmallRed.png")
        self.blue = pygame.image.load("./images/SmallBlue.png")
        self.yellow = pygame.image.load("./images/SmallYellow.png")
        self.green = pygame.image.load("./images/SmallGreen.png")


class Sound(object):
    def __init__(self):
        # 필요한 사운드 파일 로딩
        self.back_g = "./sound/bg.wav"
        self.click = pygame.mixer.Sound('./sound/Minecraft-hat.wav')
        self.card_drawn = pygame.mixer.Sound('./sound/card_drawn.wav')
        self.card_played = pygame.mixer.Sound('./sound/card_played.wav')
        self.shuffled = pygame.mixer.Sound('./sound/shuffle.wav')
        self.uno = pygame.mixer.Sound("./sound/Recording.wav")
        self.victory = pygame.mixer.Sound("./sound/victory.wav")


class TextFont(object):
    def __init__(self):
        # 필요한 폰트 파일 로딩
        self.pacifico = "./fonts/Pacifico.ttf"
        self.joe_fin = "./fonts/JosefinSans-Bold.ttf"

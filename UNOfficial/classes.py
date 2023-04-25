import pygame

# saves dictionary에 저장된 설정 내용 불러오기
saves = {}
defaults = {}
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

with open('default.txt', 'r') as f: # 모두 기본 설정으로 바꾸기 위해 만든 defaults 딕셔너리 미리 채우기
    lines = f.readlines()
    settings = lines[:3]
    settings2 = lines[3:8]
    settings3 = lines[8:]
for line in settings:
    key, value = line.strip().split(':')
    defaults[key] = value
for line in settings2:
    action, key_name = line.strip().split(':')
    key = int(key_name)
    defaults[action] = key
for line in settings3:
    action, key_name = line.strip().split(':')
    key = float(key_name)
    defaults[action] = key


# 주어진 설정에 따라 width, height 변수 크기 결정
if saves["size"] == 'large':
    width = 1500
    height = 900
elif saves["size"] == 'medium':
    width = 1000
    height = 600
elif saves["size"] == 'small':
    width = 750
    height = 450


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
        self.easy = False  # 게임 난이도
        self.bot_map = {1: "FRIDAY", 2: "EDITH", 3: "JARVIS"}  # AI 인덱스를 이름으로 인덱싱
        self.color = ['Blue', 'Red', 'Green', 'Yellow']  # 카드 색깔들


class PlayMode(object):
    def __init__(self):
        # 다양한 플레이 모드를 선언했다 (Declaring various playing modes)
        self.load = "LOAD PAGE"
        self.in_game = "IN GAME"
        self.setting = "SETTING"
        self.win = "WINNER"
        self.key = "KEY CONFIGURATION"
        self.stroy = "STORY MODE"
        self.volume = "VOLUME"


class Image(object):
    def __init__(self):
        # 필요한 이미지 파일 로딩
        icon = pygame.image.load("./images/icon.png")
        self.icon = pygame.transform.scale_by(icon, (width/1000, height/600))
        load = pygame.image.load("./images/uno_load.png")
        self.load = pygame.transform.scale_by(load, (width/1000, height/600))
        bg = pygame.image.load("./images/background.png")
        self.bg = pygame.transform.scale_by(bg, (width/1000, height/600))
        back = pygame.image.load("./images/return-button.png")
        self.back = pygame.transform.scale_by(back, (width/1000, height/600))
        
        mute = pygame.image.load("./images/mute.png")
        self.mute = pygame.transform.scale_by(mute, (width/1000, height/600))
        unmute = pygame.image.load("./images/unmute.png")
        self.unmute = pygame.transform.scale_by(unmute, (width/1000, height/600))
        
        p1 = pygame.image.load("./images/woman.png")
        self.p1 = pygame.transform.scale_by(p1, (width/1000, height/600))
        p2 = pygame.image.load("./images/man.png")
        self.p2 = pygame.transform.scale_by(p2, (width/1000, height/600))
        p3 = pygame.image.load("./images/woman (1).png")
        self.p3 = pygame.transform.scale_by(p3, (width/1000, height/600))
        p4 = pygame.image.load("./images/man (1).png")
        self.p4 = pygame.transform.scale_by(p4, (width/1000, height/600))
        
        card_back = pygame.image.load("./images/Back.png")
        self.card_back = pygame.transform.scale_by(card_back, (width/1000, height/600))
        card_back_l = pygame.image.load("./images/Back_left.png")
        self.card_back_l = pygame.transform.scale_by(card_back_l, (width/1000, height/600))
        card_back_r = pygame.image.load("./images/Back_right.png")
        self.card_back_r = pygame.transform.scale_by(card_back_r, (width/1000, height/600))
        card_back_i = pygame.image.load("./images/Back_inverted.png")
        self.card_back_i = pygame.transform.scale_by(card_back_i, (width/1000, height/600))
        done = pygame.image.load("./images/checked.png")
        self.done = pygame.transform.scale_by(done, (width/1000, height/600))
        line = pygame.image.load("./images/minus-line.png")
        self.line = pygame.transform.scale_by(line, (width/1000, height/600))
        help = pygame.image.load("./images/help.png")
        self.help = pygame.transform.scale_by(help, (width/1000, height/600))
        win = pygame.image.load("./images/winner.png")
        self.win = pygame.transform.scale_by(win, (width/1000, height/600))
        pick_color = pygame.image.load("./images/microsoft.png")
        self.pick_color = pygame.transform.scale_by(pick_color, (width/1000, height/600))
        uno = pygame.image.load("./images/UNO.png")
        self.uno = pygame.transform.scale_by(uno, (width/1000, height/600))
        uno_button = pygame.image.load("./images/UNOButton.png")
        self.uno_button = pygame.transform.scale_by(uno_button, (width/1000, height/600))
        
        red = pygame.image.load("./images/SmallRed.png")
        self.red = pygame.transform.scale_by(red, (width/1000, height/600))
        blue = pygame.image.load("./images/SmallBlue.png")
        self.blue = pygame.transform.scale_by(blue, (width/1000, height/600))
        yellow = pygame.image.load("./images/SmallYellow.png")
        self.yellow = pygame.transform.scale_by(yellow, (width/1000, height/600))
        green = pygame.image.load("./images/SmallGreen.png")
        self.green = pygame.transform.scale_by(green, (width/1000, height/600))


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

class UNOGame(object):
    def __init__(self):
        self.screen_width = width
        self.screen_height = height

        background = pygame.image.load('images/Main_background.png')
        self.background = pygame.transform.scale_by(background, (self.screen_width/800, self.screen_height/600))
        self.background_Color = (0,66,0)

        self.playernum = 2
        self.difficulty = 1
        self.font = 'Berlin Sans FB'
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("UNOfficial")
        self.screen.fill(self.background_Color)
        self.screen.blit(self.background, (-30, -30))
        pygame.display.update()
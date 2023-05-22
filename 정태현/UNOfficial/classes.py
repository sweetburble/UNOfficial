import pygame
import datetime
import json

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

# 주어진 설정에 따라 이미지 경로 결정
if saves["color_change"] == 'original':
    path = 'original'
else:
    path = 'alternative'

class Essentials(object):
    def __init__(self):
        self.player_list = []  # 2차원 리스트 생성 -> 플레이어들의 카드를 저장하기 위해서
        self.deck1 = list() # deck1 =  카드 덱
        self.deck2 = list() # deck2 =  버려진 카드 덱
        
        self.direction_check = 1  # 게임의 진행 방향, 1은 시계 방향, -1은 반시계 방향
        self.position = -1 # 플레이 하는 플레이어의 인덱스
        self.current = list() # 버려진 카드 덱의 맨 위에 있는 카드

        self.drawn = False  # 유저가 카드를 뽑았는지 확인하는 플래그
        self.played = False # 유저가 카드를 플레이 했는지 확인하는 플래그
        self.choose_color = False
        self.player_playing = False # 유저가 플레이하고 있으면 True, 아니면 False
        self.winner = -1
        self.play_lag = -1
        self.play_mode = ""
        self.is_game_paused = False

        self.played_check = 0  # Play checker
        self.special_check = 0  # 기술 카드 상태 활성화, 1은 비활성화
        self.shouted_uno = [False] * 4  # 각 플레이어가 UNO를 외쳤는지 저장하는 플래그
        self.message = "DEALING THE CARDS"  # 인게임 메세지, 한글은 폰트 문제로 인해 사용 불가
        self.bot_map = {1: "JARVIS", 2: "EDITH", 3: "FRIDAY", 4: "BRIAN", 5: "SWIFT", 6: "YOU"}  # 플레이어 인덱스를 이름으로 인덱싱
        self.color = ['Blue', 'Red', 'Green', 'Yellow']  # 카드 색깔들

        self.path = path # 색약 모드를 위해 이미지 파일을 불러오는 경로


class PlayMode(object):
    def __init__(self):
        # 다양한 플레이 모드를 선언했다 (Declaring various playing modes)
        self.load = "START SCREEN" # 시작 화면
        self.setting = "SETTING" # 설정 화면
        self.in_game = "IN GAME" # 게임 화면
        self.pause = "GAME PAUSE" # 게임 일시정지 화면
        self.win = "WINNER" # 승리 화면
        self.story = "STORY MODE" # 스토리 모드 화면
        self.multiplay = "MULTIPLAY" # 멀티플레이 화면
        self.achievement = "ACHIEVEMENT" # 업적 화면


class Image(object):
    def __init__(self):
        # 필요한 이미지 파일 로딩
        icon = pygame.image.load("./images/icon.png")
        self.icon = pygame.transform.scale_by(icon, (width/1000, height/600))
        bg = pygame.image.load("./images/background.png")
        self.bg = pygame.transform.scale_by(bg, (width/1000, height/600))
        pause = pygame.image.load("./images/pause-button.png")
        self.pause = pygame.transform.scale_by(pause, (width/1000, height/600))
        
        shouted = pygame.image.load("./images/shouted.png")
        self.shouted = pygame.transform.scale_by(shouted, (width/1000, height/600))

        p_user = pygame.image.load("./images/man_1.png") # 유저 플레이어 이미지
        self.p_user = pygame.transform.scale_by(p_user, (width/1000, height/600))

        p1 = pygame.image.load("./images/man.png") # JARVIS
        self.p1 = pygame.transform.scale_by(p1, (width/1000, height/600))
        p2 = pygame.image.load("./images/woman.png") # EDITH
        self.p2 = pygame.transform.scale_by(p2, (width/1000, height/600))
        p3 = pygame.image.load("./images/woman_1.png") # FRIDAY
        self.p3 = pygame.transform.scale_by(p3, (width/1000, height/600))
        p4 = pygame.image.load("./images/man_2.png") # BRIAN
        self.p4 = pygame.transform.scale_by(p4, (width/1000, height/600))
        p5 = pygame.image.load("./images/woman_2.png") # SWIFT
        self.p5 = pygame.transform.scale_by(p5, (width/1000, height/600))
        
        card_back = pygame.image.load("./images/Back.png")
        self.card_back = pygame.transform.scale_by(card_back, (width/1000, height/600))
        card_back_computer = pygame.image.load("./images/Back_computer.png") # 컴퓨터 플레이어의 카드를 표시할 이미지
        self.card_back_computer = pygame.transform.scale_by(card_back_computer, (width/1000, height/600))
        card_back_l = pygame.image.load("./images/Back_left.png")
        self.card_back_l = pygame.transform.scale_by(card_back_l, (width/1000, height/600))
        card_back_r = pygame.image.load("./images/Back_right.png")
        self.card_back_r = pygame.transform.scale_by(card_back_r, (width/1000, height/600))
        card_back_i = pygame.image.load("./images/Back_inverted.png")
        self.card_back_i = pygame.transform.scale_by(card_back_i, (width/1000, height/600))
        
        done = pygame.image.load("./images/done.png")
        self.done = pygame.transform.scale_by(done, (width/1000, height/600))
        line = pygame.image.load("./images/minus-line.png")
        self.line = pygame.transform.scale_by(line, (width/1000, height/600))

        win = pygame.image.load("./images/winner.png")
        self.win = pygame.transform.scale_by(win, (width/1000, height/600))
        pick_color = pygame.image.load("./images/" + path + "/microsoft.png")
        self.pick_color = pygame.transform.scale_by(pick_color, (width/1000, height/600))
        uno = pygame.image.load("./images/UNO.png")
        self.uno = pygame.transform.scale_by(uno, (width/1000, height/600))
        uno_button = pygame.image.load("./images/UNOButton.png")
        self.uno_button = pygame.transform.scale_by(uno_button, (width/1000, height/600))
        
        pick_red = pygame.image.load("./images/" + path + "/SmallRed.png")
        self.pick_red = pygame.transform.scale_by(pick_red, (width/1000, height/600))
        pick_blue = pygame.image.load("./images/" + path + "/SmallBlue.png")
        self.pick_blue = pygame.transform.scale_by(pick_blue, (width/1000, height/600))
        pick_yellow = pygame.image.load("./images/" + path + "/SmallYellow.png")
        self.pick_yellow = pygame.transform.scale_by(pick_yellow, (width/1000, height/600))
        pick_green = pygame.image.load("./images/" + path + "/SmallGreen.png")
        self.pick_green = pygame.transform.scale_by(pick_green, (width/1000, height/600))


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

        self.player_num = 2
        self.font = 'Berlin Sans FB'
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("UNOfficial")
        self.screen.fill(self.background_Color)
        self.screen.blit(self.background, (-30, -30))
        pygame.display.update()

# 스토리 모드를 관리하는 클래스 생성
class StoryMode(object):
    def __init__(self):
        self.Is_story_passed = 3 # 0은 하나도 클리어 하지 못했다는 뜻, 모든 스토리를 선택할 수 있는 상태는 3이다
        self.Is_stage_on = [False,False,False,False]


# 업적 클래스 생성
class Achievement:
    def __init__(self, name, description):
        self.name = name # 업적 이름
        self.description = description # 업적 설명
        self.achieved = False # 업적을 달성했는가? True or False
        self.achieved_time = None # 업적을 달성한 시간

    # 업적을 달성했을 때 호출되는 함수
    def set_achieved(self):
        self.achieved = True
        self.achieved_time = datetime.datetime.now().strftime("%Y-%m-%d")  # 업적 달성 시간을 연-월-일 형식으로 저장


# 업적을 관리하는 시스템 클래스 생성
class AchievementSystem:
    def __init__(self):
        self.achieve_list= [] # 업적 객체 리스트
        self.file_path = "achievement.json"

    # 업적 객체를 추가하는 함수(아마 이제 필요없을듯)
    def add_achievement(self, achievement):
        self.achieve_list.append(achievement)

    #json 파일에서 내부 리스트로 읽어오는 함수
    def load_achievements_from_file(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            for achievement_data in data:
                achievement = Achievement(
                    achievement_data["name"],
                    achievement_data["description"]
                )
                achievement.achieved = achievement_data["achieved"]
                achievement.achieved_time = achievement_data["achieved_time"]
                self.achieve_list.append(achievement)

    #업적 달성시 json 파일에 적기 위한 함수
    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "achieved": self.achieved,
            "achieved_time": self.achieved_time
        }

    #저장 된 업적 현황을 json 파일에 적을때 호출하는 함수
    def save_achievements_to_file(self, file_path):
        with open(file_path, "w") as file:
            json.dump(self.achieve_list, file, default=lambda o: o.to_json(), indent=4)

"""
achieve_single = Achievement('Singleplay_win', 'Win at the Singleplay')
achieve_story_1 = Achievement('Storymod_1_win', 'Win at the story 1')
achieve_story_2 = Achievement('Storymod_2_win', 'Win at the story 2')
achieve_story_3 = Achievement('Storymod_3_win', 'win at the story 3')
achieve_story_4 = Achievement('Storymod_4_win', 'Win at the story 4')
achieve_fast = Achievement('Fast_win', 'Win in 10 turns')
achieve_handicap = Achievement('Handicap', 'Win without a skill card')
achieve_after_UNO = Achievement('Win_afterUNO', 'Win after the opponent shouts UNO')
achieve_color = Achievement('Apply_color_weakness', 'Apply color weakness mode')
achieve_open_setting = Achievement('Open_setting', 'Open setting menu')
achieve_open_story = Achievement('Open_storymod', 'Open storymode menu')

Achieve_system = AchievementSystem()
Achieve_system.add_achievement(achieve_single)
Achieve_system.add_achievement(achieve_story_1)
Achieve_system.add_achievement(achieve_story_2)
Achieve_system.add_achievement(achieve_story_3)
Achieve_system.add_achievement(achieve_story_4)
Achieve_system.add_achievement(achieve_fast)
Achieve_system.add_achievement(achieve_handicap)
Achieve_system.add_achievement(achieve_after_UNO)
Achieve_system.add_achievement(achieve_color)
Achieve_system.add_achievement(achieve_open_setting)
Achieve_system.add_achievement(achieve_open_story)
"""#아마도 여기는 이제 필요없을 것 같아서 주석 처리합니다. 확인 후 확실할 시 지워주세요.
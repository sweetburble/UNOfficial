from classes import *
from functions import *
from settings import *
from singleplay import *
from client import *

pygame.init()
pygame.font.init()

# classes.py의 클래스들의 객체를 생성
img = Image()
PM = PlayMode()
sound = Sound()
FONT = TextFont()
ess = Essentials()
uno = UNOGame()
STORY = StoryMode()

# 파일 아이콘 설정
pygame.display.set_icon(img.icon)

# 배경음악 & 환경음 세팅
pygame.mixer.music.load(sound.back_g)
pygame.mixer.music.play(-1)  # 지속적인 배경음악 재생
pygame.mixer.music.set_volume(saves["background"])  # 배경음악 볼륨 세팅
volumesetting(sound, saves["effects"])

# 초기 게임 변수 세팅
ess.play_mode = PM.load  # 초기 play_mode는 "START SCREEN" -> 시작 화면이다

# 게임 루프
while True:
    # 모든 발생하는 이벤트를 체크한다
    for event in pygame.event.get():
        # Quit 버튼
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 마우스 클릭을 체크한다
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # 마우스 클릭 위치를 가져온다
            if width*(420/1000) < mouse_pos[0] < width*(555/1000) and height*(425/600) < mouse_pos[1] < height*(543/600) and ess.play_mode == PM.win: # 게임이 누군가의 승리로 끝나면 보이는 홈 버튼
                sound.click.play()
                re_initialize(ess, uno)
                uno.background = pygame.image.load('./images/Main_background.png')
                uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                uno.screen.blit(uno.background, (-30, -30))
                win_dec = False # 다시 승자를 초기화
                ess.play_mode = PM.load

    # 시작 화면
    if ess.play_mode == PM.load:
        function_key_config(KEYS) # 키 설정을 불러온다
        update_saves(saves) # 설정을 불러온다
        pygame.mixer.music.set_volume(saves["background"]) # 배경음악과 효과음 설정을 적용한다
        volumesetting(sound, saves["effects"])

        main_menu(ess, uno, STORY) # 필수적인 이미지와 텍스트를 표시한다

    # 싱글플레이 게임 화면 
    elif ess.play_mode == PM.in_game:
        # 게임 중에도 설정을 변경할 수 있으므로 saves 딕셔너리를 넘겨준다
        game_screen(ess, uno, sound, img, PM, saves)

    # 설정(SETTING) 화면
    elif ess.play_mode == PM.setting:
        pygame.mixer.music.set_volume(saves["background"])
        volumesetting(sound, saves["effects"])
        
        load_setting(ess, uno, sound, PM, saves) # 처음 설정 화면을 불러온다

    # 게임 승리 화면
    elif ess.play_mode == PM.win and ess.winner != -1:
        sound.victory.play() # 승리 효과음을 재생
        string = ""
        if ess.winner == 0: # 그리고 적절한 메시지를 생성한다
            string = "Well Done! You've Won this Round!"
        else:
            string = "%s has won this Round" % ess.bot_map[ess.winner]

        # 이미지와 메시지를 렌더링한다
        uno.screen.blit(img.win, (0, 0))
        text = pygame.font.Font(FONT.pacifico, int(height*(40/600))).render(string, True, (255, 238, 46))
        uno.screen.blit(text, [width*(190/1000), height*(100/600)])

    # 멀티플레이 게임 화면
    elif ess.play_mode == PM.multiplay:
        select_screen(ess, uno, saves)

    # 화면을 지속적으로 갱신
    pygame.display.update()
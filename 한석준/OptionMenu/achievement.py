import pygame

# 게임 초기화
pygame.init()

# 게임 창 설정
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("게임")

# 업적 창 설정
achievement_font = pygame.font.Font(None, 50)
achievement_window_width = 1000
achievement_window_height = 600
achievement_window_padding = 20
achievement_text_padding = 10

# 업적 시스템 초기화
class Achievement:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.achieved = False
        self.achieved_time = None

    def set_achieved(self):
        self.achieved = True
        self.achieved_time = datetime.datetime.now().strftime("%Y-%m-%d")  # 업적 달성 시간을 날짜 형식으로 저장

class AchievementSystem:
    def __init__(self):
        self.achievements = []

    def add_achievement(self, achievement):
        self.achievements.append(achievement)

achievement_1 = Achievement('Singleplay_win', 'win at the Singleplay')
achievement_2 = Achievement('storymod_1_win', 'win at the story mod stage 1')
achievement_3 = Achievement('storymod_2_win', 'win at the story mod stage 2')
achievement_4 = Achievement('storymod_3_win', 'win at the story mod stage 3')
achievement_5 = Achievement('storymod_4_win', 'win at the story mod stage 4')
achievement_6 = Achievement('fast_win', 'win in 10 turns')
achievement_7 = Achievement('handicap', 'win without a skill card')
achievement_8 = Achievement('win_afterUNO', 'winning after the opponent shouts UNO')
achievement_9 = Achievement('apply_color_weakness', 'apply color weakness mode')
achievement_10 = Achievement('open_setting', 'open setting')
achievement_11 = Achievement('open_storymod', 'open storymod')

achievement_system = AchievementSystem()
achievement_system.add_achievement(achievement_1)
achievement_system.add_achievement(achievement_2)
achievement_system.add_achievement(achievement_3)
achievement_system.add_achievement(achievement_4)
achievement_system.add_achievement(achievement_5)
achievement_system.add_achievement(achievement_6)
achievement_system.add_achievement(achievement_7)
achievement_system.add_achievement(achievement_8)
achievement_system.add_achievement(achievement_9)
achievement_system.add_achievement(achievement_10)
achievement_system.add_achievement(achievement_11)

# 업적 창 배경 이미지 로드
achievement_window_bg_image = pygame.image.load("img/background.jpg")
achievement_window_bg_image = pygame.transform.scale(achievement_window_bg_image, (achievement_window_width, achievement_window_height))

# 뒤로 가기 버튼 이미지 로드
back_button_image = pygame.image.load("img/return-button.png")

# 게임 루프
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임 창 종료 이벤트
            running = False

    # 업적 창 업데이트
    achievement_text_render_list = []

    for achievement in achievement_system.achievements:
        if achievement.achieved:
            achievement_text = f"{achievement.name}  ({achievement.description}) ({achievement.achieved_time})"
            achievement_text_color = (0, 0, 255)  # 달성된 업적의 텍스트 색상 (파란색)
        else:
            achievement_text = f"{achievement.name}  ({achievement.description})"
            achievement_text_color = (255, 255, 255)  # 달성되지 않은 업적의 텍스트 색상

        achievement_text_render = achievement_font.render(achievement_text, True, achievement_text_color)
        achievement_text_render_list.append(achievement_text_render)

    # 업적 창 그리기
    achievement_window_surface = pygame.Surface((achievement_window_width, achievement_window_height))
    achievement_window_surface.blit(achievement_window_bg_image, (0, 0))  # 배경 이미지 그리기
    text_y = achievement_window_padding

    for achievement_text_render in achievement_text_render_list:
        achievement_window_surface.blit(achievement_text_render, (achievement_window_padding, text_y))
        text_y += achievement_text_render.get_height() + achievement_text_padding

    # 업적 창 중앙에 위치
    achievement_window_x = (screen_width - achievement_window_width) // 2
    achievement_window_y = (screen_height - achievement_window_height) // 2
    screen.blit(achievement_window_surface, (achievement_window_x, achievement_window_y))

    # 뒤로 가기 버튼 그리기
    back_button_x = achievement_window_x + achievement_window_width - 60
    back_button_y = achievement_window_y + achievement_window_padding
    screen.blit(back_button_image, (back_button_x, back_button_y))

    pygame.display.flip()

# 게임 종료
pygame.quit()

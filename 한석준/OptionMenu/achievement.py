import pygame
import datetime

# 게임 초기화
pygame.init()

# 게임 창 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("게임")

# 업적 창 설정
achievement_font = pygame.font.Font(None, 36)
achievement_window_width = 400
achievement_window_height = 400
achievement_window_bg_color = (0, 0, 0)
achievement_window_border_color = (255, 255, 255)
achievement_window_text_color = (255, 255, 255)
achievement_window_padding = 20
achievement_text_padding = 10

# 스크롤 설정
scroll_position = 0
scroll_speed = 10

# 업적 시스템 초기화
class Achievement:
    def __init__(self, name):
        self.name = name
        self.achieved = False
        self.achieved_time = None

    def set_achieved(self):
        self.achieved = True
        self.achieved_time = datetime.datetime.now()

class AchievementSystem:
    def __init__(self):
        self.achievements = []

    def add_achievement(self, achievement):
        self.achievements.append(achievement)

    def check_achievements(self):
        for achievement in self.achievements:
            if not achievement.achieved:
                # 여기에서 업적 달성을 확인할 조건을 추가하세요
                if 조건:
                    achievement.set_achieved()

achievement_1 = Achievement('Singleplay_win')
achievement_2 = Achievement('storymod_1_win')
achievement_3 = Achievement('storymod_2_win')
achievement_4 = Achievement('storymod_3_win')
achievement_5 = Achievement('storymod_4_win')
achievement_6 = Achievement('fast_win')
achievement_7 = Achievement('handicap')
achievement_8 = Achievement('win_afterUNO')
achievement_9 = Achievement('apply_color_weakness')
achievement_10 = Achievement('open_setting')
achievement_11 = Achievement('open_storymod')

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

# 게임 루프
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 마우스 휠을 위로 스크롤하는 경우
                scroll_position += scroll_speed
            elif event.button == 5:  # 마우스 휠을 아래로 스크롤하는 경우
                scroll_position -= scroll_speed
        elif event.type == pygame.QUIT:  # 게임 창 종료 이벤트
            running = False

    # 업적 창 업데이트
    achievement_text_render_list = []
    for achievement in achievement_system.achievements:
        if achievement.achieved:
            achievement_text = f"{achievement.name} - 달성 시간: {achievement.achieved_time}"
            achievement_text_color = (0, 0, 255)  # 달성된 업적의 텍스트 색상 (파란색)

        else:
            achievement_text = f"{achievement.name}"
            achievement_text_color = achievement_window_text_color  # 달성되지 않은 업적의 텍스트 색상

        achievement_text_render = achievement_font.render(achievement_text, True, achievement_window_text_color)
        achievement_text_render_list.append(achievement_text_render)

    # 스크롤 기능
    achievement_window_surface = pygame.Surface((achievement_window_width, achievement_window_height))
    achievement_window_surface.fill(achievement_window_bg_color)
    text_y = achievement_window_padding - scroll_position
    for achievement_text_render in achievement_text_render_list:
        if text_y + achievement_text_render.get_height() > achievement_window_height:
            break
        if text_y > 0:
            achievement_window_surface.blit(achievement_text_render, (achievement_window_padding, text_y))
        text_y += achievement_text_render.get_height() + achievement_text_padding


    
    # 스크롤 한계 설정
    scroll_position_max = 0
    scroll_position_min = -(text_y - achievement_window_height)
    scroll_position_min -= 200  # 한계를 더욱 확장 (예: 50 픽셀)

    if scroll_position > scroll_position_max:
        scroll_position = scroll_position_max
    elif scroll_position < scroll_position_min:
        scroll_position = scroll_position_min
    
    for achievement_text_render in achievement_text_render_list:
        if text_y + achievement_text_render.get_height() > achievement_window_height:
            break
    if text_y > 0:
        achievement_window_surface.blit(achievement_text_render, (achievement_window_padding, text_y))
    text_y += achievement_text_render.get_height() + achievement_text_padding




    # 스크롤 바 그리기
    scrollbar_width = 10
    scrollbar_padding = 5
    scrollbar_color = (150, 150, 150)
    scrollbar_handle_color = (100, 100, 100)

    scrollbar_height = achievement_window_height * achievement_window_height / text_y
    scrollbar_y = scroll_position * (achievement_window_height - scrollbar_height) / (text_y - achievement_window_height)
    pygame.draw.rect(achievement_window_surface, scrollbar_color, (achievement_window_width - scrollbar_width - scrollbar_padding, 0, scrollbar_width, achievement_window_height))
    pygame.draw.rect(achievement_window_surface, scrollbar_handle_color, (achievement_window_width - scrollbar_width - scrollbar_padding, scrollbar_y, scrollbar_width, scrollbar_height))

    # 화면 업데이트
    screen.fill((0, 0, 0))  # 검은색 배경

    # 업적 창 그리기
    achievement_window_x = (screen_width - achievement_window_width) // 2
    achievement_window_y = (screen_height - achievement_window_height) // 2
    pygame.draw.rect(screen, achievement_window_border_color, (achievement_window_x, achievement_window_y, achievement_window_width, achievement_window_height))
    screen.blit(achievement_window_surface, (achievement_window_x + 2, achievement_window_y + 2))

    pygame.display.flip()

# 게임 종료
pygame.quit()

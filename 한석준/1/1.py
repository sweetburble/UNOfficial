import pygame

pygame.init()

# Pygame 창 생성
screen = pygame.display.set_mode((640, 480))

# 게임 맵 그리기
def draw_map():
    pygame.draw.rect(screen, (255, 255, 255), (100, 100, 200, 100))  # 지역 1
    pygame.draw.rect(screen, (255, 255, 255), (400, 300, 100, 100))  # 지역 2

# 이벤트 핸들러 함수
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 마우스 클릭한 지역이 어디인지 확인하는 코드 작성
            if 100 <= mouse_x <= 300 and 100 <= mouse_y <= 200:
                print("지역 1을 선택했습니다.")
            elif 400 <= mouse_x <= 500 and 300 <= mouse_y <= 400:
                print("지역 2를 선택했습니다.")
        elif event.type == pygame.KEYDOWN:
            # 키보드 이벤트 처리
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

# 게임 루프
while True:
    # 이벤트 처리
    handle_events()

    # 게임 맵 그리기
    draw_map()

    # 게임 화면 업데이트
    pygame.display.flip()

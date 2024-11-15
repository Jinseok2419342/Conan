import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
width, height = 1024, 950
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("벽돌깨기")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 행별 고정 색상 리스트
colors = [
    (255, 127, 80),  # 1번줄: 코랄
    (127, 255, 0),   # 2번줄: 차트리우스
    (0, 191, 255),   # 3번줄: 딥 스카이 블루
    (255, 215, 0),   # 4번줄: 골드
    (138, 43, 226)   # 5번줄: 블루바이올렛
]

# 공과 패들 설정
ball_speed = [6, 6]
ball = pygame.Rect(width // 2, height // 2, 20, 20)  # 공 크기
paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)

# 벽돌 설정
brick_width, brick_height = 79, 30
bricks = []
score_area_height = 50  # 점수 표시 영역 높이

# 점수 초기화
font = pygame.font.SysFont("malgungothic", 36)  # 시스템 기본 폰트로 설정
score = 0

# 시작 화면 함수
def show_start_screen():
    screen.fill(BLACK)
    title_font = pygame.font.SysFont("malgungothic", 50)
    button_font = pygame.font.SysFont("malgungothic", 30)

    # 제목 텍스트
    title_text = title_font.render("벽돌깨기 게임", True, WHITE)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))

    # 버튼
    button_rect = pygame.Rect(width // 2 - 100, height // 2, 200, 60)
    pygame.draw.rect(screen, RED, button_rect)
    button_text = button_font.render("게임 시작", True, WHITE)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    pygame.display.flip()

    # 버튼 클릭 대기
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # 버튼 클릭 감지
                    return

# 게임 초기화 함수
def reset_game():
    global ball, paddle, bricks, score, ball_speed
    ball = pygame.Rect(width // 2, height // 2, 20, 20)
    paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)

    bricks.clear()
    for row in range(5):
        color = colors[row % len(colors)]
        for col in range(12):
            # 벽돌 위치를 점수 영역 아래에 배치
            brick = pygame.Rect(10 + col * (brick_width + 5), score_area_height + 10 + row * (brick_height + 5), brick_width, brick_height)
            bricks.append((brick, color))

    score = 0
    ball_speed = [6, 6]

# 게임 오버 상태 처리 함수
def game_over():
    game_over_text = font.render("게임 오버", True, WHITE)
    restart_text = font.render("R 키를 눌러 재시작", True, WHITE)

    screen.fill(BLACK)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 10))
    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting_for_restart = False
                    return True
    return False

# 게임 승리 처리 함수
def game_win():
    win_text = font.render("축하합니다! 승리했습니다!", True, WHITE)
    screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# 게임 루프
show_start_screen()
while True:
    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-15, 0)
        if keys[pygame.K_RIGHT] and paddle.right < width:
            paddle.move_ip(15, 0)

        ball.move_ip(ball_speed)

        if ball.left <= 0 or ball.right >= width:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        for brick, color in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove((brick, color))
                score += 10
                if len(bricks) == 0:
                    game_win()
                break

        if ball.bottom >= height:
            if game_over():
                break

        if score % 100 == 0 and score > 0:
            ball_speed[0] += 1
            ball_speed[1] += 1

        screen.fill(BLACK)

        # 점수 텍스트 출력
        pygame.draw.rect(screen, BLACK, (0, 0, width, score_area_height))  # 점수 표시 영역 배경
        score_text = font.render(f"점수: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 공, 패들, 벽돌 그리기
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.rect(screen, WHITE, paddle)
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

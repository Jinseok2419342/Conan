import pygame
import sys

# 초기화
pygame.init()

# 화면 설정 (해상도 증가)
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("벽돌깨기")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
brick_width, brick_height = 79, 30  # 벽돌 크기 조정
bricks = []
for row in range(5):  # 벽돌 행 개수 1로 초기화
    color = colors[row % len(colors)]
    for col in range(12):  # 열 개수는 유지
        brick = pygame.Rect(10 + col * (brick_width + 5), 60 + row * (brick_height + 5), brick_width, brick_height)
        bricks.append((brick, color))

# 점수 초기화
score = 0
game_count = 0  # 게임 판 수 카운트
collision_count = 0  # 충돌 횟수 초기화
font = pygame.font.Font(None, 36)

# 공 속도 상한 설정
MAX_SPEED = 9  # 초기 속도 6의 1.5배

# 투명 블록 설정
score_bar_height = 60  # 점수 영역 + 흰 줄 아래 추가 높이
score_bar = pygame.Rect(0, 0, width, score_bar_height)

# 시간 계산 함수
def format_time(milliseconds):
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    hundredths = (milliseconds % 1000) // 10
    return f"{minutes:02}:{seconds:02}:{hundredths:02}"

# 텍스트를 가운데 정렬하는 함수
def draw_centered_text(text, y_offset, size=36):
    text_font = pygame.font.Font(None, size)
    text_surface = text_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# 시작 화면 함수
def show_start_screen():
    screen.fill(BLACK)
    draw_centered_text("Brick Breaker", -50, size=72)
    draw_centered_text("Press Space To Start", 10)
    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 스페이스바로 시작
                    waiting_for_start = False
                    return

# 게임 클리어 화면
def game_win(total_time, games):
    screen.fill(BLACK)
    draw_centered_text("GAME CLEAR", -100, size=72)
    draw_centered_text(f"Score: {score}", -30)
    draw_centered_text(f"Time: {format_time(total_time)}", 10)
    draw_centered_text(f"Games: {games}", 50)
    draw_centered_text("Press Space To Restart", 100)
    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_restart = False
                    return True  # 게임을 재시작
    return False

# 게임 오버 상태 처리 함수
def game_over():
    screen.fill(BLACK)
    draw_centered_text("Game Over", -50, size=72)
    draw_centered_text("Press Space To Restart", 10)
    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 스페이스바로 재시작
                    waiting_for_restart = False
                    return True
    return False

# 게임이 종료되고 다시 시작될 때마다 초기화
def reset_game():
    global ball, paddle, bricks, score, ball_speed, collision_count
    ball = pygame.Rect(width // 2, height // 2, 20, 20)
    paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)
    bricks = []
    for row in range(5):
        color = colors[row % len(colors)]
        for col in range(12):
            brick = pygame.Rect(10 + col * (brick_width + 5), 60 + row * (brick_height + 5), brick_width, brick_height)
            bricks.append((brick, color))
    score = 0
    collision_count = 0
    ball_speed = [6, 6]

# 초기화
paused = False  # 일시정지 상태 변수 추가

# 메인 게임 루프
first_game = True  # 처음 실행 여부 확인 변수
while True:
    if first_game:  # 첫 번째 게임 시작 전만 "시작 화면" 표시
        show_start_screen()
        first_game = False
    else:
        if not game_over():
            pygame.quit()
            sys.exit()

    game_count += 1
    reset_game()
    play_time_start = pygame.time.get_ticks()  # 시간 초기화

    # 게임 루프
    while True:
        # 게임 경과 시간 계산 (초기화된 시간 기준)
        current_time = pygame.time.get_ticks() - play_time_start

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC 키로 일시정지 토글
                    paused = not paused

        # 일시정지 상태 처리
        if paused:
            screen.fill(BLACK)
            draw_centered_text("PAUSED", -50, size=72)
            draw_centered_text("Press ESC to Resume", 10)
            pygame.display.flip()
            pygame.time.Clock().tick(10)
            continue

        # 키 입력 처리
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
            ball.top = paddle.top - ball.height
            ball_speed[1] = -abs(ball_speed[1])  # Y축 속도 반전만 하고, X축 속도는 그대로 유지
            diff = ball.centerx - paddle.centerx
            ball_speed[0] += diff // 10

        if ball.colliderect(score_bar):
            ball_speed[1] = -ball_speed[1]

        for brick, color in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove((brick, color))
                score += 10
                collision_count += 1
                if collision_count % 10 == 0:
                    ball_speed[0] += 1 if ball_speed[0] > 0 else -1
                    ball_speed[1] += 1 if ball_speed[1] > 0 else -1
                if len(bricks) == 0:  # 벽돌이 모두 제거되었을 때
                    if game_win(current_time, game_count):  # 클리어 후 재시작
                        reset_game()  # 벽돌 및 게임 상태 초기화
                        game_count = 0  # 게임 판 수 초기화
                        play_time_start = pygame.time.get_ticks()  # 시간 초기화
                        break
                    else:
                        pygame.quit()
                        sys.exit()

        if ball.bottom >= height:  # 공이 바닥에 닿았을 때
            reset_game()
            play_time_start = pygame.time.get_ticks()  # 시간 초기화
            break

        if abs(ball_speed[0]) > MAX_SPEED:
            ball_speed[0] = MAX_SPEED if ball_speed[0] > 0 else -MAX_SPEED
        if abs(ball_speed[1]) > MAX_SPEED:
            ball_speed[1] = MAX_SPEED if ball_speed[1] > 0 else -MAX_SPEED

        screen.fill(BLACK)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.rect(screen, WHITE, paddle)

        pygame.draw.line(screen, WHITE, (0, score_bar_height - 20), (width, score_bar_height - 20), 2)

        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        game_count_text = font.render(f"Games: {game_count}", True, WHITE)
        screen.blit(game_count_text, (width - 150, 10))

        # 시간 텍스트 수정 (게임 중 "TIME:" 제거)
        time_text = font.render(format_time(current_time), True, WHITE)
        screen.blit(time_text, (width // 2 - 50, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

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
for row in range(5):  # 벽돌 행 개수를 5로 증가
    color = colors[row % len(colors)]
    for col in range(12):  # 열 개수는 유지
        brick = pygame.Rect(10 + col * (brick_width + 5), 60 + row * (brick_height + 5), brick_width, brick_height)
        bricks.append((brick, color))

# 점수 초기화
score = 0
collision_count = 0  # 충돌 횟수 초기화
font = pygame.font.Font(None, 36)

# 공 속도 상한 설정
MAX_SPEED = 9  # 초기 속도 6의 1.5배

# 투명 블록 설정
score_bar_height = 60  # 점수 영역 + 흰 줄 아래 추가 높이
score_bar = pygame.Rect(0, 0, width, score_bar_height)

# 패들 쿨다운 타이머 설정 (단위: ms)
paddle_cooldown_timer = 0
PADDLE_COOLDOWN_DURATION = 200  # 0.2초

# 텍스트를 가운데 정렬하는 함수
def draw_centered_text(text, y_offset):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# 시작 화면 함수
def show_start_screen():
    screen.fill(BLACK)
    draw_centered_text("Brick Breaker", -50)
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

# 게임 오버 상태 처리 함수
def game_over():
    screen.fill(BLACK)
    draw_centered_text("Game Over", -50)
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

# 게임 초기화 함수
def reset_game():
    global ball, paddle, bricks, score, ball_speed, collision_count, paddle_cooldown_timer
    # 공과 패들 초기화
    ball = pygame.Rect(width // 2, height // 2, 20, 20)
    paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)
    
    # 벽돌 초기화
    bricks = []
    for row in range(5):  # 벽돌 행 개수를 5로 증가
        color = colors[row % len(colors)]
        for col in range(12):
            brick = pygame.Rect(10 + col * (brick_width + 5), 60 + row * (brick_height + 5), brick_width, brick_height)
            bricks.append((brick, color))
    
    # 점수 및 공 속도 초기화
    score = 0
    collision_count = 0  # 충돌 횟수 초기화
    ball_speed = [6, 6]
    paddle_cooldown_timer = 0  # 쿨다운 초기화

# 메인 게임 루프
first_game = True  # 처음 실행 여부 확인 변수

while True:
    if first_game:  # 첫 번째 게임 시작 전만 "시작 화면" 표시
        show_start_screen()
        first_game = False
    else:  # 이후에는 게임 오버 후 바로 재시작
        if not game_over():
            pygame.quit()
            sys.exit()

    reset_game()  # 게임 초기화

    # 게임 루프
    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 키 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-15, 0)
        if keys[pygame.K_RIGHT] and paddle.right < width:
            paddle.move_ip(15, 0)

        # 공 이동
        ball.move_ip(ball_speed)

        # 벽에 부딪히면 반사
        if ball.left <= 0 or ball.right >= width:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        # 패들과 충돌
        if paddle_cooldown_timer <= 0:  # 쿨다운이 비활성화 상태일 때만 충돌 처리
            if ball.colliderect(paddle):
                ball_speed[1] = -ball_speed[1]  # Y축 방향 반전
                if ball.centerx < paddle.left:  # 패들의 왼쪽에 닿았을 경우
                    ball_speed[0] = -abs(ball_speed[0])  # X축 방향 왼쪽으로 반전
                elif ball.centerx > paddle.right:  # 패들의 오른쪽에 닿았을 경우
                    ball_speed[0] = abs(ball_speed[0])  # X축 방향 오른쪽으로 반전
                paddle_cooldown_timer = PADDLE_COOLDOWN_DURATION  # 쿨다운 시작

        # 쿨다운 타이머 업데이트
        if paddle_cooldown_timer > 0:
            paddle_cooldown_timer -= pygame.time.Clock().get_time()  # 프레임 시간에 따라 감소

        # 투명 블록과 충돌 처리 (공의 속도와 점수 변화 없음)
        if ball.colliderect(score_bar):
            ball_speed[1] = -ball_speed[1]

        # 벽돌과 충돌
        for brick, color in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove((brick, color))
                score += 10
                collision_count += 1  # 충돌 횟수 증가
                if collision_count % 10 == 0:  # 10번 충돌마다 속도 증가
                    ball_speed[0] += 1 if ball_speed[0] > 0 else -1
                    ball_speed[1] += 1 if ball_speed[1] > 0 else -1
                if len(bricks) == 0:  # 벽돌이 모두 깨지면 승리 처리
                    game_win()
                break

        # 공이 바닥에 닿으면 게임 오버
        if ball.bottom >= height:
            break  # 게임 오버 시 루프 종료

        # 공 속도 제한
        if abs(ball_speed[0]) > MAX_SPEED:
            ball_speed[0] = MAX_SPEED if ball_speed[0] > 0 else -MAX_SPEED
        if abs(ball_speed[1]) > MAX_SPEED:
            ball_speed[1] = MAX_SPEED if ball_speed[1] > 0 else -MAX_SPEED

        # 화면 그리기
        screen.fill(BLACK)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.rect(screen, WHITE, paddle)

        # 점수 아래 흰 줄 그리기
        pygame.draw.line(screen, WHITE, (0, score_bar_height - 20), (width, score_bar_height - 20), 2)

        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # 점수 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        pygame.time.Clock().tick(60)

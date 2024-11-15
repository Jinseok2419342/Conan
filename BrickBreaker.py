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
brick_width, brick_height = 79, 30  # 벽돌 크기 조정
bricks = []
for row in range(5):  # 벽돌 행 개수 증가
    color = colors[row % len(colors)]
    for col in range(12):  # 열 개수 증가
        brick = pygame.Rect(10 + col * (brick_width + 5), 10 + row * (brick_height + 5), brick_width, brick_height)
        bricks.append((brick, color))

# 점수 초기화
score = 0
font = pygame.font.Font(None, 36)

# 게임 오버 상태 처리 함수
def game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Press 'R' to Restart", True, WHITE)
    
    # 게임 오버 화면 그리기
    screen.fill(BLACK)
    screen.blit(game_over_text, (width // 2 - 100, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - 150, height // 2 + 10))
    pygame.display.flip()

    # 'R' 키를 눌러서 게임을 다시 시작
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 'R' 키가 눌리면 게임 재시작
                    waiting_for_restart = False
                    return True  # 게임을 재시작하려면 True 반환
    return False

# 게임 승리 처리 함수
def game_win():
    win_text = font.render("You Win!", True, WHITE)
    screen.blit(win_text, (width // 2 - 100, height // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# 게임 초기화 함수
def reset_game():
    global ball, paddle, bricks, score, ball_speed
    # 공과 패들 초기화
    ball = pygame.Rect(width // 2, height // 2, 20, 20)
    paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)
    
    # 벽돌 초기화
    bricks = []
    for row in range(5):
        color = colors[row % len(colors)]
        for col in range(12):
            brick = pygame.Rect(10 + col * (brick_width + 5), 10 + row * (brick_height + 5), brick_width, brick_height)
            bricks.append((brick, color))
    
    # 점수 및 공 속도 초기화
    score = 0
    ball_speed = [6, 6]

# 게임 루프
while True:
    reset_game()  # 게임 시작 시 초기화

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
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # 벽돌과 충돌
        for brick, color in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove((brick, color))
                score += 10
                if len(bricks) == 0:  # 벽돌이 모두 깨지면 승리 처리
                    game_win()
                break

        # 공이 바닥에 닿으면 게임 오버
        if ball.bottom >= height:
            if game_over():  # 게임 오버 후 'R' 키로 다시 시작
                break

        # 공 속도 증가 (점수에 비례해서 속도 조정)
        if score % 100 == 0 and score > 0:
            ball_speed[0] += 1
            ball_speed[1] += 1

        # 화면 그리기
        screen.fill(BLACK)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.rect(screen, WHITE, paddle)
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # 점수 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        pygame.time.Clock().tick(60)

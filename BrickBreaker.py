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
ball = pygame.Rect(width // 2, height // 2, 20, 20) # 공 크기
paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)

# 벽돌 설정
brick_width, brick_height = 50, 20
bricks = []
for row in range(3):
    color = colors[row]  # 각 행에 지정된 색상 적용
    for col in range(7):
        # 벽돌 생성 및 색상 저장
        brick = pygame.Rect(10 + col * (brick_width + 5), 10 + row * (brick_height + 5), brick_width, brick_height)
        bricks.append((brick, color))

# 점수 초기화
score = 0
font = pygame.font.Font(None, 36)

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
            break
    
    # 공이 바닥에 닿으면 게임 오버
    if ball.bottom >= height:
        pygame.quit()
        sys.exit()

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

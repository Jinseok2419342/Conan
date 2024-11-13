import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("벽돌깨기")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 공과 패들 설정
ball_speed = [3, 3]
ball = pygame.Rect(width // 2, height // 2, 10, 10)
paddle = pygame.Rect(width // 2 - 30, height - 20, 60, 10)

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
        paddle.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and paddle.right < width:
        paddle.move_ip(5, 0)

    # 공 이동
    ball.move_ip(ball_speed)
    
    # 벽에 부딪히면 반사
    if ball.left <= 0 or ball.right >= width:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0 or ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
    
    # 공이 바닥에 닿으면 게임 오버
    if ball.bottom >= height:
        pygame.quit()
        sys.exit()

    # 화면 그리기
    screen.fill(BLACK)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.display.flip()
    
    # 프레임 조절
    pygame.time.Clock().tick(60)

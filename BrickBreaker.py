import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
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

paused_start_time = 0  # 일시정지 시작 시간을 기록
paused_total_time = 0  # 일시정지 중 누적된 시간

# 공과 패들 설정
initial_ball_speed = [6, 6]  # 공의 초기 속도
ball_speed = initial_ball_speed.copy()  # 공 속도 복사하여 사용
ball = pygame.Rect(width // 2, height // 2, 20, 20)  # 공 크기
paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)

# 벽돌 설정
brick_width, brick_height = 79, 30  # 벽돌 크기 조정
bricks = []
for row in range(5):  # 벽돌 행 개수
    color = colors[row % len(colors)]
    for col in range(12):  # 열 개수
        brick = pygame.Rect(10 + col * (brick_width + 5), 60 + row * (brick_height + 5), brick_width, brick_height)
        bricks.append((brick, color))

# 점수 초기화
score = 0
collision_count = 0  # 충돌 횟수 초기화
font = pygame.font.Font(None, 36)

# 공 속도 상한 설정
MAX_SPEED = 6  # 공 속도를 일정하게 유지하도록 상한 설정

# 투명 블록 설정
score_bar_height = 60  # 점수 영역 + 흰 줄 아래 추가 높이
score_bar = pygame.Rect(0, 0, width, score_bar_height)
score_bar_bumped = False

# 아이템 클래스
class Item:
    def __init__(self, x, y, item_type):
        self.rect = pygame.Rect(x, y, 20, 20)  # 아이템 크기 (20x20)
        self.type = item_type  # 아이템 타입 (1: 패들 크기 증가, 2: 공 개수 증가)
        self.color = (255, 255, 0)  # 아이템 기본 색상 (노란색)

    def draw(self, screen):
        if self.type == 1:  # 패들 크기 증가 아이템은 패들 모양으로 그리기
            pygame.draw.rect(screen, self.color, self.rect)
        elif self.type == 2:  # 공 개수 증가 아이템은 공 모양으로 그리기
            pygame.draw.ellipse(screen, self.color, self.rect)

    def update(self):
        # 아이템을 아래로 떨어지게 설정
        self.rect.y += 5

# 패들 크기 증가 아이템
def increase_paddle_size():
    paddle.width += 40  # 패들 크기를 40px 증가

# 공의 갯수 증가 아이템
def add_extra_ball():
    # 새로운 공을 패들의 위치에서 시작하게 설정
    new_ball = pygame.Rect(paddle.centerx - 10, paddle.top - 20, 20, 20)  # 패들 중심에서 위로 20px 떨어진 위치
    new_ball_speed = initial_ball_speed.copy()  # 초기 공 속도 복사
    new_ball_speed[0] = -new_ball_speed[0]  # x축 속도를 반대로 설정
    return new_ball, new_ball_speed

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
    global paused_total_time, paused_start_time
    paused_total_time = 0
    paused_start_time = 0

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
    global paused_total_time, paused_start_time
    paused_total_time = 0
    paused_start_time = 0

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
    global ball, paddle, bricks, score, ball_speed, collision_count, items, ball_list, game_count, paused_total_time, score_bar_bumped
    ball = pygame.Rect(width // 2, height // 2, 20, 20)
    paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)
    bricks = []
    items = []  # 아이템 리스트 초기화
    ball_list = [(ball, initial_ball_speed.copy())]  # 공 리스트 초기화, 속도 초기화
    for row in range(5):
        color = colors[row % len(colors)]
        for col in range(12):
            brick = pygame.Rect(10 + col * (brick_width + 5), 60 + row * (brick_height + 5), brick_width, brick_height)
            bricks.append((brick, color))
    score = 0
    collision_count = 0
    ball_speed = initial_ball_speed.copy()  # 공 속도 초기화
    paused_total_time = 0  # 누적 일시정지 시간 초기화
    game_count += 1  # 게임 횟수 증가
    score_bar_bumped = False

# 초기화
paused = False  # 일시정지 상태 변수 추가
game_count = 0  # 게임 횟수 초기화

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

    reset_game()
    play_time_start = pygame.time.get_ticks()  # 시간 초기화

    # 게임 루프
    while True:
        current_time = pygame.time.get_ticks() - play_time_start - paused_total_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC 키로 일시정지 토글
                    paused = not paused
                    if paused:
                        paused_start_time = pygame.time.get_ticks()  # 일시정지 시작 시간 기록
                    else:
                        if paused_start_time != 0:  # 일시정지 시작이 기록된 경우만 처리
                            paused_total_time += pygame.time.get_ticks() - paused_start_time
                            paused_start_time = 0

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

        # 공 이동 및 처리
        for ball, ball_speed in ball_list[:]:
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
                if score_bar_bumped == False:
                    score_bar_bumped = True
                    ball_speed[1] = -ball_speed[1]
                score_bar_bumped = False

            for brick, color in bricks[:]:
                if ball.colliderect(brick):
                    ball_speed[1] = -ball_speed[1]
                    bricks.remove((brick, color))
                    score += 10
                    collision_count += 1

                    # 일정 확률로 아이템 생성
                    if random.random() < 0.3:  # 30% 확률로 아이템 생성
                        item_type = random.choice([1, 2])  # 1: 패들 크기 증가, 2: 공 개수 증가
                        item = Item(brick.centerx - 10, brick.centery, item_type)
                        items.append(item)

                    if len(bricks) == 0:  # 벽돌이 모두 제거되었을 때
                        if game_win(current_time, game_count):
                            reset_game()
                            play_time_start = pygame.time.get_ticks()
                            break
                        else:
                            pygame.quit()
                            sys.exit()

        # 아이템 업데이트 및 처리
        for item in items[:]:
            item.update()
            if item.rect.colliderect(paddle):
                if item.type == 1:  # 패들 크기 증가
                    increase_paddle_size()
                elif item.type == 2:  # 공 개수 증가
                    new_ball, new_ball_speed = add_extra_ball()
                    ball_list.append((new_ball, new_ball_speed))

                items.remove(item)

        # 공이 바닥에 닿았을 때
        for ball, ball_speed in ball_list[:]:
            if ball.bottom >= height:
                ball_list.remove((ball, ball_speed))
                if len(ball_list) == 0:
                    if game_over():
                        reset_game()
                        play_time_start = pygame.time.get_ticks()
                    break

        # 화면 그리기
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)

        # 벽돌 그리기
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # 아이템 그리기
        for item in items:
            item.draw(screen)

        # 공 그리기
        for ball, _ in ball_list:
            pygame.draw.ellipse(screen, WHITE, ball)

        # 점수와 게임 시간 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        game_count_text = font.render(f"Game {game_count}", True, WHITE)  # 게임 번호 표시
        screen.blit(game_count_text, (width - 150, 10))

        time_text = font.render(format_time(current_time), True, WHITE)
        screen.blit(time_text, (width // 2 - 50, 10))

        # 시간 밑에 구분선 추가
        pygame.draw.line(screen, WHITE, (0, 50), (width, 50), 2)  # 선을 추가합니다.

        pygame.display.flip()
        pygame.time.Clock().tick(60)

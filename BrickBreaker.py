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

# 이미지 로드 및 투명도 설정
background_image = pygame.image.load("background_image.jpeg").convert_alpha()  # 알파 채널 포함하여 로드
background_image = pygame.transform.scale(background_image, (width, height))  # 화면 크기에 맞게 조정
background_image.set_alpha(100)  # 투명도 설정 (0~255, 128은 50% 투명)

start_screen_image = pygame.image.load("start_screen.jpg").convert()
start_screen_image = pygame.transform.scale(start_screen_image, (width, height))

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

# 파괴 불가능한 벽돌 리스트
unbreakable_bricks = []


# 점수 초기화
score = 0
collision_count = 0  # 충돌 횟수 초기화
font = pygame.font.Font(None, 36)

# 공 속도 상한 설정
MAX_SPEED = 6  # 공 속도를 일정하게 유지하도록 상한 설정

# 투명 블록 설정
score_bar_height = 60  # 점수 영역 + 흰 줄 아래 추가 높이
score_bar = pygame.Rect(0, 0, width, score_bar_height)

# 충돌 체크 함수
def check_collision_with_bricks_and_items(new_rect, bricks, items, unbreakable_bricks):
    # 벽돌들 및 아이템들과 겹치는지 확인
    for brick, _ in bricks:
        if new_rect.colliderect(brick):
            return True  # 겹치면 True 반환
    for item in items:
        if new_rect.colliderect(item.rect):
            return True  # 겹치면 True 반환
    for unbreakable_brick in unbreakable_bricks:
        if new_rect.colliderect(unbreakable_brick):
            return True  # 겹치면 True 반환
    return False  # 겹치지 않으면 False 반환



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


# 파괴 불가능한 벽돌 생성 아이템 클래스
class UnbreakableItem:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  # 아이템 크기 (20x20)
        self.color = (169, 169, 169)  # 회색 (Dark Gray)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # 회색으로 표시

    def update(self):
        # 아이템을 아래로 떨어지게 설정
        self.rect.y += 5

# 파괴 불가능한 벽돌을 생성하는 함수 수정
def generate_unbreakable_brick():
    # 아이템 위치가 벽돌들과 겹치지 않도록 확인하는 함수
    while True:
        brick_x = random.randint(0, width - brick_width)
        brick_y = random.randint(score_bar_height + 10, height // 2)
        new_unbreakable_brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        
        # 새 아이템이 기존의 벽돌들과 겹치는지 확인
        collision = False
        for brick, _ in bricks:  # 기존 벽돌들과 겹치는지 확인
            if new_unbreakable_brick.colliderect(brick):
                collision = True
                break
        if not collision:
            return new_unbreakable_brick  # 겹치지 않으면 아이템 반환
        
# 패들 크기 증가 아이템
def increase_paddle_size():
    paddle.width += 40  # 패들 크기를 40px 증가

# 공의 갯수 증가 아이템
def add_extra_ball():
    new_ball = pygame.Rect(width // 2, height // 2, 20, 20)
    new_ball_speed = initial_ball_speed.copy()  # 새로운 공은 초기 공 속도를 그대로 적용
    return new_ball, new_ball_speed

# 시간 계산 함수
def format_time(milliseconds):
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    hundredths = (milliseconds % 1000) // 10
    return f"{minutes:02}:{seconds:02}:{hundredths:02}"

# 텍스트를 가운데 정렬하는 함수
def draw_centered_text(text, y_offset, size=36, color=WHITE):
    text_font = pygame.font.Font(None, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# 시작 화면 함수
def show_start_screen():
    screen.blit(start_screen_image, (0, 0))  # 시작 화면에 이미지 추가
    # draw_centered_text("Brick Breaker", -50, size=72)
    draw_centered_text("Press Space To Start", 10, color=(153, 255, 255), size=50)
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
    global paused_total_time, paused_start_time, game_count
    paused_total_time = 0
    paused_start_time = 0
    game_count = 0  # 게임 클리어 시 게임 횟수 초기화

    # Game Clear 화면 이미지 로드
    game_vict_image = pygame.image.load("game_vict.jpg").convert()
    game_vict_image = pygame.transform.scale(game_vict_image, (width, height))

    screen.blit(game_vict_image, (0, 0))  # Game Clear 이미지 표시
    draw_centered_text("GAME CLEAR", -100, size=72, color=(0, 51, 102))
    draw_centered_text(f"Score: {score}", -30, color=(0, 51, 102))
    draw_centered_text(f"Time: {format_time(total_time)}", 10, color=(0, 51, 102))
    draw_centered_text(f"Games: {games}", 50, color=(0, 51, 102))
    draw_centered_text("Press Space To Restart", 100, color=(0, 51, 102))
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

    # Game Over 화면 이미지 로드
    game_over_image = pygame.image.load("Game_Over.jpg").convert()
    game_over_image = pygame.transform.scale(game_over_image, (width, height))

    screen.blit(game_over_image, (0, 0))  # Game Over 이미지 표시
    # draw_centered_text("Press Space To Restart", 10)
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
    global ball, paddle, bricks, score, ball_speed, collision_count, items, ball_list, game_count, paused_total_time, unbreakable_bricks
    ball = pygame.Rect(width // 2, height // 2, 20, 20)
    paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)
    bricks = []
    items = []  # 아이템 리스트 초기화
    ball_list = [(ball, initial_ball_speed.copy())]  # 공 리스트 초기화, 속도 초기화
    unbreakable_bricks = []  # 파괴 불가능한 벽돌 초기화
    
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
                if event.key in [pygame.K_ESCAPE, pygame.K_SPACE]:  # ESC 또는 SPACE로 일시정지/해제
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
            draw_centered_text("Press ESC or SPACE to Resume", 10)
            pygame.display.flip()
            pygame.time.Clock().tick(10)
            continue

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle.left > 0:
            paddle.move_ip(-15, 0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle.right < width:
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
            
            # 투명 블록(score_bar)과 충돌 처리
            if ball.colliderect(score_bar):
                ball.top = score_bar.bottom  # 투명 블록 아래로 이동
                ball_speed[1] = -ball_speed[1]  # Y축 속도 반전
                    
            # 파괴 불가능한 벽돌과 충돌 처리
            for unbreakable_brick in unbreakable_bricks:
                if ball.colliderect(unbreakable_brick):
                    # 공이 벽돌에 맞으면 튕기도록 반사
                    if ball.centerx < unbreakable_brick.left or ball.centerx > unbreakable_brick.right:
                        ball_speed[0] = -ball_speed[0]  # X축 반사
                    else:
                        ball_speed[1] = -ball_speed[1]  # Y축 반사
                    break  # 한 번 충돌하면 다른 벽돌은 검사하지 않음

            for brick, color in bricks[:]:
                if ball.colliderect(brick):
                    ball_speed[1] = -ball_speed[1]
                    bricks.remove((brick, color))
                    score += 10
                    collision_count += 1

                    # 일정 확률로 아이템 생성
                    if random.random() < 0.8:  # 30% 확률로 아이템 생성
                        item_type = random.choice([1, 2, 3])  # 1: 패들 크기 증가, 2: 공 개수 증가, 3: 절대 안 깨지는 벽돌 생성
                        if item_type == 3:  # 절대 안 깨지는 벽돌 생성 아이템
                            item = UnbreakableItem(brick.centerx - 10, brick.centery)
                        else:
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

       # 아이템 처리 및 생성 부분 수정
        for item in items[:]:
            item.update()
            if item.rect.colliderect(paddle):
                if isinstance(item, UnbreakableItem):  # 파괴 불가능한 벽돌 생성
                    # 새로운 위치를 찾기 위한 루프
                    while True:
                        brick_x = random.randint(0, width - brick_width)
                        brick_y = random.randint(score_bar_height + 10, height // 2)
                        new_unbreakable_brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)

                        # 겹치지 않는 위치인지 확인
                        if not check_collision_with_bricks_and_items(new_unbreakable_brick, bricks, items, unbreakable_bricks):
                            unbreakable_bricks.append(new_unbreakable_brick)
                            break  # 겹치지 않으면 아이템 추가 후 종료
                elif item.type == 1:  # 패들 크기 증가
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
        # 배경 이미지를 투명하게 화면에 그리기
        screen.fill(BLACK)  # 투명 이미지 아래 기본 배경색 설정
        screen.blit(background_image, (0, 0))  # 투명도가 적용된 배경 이미지 그리기
        
        pygame.draw.rect(screen, WHITE, paddle)

        # 벽돌 그리기
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # 파괴 불가능한 벽돌 그리기 (회색)
        for unbreakable_brick in unbreakable_bricks:
            pygame.draw.rect(screen, (128, 128, 128), unbreakable_brick)  # RGB 값: 회색


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
        pygame.time.Clock().tick(120)

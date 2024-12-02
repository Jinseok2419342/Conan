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
    (138, 43, 226),  # 5번줄: 블루바이올렛
    (255, 105, 180), # 6번줄: 핫핑크
    (0, 255, 127)    # 7번줄: 스프링 그린
]

paused_start_time = 0  # 일시정지 시작 시간을 기록
paused_total_time = 0  # 일시정지 중 누적된 시간

# 이미지 로드 및 투명도 설정
background_image = pygame.image.load("background_image.jpeg").convert_alpha()  # 알파 채널 포함하여 로드
background_image = pygame.transform.scale(background_image, (width, height))  # 화면 크기에 맞게 조정
background_image.set_alpha(100)  # 투명도 설정 (0~255, 128은 50% 투명)

start_screen_image = pygame.image.load("start_screen.jpg").convert()
start_screen_image = pygame.transform.scale(start_screen_image, (width, height))

# 추가된 이미지 로드
paused_image = pygame.image.load("paused.jpg").convert()
paused_image = pygame.transform.scale(paused_image, (width, height))

stage_cleared_image = pygame.image.load("stage_cleared.jpg").convert()
stage_cleared_image = pygame.transform.scale(stage_cleared_image, (width, height))

# 효과음 로드
paddle_hit_sound = pygame.mixer.Sound("paddle_sound.mp3")
brick_hit_sound = pygame.mixer.Sound("brick_sound.mp3")

# 공과 패들 설정
initial_ball_speed = [6, -6]  # 공의 초기 속도를 조금 빠르게 설정
ball_speed = initial_ball_speed.copy()  # 공 속도 복사하여 사용
ball = pygame.Rect(width // 2, height // 2, 20, 20)  # 공 크기
paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)
default_paddle_speed = 15  # 패들 기본 속도

def initialize_ball():
    global ball_speed
    ball = pygame.Rect(width // 2, height // 2, 20, 20)  # 공의 위치는 화면 중앙
    # x축 방향에 랜덤성을 부여
    x_direction = random.choice([-1 ,1])  # x축 방향을 왼쪽(-) 또는 오른쪽(+)으로 설정
    ball_speed = [initial_ball_speed[0] * x_direction, initial_ball_speed[1]]  # x축은 랜덤, y축 속도는 고정된 값
    return ball


# 벽돌 클래스 정의
class Brick:
    def __init__(self, rect, color, hits_required=1):
        self.rect = rect
        self.color = color  # 벽돌의 색상을 저장
        self.hits_required = hits_required
        self.hits_remaining = hits_required

# 벽돌 설정
brick_width, brick_height = 79, 30  # 벽돌 크기 조정
bricks = []

# 파괴 불가능한 벽돌 리스트
unbreakable_bricks = []

# 점수 초기화
score = 0
collision_count = 0  # 충돌 횟수 초기화
font = pygame.font.Font(None, 36)

# 게임 단계 설정
current_stage = 1

n = 5  # base_ball_speed

# 각 스테이지별 설정
stages = [
    {
        'stage_number': 1,
        'max_ball_speed': n,
        'item_probability': 0.5,
        'multi_hit_bricks': [],
        'paddle_speed_multiplier': 1.0,
        'ball_speed_multiplier': 1.0,
        'brick_rows': 5,
        'new_brick_interval': None,
        'new_brick_type': None,
        'new_brick_count': None,
    },
    {
        'stage_number': 2,
        'max_ball_speed': n,
        'item_probability': 0.45,
        'multi_hit_bricks': [(12, 2)],
        'paddle_speed_multiplier': 1.0,
        'ball_speed_multiplier':1.0,
        'brick_rows':5,
        'new_brick_interval': None,
        'new_brick_type': None,
        'new_brick_count': None,
    },
    {
        'stage_number':3,
        'max_ball_speed':n,
        'item_probability':0.4,
        'multi_hit_bricks':[(16,2)],
        'paddle_speed_multiplier':1.0,
        'ball_speed_multiplier':1.0,
        'brick_rows':5,
        'new_brick_interval': None,
        'new_brick_type': None,
        'new_brick_count': None,
    },
    {
        'stage_number':4,
        'max_ball_speed': n * 1.15,  # Increase max speed by 15%
        'item_probability':0.37,
        'multi_hit_bricks':[(20,2)],
        'paddle_speed_multiplier':1.0,
        'ball_speed_multiplier':1.0,
        'brick_rows':5,
        'new_brick_interval': None,
        'new_brick_type': None,
        'new_brick_count': None,
    },
    {
        'stage_number':5,
        'max_ball_speed': n * 1.15,
        'item_probability':0.37,  # Assuming same as previous
        'multi_hit_bricks':[(10,3),(10,2)],
        'paddle_speed_multiplier':1.0,
        'ball_speed_multiplier':1.0,
        'brick_rows':5,
        'new_brick_interval': None,
        'new_brick_type': None,
        'new_brick_count': None,
    },
    {
        'stage_number':6,
        'max_ball_speed': (n * 1.15) * 1.10,  # Increase by 10% over stage 4
        'item_probability':0.34,
        'multi_hit_bricks':[(20,3)],
        'paddle_speed_multiplier':1.10,  # 10% faster than previous stages
        'ball_speed_multiplier':1.0,
        'brick_rows':6,
        'new_brick_interval': None,
        'new_brick_type': None,
        'new_brick_count': None,
    },
    {
        'stage_number':7,
        'max_ball_speed': (n * 1.15) * 1.10,
        'item_probability':0.34,
        'multi_hit_bricks':[(20,3)],
        'paddle_speed_multiplier':1.10,
        'ball_speed_multiplier':1.0,
        'brick_rows':6,
        'new_brick_interval':15,
        'new_brick_type':1,
        'new_brick_count':1,
    },
    {
        'stage_number':8,
        'max_ball_speed': ((n * 1.15) * 1.10) * 1.05,  # Increase by 5% over stage 6
        'item_probability':0.30,
        'multi_hit_bricks':[(23,3)],
        'paddle_speed_multiplier':1.10 * 1.06,  # 6% increase over stage 6
        'ball_speed_multiplier':1.0,
        'brick_rows':6,
        'new_brick_interval':13,
        'new_brick_type':1,
        'new_brick_count':1,
    },
    {
        'stage_number':9,
        'max_ball_speed': ((n * 1.15) * 1.10) * 1.05,
        'item_probability':0.25,
        'multi_hit_bricks':[(20,3)],
        'paddle_speed_multiplier':1.10 * 1.06,
        'ball_speed_multiplier':1.0,
        'brick_rows':6,
        'new_brick_interval':21,
        'new_brick_type':2,
        'new_brick_count':1,
    },
    {
        'stage_number':10,
        'max_ball_speed': (((n * 1.15) * 1.10) * 1.05) * 1.03,  # 3% increase over stage 8
        'item_probability':0.15,
        'multi_hit_bricks':[(25,3)],
        'paddle_speed_multiplier':1.10 * 1.06 * 1.03,  # 3% increase over stage 8
        'ball_speed_multiplier':1.0,
        'brick_rows':7,
        'new_brick_interval':35,
        'new_brick_type':2,
        'new_brick_count':2,
    }
]

# 투명 블록 설정
score_bar_height = 60  # 점수 영역 + 흰 줄 아래 추가 높이
score_bar = pygame.Rect(0, 0, width, score_bar_height)

# 아이템 등장 확률
item_probability = 0.5  # 초기값 (스테이지 1)

# 충돌 체크 함수
def check_collision_with_bricks_and_items(new_rect, bricks, items, unbreakable_bricks):
    # 벽돌들 및 아이템들과 겹치는지 확인
    for brick in bricks:
        if new_rect.colliderect(brick.rect):
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

# 패들 크기 증가 아이템
def increase_paddle_size():
    paddle.width += 40  # 패들 크기를 40px 증가

# 공의 갯수 증가 아이템
def add_extra_ball():
    # 새로운 공을 패들의 중심 바로 위에 생성
    new_ball = pygame.Rect(paddle.centerx - 10, paddle.top - 20, 20, 20)
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

# 게임 클리어 텍스트를 가운데 정렬하는 함수
def draw_centered_over_text(text, y_offset, size=50, color=None, bg_color=None, border_radius=20):
    text_font = pygame.font.Font(None, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + y_offset))
    
    if bg_color:  # 배경 색상이 지정되었을 경우
        padding = 20  # 여백 크기를 확대
        bg_rect = text_rect.inflate(padding * 1.5, padding * 1.5)  # 여백만큼 사각형 크기 확장
        pygame.draw.rect(screen, bg_color, bg_rect, border_radius=border_radius)  # 둥근 모서리 사각형 그리기
        
    screen.blit(text_surface, text_rect)  # 텍스트 그리기
    
# 텍스트를 가운데 정렬하는 함수
def draw_centered_text(text, y_offset, size=50, color=(255, 255, 255), bg_color=None, border_radius=20):
    text_font = pygame.font.Font(None, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + y_offset))
    
    if bg_color:  # 배경 색상이 지정되었을 경우
        padding = 20  # 여백 크기를 확대
        bg_rect = text_rect.inflate(padding * 2, padding * 2)  # 여백만큼 사각형 크기 확장
        pygame.draw.rect(screen, bg_color, bg_rect, border_radius=border_radius)  # 둥근 모서리 사각형 그리기
    
    screen.blit(text_surface, text_rect)  # 텍스트 그리기

# 시작 화면 함수
def show_start_screen():
    screen.blit(start_screen_image, (0, 0))  # 시작 화면에 이미지 추가
    draw_centered_text("Press Space To Start", 50, size=80, color=(252,148,12), bg_color=(109,0,142), border_radius=30) 
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
def game_over_screen():
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

# 스테이지 클리어 화면 함수
def stage_cleared_screen(current_stage):
    # 스테이지 클리어 이미지를 표시
    screen.blit(stage_cleared_image, (0, 0))
    pygame.display.flip()

    waiting_for_next_stage = True
    while waiting_for_next_stage:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_next_stage = False

# 게임이 종료되고 다시 시작될 때마다 초기화    
def reset_game(stage_config):
    global ball, paddle, bricks, score, ball_speed, collision_count, items, ball_list, game_count, paused_total_time, unbreakable_bricks, MAX_SPEED, item_probability, paddle_speed, last_new_brick_time, current_stage
    ball = initialize_ball()  # 공 초기화
    paddle = pygame.Rect(width // 2 - 50, height - 40, 160, 15)
    items = []  # 아이템 리스트 초기화
    ball_list = [(ball, ball_speed.copy())]  # 공 리스트 초기화
    unbreakable_bricks = []  # 파괴 불가능한 벽돌 초기화
    bricks = []  # 벽돌 리스트 초기화

    MAX_SPEED = stage_config['max_ball_speed']
    item_probability = stage_config['item_probability']
    paddle_speed = default_paddle_speed * stage_config['paddle_speed_multiplier']
    brick_rows = stage_config['brick_rows']

    # 벽돌 생성
    for row in range(brick_rows):
        color = colors[row % len(colors)]
        for col in range(12):
            rect = pygame.Rect(10 + col * (brick_width + 5), 60 + row * (brick_height + 5), brick_width, brick_height)
            brick = Brick(rect, color)
            bricks.append(brick)

    # 다중 히트 벽돌 설정
    for num_bricks, hits_required in stage_config['multi_hit_bricks']:
        selected_bricks = random.sample(bricks, num_bricks)
        for brick in selected_bricks:
            brick.hits_required = hits_required
            brick.hits_remaining = hits_required

    score = 0
    collision_count = 0
    ball_speed = initial_ball_speed.copy()  # 공 속도 초기화
    paused_total_time = 0  # 누적 일시정지 시간 초기화
    game_count += 1  # 게임 횟수 증가

    # 새로운 벽돌 등장 관련 시간 초기화
    last_new_brick_time = pygame.time.get_ticks()

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
        if not game_over_screen():
            pygame.quit()
            sys.exit()

    if current_stage > 10:
        # 전체 게임 클리어 시 처리
        # full_clear.jpg 이미지를 표시하고 스페이스바 누르면 다시 1스테이지로
        full_clear_image = pygame.image.load("full_clear.jpg").convert()
        full_clear_image = pygame.transform.scale(full_clear_image, (width, height))
        screen.blit(full_clear_image, (0, 0))
        pygame.display.flip()

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_stage = 1  # 1스테이지로 리셋
                        waiting_for_restart = False

    reset_game(stages[current_stage - 1])
    play_time_start = pygame.time.get_ticks()  # 시간 초기화

    # 게임 루프
    while True:
        current_time = pygame.time.get_ticks() - play_time_start - paused_total_time

        # 새로운 벽돌 등장 처리
        stage_config = stages[current_stage - 1]
        if stage_config['new_brick_interval']:
            if current_time - last_new_brick_time >= stage_config['new_brick_interval'] * 1000:
                last_new_brick_time = current_time
                for _ in range(stage_config.get('new_brick_count', 1)):
                    # 새로운 벽돌 생성
                    while True:
                        brick_x = random.randint(0, width - brick_width)
                        brick_y = random.randint(score_bar_height + 10, height // 2)
                        rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                        if not check_collision_with_bricks_and_items(rect, bricks, items, unbreakable_bricks):
                            new_brick = Brick(rect, color=random.choice(colors), hits_required=stage_config['new_brick_type'])
                            bricks.append(new_brick)
                            break  # 겹치지 않으면 생성 완료

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
            screen.blit(paused_image, (0, 0))  # 일시정지 이미지 표시
            pygame.display.flip()
            pygame.time.Clock().tick(10)
            continue

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle.left > 0:
            paddle.move_ip(-paddle_speed, 0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle.right < width:
            paddle.move_ip(paddle_speed, 0)

        # 공 이동 및 처리
        for ball, ball_speed in ball_list[:]:
            ball.move_ip(ball_speed)

            # 공의 속도 제한
            speed = (ball_speed[0] ** 2 + ball_speed[1] ** 2) ** 0.5
            if speed > MAX_SPEED:
                scaling_factor = MAX_SPEED / speed
                ball_speed[0] *= scaling_factor
                ball_speed[1] *= scaling_factor

            # 벽에 부딪히면 반사
            if ball.left <= 0:  # 왼쪽 벽에 닿을 때
                ball.left = 0 # 공을 왼쪽 벽 바로 오른쪽에 위치
                ball_speed[0] = -ball_speed[0]  # X축 방향 반전
            if ball.right >= width:  # 오른쪽 벽에 닿을 때
                ball.right = width  # 공을 오른쪽 벽 바로 왼쪽에 위치
                ball_speed[0] = -ball_speed[0]  # X축 방향 반전

            if ball.colliderect(paddle):
                # 패들과 공 충돌 시 효과음 재생
                paddle_hit_sound.play()
                ball.top = paddle.top - ball.height
                # 최소 수직 속도를 보장하도록 수정
                min_vertical_speed = 4  # 최소 수직 속도 설정
                ball_speed[1] = -abs(ball_speed[1])
                if abs(ball_speed[1]) < min_vertical_speed:
                    ball_speed[1] = -min_vertical_speed
                diff = ball.centerx - paddle.centerx
                ball_speed[0] += diff / (paddle.width / 2) * 5  # 패들 너비에 비례하여 조정

            # 투명 블록(score_bar)과 충돌 처리
            if ball.colliderect(score_bar):
                ball.top = score_bar.bottom  # 투명 블록 아래로 이동
                ball_speed[1] = abs(ball_speed[1])  # Y축 속도를 양수로 설정

            # 공이 파괴 불가능 벽돌과 충돌 처리
            for unbreakable_brick in unbreakable_bricks:
                if ball.colliderect(unbreakable_brick):
                    # 공과 벽돌의 중심 차이 계산
                    dx = (ball.centerx - unbreakable_brick.centerx) / (unbreakable_brick.width / 2)
                    dy = (ball.centery - unbreakable_brick.centery) / (unbreakable_brick.height / 2)

                    # dx와 dy 중 절대값이 큰 방향을 기준으로 충돌 판단
                    if abs(dx) > abs(dy):
                        # 좌우 충돌
                        if dx > 0:  # 오른쪽에서 충돌
                            ball.left = unbreakable_brick.right
                            ball_speed[0] = abs(ball_speed[0])  # X축 속도를 양수로 (오른쪽으로)
                        else:  # 왼쪽에서 충돌
                            ball.right = unbreakable_brick.left
                            ball_speed[0] = -abs(ball_speed[0])  # X축 속도를 음수로 (왼쪽으로)
                    else:
                        # 상하 충돌
                        if dy > 0:  # 아래쪽에서 충돌
                            ball.top = unbreakable_brick.bottom
                            ball_speed[1] = abs(ball_speed[1])  # Y축 속도를 양수로 (아래로)
                        else:  # 위쪽에서 충돌
                            ball.bottom = unbreakable_brick.top
                            ball_speed[1] = -abs(ball_speed[1])  # Y축 속도를 음수로 (위로)
                    break  # 충돌 후 다른 벽돌은 검사하지 않음

            for brick in bricks[:]:
                if ball.colliderect(brick.rect):
                    # 벽돌과 공 충돌 시 효과음 재생
                    brick_hit_sound.play()
                    ball_speed[1] = -ball_speed[1]
                    brick.hits_remaining -= 1
                    if brick.hits_remaining <= 0:
                        bricks.remove(brick)
                        score += 10
                        collision_count += 1
                        # 아이템 등장 확률에 따라 아이템 생성
                        if random.random() < item_probability:
                            item_type = random.choice([1, 2, 3])  # 1: 패들 크기 증가, 2: 공 개수 증가, 3: 절대 안 깨지는 벽돌 생성
                            if item_type == 3:  # 절대 안 깨지는 벽돌 생성 아이템
                                item = UnbreakableItem(brick.rect.centerx - 10, brick.rect.centery)
                            else:
                                item = Item(brick.rect.centerx - 10, brick.rect.centery, item_type)
                            items.append(item)
                    else:
                        pass  # 히트 수에 따른 처리는 그리기 부분에서 처리

                    if len(bricks) == 0:  # 벽돌이 모두 제거되었을 때
                        if current_stage == 10:
                            # 전체 게임 클리어 처리
                            # 'full_clear.jpg'를 화면에 띄우고 스페이스바 누르면 1스테이지로
                            full_clear_image = pygame.image.load("full_clear.jpg").convert()
                            full_clear_image = pygame.transform.scale(full_clear_image, (width, height))
                            screen.blit(full_clear_image, (0, 0))
                            pygame.display.flip()

                            waiting_for_restart = True
                            while waiting_for_restart:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                            current_stage = 1  # 1스테이지로 리셋
                                            waiting_for_restart = False
                            break
                        else:
                            # 스테이지 클리어 화면 표시
                            stage_cleared_screen(current_stage)
                            current_stage += 1
                            reset_game(stages[current_stage - 1])
                            play_time_start = pygame.time.get_ticks()
                            break

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
                    if game_over_screen():
                        reset_game(stages[current_stage - 1])
                        play_time_start = pygame.time.get_ticks()
                    break

        # 화면 그리기
        # 배경 이미지를 투명하게 화면에 그리기
        screen.fill(BLACK)  # 투명 이미지 아래 기본 배경색 설정
        screen.blit(background_image, (0, 0))  # 투명도가 적용된 배경 이미지 그리기
        
        pygame.draw.rect(screen, WHITE, paddle)

        # 벽돌 그리기
        for brick in bricks:
            color = brick.color  # 벽돌의 색상 사용
            pygame.draw.rect(screen, color, brick.rect)
            if brick.hits_remaining == 3:
                pygame.draw.rect(screen, (0, 0, 0), brick.rect, 3)  # 검은색 테두리
            elif brick.hits_remaining == 2:
                pygame.draw.rect(screen, (128, 128, 128), brick.rect, 3)  # 회색 테두리
            # 히트 수가 1일 때는 테두리 없음

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

        stage_text = font.render(f"Stage {current_stage}", True, WHITE)  # 스테이지 번호 표시
        screen.blit(stage_text, (width - 150, 10))

        time_text = font.render(format_time(current_time), True, WHITE)
        screen.blit(time_text, (width // 2 - 50, 10))

        # 시간 밑에 구분선 추가
        pygame.draw.line(screen, WHITE, (0, 50), (width, 50), 2)  # 선을 추가합니다.

        pygame.display.flip()
        pygame.time.Clock().tick(120)

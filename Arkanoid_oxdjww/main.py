# Need to..
# pip install pygame
# pip install easygui
import pygame
import random
import time
import easygui

# 게임 설정
WIDTH = 800
HEIGHT = 600
FPS = 60

# 색깔 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (107, 55, 69)  # 진짜 벽돌색
SKY_BLUE = (135, 206, 235)


# 벽돌 설정
BRICK_WIDTH = 50  # Decrease the width of the bricks
BRICK_HEIGHT = 20  # Decrease the height of the bricks
BRICK_ROWS = 5  # Increase the number of rows
BRICK_COLUMNS = 13  # Keep the number of columns as 10
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 30


# 패들 클래스 정의
class Paddle(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.name = name

        # Set text properties
        font = pygame.font.SysFont("새굴림", 20)  # Choose the font and size
        text = font.render(self.name, True, WHITE)  # Render the text with white color
        text_rect = text.get_rect(center=self.image.get_rect().center)  # Center the text on the image

        # Blit the text onto the image
        self.image.blit(text, text_rect)

    def update(self):
        self.speedx = 0
        mouse_pos = pygame.mouse.get_pos()
        self.rect.centerx = mouse_pos[0]
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


# 공 클래스 정의
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Increase the size of the ball
        pygame.draw.circle(self.image, RED, (10, 10), 10)  # Draw a circle for the ball
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30
        self.speedx = random.choice([-4, 4])  # Increase the absolute values to increase speed
        self.speedy = -4  # Increase the absolute value to increase speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.top < 0:
            self.speedy = -self.speedy


# 벽돌 클래스 정의
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = "과제"
        self.font = pygame.font.SysFont("새굴림", 15)

    def update(self):
        pass

    def draw_text(self, screen):
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)


# 게임 초기화
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid_oxdjww")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

player_name = easygui.enterbox("Enter your name")  # Popup to enter the player's name

paddle = Paddle(player_name)
ball = Ball()
all_sprites.add(paddle)
all_sprites.add(ball)

# 벽돌 생성
for row in range(BRICK_ROWS):
    for column in range(BRICK_COLUMNS):
        brick_x = column * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
        brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_OFFSET_TOP
        brick = Brick(brick_x, brick_y)
        all_sprites.add(brick)
        bricks.add(brick)

# 랜덤한 벽돌 25개를 초록으로 설정
random_bricks = random.sample(bricks.sprites(), 25)
for brick in random_bricks:
    brick.image.fill(SKY_BLUE)

# 게임 루프
running = True
move_down = False  # 벽돌을 아래로 움직이는 플래그
move_distance = 1  # 벽돌이 한 번에 내려가는 거리

score = 0
game_start_time = time.time()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # 패들과 공의 충돌 감지
    if pygame.sprite.collide_rect(ball, paddle):
        ball.speedy = -ball.speedy

    # 공이 벽돌과의 충돌 감지
    brick_collision = pygame.sprite.spritecollide(ball, bricks, True)
    if brick_collision:
        ball.speedy = -ball.speedy
        for brick in brick_collision:
            if brick.image.get_at((0, 0)) == SKY_BLUE:
                ball.speedx *= 1.1
                ball.speedy *= 1.1
                paddle.speedx += 50
            else :
                ball.speedx *= 0.9
                ball.speedy *= 0.9
            score += 10

    # 벽돌들이 아래로 내려가는 로직
    if not bricks:  # 모든 벽돌이 제거되었을 때
        running = False  # 움직임을 멈춤
    if move_down:
        for brick in bricks:
            brick.rect.y += move_distance

    # 공이 바닥에 닿을 경우 게임 종료
    if ball.rect.top > HEIGHT:
        running = False

    screen.fill(BLACK)
    all_sprites.draw(screen)

    # 벽돌의 텍스트를 그립니다.
    for brick in bricks:
        brick.draw_text(screen)

    # 게임 플레이 시간 계산
    game_play_time = int(time.time() - game_start_time)

    # 시간과 점수를 화면에 표시
    font = pygame.font.Font(None, 36)
    time_text = font.render("Time: " + str(game_play_time), True, WHITE)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(time_text, (10, 10))
    screen.blit(score_text, (10, 50))

    pygame.display.flip()

    # 벽돌이 가장 아래까지 도달했을 때 움직임을 멈춥니다.
    if any(brick.rect.bottom >= HEIGHT for brick in bricks):
        move_down = False

# 게임 종료 화면 출력
game_result = f"Player: {player_name}, Game Time: {game_play_time} seconds, Score: {score}"

screen.fill(BLACK)
font = pygame.font.Font(None, 48)
result_text = font.render(game_result, True, WHITE)
result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(result_text, result_rect)

pygame.display.flip()

# 종료 대기
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

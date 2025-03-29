import pygame
import os

pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = int(SCREEN_WIDTH * 9/16)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kaio's game")

clock = pygame.time.Clock()
FPS = 120

# Các biến của game
GRAVITY = 0.25

# Các biến điều khiển di chuyển của nhân vật
moving_left = moving_right = False
# Các biến điều khiển bắn đạn
shoot_left = shoot_right = False

# Load ảnh của viên đạn (chuyển sang alpha để có nền trong suốt)
bullet_image = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Shooting python game (original)/img/bullets/p_bullet.png').convert_alpha()

# Màu
BG = (144, 201, 120)
RED = (225, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 450), (SCREEN_WIDTH, 450))

# Lớp unit: đại diện cho các nhân vật (player và enemy)
class unit(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1  # Ban đầu hướng phải (1) hoặc trái (-1)
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: chạy
        self.update_time = pygame.time.get_ticks()
        
        # Tạo list animation cho các trạng thái của nhân vật
        animation_types = ['idle', 'run']
        for animation in animation_types:
            temp_list = []
            # Đếm số lượng khung hình trong thư mục tương ứng
            num_of_frames = len(os.listdir(f'C:/Users/ADMIN/Desktop/CODES/Shooting python game (original)/img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Shooting python game (original)/img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        
        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = 1
        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1

        # Nhảy
        if self.jump == True and self.in_air == False:
            self.vel_y = -10
            self.jump = False
            self.in_air = True

        # Áp dụng trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # Kiểm tra collision với floor
        if self.rect.bottom + dy > 450:
            dy = 450 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 60
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Khởi tạo nhân vật và enemy
x = 750
y = 400
scale = 3
speed = 4

class Bullet(pygame.sprite.Sprite):
    def _init_(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


player = unit('player', x, y, scale, speed)
enemy = unit('enemy', 1200, y - 30, scale, 0.8 * speed)

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    
    # Cập nhật và vẽ nhân vật cũng như enemy
    player.update_animation()
    player.draw()
    enemy.draw()

    # Cập nhật trạng thái chạy/idle của player dựa vào phím di chuyển
    if player.alive:
        if moving_left or moving_right:
            player.update_action(1)  # 1: chạy
        else:
            player.update_action(0)  # 0: idle
        player.move(moving_left, moving_right)

    # Xử lý các sự kiện bàn phím
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Khi nhấn phím xuống
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shoot_left = True
            if event.key == pygame.K_RIGHT:
                shoot_right = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # Khi thả phím ra
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                shoot_left = False
            if event.key == pygame.K_RIGHT:
                shoot_right = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()

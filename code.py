import pygame
import os

pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = int(SCREEN_WIDTH * 9/16)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kaio's game")

clock = pygame.time.Clock()
FPS = 60

# Các biến của game
GRAVITY = 0.5

# Biến của nhân vật
x = 750
y = 400
scale = 3
speed = 6
base_player_ammo = 20

# Các biến điều khiển di chuyển của nhân vật
moving_left = False
moving_right = False
shoot = False

# Load các ảnh
# Load ảnh của viên đạn (chuyển sang alpha để có nền trong suốt)
bullet_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/bullets/p_bullet.png').convert_alpha()

# Màu
BG = (144, 201, 120)
RED = (225, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 450), (SCREEN_WIDTH, 450))

# Lớp unit: đại diện cho các nhân vật (player và enemy)
class unit(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
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
        animation_types = ['idle', 'run', 'jump', 'death', 'shooting']
        for animation in animation_types:
            # Reset lại list tạm thời của các ảnh
            temp_list = []
            # Đếm số lượng khung hình trong thư mục tương ứng
            num_of_frames = len(os.listdir(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check__alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


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
            self.vel_y = -11
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

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 36
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Giảm số lượng đạn
            self.ammo -= 1

    def update_animation(self):
        ANIMATION_COOLDOWN = 60
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check__alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 8
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed)
        # Kiểm tra xem bullet đã rời khỏi màn hình hay chưa
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        # Kiểm tra collision với nhân vật
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 50
                self.kill()

# Tạo sprite group
bullet_group = pygame.sprite.Group()

# Khởi tạo nhân vật và enemy
player = unit('player', x, y, scale, speed, base_player_ammo)
enemy = unit('enemy', 1200, 400, scale, 0.8 * speed, base_player_ammo)

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    
    # Cập nhật và vẽ nhân vật cũng như enemy
    player.update()
    player.draw()
    enemy.update( )
    enemy.draw()

    # Cập nhật và vẽ groups
    bullet_group.update()
    bullet_group.draw(screen)

    # Cập nhật trạng thái chạy/idle của player dựa vào phím di chuyển
    if player.alive:
        # Bắn đạn
        if shoot:
            player.update_action(4)
            player.shoot()
        elif player.in_air:
            player.update_action(2)  # nhảy
        elif moving_left or moving_right:
            player.update_action(1)  # chạy
        else:
            player.update_action(0)  # idle
        player.move(moving_left, moving_right)


    # Xử lý các sự kiện bàn phím
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Khi nhấn phím xuống
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # Khi thả phím ra
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()

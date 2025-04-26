import pygame
from pygame import mixer
import os
import random
import csv
import button

mixer.init()
pygame.init()

# TODO: Thêm kẻ địch cận chiến
# TODO: người chơi tấn công cận chiến
# TODO: Thêm shop giữa các màn chơi
# TODO: Thay đổi background theo level
# TODO: Thay đổi nhạc theo level

# Kích thước màn hình
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = int(SCREEN_WIDTH * 9/16)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kaio's wizard game")

clock = pygame.time.Clock()
FPS = 60

# Các biến của game
GRAVITY = 0.5
SCROLL_THRESH = 350
ROWS = 16
COLS = 150
TILE_SIZE = (SCREEN_HEIGHT ) // ROWS
TILE_TYPES = 26
MAX_LEVELS = 5
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False


# Biến của nhân vật
scale = 2
speed = 5
base_player_ammo = 25
max_ammo = 80
saved_health = None
saved_mana = None
saved_coin = None

# Các biến điều khiển di chuyển của nhân vật
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Load âm thanh
# Các music:
# Nhạc menu
menu_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/menu.mp3')
menu_fx.set_volume(0.5)
menu_fx.play()
# Nhạc level:
# Level 1:
level_1_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/level_1_ost.mp3')
level_1_fx.set_volume(0.2)
# Các sound fx
jump_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/jump.wav')
jump_fx.set_volume(0.5)
p_attack_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/p_attack.wav')
p_attack_fx.set_volume(0.2)
p_hit_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/p_hit.wav')
p_hit_fx.set_volume(0.8)
spell_cast_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/spell_cast.wav')
spell_cast_fx.set_volume(0.5)
spell_explode_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/spell_explode.mp3')
spell_explode_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/sounds/pennypickup.mp3')
coin_fx.set_volume(0.5)

# Load các ảnh
# Background
pine1_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/back_ground/level_1/0.png').convert_alpha()
pine2_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/back_ground/level_1/1.png').convert_alpha()
pine3_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/back_ground/level_1/2.png').convert_alpha()
pine4_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/back_ground/level_1/3.png').convert_alpha()
pine5_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/back_ground/level_1/4.png').convert_alpha()
pine6_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/back_ground/level_1/5.png').convert_alpha()
pine1_img = pygame.transform.scale(pine1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine2_img = pygame.transform.scale(pine2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine3_img = pygame.transform.scale(pine3_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine4_img = pygame.transform.scale(pine4_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine5_img = pygame.transform.scale(pine5_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine6_img = pygame.transform.scale(pine6_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# ảnh buttons
start_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/menu_button/newgame.png').convert_alpha()
exit_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/menu_button/exit.png').convert_alpha()
restart_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/menu_button/restart.png').convert_alpha()


# Lưu trữ các tiles vào 1 list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/tiles/level_1/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# Load ảnh của viên đạn (chuyển sang alpha để có nền trong suốt)
bullet_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/bullets/p_bullet.png').convert_alpha()

# Load ảnh của grenade
grenade_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/bullets/grenade.png').convert_alpha()
# Load ảnh của pick up
health_box_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/pick_up/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/pick_up/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/pick_up/grenade_box.png').convert_alpha()
coin_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/pick_up/coin.png').convert_alpha()
coin_img = pygame.transform.scale(coin_img, (TILE_SIZE, TILE_SIZE))

item_boxes = {
    'Health'    : health_box_img,
    'Ammo'      : ammo_box_img,
    'Grenade'   : grenade_box_img,
    'Coin'      : coin_img
}


# Màu
BG = (144, 201, 120)
RED = (225, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (224, 255, 255)
PINK = (235, 65, 54)
YELLOW = (255, 170, 29)

# Định nghĩa font
font = pygame.font.SysFont('Futura', 30)

# Hàm để vẽ text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Hàm để vẽ background
def draw_bg():
    screen.fill(GREEN)
    width = pine1_img.get_width()
    for x in range(5):
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.3, 0))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.4, 0))
        screen.blit(pine3_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(pine4_img, ((x * width) - bg_scroll * 0.6, 0))
        screen.blit(pine5_img, ((x * width) - bg_scroll * 0.7, 0))
        screen.blit(pine6_img, ((x * width) - bg_scroll * 0.8, 0))

# Hàm để reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    ladder_group.empty()

    # Lưu lại các chỉ số của người chơi
    player_stats = {
        'health' : player.health,
        'ammo' : player.ammo,
        'coin' : player.coin
    }

    # Tạo 1 list các tiles empty
    data = []
    for row in range(ROWS):
        r = [-1] * COLS     # Đây là một list theo chiều ngang chứa toàn giá trị -1
        data.append(r)

    return data, player_stats

# Lớp unit: đại diện cho các nhân vật người chơi
class unit(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.coin = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1  # Ban đầu hướng phải (1) hoặc trái (-1)
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.on_ladder = False
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
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check__alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        keys = pygame.key.get_pressed()
        self.move_up = keys[pygame.K_w]
        self.move_down = keys[pygame.K_s]


    def move(self, moving_left, moving_right):
        # Reset lại các biến di chuyển
        screen_scroll = 0
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
            self.vel_y = -12
            self.jump = False
            self.in_air = True

        # Leo thang
        if pygame.sprite.spritecollideany(self, ladder_group):
            self.on_ladder = True
        else:
            self.on_ladder = False

        if self.on_ladder:
            self.vel_y = 0
            if self.move_up:
                dy -= 5
            if self.move_down:
                dy += 5
        else:
            # Áp dụng trọng lực
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

        # Kiểm tra collision
        for tile in world.obstacle_list:
            # Kiểm tra collision ở tọa độ x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y + 2, self.width, self.height - 4):
                dx = 0
            # Kiểm tra collision ở tọa độ y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Kiểm tra xem tọa độ có ở dưới vật (chẳng hạn khi nhảy đập đầu vào tường), chẳng hạn nhảy do khi nhảy thì y giảm
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Kiểm tra nếu ở ben trên mặt (chẳng hạn rơi xuống đập vào khối), chẳng hạn khi đang rơi
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Nếu va chạm với nước
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Kiểm tra xem đã win hay chưa
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # Kiểm tra xem người chơi đã rơi ra khỏi map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # Kiểm tra xem nếu nhân vật vượt khỏi viền màn hình
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Cập nhật vị trí rectangle
        self.rect.x += dx
        self.rect.y += dy

        # Cập nhật scroll dựa trên vị trí của player
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                  or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete
    

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 30
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Giảm số lượng đạn
            self.ammo -= 1
            p_attack_fx.play()


    def update_animation(self):
        ANIMATION_COOLDOWN = 90
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

# Tạo class kẻ địch - Trunk:
class EnemyTrunk(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 100
        self.direction = 1  # Ban đầu hướng phải (1) hoặc trái (-1)
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: chạy
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 5*TILE_SIZE, 20)
        self.idling = False
        self.idling_counter = 0
        
        # Tạo list animation cho các trạng thái của nhân vật
        animation_types = ['idle', 'run', 'jump', 'death', 'shooting']
        for animation in animation_types:
            # Reset lại list tạm thời của các ảnh
            temp_list = []
            # Đếm số lượng khung hình trong thư mục tương ứng
            num_of_frames = len(os.listdir(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/{self.char_type}/trunk/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/{self.char_type}/trunk/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check__alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, moving_left, moving_right):
        # Reset lại các biến di chuyển
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

        # Áp dụng trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y


        # Kiểm tra collision
        for tile in world.obstacle_list:
            # Kiểm tra collision ở tọa độ x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y + 2, self.width, self.height - 4):
                dx = 0
                self.direction *= -1
                self.move_counter = 0
            # Kiểm tra collision ở tọa độ y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Kiểm tra xem tọa độ có ở dưới vật (chẳng hạn khi nhảy đập đầu vào tường), chẳng hạn nhảy do khi nhảy thì y giảm
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Kiểm tra nếu ở ben trên mặt (chẳng hạn rơi xuống đập vào khối), chẳng hạn khi đang rơi
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Nếu va chạm với nước
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Kiểm tra xem người chơi đã rơi ra khỏi map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # Kiểm tra xem nếu nhân vật vượt khỏi viền màn hình
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Cập nhật vị trí rectangle
        self.rect.x += dx
        self.rect.y += dy
    

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 45
            bullet = EnemyBullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, 'trunk_bullet')
            bullet_group.add(bullet)

    def ai(self):
        if self.alive and player.alive:
            # Cho phép enemy tạm dừng theo trạng thái idle ngẫu nhiên
            if not self.idling and random.randint(1, 200) == 5:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50

            # Nếu player nằm trong vùng phát hiện thì enemy bắn
            if self.vision.colliderect(player.rect):
                self.update_action(4)  # 4: shooting
                self.shoot()
            else:
                if not self.idling:
                    # Xác định hướng di chuyển dựa trên giá trị self.direction
                    ai_moving_right = True if self.direction == 1 else False
                    ai_moving_left = not ai_moving_right
                    
                    # Lưu lại vị trí x trước khi di chuyển để tính khoảng cách thực tế
                    old_x = self.rect.x
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1: chạy

                    # Tính khoảng cách đã di chuyển theo pixel
                    moved_distance = abs(self.rect.x - old_x)
                    self.move_counter += moved_distance

                    # Cập nhật lại vùng phát hiện dựa trên vị trí hiện tại
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    # Khi tổng khoảng cách di chuyển đạt đến hoặc vượt quá TILE_SIZE, đổi hướng và reset biến đếm
                    if self.move_counter >= 2 * TILE_SIZE:
                        self.direction *= -1
                        self.move_counter = 0
                else:
                    # Giảm thời gian idling nếu enemy đang trong trạng thái dừng
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # Cập nhật scroll cho enemy (để đồng bộ với màn hình)
        self.rect.x += screen_scroll


    def update_animation(self):
        ANIMATION_COOLDOWN = 80
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

# Tạo class kẻ địch - Peashooter:
class EnemyPeashooter(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, direction):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.shoot_cooldown = 0
        self.health = 125
        self.direction = direction  # Ban đầu hướng phải (1) hoặc trái (-1)
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: chạy
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 10*TILE_SIZE, 20)    # Tầm nhìn
        self.idling = True
        self.idling_counter = 0
        self.vel_y = 0
        self.in_air = True


        # Tạo list animation cho các trạng thái của nhân vật
        animation_types = ['idle', 'death', 'shooting']
        for animation in animation_types:
            # Reset lại list tạm thời của các ảnh
            temp_list = []
            # Đếm số lượng khung hình trong thư mục tương ứng
            num_of_frames = len(os.listdir(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/{self.char_type}/peashooter/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/{self.char_type}/peashooter/{animation}/{i}.png').convert_alpha()
                # Cập nhật lại hình ảnh nếu direction bằng 1
                if direction == 1:
                    img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check__alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.alive:
            self.move()

    def move (self):
        # Reset lại các biến di chuyển
        dx = 0
        dy = 0
        # Áp dụng trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Kiểm tra collision
        for tile in world.obstacle_list:
            # Kiểm tra collision ở tọa độ x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y + 2, self.width, self.height - 4):
                dx = 0
                self.direction *= -1
                self.move_counter = 0
            # Kiểm tra collision ở tọa độ y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Kiểm tra xem tọa độ có ở dưới vật (chẳng hạn khi nhảy đập đầu vào tường), chẳng hạn nhảy do khi nhảy thì y giảm
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Kiểm tra nếu ở ben trên mặt (chẳng hạn rơi xuống đập vào khối), chẳng hạn khi đang rơi
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Nếu va chạm với nước
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Kiểm tra xem nhân vật đã rơi ra khỏi map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # Kiểm tra xem nếu nhân vật vượt khỏi viền màn hình
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Cập nhật vị trí rectangle
        self.rect.x += dx
        self.rect.y += dy
    

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 80
            bullet = EnemyBullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, 'pea_bullet')
            bullet_group.add(bullet)

    def ai(self):
        if self.alive and player.alive:
            self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
            # Nếu player nằm trong vùng phát hiện thì enemy bắn
            if self.vision.colliderect(player.rect):
                self.update_action(2)  # 4: shooting
                self.shoot()
            else:
                self.update_action(0)

        # Cập nhật scroll cho enemy (để đồng bộ với màn hình)
        self.rect.x += screen_scroll


    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 1:
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
            self.update_action(1)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
# Tạo class thế giới
class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data, player_stats = None):
        self.level_length = len(data[0])
        global player, current_level, saved_health, saved_mana, saved_coin
        # Khởi tạo biến player để lưu trữ chỉ số của người chơi qua từng màn
        player = None
        # Lặp qua từng giá trị trong file level
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    # Các khối không di chuyển qua được
                    if (tile >= 0 and tile <= 3) or tile == 14:
                        self.obstacle_list.append(tile_data)
                    # Nước
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    # Các thang
                    elif tile >= 15 and tile <= 17:
                        ladder = Ladder(x * TILE_SIZE, y*TILE_SIZE, tile)
                        ladder_group.add(ladder)
                    # Khối trang trí
                    elif (tile >= 11 and tile <= 13) or (tile >= 18 and tile <= 21):
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    # Người chơi
                    elif tile == 7:
                        # Nếu có player_stats, sử dụng các chỉ số đã lưu, nếu không thì dùng giá trị mặc định
                        global saved_health, saved_mana, saved_coin 
                        if saved_health is not None:
                            player = unit('player', x * TILE_SIZE, y * TILE_SIZE, scale, speed, saved_mana)
                            player.health = saved_health
                            player.coin = saved_coin
                            health_bar = HealthBar(100, 10, player.health, player.max_health)
                            mana_bar = ManaBar(82, 35, player.ammo, player.max_ammo )
                        else:
                            player = unit('player', x * TILE_SIZE, y * TILE_SIZE, scale, speed, base_player_ammo)
                            health_bar = HealthBar(100, 10, player.health, player.health)
                            mana_bar = ManaBar(82, 35, player.ammo, player.max_ammo )
                    # Kẻ địch Trunk
                    elif tile == 8:
                        enemy = EnemyTrunk('enemy', x * TILE_SIZE, y * TILE_SIZE, 2, 0.5 * speed)
                        enemy_group.add(enemy)
                    # Tạo hộp đạn
                    elif tile == 4:
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    # Tạo hộp spells
                    elif tile == 5:
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    # Tạo hộp máu
                    elif tile == 6:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    # Lối thoát
                    elif tile == 22:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    # Thêm Coin
                    elif tile == 23:
                        coin = ItemBox('Coin', x*TILE_SIZE, y*TILE_SIZE)
                        item_box_group.add(coin)
                    # Thêm kẻ địch peashooter
                    # Hướng mặt sang trái
                    elif tile == 24:
                        enemy = EnemyPeashooter('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.5, -1)
                        enemy_group.add(enemy)
                    # Hướng mặt sang phải
                    elif tile == 25:
                        enemy = EnemyPeashooter('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.5, 1)
                        enemy_group.add(enemy)
        return player, health_bar, mana_bar
    # Hiển thị các tiles
    def draw (self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
                    
# Tạo class Ladder
class Ladder (pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/tiles/level_1/{type}.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x,y))
    def update(self):
        self.rect.x += screen_scroll

# Tạo class đồ trang trí
class Decoration(pygame.sprite.Sprite):
    def __init__(self,img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update (self):
        self.rect.x += screen_scroll
    

# Tạo class nước
class Water(pygame.sprite.Sprite):
    def __init__(self,img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update (self):
        self.rect.x += screen_scroll

# Tạo class lối thoát
class Exit (pygame.sprite.Sprite):
    def __init__(self,img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update (self):
        self.rect.x += screen_scroll

# Tạo class đồ vật
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update(self):
        # scroll
        self.rect.x += screen_scroll
        # Kiểm tra nếu người chơi đã pick item lên
        if pygame.sprite.collide_rect(self, player):
            # Kiểm tra xem loại pick up nào
            if self.item_type == 'Health':
                player.health += 40
                if (player.health > player.max_health):
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 12
                if (player.ammo > player.max_ammo):
                    player.ammo = player.max_ammo
            elif self.item_type == 'Grenade':
                player.ammo += 20
            elif self.item_type == 'Coin':
                player.coin += 1
                coin_fx.play()
            # Xóa bỏ item box
            self.kill()

# Tạo class cho thanh máu
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # Cập nhật máu hiện tại
        self.health = health
        # Tính toán ration máu
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

# Tạo class mana
# Tạo class cho thanh máu
class ManaBar():
    def __init__(self, x, y, mana, max_mana):
        self.x = x
        self.y = y
        self.mana = mana
        self.max_mana = max_mana

    def draw(self, mana):
        # Cập nhật máu hiện tại
        self.mana = mana
        # Tính toán ration máu
        ratio = self.mana / self.max_mana
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 304, 24))
        pygame.draw.rect(screen, CYAN, (self.x, self.y, 300, 20))
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 300 * ratio, 20))


# Tạo class Bullet của người chơi
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # Kiểm tra xem bullet đã rời khỏi màn hình hay chưa
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        # Kiểm tra collision với terrain
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()

# Tạo class Bullet của kẻ địch
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_type):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.direction = direction
        self.bullet_type = bullet_type
        bullet_img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/bullets/{bullet_type}.png').convert_alpha()
        bullet_img = pygame.transform.scale(bullet_img, (32, 32))
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # Kiểm tra xem bullet đã rời khỏi màn hình hay chưa
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        # Kiểm tra collision với terrain
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # Kiểm tra collision với nhân vật
        if self.bullet_type == 'trunk_bullet':
            if pygame.sprite.spritecollide(player, bullet_group, False):
                if player.alive:
                    player.health -= 20
                    p_hit_fx.play()
                self.kill()
            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, bullet_group, False):
                    if enemy.alive:
                        enemy.health -= 25
                        self.kill()

        if self.bullet_type == 'pea_bullet':
            if pygame.sprite.spritecollide(player, bullet_group, False):
                if player.alive:
                    player.health -= 35
                    p_hit_fx.play()
                self.kill()
            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, bullet_group, False):
                    if enemy.alive:
                        enemy.health -= 35
                        self.kill()

# Tạo class grenade
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

        # Kiểm tra va chạm ban đầu xem spell có bị sinh ra trong tile hay không
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                if self.direction > 0:
                    self.rect.right = tile[1].left - 1
                else:
                    self.rect.left = tile[1].right + 1
                break

    def update(self):
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y
        # Kiểm tra collision với terrain
        for tile in world.obstacle_list:
            # Kiểm tra collision nếu đập phải tiles
            if tile[1].colliderect(self.rect.x + dx, self.rect.y - 5, self.width, self.height + 5):
                self.kill()
                spell_explode_fx.play()
                explosion = Explosion(self.rect.x, self.rect.y, 3)
                explosion_group.add(explosion)
                # Gây sát thương lên bất cứ ai ở trong vùng này
                if (abs(self.rect.centerx - player.rect.centerx)) < TILE_SIZE * 2 and \
                    (abs(self.rect.centery - player.rect.centery)) < TILE_SIZE * 2:
                    player.health -= 50
                for enemy in enemy_group:
                    if (abs(self.rect.centerx - enemy.rect.centerx)) < TILE_SIZE * 2 and \
                        (abs(self.rect.centery - enemy.rect.centery)) < TILE_SIZE * 2:
                        enemy.health -= 50
        # Kiểm tra collision ở tọa độ y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # Kiểm tra ném lên
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Kiểm tra rơi xuống
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                    self.rect.y += dy
                    self.rect.y = int(self.rect.y)

        # Cập nhật vị trí grenade
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

# Tạo class vụ nổ
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(0, 8):
            img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/bullets/Spells_1/{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        # Cập nhật animation vụ nổ
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # Nếu animation hoàn thành thì xóa bỏ đi Explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else: 
                self.image = self.images[self.frame_index]

# Tạo class cho màn hình sinh động hơn
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        # Fade toàn màn hình
        if self.direction == 1: 
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0- self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        # Màn hình sẽ chạy từ trên xuống theo chiều ngang
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= 2/3 * SCREEN_WIDTH:
            fade_complete = True

        return fade_complete

# Tạo instance cho screenfade
intro_fade = ScreenFade(1, BLACK, 7)
death_fade = ScreenFade(2, PINK, 5)

# Tạo các nút
start_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150, start_img, 5)
exit_button = button.Button(SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 + 50, exit_img, 5)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, restart_img, 5)

# Tạo sprite group
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
ladder_group = pygame.sprite.Group()




# Tạo một tile list rỗng
world_data = []
for row in range(ROWS):
    r = [-1] * COLS     # Đây là một list theo chiều ngang chứa toàn giá trị -1
    world_data.append(r)

# Load dữ liệu của level và tạo thế giới
with open(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/level/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player , health_bar, mana_bar =  world.process_data(world_data)

run = True
while run:
    # FPS của con game
    clock.tick(FPS)

    # Khi chưa bắt đầu game
    if start_game == False:
        # Vẽ menu
        screen.fill(BG)
        # Thêm các nút bấm
        if start_button.draw(screen):
            start_game = True
            start_intro = True
            menu_fx.stop()
        if exit_button.draw(screen):
            run = False
    else:
        if not level_1_fx.get_num_channels() > 0:  # Kiểm tra nếu nhạc chưa phát
            level_1_fx.play(-1)
        # Cập nhật background
        draw_bg()
        # Vẽ bản đồ game
        world.draw()
        # Hiển thị thanh máu
        health_bar.draw(player.health)
        draw_text(f'HEALTH: ', font, BLACK, 10, 10)
        # Hiển thị mana
        
        # Hiển thị ammo
        draw_text(f'MANA: ', font, BLACK, 10, 35)
        mana_bar.draw(player.ammo)
        # Hiển thị coins
        draw_text(f'COINS: ', font, BLACK, 10, 60)
        draw_text(f'{player.coin}', font, YELLOW, 95, 62)
        screen.blit(coin_img, (115, 46))

        # Các vật cập nhật trước player
        ladder_group.update()
        ladder_group.draw(screen)
        decoration_group.update()
        decoration_group.draw(screen)
        # Cập nhật và vẽ nhân vật cũng như enemy
        player.update()
        player.draw()
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()
        
        # Cập nhật và vẽ groups
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)


        # Hiện lên intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # Cập nhật trạng thái chạy/idle của player dựa vào phím di chuyển
        if player.alive:
            # Bắn đạn
            if shoot:
                player.update_action(4)
                player.shoot()
            # Ném lựu đạn
            elif grenade and not grenade_thrown and player.ammo >= 3:
                grenade = Grenade(player.rect.centerx + (0.5* player.rect.size[0] * player.direction),\
                                player.rect.top, player.direction)
                grenade_group.add(grenade)
                # Giảm số grenade lại
                player.ammo -= 3
                grenade_thrown = True
            elif player.in_air:
                player.update_action(2)  # nhảy
            elif moving_left or moving_right:
                player.update_action(1)  # chạy
            else:
                player.update_action(0)  # idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # Kiểm tra xem người chơi đã hoàn thành level hay chưa
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data , player_stats = reset_level()
                if level <= MAX_LEVELS:
                    saved_health = player.health
                    saved_mana = player.ammo
                    saved_coin = player.coin
                    # Load dữ liệu của level và tạo thế giới
                    with open(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/level/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    player , health_bar, mana_bar =  world.process_data(world_data)


        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data, _ = reset_level()
                    level = 1
                    saved_health = None
                    # Load dữ liệu của level và tạo thế giới
                    with open(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/level/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    player , health_bar, mana_bar =  world.process_data(world_data)

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
            if event.key == pygame.K_q:
                grenade = True
                spell_cast_fx.play()
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
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
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()
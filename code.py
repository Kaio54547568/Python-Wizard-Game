import pygame
import os
import random
import csv
import button

pygame.init()

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
TILE_TYPES = 23
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False

# Biến của nhân vật
scale = 2.5
speed = 6
base_player_ammo = 20
base_player_grenade = 5
max_ammo = 60

# Các biến điều khiển di chuyển của nhân vật
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

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

item_boxes = {
    'Health'    : health_box_img,
    'Ammo'      : ammo_box_img,
    'Grenade'   : grenade_box_img
}


# Màu
BG = (144, 201, 120)
RED = (225, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (224, 255, 255)

# Định nghĩa font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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

# Lớp unit: đại diện cho các nhân vật (player và enemy)
class unit(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenade):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenade = grenade
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

        # Chỉ đối với ai
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 200, 20)
        self.idling = False
        self.idling_counter = 0
        
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
                # Nếu con ai gặp tường, nó sẽ quay lại
                if self.char_type == 'enemy':
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

        return screen_scroll
    

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 30
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Giảm số lượng đạn
            self.ammo -= 1

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 5:
                self.update_action(0) # 0: idle
                self.idling = True
                self.idling_counter = 50
            # Kiểm tra xem ai có ở gần người chơi không
            if self.vision.colliderect(player.rect):
                # Ngừng chạy và hướng mặt vào người chơi
                self.update_action(4)
                self.shoot()
            else:   
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action (1) # 1: chạy
                    self.move_counter += 1
                    # Cập nhật domain phát hiện
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

            # Scroll
        self.rect.x += screen_scroll

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

# Tạo class thế giới
class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
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
                    # Khối trang trí
                    elif (tile >= 11 and tile <= 13) or (tile >= 18 and tile <= 21):
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    # Người chơi
                    elif tile == 7:
                        player = unit('player', x * TILE_SIZE, y * TILE_SIZE, scale, speed, base_player_ammo, base_player_grenade)
                        health_bar = HealthBar(100, 10, player.health, player.health)
                        mana_bar = ManaBar(82, 35, player.ammo, player.max_ammo )
                    # Kẻ địch
                    elif tile == 8:
                        enemy = unit('enemy', x * TILE_SIZE, y * TILE_SIZE, scale, 0.5 * speed, base_player_ammo, 0)
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
                        exit.add(exit)
        return player, health_bar, mana_bar
    # Hiển thị các tiles
    def draw (self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
                    

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
                player.health += 25
                if (player.health > player.max_health):
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
                if (player.ammo > player.max_ammo):
                    player.ammo = player.max_ammo
            elif self.item_type == 'Grenade':
                player.grenade += 3
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


# Tạo class Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
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

        # Kiểm tra collision với nhân vật
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 10
            self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()

# Tạo class grenade
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
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
                self.direction *= -1
                dx = self.speed * self.direction
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

        # Timer đếm thời gian nổ
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
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

# Tạo các nút
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)

# Tạo sprite group
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()




# Tạo một tile list rỗng
world_data = []
for row in range(ROWS):
    r = [-1] * COLS     # Đây là một list theo chiều ngang chứa toàn giá trị -1
    world_data.append(r)

# Load dữ liệu của level và tạo thế giới
# TODO Tìm hiểu xem đoạn code này có nghĩa là gì ?
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
        start_button.draw(screen)
        exit_button.draw(screen)
    else:
        # Cập nhật background
        draw_bg()
        # Vẽ bản đồ game
        world.draw()
        # Hiển thị thanh máu
        health_bar.draw(player.health)
        draw_text(f'HEALTH: ', font, WHITE, 10, 10)
        # Hiển thị mana
        
        # Hiển thị ammo
        draw_text(f'MANA: ', font, WHITE, 10, 35)
        mana_bar.draw(player.ammo)
        # Hiển thị spell
        draw_text(f'GRENADE: ', font, WHITE, 10, 60)
        for x in range(player.grenade):
            screen.blit(grenade_img, (120 + (x * 15), 50))
        
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
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        # Cập nhật trạng thái chạy/idle của player dựa vào phím di chuyển
        if player.alive:
            # Bắn đạn
            if shoot:
                player.update_action(4)
                player.shoot()
            # Ném lựu đạn
            elif grenade and grenade_thrown == False and player.grenade > 0:
                grenade = Grenade(player.rect.centerx + (0.5* player.rect.size[0] * player.direction),\
                                player.rect.top, player.direction)
                grenade_group.add(grenade)
                # Giảm số grenade lại
                player.grenade -= 1
                grenade_thrown = True
            elif player.in_air:
                player.update_action(2)  # nhảy
            elif moving_left or moving_right:
                player.update_action(1)  # chạy
            else:
                player.update_action(0)  # idle
            screen_scroll = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll




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
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()

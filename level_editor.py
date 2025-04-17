import pygame
import button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Cửa số game
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = int(SCREEN_WIDTH * 9/16)
# Margin này là kích thước bảng điều khiển
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Trình tạo level')

# Định nghĩa các biến của game
ROWS = 16
MAX_COLS = 150
TILE_SIZE = (SCREEN_HEIGHT + 5 ) // ROWS
TILE_TYPES = 26
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# Load các ảnh
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

# Lưu trữ các tiles vào 1 list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/tiles/level_1/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/UI_button/save.png').convert_alpha()
save_img = pygame.transform.scale(save_img, (TILE_SIZE, TILE_SIZE))
load_img = pygame.image.load('C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/img/UI_button/load.png').convert_alpha()
load_img = pygame.transform.scale(load_img, (TILE_SIZE, TILE_SIZE))

# Định nghĩa màu sắc
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# Định nghĩa font
font = pygame.font.SysFont('Futura', 30)

# Tạo một tile list rỗng
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS     # Đây là một list theo chiều ngang chứa toàn giá trị -1
    world_data.append(r)

# Tạo mặt đất
for tile in range (0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0

# Hàm để output text ra màn hình
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Hàm để vẽ world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# Tạo một function để vẽ background
def draw_bg():
    screen.fill(GREEN)
    width = pine1_img.get_width()
    for x in range(4):
        screen.blit(pine1_img, ((x * width)-scroll * 0.3, 0))
        screen.blit(pine2_img, ((x * width) -scroll * 0.4, 0))
        screen.blit(pine3_img, ((x * width) -scroll * 0.5, 0))
        screen.blit(pine4_img, ((x * width)-scroll * 0.6, 0))
        screen.blit(pine5_img, ((x * width)-scroll * 0.7, 0))
        screen.blit(pine6_img, ((x * width)-scroll * 0.8, 0))

# Vẽ các grid
def draw_grid():
    # kẻ theo chiều dọc
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # Kẻ theo chiều ngang
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

# Tạo các nút
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# Tạo một list các nút
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_col = 0
        button_row += 1

run = True
while run:
    
    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('UP / DOWN thay doi level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save và load
    if save_button.draw(screen):
        # Lưu trữ dữ liệu của màn chơi
        with open(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/level/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        # Load dữ liệu của level
        # Reset scroll quay lại ban đầu
        scroll = 0
        with open(f'C:/Users/ADMIN/Desktop/CODES/Python-Shooting-Game-Original/level/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
                

    # Vẽ bảng điều khiển
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # Chọn 1 tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # Highlight tile được lựa chọn
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # Dịch chuyển bản đồ
    if scroll_left == True and scroll > 0:
        scroll -= 10 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 10 * scroll_speed

    # Thêm tile mới vào screen
    # Nhận vị trí của con chuột
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # Kiểm tra xem tọa độ có trong khu vực tiles hay không
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # Cập nhật giá trị của tile
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Ấn nút từ bàn phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed = 4
            if event.key == pygame.K_ESCAPE:
                run = False
        # Khi thả nút ra
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()


pygame.quit()
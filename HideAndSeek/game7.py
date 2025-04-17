import pygame, sys, random, time, os, heapq
from pygame.locals import *
import pytmx


# Khởi tạo pygame
pygame.init()
pygame.mixer.init()  # Khởi tạo hệ thống âm thanh

# Cài đặt cửa sổ game
DISPLAYSURF = pygame.display.set_mode((1260, 670))
pygame.display.set_caption("Hide And Seek")
footstep = 20
path = []  # Thêm này cùng với các biến toàn cục khác

# Trạng thái game
MAIN_MENU = 0
RULES = 1
SETTINGS = 2
HIDING = 3
SEEKING = 4
GAME_OVER = 5
game_state = MAIN_MENU  # Bắt đầu từ menu chính

# Cài đặt game

SEEKING_TIME = 30  # giâyß

seeking_timer = SEEKING_TIME
game_result = None  # "win" hoặc "lose"
# Thêm vào phần khai báo biến toàn cục
initial_seeker_pos = None
show_initial_pos = True  # Hiển thị vị trí ban đầu trong giai đoạn hiding

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (191, 17, 17)
BLUE = (83, 157, 176)
GREEN = (83, 176, 86)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# FPS
fpsclock = pygame.time.Clock()
FPS = 30 # Tăng FPS để mượt hơn

# Âm thanh
background_music = pygame.mixer.Sound("HideAndSeek\\Audio\\Musics\\4 - Village.ogg")
game_music = pygame.mixer.Sound("HideAndSeek\\Audio\\Musics\\1 - Adventure Begin.ogg")
try:
    click_sound = pygame.mixer.Sound("HideAndSeek\\Audio\\Sounds\\Menu\\Accept4.wav")
    win_sound = pygame.mixer.Sound("HideAndSeek\\Audio\\Jingles\\Success4.wav")
    lose_sound = pygame.mixer.Sound("HideAndSeek\\Audio\\Jingles\\GameOver4.wav")
    background_music = pygame.mixer.Sound("HideAndSeek\\Audio\\Musics\\4 - Village.ogg")
    background_music.set_volume(0.01)
    click_sound.set_volume(1)
    background_music.play(-1)  # Lặp lại nhạc nền
except:
    print("Không tìm thấy file âm thanh, game sẽ chạy không có âm thanh")
    no_sound = True
else:
    no_sound = False

# Load hình ảnh
def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        print(f"Không tìm thấy ảnh tại {path}")
        # Tạo ảnh placeholder nếu không tìm thấy file
        surf = pygame.Surface((size if size else (50, 50)))
        surf.fill(RED if "Hun" in path else BLUE)
        return surf

# Đường dẫn hình ảnh
image_path = "HideAndSeek\\Image\\"

# Background
#1248 x 
background = load_image(os.path.join(image_path, "Background.jpg"), (1260, 200))
ground = load_image(os.path.join(image_path, "Ground.png"), (1260, 540))
mainbackground = load_image(os.path.join(image_path, "menubackground.jpg"), (1260, 700))
setbackground = load_image(os.path.join(image_path, "setBackground.jpg"), (1260,700))

# Blocks
block = load_image(os.path.join(image_path, "Block.png"), (60, 60))
block1 = load_image(os.path.join(image_path, "Block.png"), (60, 60))
block2 = load_image(os.path.join(image_path, "Block2.png"), (60, 60))

# Hunter animations (người trốn)
hunD1 = load_image(os.path.join(image_path, "Hun/HunterD1.png"))
hunD2 = load_image(os.path.join(image_path, "Hun/HunterD2.png"))
hunU1 = load_image(os.path.join(image_path, "Hun/HunterU1.png"))
hunU2 = load_image(os.path.join(image_path, "Hun/HunterU2.png"))
hunLR1 = load_image(os.path.join(image_path, "Hun/HunterLR1.png"))
hunLR2 = load_image(os.path.join(image_path, "Hun/HunterLR2.png"))
hunS = load_image(os.path.join(image_path, "Hun/HunterS.png"))

# Seeker animations (người tìm)
hiderD1 = load_image(os.path.join(image_path, "Sur/SurD1.png"))
hiderD2 = load_image(os.path.join(image_path, "Sur/SurD2.png"))
hiderU1 = load_image(os.path.join(image_path, "Sur/SurU1.png"))
hiderU2 = load_image(os.path.join(image_path, "Sur/SurU2.png"))
hiderLR1 = load_image(os.path.join(image_path, "Sur/SurLR1.png"))
hiderLR2 = load_image(os.path.join(image_path, "Sur/SurLR2.png"))
hider_idle = load_image(os.path.join(image_path, "Sur/SurS.png"))

# Nút bấm
play_button = load_image(os.path.join(image_path, "Button/play.png"), (200, 50))
play_button_hover = load_image(os.path.join(image_path, "Button/play_hover.png"), (200, 50))
rule_button = load_image(os.path.join(image_path, "Button/rule.png"), (200, 50))
rule_button_hover = load_image(os.path.join(image_path, "Button/rule_hover.png"), (200, 50))
settings_button = load_image(os.path.join(image_path, "Button/Set.png"), (200, 50))
settings_button_hover = load_image(os.path.join(image_path, "Button/Set_hover.png"), (200, 50))
back_button = load_image(os.path.join(image_path, "Button/back.png"), (100, 40))
back_button_hover = load_image(os.path.join(image_path, "Button/back_hover.png"), (100, 40))

# Tạo animation dictionary cho hunter
seeker_animations = {
    'down': [pygame.transform.scale(hunD1, (30, 30)), pygame.transform.scale(hunD2, (30, 30))],
    'up': [pygame.transform.scale(hunU1, (30, 30)), pygame.transform.scale(hunU2, (30, 30))],
    'right': [pygame.transform.scale(hunLR1, (30, 30)), pygame.transform.scale(hunLR2, (30, 30))],
    'left': [pygame.transform.flip(pygame.transform.scale(hunLR1, (30, 30)), True, False),
             pygame.transform.flip(pygame.transform.scale(hunLR2, (30, 30)), True, False)],
    'idle': [pygame.transform.scale(hunS, (30, 30))]
}

# Tạo animation dictionary cho seeker
hider_animations = {
    'down': [pygame.transform.scale(hiderD1, (30, 30)), pygame.transform.scale(hiderD2, (30, 30))],
    'up': [pygame.transform.scale(hiderU1, (30, 30)), pygame.transform.scale(hiderU2, (30, 30))],
    'right': [pygame.transform.scale(hiderLR1, (30, 30)), pygame.transform.scale(hiderLR2, (30, 30))],
    'left': [pygame.transform.flip(pygame.transform.scale(hiderLR1, (30, 30)), True, False),
             pygame.transform.flip(pygame.transform.scale(hiderLR2, (30, 30)), True, False)],
    'idle': [pygame.transform.scale(hider_idle, (30, 30))]
}

# Khởi tạo trạng thái nhân vật
current_dir = 'down'
animation_frame = 0
animation_timer = 0
animation_speed = 0.05  # Tốc độ animation (nhỏ hơn = nhanh hơn)
hun_rect = seeker_animations['idle'][0].get_rect(topleft=(0, 180))

# Seeker properties
seeker_rect = pygame.Rect(0 ,180 , 30, 30)  # Bắt đầu từ trên bên trái
seeker_speed = 2.5
seeker_direction = 'right'  # Hướng ban đầu
seeker_animation_frame = 0
seeker_animation_timer = 0

# Hider properties
hider_rect = pygame.Rect(0,180,30,30)
hider_speed = 2
hider_direction = 'right'
hider_animation_frame = 0
hider_animation_timer = 0

# Tạo các block và lưu vị trí
random_tuples = []
for _ in range(50):
    xStone = random.choice([x for x in range(60, 1201) if x % 60 == 0])
    yStone = random.choice([x for x in range(220, 601) if x % 60 == 0])
    while any((xStone, yStone) == (t[0], t[1]) for t in random_tuples):
        xStone = random.choice([x for x in range(60, 1201) if x % 60 == 0])
        yStone = random.choice([x for x in range(220, 601) if x % 60 == 0])
    block_type = random.choice([0, 1, 2])
    random_tuples.append((xStone, yStone, block_type))

def move(up, down, left, right):
    global current_dir, animation_frame, animation_timer
    
    new_rect = hun_rect.copy()
    moving = False
    
    # Xác định hướng di chuyển với tốc độ hider_speed
    if up:
        new_rect.y -= hider_speed
        current_dir = 'up'
        moving = True
    if down:
        new_rect.y += hider_speed
        current_dir = 'down'
        moving = True
    if left:
        new_rect.x -= hider_speed
        current_dir = 'left'
        moving = True
    if right:
        new_rect.x += hider_speed
        current_dir = 'right'
        moving = True

    # Cập nhật animation (giữ nguyên)
    if moving:
        animation_timer += 1
        if animation_timer >= animation_speed * FPS:
            animation_frame = (animation_frame + 1) % 2
            animation_timer = 0
    else:
        animation_frame = 0
        animation_timer = 0

    # Kiểm tra va chạm (giữ nguyên)
    collision = False
    for (x, y, _) in random_tuples:
        block_rect = pygame.Rect(x, y, 60, 60)
        if new_rect.colliderect(block_rect):
            collision = True
            break

    # Giới hạn di chuyển trong màn hình
    if not collision and 0 <= new_rect.x <= 1230 and 180 <= new_rect.y <= 640:
        hun_rect.x = new_rect.x
        hun_rect.y = new_rect.y
import heapq

def move_seeker():
    global seeker_rect, seeker_direction, game_state, game_result, path  # Thêm path vào đây
    global seeker_animation_frame, seeker_animation_timer
    
    # A* Pathfinding Implementation
    def heuristic(a, b):
        # Manhattan distance for grid
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def a_star_search(start, goal, grid):
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-direction movement
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: heuristic(start, goal)}
        open_heap = []
        heapq.heappush(open_heap, (fscore[start], start))
        
        while open_heap:
            current = heapq.heappop(open_heap)[1]
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                
                # Check boundaries
                if not (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])):
                    continue
                
                # Check if walkable (0 = walkable, 1 = obstacle)
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                
                tentative_g = gscore[current] + 1
                
                if neighbor in close_set and tentative_g >= gscore.get(neighbor, float('inf')):
                    continue
                
                if tentative_g < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g
                    fscore[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (fscore[neighbor], neighbor))
        
        return []  # No path found

    if game_state == SEEKING:
        # Update animation
        seeker_animation_timer += 0.2
        if seeker_animation_timer >= animation_speed * FPS:
            seeker_animation_frame = (seeker_animation_frame + 1) % 2
            seeker_animation_timer = 0
        
        # Create grid representation (1-time per frame)
        grid_width = 1280 // 60
        grid_height = (700 - 180) // 60
        grid = [[0 for _ in range(grid_height)] for _ in range(grid_width)]
        
        # Mark obstacles
        for (x, y, _) in random_tuples:
            grid_x = x // 60
            grid_y = (y - 180) // 60
            if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
                grid[grid_x][grid_y] = 1
        
        # Convert positions to grid coordinates
        start = (seeker_rect.centerx // 60, (seeker_rect.centery - 180) // 60)
        goal = (hun_rect.centerx // 60, (hun_rect.centery - 180) // 60)
        
        # Find path using A*
        path = a_star_search(start, goal, grid)
                
        if len(path) > 0:  # Follow A* path when not too close
            next_step = path[0]  # Get next step in path
            target_x = next_step[0] * 60 + 30
            target_y = next_step[1] * 60 + 210
            
            # Calculate direction vector
            dx = target_x - seeker_rect.centerx
            dy = target_y - seeker_rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5)
            
            # Move with adaptive speed
            seeker_rect.x += int(seeker_speed * dx/dist)
            seeker_rect.y += int(seeker_speed * dy/dist)
            
            # Update direction
            if abs(dx) > abs(dy):
                seeker_direction = 'right' if dx > 0 else 'left'
            else:
                seeker_direction = 'down' if dy > 0 else 'up'
        
        # Screen boundary check
        seeker_rect.x = max(0, min(seeker_rect.x, 1300))
        seeker_rect.y = max(180, min(seeker_rect.y, 800))
        
        # Collision detection with player (using center distance)
        if (abs(seeker_rect.centerx - hun_rect.centerx) < 60 and 
            abs(seeker_rect.centery - hun_rect.centery) < 60):
            game_state = GAME_OVER
            game_result = "lose"
            if not no_sound:
                lose_sound.play()

def draw_initial_seeker_pos():
    if game_state == HIDING and show_initial_pos and initial_seeker_pos:
        # Vẽ một vòng tròn đánh dấu vị trí
        pygame.draw.circle(DISPLAYSURF, YELLOW, 
                          (initial_seeker_pos[0] + 15, initial_seeker_pos[1] + 15), 
                          20, 2)
        # Vẽ chữ "Seeker"
        font = pygame.font.SysFont(None, 24)
        text = font.render("Seeker", True, YELLOW)
        DISPLAYSURF.blit(text, (initial_seeker_pos[0] - 10, initial_seeker_pos[1] - 25))
        
def draw_path():
    for step in path:
        x = step[0] * 60
        y = step[1] * 60 + 180
        # Vẽ một hình chữ nhật mờ đỏ lên ô đường đi
        s = pygame.Surface((60, 60), pygame.SRCALPHA)
        s.fill((255, 0, 0, 100))  # Màu đỏ với độ trong suốt
        DISPLAYSURF.blit(s, (x, y))
def draw_timer():
    font = pygame.font.SysFont(None, 36)
    if game_state == SEEKING:
        timer_text = f"Thời gian tìm: {max(0, int(seeking_timer))}s"
        color = RED
    else:
        return
    
    text_surface = font.render(timer_text, True, color)
    DISPLAYSURF.blit(text_surface, (10, 10))
    
def draw_instructions():
    font = pygame.font.SysFont(None, 24)
    if game_state == HIDING:
        instruction = "Find a hiding spot and press 'Enter' when ready" 
        color = WHITE
    elif game_state == SEEKING:
        instruction = "Người tìm đang tìm bạn!"
        color = WHITE
    else:
        return
    
    text_surface = font.render(instruction, True, color)
    DISPLAYSURF.blit(text_surface, (10, 50))

def draw_main_menu():
    # Vẽ nền
    DISPLAYSURF.blit(mainbackground, (0, 0))
    
    # Vẽ tiêu đề
    font = pygame.font.SysFont(None, 72)
    title = font.render("Hide And Seek", True, WHITE)
    DISPLAYSURF.blit(title, (DISPLAYSURF.get_width()//2 - title.get_width()//2, 100))
    
    # Lấy vị trí chuột
    mouse_pos = pygame.mouse.get_pos()
    
    # Vẽ nút Play (có hiệu ứng hover)
    play_rect = pygame.Rect(DISPLAYSURF.get_width()//2 - 100, 250, 200, 50)
    if play_rect.collidepoint(mouse_pos):
        DISPLAYSURF.blit(play_button_hover, play_rect)
    else:
        DISPLAYSURF.blit(play_button, play_rect)
    
    # Vẽ nút Rules
    rules_rect = pygame.Rect(DISPLAYSURF.get_width()//2 - 100, 320, 200, 50)
    if rules_rect.collidepoint(mouse_pos):
        DISPLAYSURF.blit(rule_button_hover, rules_rect)
    else:
        DISPLAYSURF.blit(rule_button, rules_rect)
    
    # Vẽ nút Settings
    settings_rect = pygame.Rect(DISPLAYSURF.get_width()//2 - 100, 390, 200, 50)
    if settings_rect.collidepoint(mouse_pos):
        DISPLAYSURF.blit(settings_button_hover, settings_rect)
    else:
        DISPLAYSURF.blit(settings_button, settings_rect)
    
    return play_rect, rules_rect, settings_rect

def draw_rules():
    # Vẽ nền
    DISPLAYSURF.blit(setbackground, (0,0))
    
    # Vẽ tiêu đề
    font_large = pygame.font.SysFont(None, 72)
    title = font_large.render("GAME'S RULE", True, WHITE)
    DISPLAYSURF.blit(title, (DISPLAYSURF.get_width()//2 - title.get_width()//2, 50))
    
    # Vẽ nội dung hướng dẫn
    font_small = pygame.font.SysFont(None, 28)
    rules = [  
    "1. You are the hider (red color)",  
    "2. You have 15 seconds to find a hiding spot",  
    "3. Press ENTER when you're ready",  
    "4. The seeker (blue color) will try to find you",  
    "5. If you're found within 30 seconds, you lose",  
    "6. If time runs out and you're not found, you win!",  
    "",  
    "Controls: Arrow keys to move"  
    ]  
    
    for i, rule in enumerate(rules):
        text = font_small.render(rule, True, WHITE)
        DISPLAYSURF.blit(text, (100, 150 + i * 40))
    
    # Vẽ nút back
    mouse_pos = pygame.mouse.get_pos()
    back_rect = pygame.Rect(50, 50, 100, 40)
    if back_rect.collidepoint(mouse_pos):
        DISPLAYSURF.blit(back_button_hover, back_rect)
    else:
        DISPLAYSURF.blit(back_button, back_rect)
    
    return back_rect

def draw_settings():
    # Vẽ nền
    DISPLAYSURF.blit(setbackground, (0,0))
    
    # Vẽ tiêu đề
    font_large = pygame.font.SysFont(None, 72)
    title = font_large.render("CÀI ĐẶT", True, WHITE)
    DISPLAYSURF.blit(title, (DISPLAYSURF.get_width()//2 - title.get_width()//2, 50))
    
    # Vẽ nội dung cài đặt (có thể thêm các tùy chọn sau)
    font_small = pygame.font.SysFont(None, 36)
    text = font_small.render("Tính năng đang phát triển...", True, WHITE)
    DISPLAYSURF.blit(text, (DISPLAYSURF.get_width()//2 - text.get_width()//2, 200))
    
    # Vẽ nút back
    mouse_pos = pygame.mouse.get_pos()
    back_rect = pygame.Rect(50, 50, 100, 40)
    if back_rect.collidepoint(mouse_pos):
        DISPLAYSURF.blit(back_button_hover, back_rect)
    else:
        DISPLAYSURF.blit(back_button, back_rect)
    
    return back_rect

def draw_game_over():
    # Vẽ nền mờ
    s = pygame.Surface((1260, 700), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))  # Màu đen với độ trong suốt
    DISPLAYSURF.blit(s, (0, 0))
    
    font_large = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    if game_result == "win":
        result_text = "HIDER WIN!"
        color = GREEN
        message = "SEEKER CAN NOT FOUND YOU!"
        if not no_sound and not win_sound.get_num_channels():
            win_sound.play()
    else:
        result_text = "SEEKER WIN!"
        color = RED
        message = "HIDER ARE FOUND!"
    
    # Vẽ kết quả
    text_surface = font_large.render(result_text, True, color)
    text_rect = text_surface.get_rect(center=(630, 300))
    DISPLAYSURF.blit(text_surface, text_rect)
    
    # Vẽ thông báo
    msg_surface = font_small.render(message, True, WHITE)
    msg_rect = msg_surface.get_rect(center=(630, 380))
    DISPLAYSURF.blit(msg_surface, msg_rect)
    
    # Vẽ hướng dẫn chơi lại
    restart_surface = font_small.render("PRESS 'R' TO PLAY AGAIN OR 'ESC' TO QUIT!", True, WHITE)
    restart_rect = restart_surface.get_rect(center=(630, 450))
    DISPLAYSURF.blit(restart_surface, restart_rect)

def reset_game():
    global game_state, seeking_timer, game_result
    global hun_rect, seeker_rect, seeker_direction
    global animation_frame, animation_timer, seeker_animation_frame, seeker_animation_timer
    global initial_seeker_pos, show_initial_pos
    
    game_state = HIDING
    seeking_timer = SEEKING_TIME
    game_result = None
    show_initial_pos = True
    # Reset vị trí người chơi
    hun_rect = seeker_animations['idle'][0].get_rect(topleft=(0, 180))
    current_dir = 'down'
    animation_frame = 0
    animation_timer = 0
    
    # Reset vị trí người tìm (seeker) ở vị trí ngẫu nhiên
    # Tạo danh sách các vị trí hợp lệ (không trùng với block)
    valid_positions = []
    for x in range(0, 1231, 60):  # Bước nhảy 60px
        for y in range(180, 601, 60):
            valid = True
            for (bx, by, _) in random_tuples:
                if abs(x - bx) < 60 and abs(y - by) < 60:
                    valid = False
                    break
            if valid:
                valid_positions.append((x, y))
    
    # Chọn vị trí ngẫu nhiên cho seeker
    if valid_positions:
        rand_x, rand_y = random.choice(valid_positions)
        seeker_rect = pygame.Rect(rand_x, rand_y, 30, 30)
    else:
        seeker_rect = pygame.Rect(0, 180, 30, 30)  # Fallback nếu không tìm được vị trí
    
    seeker_direction = 'right'
    seeker_animation_frame = 0
    seeker_animation_timer = 0
    initial_seeker_pos = (seeker_rect.x, seeker_rect.y)

# Vòng lặp chính
last_time = time.time()
running = True

while running:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            running = False
        if game_state >= 0 and game_state <3:
            game_music.stop()
            background_music.play(-1)
        if event.type == MOUSEBUTTONDOWN:
            
            if game_state == MAIN_MENU:
                click_sound.play()
                play_rect, rules_rect, settings_rect = draw_main_menu()
                if play_rect.collidepoint(event.pos):
                    click_sound.play()
                    game_state = HIDING
                    background_music.stop()
                    game_music.play(-1)
                elif rules_rect.collidepoint(event.pos):
                    click_sound.play()
                    game_state = RULES
                elif settings_rect.collidepoint(event.pos):
                    click_sound.play()
                    game_state = SETTINGS
            
            elif game_state == RULES:
                back_rect = draw_rules()
                if back_rect.collidepoint(event.pos):
                    
                    click_sound.play()
                    game_state = MAIN_MENU
            
            elif game_state == SETTINGS:
                back_rect = draw_settings()
                if back_rect.collidepoint(event.pos):
                    
                    click_sound.play()
                    game_state = MAIN_MENU
        
        if event.type == KEYDOWN:
            if event.key == K_RETURN and game_state == HIDING:
                
                click_sound.play()
                game_state = SEEKING
                show_initial_pos = False 
            elif event.key == K_r and game_state == GAME_OVER:
                
                click_sound.play()
                reset_game()
            elif event.key == K_ESCAPE:
                if game_state == MAIN_MENU:
                    running = False
                else:
                    
                    click_sound.play()
                    game_state = MAIN_MENU

        # Cập nhật bộ đếm thời gian (chỉ còn seeking timer)
    if game_state == SEEKING:
        seeking_timer -= delta_time
        if seeking_timer <= 0:
            game_state = GAME_OVER
            game_result = "win"
            if not no_sound:
                win_sound.play()

    # Xử lý di chuyển
    keys = pygame.key.get_pressed()
    if game_state == HIDING:  # Chỉ cho di chuyển trong pha trốn
        move(keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT])
    
    # Di chuyển người tìm trong pha tìm kiếm
    if game_state == SEEKING:
        move_seeker()

        # Vẽ mọi thứ
    if game_state == MAIN_MENU:
        draw_main_menu()
    elif game_state == RULES:
        draw_rules()
    elif game_state == SETTINGS:
        draw_settings()
    else:
        # Vẽ background
        DISPLAYSURF.blit(background, (0, 0))
        DISPLAYSURF.blit(ground, (0, 160))

        # Vẽ các block
        for x, y, t in random_tuples:
            if t == 0:
                DISPLAYSURF.blit(block, (x, y))
            elif t == 1:
                DISPLAYSURF.blit(block1, (x, y))
            else:
                DISPLAYSURF.blit(block2, (x, y))

        # Vẽ vị trí ban đầu của seeker
        if game_state == HIDING and show_initial_pos:
            draw_initial_seeker_pos()

        # Vẽ người chơi (hider)
        if any([keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT]]) and game_state == HIDING:
            current_image = hider_animations[current_dir][animation_frame]
        else:
            current_image = hider_animations['idle'][0]
        DISPLAYSURF.blit(current_image, hun_rect)

        # Vẽ seeker và đường đi
        if game_state == SEEKING or game_state == GAME_OVER:
            draw_path()
            seeker_image = seeker_animations[seeker_direction][seeker_animation_frame]
            DISPLAYSURF.blit(seeker_image, seeker_rect)

        # Vẽ UI
        draw_timer()
        if game_state != GAME_OVER:
            draw_instructions()
        else:
            draw_game_over()
    
    pygame.display.update()
    fpsclock.tick(FPS)

pygame.quit()
sys.exit()
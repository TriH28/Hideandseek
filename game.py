import pygame, sys, random, time, os, heapq
from pygame.locals import *
from collections import deque
import math

# Khởi tạo pygame
pygame.init()


# Cài đặt cửa sổ game
DISPLAYSURF = pygame.display.set_mode((1260, 670))
pygame.display.set_caption("Hide And Seek - Algorithm Comparison")
footstep = 20
path = []

# Trạng thái game
MAIN_MENU = 0
RULES = 1
SETTINGS = 2
HIDING = 3
SEEKING = 4
GAME_OVER = 5
game_state = MAIN_MENU
DIFFICULTY_LEVEL = 3  # 1: Dễ, 2: Trung bình, 3: Khó
difficulty_changed = False

# Cài đặt game
SEEKING_TIME = 25 

seeking_timer = SEEKING_TIME
game_result = None  
# Thêm vào phần khai báo biến toàn cục
initial_seeker_pos = None
show_initial_pos = True  

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (191, 17, 17)
BLUE = (83, 157, 176)
GREEN = (83, 176, 86)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 165, 0)]
# FPS
fpsclock = pygame.time.Clock()
FPS = 30 


# Load hình ảnh
def load_image(path, size=None):
    full_path = os.path.join(os.path.dirname(__file__), path)
    try:
        img = pygame.image.load(full_path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        print(f"Không tìm thấy ảnh tại {full_path}")
        return None

# Đường dẫn hình ảnh
image_path = "Image"

# Background
background = load_image(os.path.join(image_path, "Background.jpg"), (1260, 200))
ground = load_image(os.path.join(image_path, "Ground.png"), (1260, 540))
mainbackground = load_image(os.path.join(image_path, "menubackground.jpg"), (1260, 700))
setbackground = load_image(os.path.join(image_path, "setBackground.jpg"), (1260,700))
ranking = load_image(os.path.join(image_path, "Card X5.png"), (460, 350))

# Blocks
block = load_image(os.path.join(image_path, "Block.png"), (60, 60))
block1 = load_image(os.path.join(image_path, "Block.png"), (60, 60))
block2 = load_image(os.path.join(image_path, "Block2.png"), (60, 60))
block3 = load_image(os.path.join(image_path, "Block3.png"), (60, 60))
block4 = load_image(os.path.join(image_path, "Block2.png"), (60, 60))
block5 = load_image(os.path.join(image_path, "Block.png"), (60, 60))

# Hunter animations (người trốn)
hunD1 = load_image(os.path.join(image_path, "Hun","HunterD1.png"))
hunD2 = load_image(os.path.join(image_path, "Hun","HunterD2.png"))
hunU1 = load_image(os.path.join(image_path, "Hun", "HunterU1.png"))
hunU2 = load_image(os.path.join(image_path, "Hun", "HunterU2.png"))
hunLR1 = load_image(os.path.join(image_path, "Hun", "HunterLR1.png"))
hunLR2 = load_image(os.path.join(image_path, "Hun", "HunterLR2.png"))
hunS = load_image(os.path.join(image_path, "Hun", "HunterS.png"))

# Seeker animations (người tìm)
hiderD1 = load_image(os.path.join(image_path, "Sur", "SurD1.png"))
hiderD2 = load_image(os.path.join(image_path, "Sur", "SurD2.png"))
hiderU1 = load_image(os.path.join(image_path, "Sur", "SurU1.png"))
hiderU2 = load_image(os.path.join(image_path, "Sur", "SurU2.png"))
hiderLR1 = load_image(os.path.join(image_path, "Sur","SurLR1.png"))
hiderLR2 = load_image(os.path.join(image_path, "Sur", "SurLR2.png"))
hider_idle = load_image(os.path.join(image_path, "Sur", "SurS.png"))

# Nút bấm
play_button = load_image(os.path.join(image_path, "Button","play.png"), (250,60 ))
play_button_hover = load_image(os.path.join(image_path, "Button","play_hover.png"), (250, 60))
rule_button = load_image(os.path.join(image_path, "Button","rule.png"), (250, 60))
rule_button_hover = load_image(os.path.join(image_path, "Button","rule_hover.png"), (250, 60))
settings_button = load_image(os.path.join(image_path, "Button","Set.png"), (250, 60))
settings_button_hover = load_image(os.path.join(image_path, "Button","Set_hover.png"), (250, 60))
back_button = load_image(os.path.join(image_path, "Button","back.png"), (150, 50))
back_button_hover = load_image(os.path.join(image_path, "Button","back_hover.png"), (150, 50))

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
animation_speed = 0.05
hider_direction = 'right'
hider_animation_frame = 0
hider_animation_timer = 0

# Hider properties
hider_rect = pygame.Rect(0, 180, 30, 30)
hider_speed = 2

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
    global current_dir, animation_frame, animation_timer, hider_rect
    
    new_rect = hider_rect.copy()
    moving = False
    
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

    # Cập nhật animation
    if moving:
        animation_timer += 1
        if animation_timer >= animation_speed * FPS:
            animation_frame = (animation_frame + 1) % 2
            animation_timer = 0
    else:
        animation_frame = 0
        animation_timer = 0

    # Kiểm tra va chạm
    collision = False
    for (x, y, _) in random_tuples:
        block_rect = pygame.Rect(x, y, 60, 60)
        if new_rect.colliderect(block_rect):
            collision = True
            break

    if not collision and 0 <= new_rect.x <= 1230 and 180 <= new_rect.y <= 640:
        hider_rect = new_rect

class Seeker:
    def __init__(self, x, y, color, algorithm_name):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = color
        self.algorithm_name = algorithm_name
        self.found = False
        self.search_time = 0
        self.path = []
        self.current_path_index = 0
        self.start_time = None
        self.direction = 'right'
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.05
        self.speed = 2.5
        self.show_path = False
        
    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed * FPS:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0
            
    def move(self, hider_pos):
        if self.found:
            return

        if not self.start_time:
            self.start_time = time.time()

        # Cập nhật animation
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed * FPS:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0
            
        if not self.path or self.current_path_index >= len(self.path):
            self.path = self.find_path(hider_pos)
            self.current_path_index = 0

        if self.path:
            next_pos = self.path[self.current_path_index]
            target_x = next_pos[0]
            target_y = next_pos[1]
            
            # Tính toán hướng di chuyển
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            dist = max(1, (dx**2 + dy**2)**0.5)
            
            # Di chuyển
            self.rect.x += int(self.speed * dx/dist)
            self.rect.y += int(self.speed * dy/dist)
            
            # Cập nhật hướng
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'
            
            # Kiểm tra nếu đã đến vị trí tiếp theo
            if (abs(self.rect.x - target_x) < 5 and 
                abs(self.rect.y - target_y) < 5):
                self.current_path_index += 1

            # Kiểm tra xem đã tìm thấy hider chưa
            if abs(self.rect.x - hider_pos[0]) < 30 and abs(self.rect.y - hider_pos[1]) < 30:
                self.found = True
                self.search_time = time.time() - self.start_time

    def find_path(self, hider_pos):
        if self.algorithm_name == "BFS":
            return self.bfs_search(hider_pos)
        elif self.algorithm_name == "A*":
            return self.a_star_search(hider_pos)
        elif self.algorithm_name == "Backtracking":
            return self.backtracking_search(hider_pos)
        elif self.algorithm_name == "Partial Observation":
            return self.partial_observation_search(hider_pos)
        elif self.algorithm_name == "Simple Hill":
            return self.simple_hill_search(hider_pos)
        return []

    def bfs_search(self, goal):
        start = (self.rect.x, self.rect.y)
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            if abs(current[0] - goal[0]) < 30 and abs(current[1] - goal[1]) < 30:
                return path
                
            for dx, dy in [(0, 30), (30, 0), (0, -30), (-30, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] <= 1230 and 180 <= next_pos[1] <= 640 and 
                    next_pos not in visited and not self.check_collision(next_pos)):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        return []

    def a_star_search(self, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
            
        start = (self.rect.x, self.rect.y)
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            if abs(current[0] - goal[0]) < 30 and abs(current[1] - goal[1]) < 30:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
                
            for dx, dy in [(0, 30), (30, 0), (0, -30), (-30, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] <= 1230 and 180 <= next_pos[1] <= 640 and 
                    not self.check_collision(next_pos)):
                    tentative_g_score = g_score[current] + 1
                    if next_pos not in g_score or tentative_g_score < g_score[next_pos]:
                        came_from[next_pos] = current
                        g_score[next_pos] = tentative_g_score
                        f_score[next_pos] = tentative_g_score + heuristic(next_pos, goal)
                        heapq.heappush(open_set, (f_score[next_pos], next_pos))
        return []

    def backtracking_search(self, goal):
        """Triển khai backtracking theo chuẩn CSP với giới hạn độ sâu"""
        start = (self.rect.x, self.rect.y)
        max_depth = 100
        path = []
        visited = set()

        def heuristic(pos):
            """Heuristic khoảng cách Manhattan"""
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

        def backtrack(current, depth):
            nonlocal path
            
            # Kiểm tra mục tiêu
            if abs(current[0] - goal[0]) < 30 and abs(current[1] - goal[1]) < 30:
                return True
                
            # Giới hạn độ sâu
            if depth >= max_depth:
                return False
                
            visited.add(current)
            
            # Tạo danh sách hướng đi kế tiếp và sắp xếp theo heuristic
            next_moves = []
            for dx, dy in [(0, 30), (30, 0), (0, -30), (-30, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] <= 1230 and 180 <= next_pos[1] <= 640 and 
                    next_pos not in visited and not self.check_collision(next_pos)):
                    next_moves.append(next_pos)
            
            # Sắp xếp theo heuristic (ưu tiên hướng gần mục tiêu)
            next_moves.sort(key=heuristic)

            # Thử từng hướng đi
            for next_pos in next_moves:
                path.append(next_pos)
                if backtrack(next_pos, depth + 1):
                    return True
                path.pop()  

            visited.remove(current)  
            return False

        if backtrack(start, 0):
            return path
        return []
    def partial_observation_search(self, goal):
        vision_radius = 150
        start = (self.rect.x, self.rect.y)
        
        # Nếu đã từng thấy mục tiêu, lưu lại vị trí cuối cùng
        if not hasattr(self, 'last_known_pos'):
            self.last_known_pos = None
            self.belief_map = {} 
        
        # Kiểm tra nếu mục tiêu trong tầm nhìn
        if (abs(start[0] - goal[0]) < vision_radius and 
            abs(start[1] - goal[1]) < vision_radius):
            self.last_known_pos = goal
            return self.a_star_search(goal)
        
        # Nếu có thông tin về vị trí cuối cùng của mục tiêu
        if self.last_known_pos:
            # Cập nhật belief map - giảm dần độ tin cậy theo thời gian
            for pos in self.belief_map:
                self.belief_map[pos] *= 0.9 
            
            # Thêm vị trí mới với xác suất cao
            self.belief_map[self.last_known_pos] = self.belief_map.get(self.last_known_pos, 0) + 0.5
            
            # Chọn vị trí có xác suất cao nhất
            most_likely_pos = max(self.belief_map.items(), key=lambda x: x[1])[0]
            return self.a_star_search(most_likely_pos)
        else:
            # Chiến lược khám phá khi không có thông tin
            possible_moves = []
            unexplored_directions = []
            
            # Ưu tiên di chuyển đến khu vực chưa khám phá
            for dx, dy in [(0, 30), (30, 0), (0, -30), (-30, 0)]:
                next_pos = (start[0] + dx, start[1] + dy)
                if (0 <= next_pos[0] <= 1230 and 180 <= next_pos[1] <= 640 and 
                    not self.check_collision(next_pos)):
                    
                    # Đánh giá hướng này có khả năng chứa mục tiêu không
                    score = 0
                    
                    # Ưu tiên hướng xa tường và trung tâm
                    dist_to_wall = min(
                        next_pos[0], 1230 - next_pos[0],
                        next_pos[1] - 180, 640 - next_pos[1]
                    )
                    score += dist_to_wall * 0.1
                    
                    # Ưu tiên di chuyển về phía trung tâm
                    center_x, center_y = 630, 410
                    dist_to_center = abs(next_pos[0] - center_x) + abs(next_pos[1] - center_y)
                    score += (1000 - dist_to_center) * 0.05
                    
                    unexplored_directions.append((next_pos, score))
            
            if unexplored_directions:
                # Chọn hướng có điểm cao nhất
                best_move = max(unexplored_directions, key=lambda x: x[1])[0]
                return [best_move]
        
        # Fallback: di chuyển ngẫu nhiên nếu không có lựa chọn nào tốt
        possible_moves = []
        for dx, dy in [(0, 30), (30, 0), (0, -30), (-30, 0)]:
            next_pos = (start[0] + dx, start[1] + dy)
            if (0 <= next_pos[0] <= 1230 and 180 <= next_pos[1] <= 640 and 
                not self.check_collision(next_pos)):
                possible_moves.append(next_pos)
        
        return [random.choice(possible_moves)] if possible_moves else []

    def simple_hill_search(self, goal, max_attempts=100):
        def get_score(pos):
            return -((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)  

        def is_goal(pos):
            return abs(pos[0] - goal[0]) < 30 and abs(pos[1] - goal[1]) < 30

        current = (self.rect.x, self.rect.y)
        path = [current]

        for _ in range(max_attempts):
            if is_goal(current):
                return path

            neighbors = []
            for dx, dy in [(0, 30), (30, 0), (0, -30), (-30, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] <= 1230 and 180 <= next_pos[1] <= 640 
                    and not self.check_collision(next_pos)):
                    neighbors.append(next_pos)

            if not neighbors:
                break  

            best_neighbor = max(neighbors, key=get_score)
            if get_score(best_neighbor) <= get_score(current):
                break  

            current = best_neighbor
            path.append(current)

        return path

    def check_collision(self, pos):
        for (x, y, _) in random_tuples:
            block_rect = pygame.Rect(x, y, 60, 60)
            if pygame.Rect(pos[0], pos[1], 30, 30).colliderect(block_rect):
                return True
        return False

# Tạo các seeker
seekers = [
    Seeker(0, 180, COLORS[0], "BFS"),
    Seeker(30, 180, COLORS[1], "A*"),
    Seeker(60, 180, COLORS[2], "Backtracking"),
    Seeker(90, 180, COLORS[3], "Partial Observation"),
    Seeker(120, 180, COLORS[4], "Simple Hill")
]
#Class Q-learning
class QLearningSeeker(Seeker):
    def __init__(self, x, y, color, algorithm_name):
        super().__init__(x, y, color, algorithm_name)
        self.q_table = {}  
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.3
        self.last_state = None
        self.last_action = None
        
    def get_state(self, hider_pos):
        """Chuyển trạng thái hiện tại thành một tuple đơn giản"""
        # Làm tròn vị trí về các ô 30x30 để giảm số lượng trạng thái
        rounded_x = (self.rect.x // 30) * 30
        rounded_y = (self.rect.y // 30) * 30
        hider_rounded_x = (hider_pos[0] // 30) * 30
        hider_rounded_y = (hider_pos[1] // 30) * 30
        return (rounded_x, rounded_y, hider_rounded_x, hider_rounded_y)
    
    def get_possible_actions(self):
        """Trả về các hành động có thể thực hiện từ vị trí hiện tại"""
        actions = []
        for dx, dy, action in [(0, 30, 'down'), (30, 0, 'right'), 
                              (0, -30, 'up'), (-30, 0, 'left')]:
            new_pos = (self.rect.x + dx, self.rect.y + dy)
            if (0 <= new_pos[0] <= 1230 and 180 <= new_pos[1] <= 640 and 
                not self.check_collision(new_pos)):
                actions.append(action)
        return actions
    
    def choose_action(self, state, hider_pos):
        """Chọn hành động dựa trên Q-table và exploration rate"""
        possible_actions = self.get_possible_actions()
        if not possible_actions:
            return None
            
        # Khám phá ngẫu nhiên
        if random.random() < self.exploration_rate:
            return random.choice(possible_actions)
            
        # Khai thác: chọn hành động có giá trị Q cao nhất
        q_values = []
        for action in possible_actions:
            q_value = self.q_table.get((state, action), 0)
            q_values.append((q_value, action))
            
        # Chọn hành động có Q-value cao nhất
        max_q = max(q_values, key=lambda x: x[0])[0]
        best_actions = [action for q, action in q_values if q == max_q]
        return random.choice(best_actions)
    
    def update_q_table(self, state, action, reward, next_state):
        """Cập nhật Q-table dựa trên phần thưởng nhận được"""
        current_q = self.q_table.get((state, action), 0)
        
        # Tìm Q-value lớn nhất cho trạng thái tiếp theo
        max_next_q = 0
        possible_next_actions = self.get_possible_actions()
        if possible_next_actions:
            max_next_q = max([self.q_table.get((next_state, a), 0) 
                            for a in possible_next_actions])
        
        # Công thức Q-learning
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q
    
    def get_reward(self, hider_pos):
        """Tính phần thưởng dựa trên khoảng cách tới hider"""
        distance = abs(self.rect.x - hider_pos[0]) + abs(self.rect.y - hider_pos[1])
        if distance < 30:  
            return 100
        return -distance / 100  
    
    def find_path(self, hider_pos):
        """Triển khai Q-learning để tìm đường"""
        current_state = self.get_state(hider_pos)
        possible_actions = self.get_possible_actions()
        
        if not possible_actions:
            return []
            
        # Chọn hành động
        action = self.choose_action(current_state, hider_pos)
        if not action:
            return []
            
        # Thực hiện hành động
        dx, dy = 0, 0
        if action == 'up':
            dy = -30
        elif action == 'down':
            dy = 30
        elif action == 'left':
            dx = -30
        elif action == 'right':
            dx = 30
            
        next_pos = (self.rect.x + dx, self.rect.y + dy)
        
        # Tính phần thưởng
        reward = self.get_reward(hider_pos)
        
        # Cập nhật Q-table nếu có trạng thái và hành động trước đó
        if self.last_state and self.last_action:
            self.update_q_table(self.last_state, self.last_action, 
                               reward, current_state)
        
        # Lưu trạng thái và hành động hiện tại cho lần sau
        self.last_state = current_state
        self.last_action = action
        
        return [next_pos]
def draw_game():
    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(ground, (0, 200))
    
    # Vẽ các block
    for x, y, block_type in random_tuples:
        if block_type == 0:
            DISPLAYSURF.blit(block, (x, y))
        elif block_type == 1:
            DISPLAYSURF.blit(block1, (x, y))
        elif block_type == 2:
            DISPLAYSURF.blit(block2, (x, y))
        elif block_type == 3:
            DISPLAYSURF.blit(block3, (x, y))
        elif block_type == 4:
            DISPLAYSURF.blit(block4, (x, y))
        elif block_type == 5:
            DISPLAYSURF.blit(block5, (x, y))
    
    # Vẽ hider với animation
    keys = pygame.key.get_pressed()
    if any([keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT]]) and game_state == HIDING:
        current_image = hider_animations[current_dir][animation_frame]
    else:
        current_image = hider_animations['idle'][0]
    DISPLAYSURF.blit(current_image, hider_rect)
    
    # Vẽ đường đi của seekers (nếu cần)
    for seeker in seekers:
        if seeker.show_path:
            for step in seeker.path:
                x = step[0]
                y = step[1]
                s = pygame.Surface((30, 30), pygame.SRCALPHA)
                s.fill((*seeker.color, 100))  
                DISPLAYSURF.blit(s, (x, y))
    
    # Vẽ các seeker với animation
    for seeker in seekers:
        # Thêm hiển thị độ khó
        font = pygame.font.Font(None, 36)
        difficulty_text = font.render(f"Difficulty: {['Easy', 'Medium', 'Hard'][DIFFICULTY_LEVEL-1]}", True, WHITE)
        DISPLAYSURF.blit(difficulty_text, (1000, 10))
        if not seeker.found:
            seeker.update_animation()
            current_image = seeker_animations[seeker.direction][seeker.animation_frame]
            DISPLAYSURF.blit(current_image, seeker.rect)
        else:
            # Khi đã tìm thấy, có thể hiển thị hình ảnh khác
            DISPLAYSURF.blit(seeker_animations['idle'][0], seeker.rect)
        
        # Vẽ tên thuật toán
        font = pygame.font.Font(None, 24)
        text = font.render(seeker.algorithm_name, True, WHITE)
        DISPLAYSURF.blit(text, (seeker.rect.x, seeker.rect.y - 20))
        
        # Nếu đã tìm thấy, hiển thị thời gian
        if seeker.found:
            time_text = font.render(f"{seeker.search_time:.2f}s", True, WHITE)
            DISPLAYSURF.blit(time_text, (seeker.rect.x, seeker.rect.y + 30))

def draw_results():
    # Vẽ bảng kết quả
    DISPLAYSURF.blit(ranking, (400, 200))

    font = pygame.font.Font(None, 36)
    win = False
    for seeker in seekers:
        if seeker.found:
            win = True
            break
    if win:
        title = font.render("Rank", True, WHITE)
        DISPLAYSURF.blit(title, (600, 230))
    
    # Sắp xếp seekers theo thời gian tìm kiếm
        sorted_seekers = sorted([s for s in seekers if s.found], key=lambda x: x.search_time)
    
        y = 280
        for i, seeker in enumerate(sorted_seekers):
            result_text = font.render(f"{i+1}. {seeker.algorithm_name}: {seeker.search_time:.2f}s", True, seeker.color)
            DISPLAYSURF.blit(result_text, (450, y))
            y += 40
    else:
        result_text = font.render("Hider win!", True, WHITE)
        DISPLAYSURF.blit(result_text, (570, 350))

def draw_main_menu():
    DISPLAYSURF.blit(mainbackground, (0, 0))
    
    # Vẽ tiêu đề
    font = pygame.font.Font(None, 74)
    title = font.render("Hide And Seek", True, WHITE)
    DISPLAYSURF.blit(title, (450, 100))
    
    # Vẽ các nút
    mouse_pos = pygame.mouse.get_pos()
    
    # Nút Play
    if 530 <= mouse_pos[0] <= 730 and 300 <= mouse_pos[1] <= 350:
        DISPLAYSURF.blit(play_button_hover, (530, 300))
    else:
        DISPLAYSURF.blit(play_button, (530, 300))
    
    # Nút Rules
    if 530 <= mouse_pos[0] <= 730 and 400 <= mouse_pos[1] <= 450:
        DISPLAYSURF.blit(rule_button_hover, (530, 400))
    else:
        DISPLAYSURF.blit(rule_button, (530, 400))
    
    # Nút Settings
    if 530 <= mouse_pos[0] <= 730 and 500 <= mouse_pos[1] <= 550:
        DISPLAYSURF.blit(settings_button_hover, (530, 500))
    else:
        DISPLAYSURF.blit(settings_button, (530, 500))

def draw_rules():
    DISPLAYSURF.blit(mainbackground, (0, 0))
    
    # Vẽ nút back
    mouse_pos = pygame.mouse.get_pos()
    if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
        pygame.draw.rect(DISPLAYSURF, GREEN, (50, 50, 100, 40))
    else:
        pygame.draw.rect(DISPLAYSURF, GRAY, (50, 50, 100, 40))
    back_text = pygame.font.Font(None, 36).render("Back", True, WHITE)
    DISPLAYSURF.blit(back_text, (70, 60))
    
    # Vẽ nội dung rules
    font = pygame.font.Font(None, 36)
    rules = [
        "How to play:",
        "1. You are the hider",
        "2. Use the arrow keys to move",
        "3. Press ENTER when you have found a hiding place",
        "4. 5 seekers will search for you with different algorithms",
        "5. The result will show the search time of each seeker",
        "6. Press R to play again"
    ]
    
    y = 200
    for rule in rules:
        text = font.render(rule, True, WHITE)
        DISPLAYSURF.blit(text, (100, y))
        y += 50

def draw_settings():
    DISPLAYSURF.blit(setbackground, (0, 0))
    
    # Vẽ nút back
    mouse_pos = pygame.mouse.get_pos()
    if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
        pygame.draw.rect(DISPLAYSURF, GREEN, (50, 50, 100, 40))
    else:
        pygame.draw.rect(DISPLAYSURF, GRAY, (50, 50, 100, 40))
    back_text = pygame.font.Font(None, 36).render("Back", True, WHITE)
    DISPLAYSURF.blit(back_text, (70, 60))
    
    # Vẽ nội dung settings
    font = pygame.font.Font(None, 36)
    settings = [
        "Settings:",
        "Search time: 15 seconds",
        "Number of seekers: 5",
        "Map size: 1260x670"
    ]
    
    y = 200
    for setting in settings:
        text = font.render(setting, True, WHITE)
        DISPLAYSURF.blit(text, (100, y))
        y += 50

def draw_timer():
    font = pygame.font.SysFont(None, 36)
    if game_state == SEEKING:
        timer_text = f"Time to find: {max(0, int(seeking_timer))}s"
        color = RED
    else:
        return
    
    text_surface = font.render(timer_text, True, color)
    DISPLAYSURF.blit(text_surface, (10, 10))

def draw_instructions():
    font = pygame.font.Font(None, 24)
    if game_state == HIDING:
        instruction = "Find a hiding place and press ENTER when ready." 
        color = WHITE
    elif game_state == SEEKING:
        instruction = "Seekers are looking for you"
        color = WHITE
    else:
        return
    
    text_surface = font.render(instruction, True, color)
    DISPLAYSURF.blit(text_surface, (10, 50))

def draw_settings():
    DISPLAYSURF.blit(setbackground, (0, 0))
    
    # Vẽ nút back
    mouse_pos = pygame.mouse.get_pos()
    if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
        DISPLAYSURF.blit(back_button_hover, (50, 50))
    else:
        DISPLAYSURF.blit(back_button, (50, 50))
    
    # Vẽ nội dung settings
    font = pygame.font.Font(None, 36)
    settings = [
        "Settings:",
        f"Difficulty: {['Easy', 'Medium', 'Hard'][DIFFICULTY_LEVEL-1]}",
        "Search time: 15 seconds",
        "Number of seekers: 5",
        "Map size: 1260x670",
        "Click to change difficulty"
    ]
    
    y = 200
    for setting in settings:
        text = font.render(setting, True, WHITE)
        DISPLAYSURF.blit(text, (100, y))
        y += 50
    
    # Vẽ các nút độ khó
    for i in range(3):
        if DIFFICULTY_LEVEL == i+1:
            color = GREEN
        else:
            color = GRAY
        pygame.draw.rect(DISPLAYSURF, color, (400 + i*150, 400, 120, 50))
        diff_text = font.render(["Easy", "Medium", "Hard"][i], True, WHITE)
        DISPLAYSURF.blit(diff_text, (430 + i*150, 415))

def reset_game():
    global game_state, seeking_timer, hider_rect, seekers, random_tuples
    global current_dir, animation_frame, animation_timer, DIFFICULTY_LEVEL, difficulty_changed
    
    # Tạo map mới theo độ khó
    random_tuples = []
    num_blocks = 30  # Số lượng block cơ bản
    
    if DIFFICULTY_LEVEL == 3:  # Dễ
        num_blocks = 25 
        block_range_x = (120, 1080)
        block_range_y = (240, 540)
    elif DIFFICULTY_LEVEL == 2:  # Trung bình
        num_blocks = 35 
        block_range_x = (60, 1140)
        block_range_y = (220, 580)
    else:  # Khó
        num_blocks = 45
        block_range_x = (60, 1140)
        block_range_y = (220, 580)

    # Tạo hider ở vị trí cố định
    hider_rect = pygame.Rect(0, 180, 30, 30)
    
    # Tạo seekers ở cùng 1 vị trí (xếp thành hàng ngang)
    algorithms = ["BFS", "A*", "Backtracking", "Partial Observation", "Simple Hill", "Q-learning"]
    colors = COLORS + [(255, 165, 0)]
    
    seekers = []
    seeker_start_x = 600 # Vị trí xuất phát chung (giữa màn hình)
    seeker_start_y = 180
    
    # Danh sách vị trí cấm (nơi không được đặt block)
    forbidden_positions = [
        (hider_rect.x, hider_rect.y)  # Vị trí hider
    ]
    
    # Thêm vị trí các seekers vào danh sách cấm
    for i in range(6):
        x = seeker_start_x + i * 30  # Xếp các seekers thành hàng ngang
        y = seeker_start_y
        forbidden_positions.append((x, y))
        if algorithms[i] == "Q-learning":
            seekers.append(QLearningSeeker(x, y, colors[i], algorithms[i]))
        else:
            seekers.append(Seeker(x, y, colors[i], algorithms[i]))


    # Tạo các block, đảm bảo không đè lên hider và seekers
    for _ in range(num_blocks):
        while True:
            xStone = random.choice([x for x in range(block_range_x[0], block_range_x[1]+1) if x % 60 == 0])
            yStone = random.choice([x for x in range(block_range_y[0], block_range_y[1]+1) if x % 60 == 0])
            
            # Kiểm tra không trùng với vị trí cấm
            collision = False
            for (fx, fy) in forbidden_positions:
                if abs(xStone - fx) < 90 and abs(yStone - fy) < 90:  # Khoảng cách an toàn 90px
                    collision = True
                    break
            
            # Kiểm tra không trùng với block khác
            if not collision and not any((xStone, yStone) == (t[0], t[1]) for t in random_tuples):
                break
        
        block_type = random.choice([0, 1, 2, 3, 4, 5])
        random_tuples.append((xStone, yStone, block_type))
    
    game_state = HIDING
    seeking_timer = SEEKING_TIME
    current_dir = 'right'
    animation_frame = 0
    animation_timer = 0
    
    difficulty_changed = False

def main():
    global game_state, seeking_timer, current_dir, animation_frame, animation_timer
    global DIFFICULTY_LEVEL, difficulty_changed
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_RETURN and game_state == HIDING:
                    game_state = SEEKING
                    seeking_timer = SEEKING_TIME
                    for seeker in seekers:
                        seeker.start_time = time.time()
                elif event.key == K_r and game_state == GAME_OVER:
                    reset_game()
                elif event.key == K_ESCAPE:
                    if game_state == MAIN_MENU:
                        pygame.quit()
                        sys.exit()
                    else:
                        game_state = MAIN_MENU
            
            if event.type == MOUSEBUTTONDOWN:
                if game_state == MAIN_MENU:
                    mouse_pos = pygame.mouse.get_pos()
                    if 530 <= mouse_pos[0] <= 730 and 300 <= mouse_pos[1] <= 350:
                        reset_game()
                        game_state = HIDING
                    elif 530 <= mouse_pos[0] <= 730 and 400 <= mouse_pos[1] <= 450:
                        game_state = RULES
                    elif 530 <= mouse_pos[0] <= 730 and 500 <= mouse_pos[1] <= 550:
                        game_state = SETTINGS
                elif game_state == SETTINGS:
                    mouse_pos = pygame.mouse.get_pos()
                    if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
                        game_state = MAIN_MENU
                    # Kiểm tra click vào nút độ khó
                    for i in range(3):
                        if 400 + i*150 <= mouse_pos[0] <= 520 + i*150 and 400 <= mouse_pos[1] <= 450:
                            DIFFICULTY_LEVEL = i + 1
                            difficulty_changed = True
                elif game_state in [RULES, SETTINGS]:
                    mouse_pos = pygame.mouse.get_pos()
                    if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
                        game_state = MAIN_MENU
        
        # Nếu độ khó thay đổi, reset game
        if difficulty_changed:
            reset_game()
        
        # Xử lý di chuyển hider
        keys = pygame.key.get_pressed()
        if game_state == HIDING:
            move(keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT])
        
        if game_state == SEEKING:
            seeking_timer -= 1/FPS
            if seeking_timer <= 0:
                game_state = GAME_OVER
               
            
            # Di chuyển các seeker
            for seeker in seekers:
                if not seeker.found:
                    seeker.move((hider_rect.x, hider_rect.y))
            
            # Kiểm tra xem tất cả seekers đã tìm thấy hider chưa
            if all(seeker.found for seeker in seekers):
                game_state = GAME_OVER
                
        
        # Vẽ game
        if game_state == MAIN_MENU:
            draw_main_menu()
        elif game_state == RULES:
            draw_rules()
        elif game_state == SETTINGS:
            draw_settings()
        elif game_state in [HIDING, SEEKING, GAME_OVER]:
            draw_game()
            if game_state == SEEKING:
                draw_timer()
            elif game_state == GAME_OVER:
                draw_results()
            draw_instructions()
        
        pygame.display.update()
        fpsclock.tick(FPS)

if __name__ == "__main__":
    main()

import pygame, sys, random
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1260, 700))
pygame.display.set_caption("Hide And Seek")
footstep = 30

# Màu sắc
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (191, 17, 17)
Blue = (83, 157, 176)
Green = (83, 176, 86)

# FPS
fpsclock = pygame.time.Clock()
fps = 8

# Load hình ảnh
background = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Background.jpg")
background = pygame.transform.scale(background, (1260, 200))
ground = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Ground.png")
ground = pygame.transform.scale(ground, (1260, 540))

# Load block
block = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Block.png")
block = pygame.transform.scale(block, (60, 60))
block1 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Block.png")
block1 = pygame.transform.scale(block1, (60, 60))
block2 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Block2.png")
block2 = pygame.transform.scale(block2, (60, 60))

# Load Hunter animations
hunD1 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Hun/HunterD1.png").convert_alpha()
hunD2 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Hun/HunterD2.png").convert_alpha()
hunU1 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Hun/HunterU1.png").convert_alpha()
hunU2 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Hun/HunterU2.png").convert_alpha()
hunLR1 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Hun/HunterLR1.png").convert_alpha()
hunLR2 = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Hun/HunterLR2.png").convert_alpha()
hunS = pygame.image.load("/Users/huuhuynh/Desktop/Năm 2 kì 2/Trí tuệ nhân tạo/HideAndSeek/Image/Hun/HunterS.png").convert_alpha()

# Tạo animation dictionary
hunter_animations = {
    'down': [pygame.transform.scale(hunD1, (30, 30)), pygame.transform.scale(hunD2, (30, 30))],
    'up': [pygame.transform.scale(hunU1, (30, 30)), pygame.transform.scale(hunU2, (30, 30))],
    'right': [pygame.transform.scale(hunLR1, (30, 30)), pygame.transform.scale(hunLR2, (30, 30))],
    'left': [pygame.transform.flip(pygame.transform.scale(hunLR1, (30, 30)), True, False),
             pygame.transform.flip(pygame.transform.scale(hunLR2, (30, 30)), True, False)],
    'idle': [pygame.transform.scale(hunS, (30, 30))]
}

# Khởi tạo trạng thái nhân vật
current_dir = 'down'
animation_frame = 0
animation_timer = 0
animation_speed = 1  # Tốc độ animation (càng nhỏ càng nhanh)
hun_rect = hunter_animations['idle'][0].get_rect(topleft = (0,180))

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
    
    # Xác định hướng di chuyển
    if up:
        new_rect.y -= footstep
        current_dir = 'up'
        moving = True
    if down:
        new_rect.y += footstep
        current_dir = 'down'
        moving = True
    if left:
        new_rect.x -= footstep
        current_dir = 'left'
        moving = True
    if right:
        new_rect.x += footstep
        current_dir = 'right'
        moving = True

    # Cập nhật animation
    if moving:
        animation_timer += 1
        if animation_timer >= animation_speed:
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

    if not collision and 0 <= new_rect.x <= 1230 and 180 <= new_rect.y <= 670:
        hun_rect.x = new_rect.x
        hun_rect.y = new_rect.y

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Xử lý di chuyển
    keys = pygame.key.get_pressed()
    move(keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT])

    # Vẽ màn hình
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
    
    # Vẽ nhân vật với animation
    if any([keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT]]):
        current_image = hunter_animations[current_dir][animation_frame]
    else:
        current_image = hunter_animations['idle'][0]
    
    DISPLAYSURF.blit(current_image, hun_rect)
    pygame.display.update()
    fpsclock.tick(fps)
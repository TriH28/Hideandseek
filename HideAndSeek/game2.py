import pygame, sys, random, time
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1260, 700))
pygame.display.set_caption("Hide And Seek")
footstep = 30

# Game states
HIDING = 0
SEEKING = 1
GAME_OVER = 2
game_state = HIDING

# Game settings
HIDING_TIME = 30  # seconds
SEEKING_TIME = 60  # seconds
hiding_timer = HIDING_TIME
seeking_timer = SEEKING_TIME
game_result = None  # "win" or "lose"

# Colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (191, 17, 17)
Blue = (83, 157, 176)
Green = (83, 176, 86)
Yellow = (255, 255, 0)

# FPS
fpsclock = pygame.time.Clock()
fps = 8

# Load images
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

# Create animation dictionary
hunter_animations = {
    'down': [pygame.transform.scale(hunD1, (30, 30)), pygame.transform.scale(hunD2, (30, 30))],
    'up': [pygame.transform.scale(hunU1, (30, 30)), pygame.transform.scale(hunU2, (30, 30))],
    'right': [pygame.transform.scale(hunLR1, (30, 30)), pygame.transform.scale(hunLR2, (30, 30))],
    'left': [pygame.transform.flip(pygame.transform.scale(hunLR1, (30, 30)), True, False),
             pygame.transform.flip(pygame.transform.scale(hunLR2, (30, 30)), True, False)],
    'idle': [pygame.transform.scale(hunS, (30, 30))]
}

# Initialize character state
current_dir = 'down'
animation_frame = 0
animation_timer = 0
animation_speed = 1  # Animation speed (smaller is faster)
hun_rect = hunter_animations['idle'][0].get_rect(topleft=(0, 180))

# Seeker (AI) properties
seeker_rect = pygame.Rect(1230, 670, 30, 30)  # Start at bottom right
seeker_speed = 3
seeker_path = []
seeker_direction = 'left'  # Initial direction

# Create blocks and save positions
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
    
    # Determine movement direction
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

    # Update animation
    if moving:
        animation_timer += 1
        if animation_timer >= animation_speed:
            animation_frame = (animation_frame + 1) % 2
            animation_timer = 0
    else:
        animation_frame = 0
        animation_timer = 0

    # Check collision
    collision = False
    for (x, y, _) in random_tuples:
        block_rect = pygame.Rect(x, y, 60, 60)
        if new_rect.colliderect(block_rect):
            collision = True
            break

    if not collision and 0 <= new_rect.x <= 1230 and 180 <= new_rect.y <= 670:
        hun_rect.x = new_rect.x
        hun_rect.y = new_rect.y

def move_seeker():
    global seeker_rect, seeker_direction, game_state, game_result
    
    # Simple AI: move toward player's last known position
    if game_state == SEEKING:
        # Calculate direction to player
        dx = hun_rect.x - seeker_rect.x
        dy = hun_rect.y - seeker_rect.y
        
        # Normalize direction
        if abs(dx) > abs(dy):
            if dx > 0:
                seeker_direction = 'right'
                seeker_rect.x += seeker_speed
            else:
                seeker_direction = 'left'
                seeker_rect.x -= seeker_speed
        else:
            if dy > 0:
                seeker_direction = 'down'
                seeker_rect.y += seeker_speed
            else:
                seeker_direction = 'up'
                seeker_rect.y -= seeker_speed
        
        # Check collision with blocks
        for (x, y, _) in random_tuples:
            block_rect = pygame.Rect(x, y, 60, 60)
            if seeker_rect.colliderect(block_rect):
                # If collided, choose random direction
                seeker_direction = random.choice(['up', 'down', 'left', 'right'])
                if seeker_direction == 'up':
                    seeker_rect.y -= seeker_speed
                elif seeker_direction == 'down':
                    seeker_rect.y += seeker_speed
                elif seeker_direction == 'left':
                    seeker_rect.x -= seeker_speed
                else:
                    seeker_rect.x += seeker_speed
                break
        
        # Keep seeker within bounds
        seeker_rect.x = max(0, min(seeker_rect.x, 1230))
        seeker_rect.y = max(180, min(seeker_rect.y, 670))
        
        # Check if seeker found hider
        if hun_rect.colliderect(seeker_rect):
            game_state = GAME_OVER
            game_result = "lose"

def draw_timer():
    font = pygame.font.SysFont(None, 36)
    if game_state == HIDING:
        timer_text = f"Hiding Time: {int(hiding_timer)}"
        color = Green
    elif game_state == SEEKING:
        timer_text = f"Seeking Time: {int(seeking_timer)}"
        color = Red
    else:
        return
    
    text_surface = font.render(timer_text, True, color)
    DISPLAYSURF.blit(text_surface, (10, 10))

def draw_instructions():
    font = pygame.font.SysFont(None, 24)
    if game_state == HIDING:
        instruction = "Find a hiding spot and press ENTER when ready"
        color = White
    elif game_state == SEEKING:
        instruction = "Seeker is searching for you!"
        color = White
    else:
        return
    
    text_surface = font.render(instruction, True, color)
    DISPLAYSURF.blit(text_surface, (10, 50))

def draw_game_over():
    font_large = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    if game_result == "win":
        result_text = "You Win!"
        color = Green
        message = "The seeker didn't find you in time!"
    else:
        result_text = "You Lose!"
        color = Red
        message = "The seeker found you!"
    
    # Draw result
    text_surface = font_large.render(result_text, True, color)
    text_rect = text_surface.get_rect(center=(630, 300))
    DISPLAYSURF.blit(text_surface, text_rect)
    
    # Draw message
    msg_surface = font_small.render(message, True, White)
    msg_rect = msg_surface.get_rect(center=(630, 380))
    DISPLAYSURF.blit(msg_surface, msg_rect)
    
    # Draw restart instruction
    restart_surface = font_small.render("Press R to restart or ESC to quit", True, Yellow)
    restart_rect = restart_surface.get_rect(center=(630, 450))
    DISPLAYSURF.blit(restart_surface, restart_rect)

def reset_game():
    global game_state, hiding_timer, seeking_timer, game_result
    global hun_rect, seeker_rect, seeker_direction
    
    game_state = HIDING
    hiding_timer = HIDING_TIME
    seeking_timer = SEEKING_TIME
    game_result = None
    
    # Reset player position
    hun_rect = hunter_animations['idle'][0].get_rect(topleft=(0, 180))
    
    # Reset seeker position
    seeker_rect = pygame.Rect(1230, 670, 30, 30)
    seeker_direction = 'left'

# Main game loop
last_time = time.time()
while True:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_RETURN and game_state == HIDING:
                game_state = SEEKING
            elif event.key == K_r and game_state == GAME_OVER:
                reset_game()
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update timers
    if game_state == HIDING:
        hiding_timer -= delta_time
        if hiding_timer <= 0:
            game_state = SEEKING
    elif game_state == SEEKING:
        seeking_timer -= delta_time
        if seeking_timer <= 0:
            game_state = GAME_OVER
            game_result = "win"

    # Handle movement
    keys = pygame.key.get_pressed()
    if game_state == HIDING:  # Only allow movement during hiding phase
        move(keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT])
    
    # Move seeker during seeking phase
    if game_state == SEEKING:
        move_seeker()

    # Draw everything
    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(ground, (0, 160))
    
    # Draw blocks
    for x, y, t in random_tuples:
        if t == 0:
            DISPLAYSURF.blit(block, (x, y))
        elif t == 1:
            DISPLAYSURF.blit(block1, (x, y))
        else:
            DISPLAYSURF.blit(block2, (x, y))
    
    # Draw player with animation
    if any([keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT]]) and game_state == HIDING:
        current_image = hunter_animations[current_dir][animation_frame]
    else:
        current_image = hunter_animations['idle'][0]
    
    DISPLAYSURF.blit(current_image, hun_rect)
    
    # Draw seeker
    if game_state == SEEKING or game_state == GAME_OVER:
        seeker_image = hunter_animations[seeker_direction][0]  # Simple animation for seeker
        DISPLAYSURF.blit(seeker_image, seeker_rect)
    
    # Draw UI elements
    draw_timer()
    if game_state != GAME_OVER:
        draw_instructions()
    else:
        draw_game_over()
    
    pygame.display.update()
    fpsclock.tick(fps)
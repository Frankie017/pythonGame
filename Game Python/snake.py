import pygame
import sys
import time
import random

# Window size
frame_size_x = 720
frame_size_y = 480

check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)

fps_controller = pygame.time.Clock()

def game_over():
    my_font = pygame.font.SysFont('comicsansms', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'comicsansms', 30)
    pygame.display.flip()
    time.sleep(3)
    show_speed_menu()

////// Moeglichkeit die Geschwindigket auszuwaehlen //////////////////////////////////////////////////////////
def show_speed_menu():
    global difficulty
    game_window.fill(black)
    font = pygame.font.SysFont('comicsansms', 36)
    text = font.render("Please choose the speed:", True, white)
    text_rect = text.get_rect(center=(frame_size_x/2, frame_size_y/2))
    game_window.blit(text, text_rect)
    speed_options = ['Slow', 'Medium', 'Fast']
    current_option = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_option = (current_option - 1) % len(speed_options)
                elif event.key == pygame.K_DOWN:
                    current_option = (current_option + 1) % len(speed_options)
                elif event.key == pygame.K_RETURN:
                    if current_option == 0:
                        difficulty = 10
                    elif current_option == 1:
                        difficulty = 15
                    elif current_option == 2:
                        difficulty = 20
                    return
        
        game_window.fill(black)
        for i, option in enumerate(speed_options):
            text = font.render(option, True, white if i == current_option else green)
            text_rect = text.get_rect(center=(frame_size_x/2, frame_size_y/2 + i * 50))
            game_window.blit(text, text_rect)
        
        pygame.display.update()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

# Set the default difficulty before asking the player to choose
difficulty = 10

# Ask the player to choose the speed when the program launches
show_speed_menu()

snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True


# ///////////// Hindernisse, dass die Schlange vermeiden soll ////////////////////////////////////////////////////////////////////////////////////////////
obstacle_pos = [(random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10) for _ in range(10)]

direction = 'RIGHT'
change_to = direction

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # /////////////////////////////////////////////////////// Kollision von Bildschirm //////////////////////////////
    if direction == 'UP':
        snake_pos[1] -= 10
        if snake_pos[1] < 0:
            snake_pos[1] = frame_size_y - 10
    if direction == 'DOWN':
        snake_pos[1] += 10
        if snake_pos[1] >= frame_size_y:
            snake_pos[1] = 0
    if direction == 'LEFT':
        snake_pos[0] -= 10
        if snake_pos[0] < 0:
            snake_pos[0] = frame_size_x - 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
        if snake_pos[0] >= frame_size_x:
            snake_pos[0] = 0

    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        # ///////////////////////////////////////////// Frucht muss nicht da erscheinen, wo bereits Hindernisse sind, es muss verhindert werden ///////////////////////////////////////
        while food_pos in obstacle_pos:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    for pos in obstacle_pos:
        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    if snake_pos[0] < 0 or snake_pos[0] >= frame_size_x or snake_pos[1] < 0 or snake_pos[1] >= frame_size_y:
        game_over()
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if tuple(snake_pos) in obstacle_pos:
        game_over()

    show_score(1, white, 'comicsansms', 20)
    pygame.display.update()
    fps_controller.tick(difficulty)

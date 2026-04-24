import pygame
import sys
import time
import random
from nim_next import next_move
pygame.init()

DEFAULT_WIDTH, DEFAULT_HEIGHT = 1200, 600
ROWS, COLS = 3, 14
OFFSET = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BROWN = (50, 143, 209)
LIGHT_BROWN = (255, 255, 255)
GRAY = (232, 181, 72)

WIDTH, HEIGHT = DEFAULT_WIDTH, DEFAULT_HEIGHT
SQUARE_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess")

SPRITE_SHEET_BLUE_STAND = pygame.image.load("images/knight_blue_stand.png").convert_alpha()
SPRITE_SHEET_BLUE_STAND_R = pygame.image.load("images/knight_blue_stand_r.png").convert_alpha()
SPRITE_SHEET_BLUE_RUN = pygame.image.load("images/knight_blue_run.png").convert_alpha()
SPRITE_SHEET_GREEN_STAND = pygame.image.load("images/knight_green_stand.png").convert_alpha()
SPRITE_SHEET_GREEN_STAND_R = pygame.image.load("images/knight_green_stand_r.png").convert_alpha()
SPRITE_SHEET_GREEN_RUN = pygame.image.load("images/knight_green_run.png").convert_alpha()
SPRITE_SHEET_GOLD_STAND = pygame.image.load("images/knight_gold_stand.png").convert_alpha()
SPRITE_SHEET_GOLD_STAND_R = pygame.image.load("images/knight_gold_stand_r.png").convert_alpha()
SPRITE_SHEET_GOLD_RUN = pygame.image.load("images/knight_gold_run.png").convert_alpha()
SPRITE_SHEET_RED_STAND = pygame.image.load("images/knight_red_stand.png").convert_alpha()
SPRITE_SHEET_RED_STAND_R = pygame.image.load("images/knight_red_stand_r.png").convert_alpha()
SPRITE_SHEET_RED_RUN = pygame.image.load("images/knight_red_run.png").convert_alpha()

FRAME_WIDTH = 64
FRAME_HEIGHT = 64
FRAMES_PER_ROW = 4
TOTAL_FRAMES = 4

game_over = False

def load_frames(sprite_sheet, frame_width, frame_height, frames_per_row):
    frames = []
    sheet_width = sprite_sheet.get_width()
    sheet_height = sprite_sheet.get_height()
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame)
    return frames

frames_run_blue = load_frames(SPRITE_SHEET_BLUE_RUN, FRAME_WIDTH, FRAME_HEIGHT, FRAMES_PER_ROW)
frames_run_green = load_frames(SPRITE_SHEET_GREEN_RUN, FRAME_WIDTH, FRAME_HEIGHT, FRAMES_PER_ROW)
frames_run_gold = load_frames(SPRITE_SHEET_GOLD_RUN, FRAME_WIDTH, FRAME_HEIGHT, FRAMES_PER_ROW)
frames_run_red = load_frames(SPRITE_SHEET_RED_RUN, FRAME_WIDTH, FRAME_HEIGHT, FRAMES_PER_ROW)

PIECES = {
    "w_knight_run_blue": frames_run_blue,
    "w_knight_run_green": frames_run_green,
    "w_knight_run_gold": frames_run_gold,
    "w_knight_run_red": frames_run_red,
}
for key in PIECES:
    PIECES[key] = [pygame.transform.scale(frame, (SQUARE_SIZE, SQUARE_SIZE)) for frame in PIECES[key]]

class Knight:
    def __init__(self, name, color, row, col):
        self.name = name
        self.color = color
        self.row = row
        self.col = col

    def get_pos(self):
        return self.row, self.col

    def set_pos(self, row, col):
        self.row = row
        self.col = col

def init_knights():
    available_colors = ["blue", "green", "red", "gold"]
    selected_colors = random.sample(available_colors, 3)
    knights = []
    for color in selected_colors:
        knight = Knight("knight_" + color, color, 0, 0)
        knights.append(knight)
    return knights

def randomize_knight_colors(knights):
    available_colors = ["blue", "green", "red", "gold"]
    selected_colors = random.sample(available_colors, len(knights))
    for knight, color in zip(knights, selected_colors):
        knight.color = color
        knight.name = "knight_" + color

def resize_screen(new_width, new_height):
    global WIDTH, HEIGHT, SQUARE_SIZE, SPRITE_SHEET_BLUE_STAND, SPRITE_SHEET_RED_STAND, SPRITE_SHEET_GREEN_STAND, SPRITE_SHEET_GOLD_STAND, SPRITE_SHEET_BLUE_STAND_R, SPRITE_SHEET_GREEN_STAND_R, SPRITE_SHEET_GOLD_STAND_R, SPRITE_SHEET_RED_STAND_R
    WIDTH, HEIGHT = new_width, new_height
    SQUARE_SIZE = WIDTH // COLS
    SPRITE_SHEET_BLUE_STAND = pygame.transform.scale(SPRITE_SHEET_BLUE_STAND, (SQUARE_SIZE, SQUARE_SIZE))
    SPRITE_SHEET_RED_STAND = pygame.transform.scale(SPRITE_SHEET_RED_STAND, (SQUARE_SIZE, SQUARE_SIZE))
    SPRITE_SHEET_GREEN_STAND = pygame.transform.scale(SPRITE_SHEET_GREEN_STAND, (SQUARE_SIZE, SQUARE_SIZE))
    SPRITE_SHEET_GOLD_STAND = pygame.transform.scale(SPRITE_SHEET_GOLD_STAND, (SQUARE_SIZE, SQUARE_SIZE))
    SPRITE_SHEET_BLUE_STAND_R = pygame.transform.scale(SPRITE_SHEET_BLUE_STAND_R, (SQUARE_SIZE, SQUARE_SIZE))
    SPRITE_SHEET_RED_STAND_R = pygame.transform.scale(SPRITE_SHEET_RED_STAND_R, (SQUARE_SIZE, SQUARE_SIZE))
    SPRITE_SHEET_GREEN_STAND_R = pygame.transform.scale(SPRITE_SHEET_GREEN_STAND_R, (SQUARE_SIZE, SQUARE_SIZE))
    SPRITE_SHEET_GOLD_STAND_R = pygame.transform.scale(SPRITE_SHEET_GOLD_STAND_R, (SQUARE_SIZE, SQUARE_SIZE))
    for key in PIECES:
        PIECES[key] = [pygame.transform.scale(frame, (SQUARE_SIZE, SQUARE_SIZE)) for frame in PIECES[key]]

def draw_board(selected_knight_pos=None):
    start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
    start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if selected_knight_pos:
                selected_row, selected_col = selected_knight_pos
                if row == selected_row and col > selected_col:
                    pygame.draw.circle(
                        screen, GRAY,
                        (start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, start_y + row * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 4
                    )            

def place_pieces(knights):
    start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
    start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET
    for knight in knights:
        row, col = knight.get_pos()
        if col != COLS - 1:
            if knight.color == "blue":
                screen.blit(SPRITE_SHEET_BLUE_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
            elif knight.color == "red":
                screen.blit(SPRITE_SHEET_RED_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
            elif knight.color == "green":
                screen.blit(SPRITE_SHEET_GREEN_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
            elif knight.color == "gold":
                screen.blit(SPRITE_SHEET_GOLD_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
        else:
            if knight.color == "blue":
                screen.blit(SPRITE_SHEET_BLUE_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
            elif knight.color == "red":
                screen.blit(SPRITE_SHEET_RED_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
            elif knight.color == "green":
                screen.blit(SPRITE_SHEET_GREEN_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
            elif knight.color == "gold":
                screen.blit(SPRITE_SHEET_GOLD_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))

def select_knight(knights, mouse_pos):
    start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
    start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET
    for knight in knights:
        knight_rect = pygame.Rect(start_x + knight.col * SQUARE_SIZE, start_y + knight.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        if knight_rect.collidepoint(mouse_pos):
            return knight
    return None

def move_knight(knights, selected_knight, target_pos, animation_time=1, run_animation_speed=4):
    start_row, start_col = selected_knight.get_pos()
    target_row, target_col = target_pos

    if target_row != start_row or target_col <= start_col or target_col >= COLS:
        return False

    steps = 30
    dx = (target_col - start_col) * SQUARE_SIZE / steps
    for step in range(steps):
        current_x = (WIDTH - COLS * SQUARE_SIZE) // 2 + (start_col * SQUARE_SIZE) + dx * step
        current_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + (start_row * SQUARE_SIZE) + OFFSET
        draw_board()
        place_pieces_move(knights, selected_knight)
        if selected_knight.color == "blue":
            sprite_frames = PIECES["w_knight_run_blue"]
        elif selected_knight.color == "green":
            sprite_frames = PIECES["w_knight_run_green"]
        elif selected_knight.color == "red":
            sprite_frames = PIECES["w_knight_run_red"]
        elif selected_knight.color == "gold":
            sprite_frames = PIECES["w_knight_run_gold"]
        frame_index = (step // run_animation_speed) % TOTAL_FRAMES
        screen.blit(sprite_frames[frame_index], (current_x, current_y))
        pygame.display.flip()
        pygame.time.wait(int(animation_time * 1000 / steps))
    selected_knight.set_pos(target_row, target_col)
    return True

def boss_turn(knights):
    global game_over
    effective_a = (COLS-1) - knights[0].col
    effective_b = (COLS-1) - knights[1].col
    effective_c = (COLS-1) - knights[2].col
    result = next_move(effective_a, effective_b, effective_c)
    if result == "win":
        print("win")
        game_over = True    
        return
    new_effective_a, new_effective_b, new_effective_c = result
    
    if new_effective_a != effective_a:
        target_knight = knights[0]
        effective_new_value = new_effective_a
    elif new_effective_b != effective_b:
        target_knight = knights[1]
        effective_new_value = new_effective_b
    elif new_effective_c != effective_c:
        target_knight = knights[2]
        effective_new_value = new_effective_c
    else:
        return
    new_col = (COLS-1) - effective_new_value
    start_row, start_col = target_knight.get_pos()
    if new_col <= start_col or new_col >= COLS:
        return
    move_knight(
        knights,
        target_knight,
        (start_row, new_col),
        animation_time=0.5,
        run_animation_speed=4
    )

def draw_reset_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Reset", True, BLACK, GRAY)
    text_rect = text.get_rect(center=(WIDTH // 2 + 70, OFFSET // 2))
    pygame.draw.rect(screen, GRAY, text_rect.inflate(20, 10))
    screen.blit(text, text_rect)
    return text_rect

def draw_back_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Back", True, BLACK, GRAY)
    text_rect = text.get_rect(center=(WIDTH // 2 - 70, OFFSET // 2))
    pygame.draw.rect(screen, GRAY, text_rect.inflate(20, 10))
    screen.blit(text, text_rect)
    return text_rect

def reset_knights(knights):
    available_columns = list(range(COLS // 2))
    available_rows = list(range(ROWS))
    random_columns = random.sample(available_columns, len(knights))
    random_rows = random.sample(available_rows, len(knights))
    for knight, col, row in zip(knights, random_columns, random_rows):
        knight.set_pos(row, col)

def player_turn(knights, turn_label):
    global game_over
    if game_over:
        return
    a = (COLS-1) - knights[0].col
    b = (COLS-1) - knights[1].col
    c = (COLS-1) - knights[2].col
    if a == 0 and b == 0 and c == 0:
        print("lose")
    turn_done = False
    selected_knight = None
    selected_knight_pos = None
    font = pygame.font.Font(None, 36)
    while not turn_done:
        screen.fill(BLACK)
        if selected_knight_pos:
            draw_board(selected_knight_pos)
        else:
            draw_board()
        place_pieces(knights)
        reset_button_rect = draw_reset_button()
        back_button_rect = draw_back_button()
        turn_text = font.render("Turn: " + turn_label, True, BLACK)
        screen.blit(turn_text, (20, 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if reset_button_rect.collidepoint(event.pos):
                    randomize_knight_colors(knights)
                    reset_knights(knights)
                    selected_knight = None
                    selected_knight_pos = None
                    continue
                if back_button_rect.collidepoint(event.pos):
                    return "back"
                if selected_knight is None:
                    selected_knight = select_knight(knights, event.pos)
                    if selected_knight:
                        selected_knight_pos = selected_knight.get_pos()
                else:
                    start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
                    start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET
                    target_row = (event.pos[1] - start_y) // SQUARE_SIZE
                    target_col = (event.pos[0] - start_x) // SQUARE_SIZE
                    if move_knight(knights, selected_knight, (target_row, target_col)):
                        draw_board()
                        place_pieces(knights)
                        pygame.display.flip()
                        turn_done = True
                        selected_knight = None
                        selected_knight_pos = None

def place_pieces_move(knights, selected_knight):
    start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
    start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET

    for knight in knights:
        if knight != selected_knight:
            row, col = knight.get_pos()
            if col != COLS - 1:
                if knight.color == "blue":
                    screen.blit(SPRITE_SHEET_BLUE_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
                elif knight.color == "red":
                    screen.blit(SPRITE_SHEET_RED_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
                elif knight.color == "green":
                    screen.blit(SPRITE_SHEET_GREEN_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
                elif knight.color == "gold":
                    screen.blit(SPRITE_SHEET_GOLD_STAND, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
            else: 
                if knight.color == "blue":
                    screen.blit(SPRITE_SHEET_BLUE_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
                elif knight.color == "red":
                    screen.blit(SPRITE_SHEET_RED_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
                elif knight.color == "green":
                    screen.blit(SPRITE_SHEET_GREEN_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))
                elif knight.color == "gold":
                    screen.blit(SPRITE_SHEET_GOLD_STAND_R, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE))

def mode_selection():
    selecting = True
    mode = None
    font = pygame.font.Font(None, 48)
    while selecting:
        screen.fill(BLACK)
        vs_cpu_text = font.render("Vs CPU", True, BLACK)
        vs_player_text = font.render("Vs Player", True, BLACK)
        vs_cpu_rect = vs_cpu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        vs_player_rect = vs_player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        pygame.draw.rect(screen, GRAY, vs_cpu_rect.inflate(20, 10))
        pygame.draw.rect(screen, GRAY, vs_player_rect.inflate(20, 10))
        screen.blit(vs_cpu_text, vs_cpu_rect)
        screen.blit(vs_player_text, vs_player_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if vs_cpu_rect.collidepoint(event.pos):
                    mode = "vs_cpu"
                    selecting = False
                elif vs_player_rect.collidepoint(event.pos):
                    mode = "vs_player"
                    selecting = False
    return mode

def main():
    global game_over
    clock = pygame.time.Clock()
    while True:
        game_mode = mode_selection()
        knights = init_knights()
        reset_knights(knights)
        if game_mode == "vs_cpu":
            turn_label = "Player"
        else:
            turn_label = "Player 1"
        running = True
        game_over = False
        while running and not game_over:
            result = player_turn(knights, turn_label)
            if result == "back":
                running = False
                break

            if game_mode == "vs_cpu":
                pygame.time.wait(1000)
                boss_turn(knights)
            else:
                turn_label = "Player 2" if turn_label == "Player 1" else "Player 1"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(60)
        if game_over:
            pygame.time.wait(2000)
        if not running:
            break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

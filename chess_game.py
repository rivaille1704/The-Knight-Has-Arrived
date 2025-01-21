import pygame
import sys
import time

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

    

def draw_board(selected_pawn_pos=None):
    start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
    start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET
    
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if selected_pawn_pos:
                selected_row, selected_col = selected_pawn_pos
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

def select_knight(knights, mouse_pos):
    start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
    start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET

    for knight in knights:
        knight_rect = pygame.Rect(start_x + knight.col * SQUARE_SIZE, start_y + knight.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        if knight_rect.collidepoint(mouse_pos):
            return knight, knight.get_pos()
    return None, None

def move_knight(knights, selected_knight, target_pos, animation_time=1, run_animation_speed=4):
    start_row, start_col = selected_knight.get_pos()
    target_row, target_col = target_pos

    if target_row < 0 or target_row >= ROWS or target_col < 0 or target_col >= COLS:
        print("Invalid move. Cancelling move.")
        return

    if target_row != start_row:
        print("Invalid move. Cancelling move.")
        return

    if target_col <= start_col:
        print("Invalid move. Cancelling move.")
        return

    steps = 30
    dx = (target_col - start_col) * SQUARE_SIZE / steps
    dy = (target_row - start_row) * SQUARE_SIZE / steps

    for step in range(steps):
        current_x = (WIDTH - COLS * SQUARE_SIZE) // 2 + (start_col * SQUARE_SIZE) + dx * step
        current_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + (start_row * SQUARE_SIZE) + dy * step + OFFSET
        
        draw_board()
        place_pieces_move(knights, selected_knight)
        if selected_knight.color == "blue":
            screen.blit(PIECES["w_knight_run_blue"][(step // run_animation_speed) % TOTAL_FRAMES], (current_x, current_y))
        elif selected_knight.color == "green":
            screen.blit(PIECES["w_knight_run_green"][(step // run_animation_speed) % TOTAL_FRAMES], (current_x, current_y))
        elif selected_knight.color == "red":
            screen.blit(PIECES["w_knight_run_red"][(step // run_animation_speed) % TOTAL_FRAMES], (current_x, current_y))
        elif selected_knight.color == "gold":
            screen.blit(PIECES["w_knight_run_gold"][(step // run_animation_speed) % TOTAL_FRAMES], (current_x, current_y))

        pygame.display.flip()
        pygame.time.wait(int(animation_time * 1000 / steps))

    selected_knight.set_pos(target_row, target_col)

def draw_reset_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Reset", True, BLACK, GRAY)
    text_rect = text.get_rect(center=(WIDTH // 2, OFFSET // 2))
    pygame.draw.rect(screen, GRAY, text_rect.inflate(20, 10))
    screen.blit(text, text_rect)
    return text_rect
def reset_board(knights):
    knights[0].set_pos(0, 0)  
    knights[1].set_pos(1, 0)
    knights[2].set_pos(2, 0)  
def main():
    clock = pygame.time.Clock()
    running = True

    knights = [
        Knight("knight_blue", "blue", 0, 0),
        Knight("knight_green", "green", 1, 0),
        Knight("knight_red", "red", 2, 0),
    ]
    selected_knight = None
    selected_knight_pos = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if reset_button_rect.collidepoint(event.pos):
                        reset_board(knights)
                    elif selected_knight is None:
                        selected_knight, selected_knight_pos = select_knight(knights, event.pos)
                    else:
                        start_x = (WIDTH - COLS * SQUARE_SIZE) // 2
                        start_y = (HEIGHT - ROWS * SQUARE_SIZE) // 2 + OFFSET
                        target_row = (event.pos[1] - start_y) // SQUARE_SIZE
                        target_col = (event.pos[0] - start_x) // SQUARE_SIZE
                        move_knight(knights, selected_knight, (target_row, target_col))
                        selected_knight = None
                        selected_knight_pos = None
        draw_board(selected_knight_pos)
        place_pieces(knights)
        reset_button_rect = draw_reset_button()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

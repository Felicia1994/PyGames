import pygame
from Elements import Button

DARK = (77, 51, 0)
LIGHT = (255, 221, 153)
BLACK = DARK
WHITE = (255, 255, 255)

NUM_CONN = 4

def SymbolColorScreen(screen, framerate):
    display_width = screen.get_width()
    display_height = screen.get_height()

    clock = pygame.time.Clock()
    pygame.display.set_caption('SymbolColor')
    screen.fill(LIGHT)
    board = SymbolColorBoard()
    
    board.display(screen)
    restart_button = Button('Restart', LIGHT, screen, display_width*0.65, display_height*0.2, bg_color=DARK)
    home_button = Button('Home', LIGHT, screen, display_width*0.85, display_height*0.2, bg_color=DARK)
    rotate_button = Button('Rotate', LIGHT, screen, display_width*0.85, display_height*0.5, bg_color=DARK)

    running = True
    pattern = 0
    while running:
        clock.tick(framerate)

        if restart_button.is_clicked(pygame.mouse.get_pos()):
            restart_button = Button('Restart', DARK, screen, display_width*0.65, display_height*0.2, bg_color=LIGHT)
        else:
            restart_button = Button('Restart', LIGHT, screen, display_width*0.65, display_height*0.2, bg_color=DARK)
        restart_button.display(screen)
        if home_button.is_clicked(pygame.mouse.get_pos()):
            home_button = Button('Home', DARK, screen, display_width*0.85, display_height*0.2, bg_color=LIGHT)
        else:
            home_button = Button('Home', LIGHT, screen, display_width*0.85, display_height*0.2, bg_color=DARK)
        home_button.display(screen)
        if rotate_button.is_clicked(pygame.mouse.get_pos()):
            rotate_button = Button('Rotate', DARK, screen, display_width*0.85, display_height*0.5, bg_color=LIGHT)
        else:
            rotate_button = Button('Rotate', LIGHT, screen, display_width*0.85, display_height*0.5, bg_color=DARK)
        rotate_button.display(screen)
        DrawPattern(screen, pattern)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.is_clicked(pygame.mouse.get_pos()):
                    screen.fill(LIGHT)
                    board.reset()
                    board.display(screen)
                    player = 0
                    break
                if home_button.is_clicked(pygame.mouse.get_pos()):
                    running = False
                    break
                if rotate_button.is_clicked(pygame.mouse.get_pos()):
                    pattern = (pattern + 1) % 8
                    screen.fill(LIGHT)
                    board.display(screen)
                    break
                x, y = event.pos
                row = (y - 40) // 40  
                col = (x - 40) // 40
                if board.move(row, col, pattern):
                    board.display(screen)

                    result = board.is_win()
                    if result["is_over"]:
                        if result["winner"] == "Tie":
                            game_result = Button("It's a tie!", DARK, screen, display_width*0.75, display_height*0.8)
                        else:
                            game_result = Button(result["winner"]+" player wins!", DARK, screen, display_width*0.75, display_height*0.8)
                        game_result.display(screen)

def DrawPattern(screen, pattern):
    display_width = screen.get_width()
    display_height = screen.get_height()
    if pattern <= 3: # horizontal patterns
        poss = [[display_width*0.65-80, display_height*0.5-40, 80, 80], [display_width*0.65, display_height*0.5-40, 80, 80]]
    elif pattern >= 4 : # vertical patterns
        poss = [[display_width*0.65-40, display_height*0.5, 80, 80], [display_width*0.65-40, display_height*0.5-80, 80, 80]]
    if pattern%4 == 0:
        pattern_ = [(0,0), (1,1)]
    elif pattern%4 == 1:
        pattern_ = [(0,1), (1,0)]
    elif pattern%4 == 2:
        pattern_ = [(1,0), (0,1)]
    elif pattern%4 == 3:
        pattern_ = [(1,1), (0,0)]

    colors = [BLACK, WHITE]
    for i in range(2):
        color = colors[pattern_[i][1]]
        pygame.draw.rect(screen, color, poss[i], 0, border_radius=12)
        color = colors[1 - pattern_[i][1]] # flip color
        symbol = pattern_[i][0]
        if symbol == 0:
            pygame.draw.circle(screen, color, [poss[i][0] + 40, poss[i][1] + 40], 24, 8)
        elif symbol == 1:
            pygame.draw.line(screen, color, [poss[i][0] + 20, poss[i][1] + 20], [poss[i][0] + 60, poss[i][1] + 60], 12)
            pygame.draw.line(screen, color, [poss[i][0] + 60, poss[i][1] + 20], [poss[i][0] + 20, poss[i][1] + 60], 12)
    
class SymbolColorBoard(object):
    def __init__(self, num_rows=14, num_cols=14):
        self.colors = [BLACK, WHITE]
        self.num_rows, self.num_cols = num_rows, num_cols
        self.board_ = [[]] * self.num_rows
        self.reset()
    def reset(self):
        self.is_active = True
        for row in range(self.num_rows):
            self.board_[row] = [(-1, -1)] * self.num_cols # (symbol, color)
    def display(self, screen):
        for i in range(self.num_rows+1):
            pygame.draw.line(screen, DARK, [40, (i+1) * 40], [(self.num_cols+1) * 40, (i+1) * 40], 1)
        for i in range(self.num_cols+1):
            pygame.draw.line(screen, DARK, [(i+1) * 40, 40], [(i+1) * 40, (self.num_rows+1) * 40], 1)
        pygame.draw.rect(screen, DARK, [36, 36, self.num_cols * 40 + 9, self.num_rows * 40 + 9], 3)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.board_[row][col] != (-1, -1):
                    pos = [40 * (col + 1), 40 * (row + 1), 40, 40]
                    color = self.colors[self.board_[row][col][1]]
                    pygame.draw.rect(screen, color, pos, 0, border_radius=8)
                    color = self.colors[1 - self.board_[row][col][1]] # flip color
                    symbol = self.board_[row][col][0]
                    if symbol == 0:
                        pygame.draw.circle(screen, color, [pos[0] + 20, pos[1] + 20], 12, 4)
                    elif symbol == 1:
                        pygame.draw.line(screen, color, [pos[0] + 10, pos[1] + 10], [pos[0] + 30, pos[1] + 30], 4)
                        pygame.draw.line(screen, color, [pos[0] + 30, pos[1] + 10], [pos[0] + 10, pos[1] + 30], 4)

    def move(self, row, col, pattern):
        if not self.is_active:
            return False
        elif row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            return False
        elif self.board_[row][col] != (-1, -1):
            return False
        elif row != self.num_rows - 1 and self.board_[row+1][col] == (-1, -1):
            return False
        elif pattern <= 3 and col == self.num_cols - 1: # horizontal patterns
            return False
        elif pattern <= 3 and self.board_[row][col+1] != (-1, -1):
            return False
        elif pattern <= 3 and row != self.num_rows - 1 and self.board_[row+1][col+1] == (-1, -1):
            return False
        elif pattern >= 4 and row == 0: # vertical patterns
            return False
        elif pattern >= 4 and self.board_[row-1][col] != (-1, -1):
            return False
        if pattern == 0:
            self.board_[row][col], self.board_[row][col+1] = (0,0), (1,1)
        elif pattern == 1:
            self.board_[row][col], self.board_[row][col+1] = (0,1), (1,0)
        elif pattern == 2:
            self.board_[row][col], self.board_[row][col+1] = (1,0), (0,1)
        elif pattern == 3:
            self.board_[row][col], self.board_[row][col+1] = (1,1), (0,0)
        elif pattern == 4:
            self.board_[row][col], self.board_[row-1][col] = (0,0), (1,1)
        elif pattern == 5:
            self.board_[row][col], self.board_[row-1][col] = (0,1), (1,0)
        elif pattern == 6:
            self.board_[row][col], self.board_[row-1][col] = (1,0), (0,1)
        elif pattern == 7:
            self.board_[row][col], self.board_[row-1][col] = (1,1), (0,0)
        return True

    def is_win(self):
        winners = set()
        for i in range(self.num_rows):
            cnt_circle, cnt_cross, cnt_black, cnt_white,  = 0, 0, 0, 0
            for j in range(self.num_cols):
                if self.board_[i][j][0] == 0:
                    cnt_circle += 1
                    cnt_cross = 0
                elif self.board_[i][j][0] == 1:
                    cnt_circle = 0
                    cnt_cross += 1
                else:
                    cnt_circle, cnt_cross = 0, 0
                if self.board_[i][j][1] == 0:
                    cnt_black += 1
                    cnt_white = 0
                elif self.board_[i][j][1] == 1:
                    cnt_black = 0
                    cnt_white += 1
                else:
                    cnt_black, cnt_white = 0, 0
                if cnt_circle == NUM_CONN or cnt_cross == NUM_CONN:
                    winners.add("Symbol")
                if cnt_black == NUM_CONN or cnt_white == NUM_CONN:
                    winners.add("Color")
        for j in range(self.num_cols):
            cnt_circle, cnt_cross, cnt_black, cnt_white,  = 0, 0, 0, 0
            for i in range(self.num_rows):
                if self.board_[i][j][0] == 0:
                    cnt_circle += 1
                    cnt_cross = 0
                elif self.board_[i][j][0] == 1:
                    cnt_circle = 0
                    cnt_cross += 1
                else:
                    cnt_circle, cnt_cross = 0, 0
                if self.board_[i][j][1] == 0:
                    cnt_black += 1
                    cnt_white = 0
                elif self.board_[i][j][1] == 1:
                    cnt_black = 0
                    cnt_white += 1
                else:
                    cnt_black, cnt_white = 0, 0
                if cnt_circle == NUM_CONN or cnt_cross == NUM_CONN:
                    winners.add("Symbol")
                if cnt_black == NUM_CONN or cnt_white == NUM_CONN:
                    winners.add("Color")
        for x in range(NUM_CONN - 1, 28 - NUM_CONN):
            cnt_circle, cnt_cross, cnt_black, cnt_white,  = 0, 0, 0, 0
            for i,b in enumerate(self.board_):
                if 0 <= x - i < self.num_rows:
                    if b[x - i][0] == 0:
                        cnt_circle += 1
                        cnt_cross = 0
                    elif b[x - i][0] == 1:
                        cnt_circle = 0
                        cnt_cross += 1
                    else:
                        cnt_circle, cnt_cross = 0, 0
                    if b[x - i][1] == 0:
                        cnt_black += 1
                        cnt_white = 0
                    elif b[x - i][1] == 1:
                        cnt_black = 0
                        cnt_white += 1
                    else:
                        cnt_black, cnt_white = 0, 0
                    if cnt_circle == NUM_CONN or cnt_cross == NUM_CONN:
                        winners.add("Symbol")
                    if cnt_black == NUM_CONN or cnt_white == NUM_CONN:
                        winners.add("Color")
        for x in range(14 - NUM_CONN, NUM_CONN - 15, -1):
            cnt_circle, cnt_cross, cnt_black, cnt_white,  = 0, 0, 0, 0
            for i,b in enumerate(self.board_):
                if 0 <= x + i < self.num_rows:
                    if b[x + i][0] == 0:
                        cnt_circle += 1
                        cnt_cross = 0
                    elif b[x + i][0] == 1:
                        cnt_circle = 0
                        cnt_cross += 1
                    else:
                        cnt_circle, cnt_cross = 0, 0
                    if b[x + i][1] == 0:
                        cnt_black += 1
                        cnt_white = 0
                    elif b[x + i][1] == 1:
                        cnt_black = 0
                        cnt_white += 1
                    else:
                        cnt_black, cnt_white = 0, 0
                    if cnt_circle == NUM_CONN or cnt_cross == NUM_CONN:
                        winners.add("Symbol")
                    if cnt_black == NUM_CONN or cnt_white == NUM_CONN:
                        winners.add("Color")
        if len(winners) == 2:
            self.is_active = False
            return {"is_over": True, "winner": "Tie"}
        elif len(winners) == 1:
            self.is_active = False
            return {"is_over": True, "winner": next(iter(winners))}
        else:
            return {"is_over": False, "winner": ""}

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 640))
    SymbolColorScreen(screen, 10)
    pygame.quit()

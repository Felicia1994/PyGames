import pygame
from Elements import Button

DARK = (77, 51, 0)
LIGHT = (255, 221, 153)
BLACK = DARK
WHITE = (255, 255, 255)

def RenjuScreen(screen, framerate):
    display_width = screen.get_width()
    display_height = screen.get_height()

    clock = pygame.time.Clock()
    pygame.display.set_caption('Renju')
    screen.fill(LIGHT)

    board = RenjuBoard()
    board.display(screen)
    restart_button = Button('Restart', LIGHT, screen, display_width*0.65, display_height*0.3, bg_color=DARK)
    home_button = Button('Home', LIGHT, screen, display_width*0.85, display_height*0.3, bg_color=DARK)

    running = True
    player = 0
    while running:
        clock.tick(framerate)

        if restart_button.is_clicked(pygame.mouse.get_pos()):
            restart_button = Button('Restart', DARK, screen, display_width*0.65, display_height*0.3, bg_color=LIGHT)
        else:
            restart_button = Button('Restart', LIGHT, screen, display_width*0.65, display_height*0.3, bg_color=DARK)
        restart_button.display(screen)
        if home_button.is_clicked(pygame.mouse.get_pos()):
            home_button = Button('Home', DARK, screen, display_width*0.85, display_height*0.3, bg_color=LIGHT)
        else:
            home_button = Button('Home', LIGHT, screen, display_width*0.85, display_height*0.3, bg_color=DARK)
        home_button.display(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if home_button.is_clicked(pygame.mouse.get_pos()):
                    running = False
                    break
                if restart_button.is_clicked(pygame.mouse.get_pos()):
                    screen.fill(LIGHT)
                    board.reset()
                    board.display(screen)
                    player = 0
                    break
                x, y = event.pos
                row = round((y - 40) / 40)     
                col = round((x - 40) / 40)
                if board.move(row, col, player):
                    player = 1 - player
                    board.display(screen)

                    result = board.is_win()
                    if result["is_over"]:
                        game_result = Button(result["winner"]+" player wins!", DARK, screen, display_width*0.75, display_height*0.6)
                        game_result.display(screen)

class RenjuBoard(object):
    def __init__(self, num_rows=15, num_cols=15):
        self.colors = [BLACK, WHITE]
        self.num_rows, self.num_cols = num_rows, num_cols
        self.board_ = [[]] * self.num_rows
        self.reset()
    def reset(self):
        self.is_active = True
        for row in range(self.num_rows):
            self.board_[row] = [-1] * self.num_cols
    def display(self, screen):
        for i in range(1, self.num_rows+1):
            pygame.draw.line(screen, DARK, [40, i * 40], [self.num_cols * 40, i * 40], 1)
        for i in range(1, self.num_cols+1):
            pygame.draw.line(screen, DARK, [i * 40, 40], [i * 40, self.num_rows * 40], 1)
        pygame.draw.rect(screen, DARK, [36, 36, self.num_cols * 40 - 31, self.num_rows * 40 - 31], 3)
        pygame.draw.circle(screen, DARK, [320, 320], 5, 0)
        pygame.draw.circle(screen, DARK, [160, 160], 3, 0)
        pygame.draw.circle(screen, DARK, [160, 480], 3, 0)
        pygame.draw.circle(screen, DARK, [480, 160], 3, 0)
        pygame.draw.circle(screen, DARK, [480, 480], 3, 0)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.board_[row][col] != -1:
                    color = self.colors[self.board_[row][col]]
                    pos = [40 * (col + 1), 40 * (row + 1)]
                    pygame.draw.circle(screen, color, pos, 18, 0)
    def move(self, row, col, player):
        if not self.is_active:
            return False
        elif row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            return False
        elif self.board_[row][col] != -1:
            return False
        self.board_[row][col] = player
        return True
    def is_win(self):
        result = {"is_over": False, "winner": ""}
        for i in range(15):
            cnt_black, cnt_white = 0, 0
            for j in range(15):
                if self.board_[i][j] == 0:
                    cnt_black += 1
                    cnt_white = 0
                elif self.board_[i][j] == 1:
                    cnt_black = 0
                    cnt_white += 1
                else:
                    cnt_black, cnt_white = 0, 0
                if cnt_black == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "Black"
                    return result
                if cnt_white == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "White"
                    return result
        for j in range(15):
            cnt_black, cnt_white = 0, 0
            for i in range(15):
                if self.board_[i][j] == 0:
                    cnt_black += 1
                    cnt_white = 0
                elif self.board_[i][j] == 1:
                    cnt_black = 0
                    cnt_white += 1
                else:
                    cnt_black, cnt_white = 0, 0
                if cnt_black == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "Black"
                    return result
                if cnt_white == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "White"
                    return result
        for x in range(4, 25):
            cnt_black, cnt_white = 0, 0
            for i,b in enumerate(self.board_):
                if 14 >= x - i >= 0 and b[x - i] == 0:
                    cnt_black += 1
                    cnt_white = 0
                elif 14 >= x - i >= 0 and b[x - i] == 1:
                    cnt_black = 0
                    cnt_white += 1
                else:
                    cnt_black, cnt_white = 0, 0
                if cnt_black == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "Black"
                    return result
                if cnt_white == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "White"
                    return result
        for x in range(10, -11, -1):
            cnt_black, cnt_white = 0, 0
            for i,b in enumerate(self.board_):
                if 0 <= x + i <= 14 and b[x + i] == 0:
                    cnt_black += 1
                    cnt_white = 0
                elif 0 <= x + i <= 14 and b[x + i] == 1:
                    cnt_black = 0
                    cnt_white += 1
                else:
                    cnt_black, cnt_white = 0, 0
                if cnt_black == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "Black"
                    return result
                if cnt_white == 5:
                    self.is_active = False
                    result["is_over"] = True
                    result["winner"] = "White"
                    return result
        return result

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 640))
    RenjuScreen(screen, 10)
    pygame.quit()


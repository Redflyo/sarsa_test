from sarsa import SARSA
import random
import pygame
import random

# Colors
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game dimensions
BLOCK_SIZE = 100
WIDTH, HEIGHT = 10*BLOCK_SIZE, 10*BLOCK_SIZE

BOARD_SIZE = 3
EMPTY = " "

# Define the MorpionGame class
class MorpionGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = "X"
        self.game_over = False
        player_to_play = random.randint(0,1) == 1
        if not player_to_play:
            self.step(None)
        self.winner = None

    def __str__(self) -> str:
        return "\n".join([" ".join(row) for row in self.board])
    
    def __hash__(self) -> int:
        return hash(self.__str__())

    def get_state(self):
        return str(self)
    
    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        for letter in ["X","O"]:
            for i in range(BOARD_SIZE):
                if all(self.board[i][j] == letter for j in range(BOARD_SIZE)):
                    return True
                if all(self.board[j][i] == letter for j in range(BOARD_SIZE)):
                    return True
            
            # Check diagonals
            if all(self.board[i][i] == letter for i in range(BOARD_SIZE)):
                return True
            if all(self.board[i][BOARD_SIZE - 1 - i] == letter for i in range(BOARD_SIZE)):
                return True
        
        return False

    def check_draw(self):
        # If there are no empty spaces left, it's a draw
        return all(self.board[i][j] != EMPTY for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

    def step(self, action):
            
        reward = 0
        
        # Place the player's mark on the board
        if action is not None:
            
            x, y = action

            # If the game is over or the spot is taken, return invalid move
            if self.board[x][y] != EMPTY:
                self.game_over = True
                return -1, self.game_over
        
            self.board[x][y] = self.current_player
            # Check for a AI win
            if self.check_winner():
                self.game_over = True
                return 5, True
            elif self.check_draw():
                self.game_over = True
                return 0, True
            # Check for a draw
        if not self.game_over: # Random agent play
            have_play = False
            while not have_play and not self.game_over:
                rx,ry = random.randint(0,2),random.randint(0,2)
                if self.board[rx][ry] == " ":
                    self.board[rx][ry] = "O"
                    have_play = True
            if self.check_winner():
                reward=-1
                self.game_over = True
            if self.check_draw():
                reward = 0
                self.game_over = True
        
        return reward, self.game_over

    def reset(self):
        # Reset the board and game state
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = "X" if random.choice([True, False]) else "O"
        self.game_over = False
        self.winner = None


CELL_SIZE = 100
GRID_COLOR = (0, 0, 0)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
LINE_WIDTH = 5

screen = pygame.display.set_mode((CELL_SIZE * 3, CELL_SIZE * 3))

def draw_board(game):
    screen.fill((255, 255, 255))  # Fill the background with white
    
    # Draw the grid lines
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, i * CELL_SIZE), (CELL_SIZE * BOARD_SIZE, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, GRID_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, CELL_SIZE * BOARD_SIZE), LINE_WIDTH)

    # Draw the Xs and Os
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game.board[row][col] == "X":
                # Draw an X
                pygame.draw.line(screen, X_COLOR, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4), 
                                 (col * CELL_SIZE + CELL_SIZE - CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE - CELL_SIZE // 4), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE - CELL_SIZE // 4), 
                                 (col * CELL_SIZE + CELL_SIZE - CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4), LINE_WIDTH)
            elif game.board[row][col] == "O":
                # Draw an O
                pygame.draw.circle(screen, O_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 
                                   CELL_SIZE // 2 - CELL_SIZE // 8, LINE_WIDTH)

    # Update the display
    pygame.display.flip()



def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH / 6, HEIGHT / 3])




game = MorpionGame()
actions_possible = [(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(0,0),(0,1),(0,2)]

agent = SARSA(actions_possible)

agent.train(10000,MorpionGame)


pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 50)


# Game loop
print("=========Test Model=======")
for i in range(5):
    game = MorpionGame()
    while not game.game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
            if event.type == pygame.KEYDOWN:
                    
                agent_action = agent.choose_action(game.get_state(),0.)
                action = actions_possible[agent_action]
                reward, game_over = game.step(action)
                print(f"Get reward : {str(reward)}")

        win.fill(WHITE)
        draw_board(game)
        pygame.display.update()
    while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
        pass
pygame.quit()
quit()
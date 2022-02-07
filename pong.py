# imports
import os
import pygame
pygame.init()

# constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Ball class


class Ball(pygame.sprite.Sprite):
    def __init__(self, player1: pygame.sprite, player2: pygame.sprite) -> None:
        super().__init__()
        self.image = pygame.image.load(
            os.path.abspath("./static/white_ball.png"))
        self.rect = self.image.get_rect()
        self.delta_x = 0
        self.delta_y = 0
        self.dx = 2
        self.dy = 4
        self.rect.left = SCREEN_WIDTH/2
        self.rect.top = SCREEN_HEIGHT/2
        self.player1 = player1
        self.player2 = player2

    def update(self) -> None:
        global score1, score2
        if self.rect.left < 0:
            score2 += 1
            self.reset_pos()
        elif self.rect.right > SCREEN_WIDTH:
            score1 += 1
            self.reset_pos()
        elif self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.dy = self.dy * -1
        elif(pygame.sprite.collide_rect(self.player1, self) or pygame.sprite.collide_rect(self, self.player2)):
            self.dx = self.dx * -1

    def begin_move(self) -> None:
        self.rect.x += self.dx
        self.rect.y += self.dy

    def stop_move(self) -> None:
        self.dy = 0
        self.dx = 0

    def reset_pos(self):
        self.rect.left = SCREEN_WIDTH/2
        self.rect.top = SCREEN_HEIGHT/2

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type
        if(type == 1):
            self.image = pygame.image.load(os.path.abspath("./static/player1_small.png"))
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = SCREEN_HEIGHT/2
        else:
            self.image = pygame.image.load(os.path.abspath("./static/player2_small.png"))
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH - self.rect.size[0]
            self.rect.y = SCREEN_HEIGHT/2
        self.dy = 0

    def update(self) -> None:
        self.rect.y += self.dy
        self.stop_move()

    def move_up(self) -> None:
        self.dy -= 50

    def move_down(self) -> None:
        self.dy += 50

    def stop_move(self) -> None:
        self.dy = 0

    def __str__(self) -> str:
        return f"Player{self.type}"


class ScroeBoard():
 def __init__(self) -> None:
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.text = self.font.render(f"P1:{0} vs P2:{0}", True, WHITE)
        self.t_rect = self.text.get_rect()
        self.t_rect.center = (SCREEN_WIDTH/2, 20)

 def update(self, score1: int, score2: int) -> None:
        self.text = self.font.render(f"P1:{score1} vs P2:{score2}", True, WHITE)


def main():
    # setups
    screen = pygame.display.set_mode(SCREEN_SIZE)
    active_sprite_list = pygame.sprite.Group()

    # fonts
    score_board = ScroeBoard()
    game_over_font = pygame.font.Font("freesansbold.ttf", 26)

    # sprites
    player1 = Player(1)
    player2 = Player(2)
    pong = Ball(player1, player2)
    clock = pygame.time.Clock()

    # listing sprites
    active_sprite_list.add(pong)
    active_sprite_list.add(player1)
    active_sprite_list.add(player2)

    # scores and winner
    global score1, score2, Winner
    score1 = 0
    score2 = 0
    Winner = "No one"

    # Game Over
    GAME_OVER = False
    game_over_rect = pygame.rect.Rect(1, SCREEN_HEIGHT/2, SCREEN_WIDTH, 60)
    # for debug
    BEGIN = False

    while not GAME_OVER:
        for ev in pygame.event.get():
            if(ev.type == pygame.QUIT):
                GAME_OVER = True

            if(ev.type == pygame.KEYDOWN):
                if(ev.key == pygame.K_SPACE):
                    BEGIN = True
                if(ev.key == pygame.K_w):
                    player1.move_up()
                if(ev.key == pygame.K_s):
                    player1.move_down()
                if(ev.key == pygame.K_UP):
                    player2.move_up()
                if(ev.key == pygame.K_DOWN):
                    player2.move_down()

        # screen uptades
        screen.fill(BLACK)
        if BEGIN:
            pong.begin_move()
        # active_sprite_list updates
        active_sprite_list.update()
        active_sprite_list.draw(screen)
        # score updates
        score_board.update(score1, score2)
        screen.blit(score_board.text, score_board.t_rect)
        if score1 == 2:
            Winner = f"{player1}"
            GAME_OVER = True
        elif score2 == 2:
            Winner = f"{player2}"
            GAME_OVER = True
        # fps 60
        clock.tick(60)
        pygame.display.flip()

    while GAME_OVER:
        # event listening for quit or replay
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                GAME_OVER = False  # quit
            if(event.type == pygame.KEYDOWN):
                if event.key == pygame.K_r:
                    return main()  # restart
        screen.fill(BLACK)
        game_over_text = game_over_font.render(f"                     Game Over! {Winner} is winner(press r restart)", True, WHITE)
        game_over_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()

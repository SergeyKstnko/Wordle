import pygame

from wordle.constants import HEIGHT, WIDTH
from wordle.board import Board
from wordle.solver import Solver


#provides refresh rate for the 
FPS = 60

pygame.init()

game_window = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption("Wordle")

def main():

    clock = pygame.time.Clock()
    run = True
    board = Board()
    solver = Solver(board)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    board.update_letter(event.unicode)
                elif event.key == pygame.K_BACKSPACE:
                    board.delete_letter()
                elif event.key == pygame.K_RETURN:
                    board.enter_word()
                elif event.key == pygame.K_SPACE:
                    solver.make_suggestion()



        game_window.fill((255,255,255))
        board.draw_squares(game_window)


        pygame.display.update()

    pygame.quit()

main()
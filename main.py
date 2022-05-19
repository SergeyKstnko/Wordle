'''GUI for Wordle game

TODO: * Add Keyboard
* Add Suggestions/Hints
* Add Definitions at request'''


import ctypes, os

if os.name == 'nt':
    ctypes.windll.user32.SetProcessDPIAware()


import pygame

from wordle.constants import HEIGHT, SQUARES_X, SQUARES_Y, WHITE, WIDTH, BLACK, MIDDLE
from wordle.board import Board
from wordle.solver import Solver


#provides refresh rate for the 
FPS = 60

pygame.init()

game_window = pygame.display.set_mode((WIDTH, HEIGHT))
#, pygame.SCALED

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



        game_window.fill(WHITE)
        
        #HEADER
        font_wordle = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 50)
        txt_surface = font_wordle.render("Wordle", True, BLACK) 
        game_window.blit(txt_surface, (MIDDLE-90, 0))
        pygame.draw.line(game_window, BLACK, (0,65), (WIDTH,65), width=2)

        board.draw_squares(game_window)
        solver.draw_hint(game_window)


        pygame.display.update()

    pygame.quit()

main()
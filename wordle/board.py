'''This class will handle "board" for Wordle.

TODO: * Handling repeating letters
*Update dictionaries I use'''

import pygame, random
#import enchant
#from random_words import RandomWords

from .constants import BLACK, COLS, DICT_ADDRESS, MIDDLE, ROWS, SQUARES_X, SQUARES_Y, WHITE, SQUARE_SIZE
from .square import Square

class Board:
    def __init__(self):
        self.board = [[]]
        self.secret_word, self.my_dict = self.pick_word_of_the_day()
        print(self.my_dict)
        print(self.secret_word)
        self.attempt = 0
        #between 0 and 4
        self.letter_count = 0
        self.initialize_board()
        #self.my_dict = enchant.Dict("en_US")
        self.warning = ""
        self.warning_duration = 0
        

    def initialize_board(self):
        for r in range(ROWS):
            self.board.append([])
            for c in range(COLS):
                self.board[r].append(Square())
    
    def get_attempt(self):
        return self.attempt

    def get_warning(self) -> str:
        return self.warning
    
    def get_warning_duration(self) -> int:
        return self.warning_duration


    def pick_word_of_the_day(self):
        f = open(DICT_ADDRESS)
        words = f.read().split()
        a = random.randint(0, len(words))
        return words[a].upper(), words
        #return "FLUFF"
        #return "BLUFF" #FLUFF
        #return "STEAL" #THESE
        '''Old implementation
        rw = RandomWords()
        word = rw.random_word()
        while len(word) != 5:
            word = rw.random_word()'''

    def draw_squares(self, game_window):
        '''Draw squares and letters on the game window'''
        
        font = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 40)

        #Draw squares and letters
        for row in range(ROWS):
            for col in range(COLS):
                next_square_x = SQUARES_X+col*68
                next_square_y = SQUARES_Y+row*68
                rect = pygame.Rect(next_square_x, next_square_y ,SQUARE_SIZE, SQUARE_SIZE)
                sq = self.board[row][col]
                pygame.draw.rect(game_window, sq.back_color, rect, sq.thickness)
                
                txt_surface = font.render(sq.letter, True, sq.letter_color) 
                if sq.letter in ["J", "I",]:
                    indent = 21
                elif sq.letter == "W":
                    indent = 11
                elif sq.letter in ["H", "M"]:
                    indent = 16
                else:
                    indent = 18
                #indent = 20 if sq.letter in ["J", "I"] else 15
                game_window.blit(txt_surface, (next_square_x+indent, next_square_y+5))

    def display_warning(self, game_window):
        #Display Not in list/Not enough letters message
        if self.warning and self.warning_duration >= pygame.time.get_ticks():

            rect_x, rect_y = MIDDLE-120, SQUARES_Y+450
            rect = pygame.Rect(rect_x, rect_y, 250, 35)
            pygame.draw.rect(game_window, BLACK, rect, 0)

            warning_font = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 20)
            warning = warning_font.render(self.warning, True, WHITE)

            indent = 50 if self.warning == "Not in word list" else 30
            game_window.blit(warning, (rect_x+indent, rect_y+2))


    def update_letter(self, letter):
        if self.letter_count < COLS and self.attempt < ROWS:
            letter = letter.upper()
            self.board[self.attempt][self.letter_count].letter = letter
            self.letter_count += 1

    def delete_letter(self):
        if self.letter_count-1 >= 0 and self.attempt < ROWS:
            self.letter_count -= 1
            self.board[self.attempt][self.letter_count].letter = ""
            

    def change_warning(self, switch = 0):        
        self.warning_duration = pygame.time.get_ticks() + 2000
        if switch == 1:
            self.warning = "Not enough letters"
        else:
            self.warning = "Not in word list"


    def enter_word(self):
        '''
        To implement::  declare victory
        '''
        if self.letter_count < COLS:
            self.change_warning(1)
            return
        #number of letters that are correct in entered word. 
        #Used to stop the game if solution is found in less than 6 attempts
        letters_correct = 0
        #check if word exists. Return if there is no such word
            #get the word
        word = ""
        for i in range(COLS):
            word += self.board[self.attempt][i].letter
        word = word.lower()
        if word not in self.my_dict:
            self.change_warning(0)
            return

            
        #make changes to background and letter colors
        for i in range(COLS):
            #if letter in secret_word and in correct position
            sq = self.board[self.attempt][i]
            if sq.letter in self.secret_word and sq.letter == self.secret_word[i]:
                sq.correct_position()
                letters_correct += 1
            #if letter is in secret word and possition is not correct
            elif sq.letter in self.secret_word and sq.letter != self.secret_word[i]:
                sq.wrong_position()
            #if letter is not in the word
            else:
                sq.wrong_letter()
        
        #move to the next line if not correct
        self.letter_count = 0
        self.attempt = ROWS if letters_correct == COLS else (self.attempt + 1)

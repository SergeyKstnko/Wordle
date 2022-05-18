'''This class will handle "board" for Wordle.
Function I'm planning to implement:
* drawing squares
* creating 2D array fo squares'''

import pygame, enchant, random
#from random_words import RandomWords

from .constants import COLS, ROWS, SQUARES_X, SQUARES_Y, WHITE, SQUARE_SIZE
from .square import Square

class Board:
    def __init__(self):
        self.board = [[]]
        self.secret_word = self.pick_word_of_the_day()
        print(self.secret_word)
        self.attempt = 0
        #between 0 and 4
        self.letter_count = 0
        self.initialize_board()
        self.my_dict = enchant.Dict("en_US")
        

    def initialize_board(self):
        for r in range(ROWS):
            self.board.append([])
            for c in range(COLS):
                self.board[r].append(Square())
    
    def get_attempt(self):
        return self.attempt

    def pick_word_of_the_day(self):
        '''Old implementation
        rw = RandomWords()
        word = rw.random_word()
        while len(word) != 5:
            word = rw.random_word()'''
        f = open('dictionaries/answers.txt')
        words = f.read().split('\n')
        a = random.randint(0, len(words))
        return words[a].upper()

    def draw_squares(self, game_window):
        '''Draw squares and letters on the game window'''
        
        game_window.fill(WHITE)
        font = pygame.font.SysFont("comicsans", 50)

        #Draw squares and letters
        for row in range(ROWS):
            for col in range(COLS):
                next_square_x = SQUARES_X+col*68
                next_square_y = SQUARES_Y+row*68
                rect = pygame.Rect(next_square_x, next_square_y ,SQUARE_SIZE, SQUARE_SIZE)
                sq = self.board[row][col]
                pygame.draw.rect(game_window, sq.back_color, rect, sq.thickness)
                
                txt_surface = font.render(sq.letter, True, sq.letter_color) 
                indent = 25 if sq.letter == "I" else 18
                game_window.blit(txt_surface, (next_square_x+indent, next_square_y+15))

    def update_letter(self, letter):
        if self.letter_count < COLS and self.attempt < ROWS:
            letter = letter.upper()
            self.board[self.attempt][self.letter_count].letter = letter
            self.letter_count += 1

    def delete_letter(self):
        if self.letter_count-1 >= 0 and self.attempt < ROWS:
            self.letter_count -= 1
            self.board[self.attempt][self.letter_count].letter = ""
            

    def enter_word(self):
        '''
        To implement::  declare victory
        '''
        if self.letter_count < COLS:
            return
        #number of letters that are correct in entered word. 
        #Used to stop the game if solution is found in less than 6 attempts
        letters_correct = 0
        #check if word exists. Return if there is no such word
            #get the word
        word = ""
        for i in range(COLS):
            word += self.board[self.attempt][i].letter
        if not self.my_dict.check(word):
            return

            
        #make changes to background and letter colors
        for i in range(COLS):
            #if letter in secret_word and in correct position
            sq = self.board[self.attempt][i]
            if sq.letter in self.secret_word and sq.letter == self.secret_word[i]:
                sq.both_correct()
                letters_correct += 1
            #if letter is in secret word and possition is not correct
            elif sq.letter in self.secret_word and sq.letter != self.secret_word[i]:
                sq.correct_letter_only()
            #if letter is not in the word
            else:
                sq.letter_not_in()
        
        #move to the next line if not correct
        self.letter_count = 0
        self.attempt = ROWS if letters_correct == COLS else (self.attempt + 1)

    def suggest_a_word(self):
        '''this function will pick the most popular word from the list'''
        pass


    def narrow_down_words(self, conditions):
        '''this function will create a dictionary of narrowed down words
        param:: conditions'''
        #self.temp_dict = [x for x im self.dict if all(conditions)]
        pass
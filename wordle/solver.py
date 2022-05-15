'''This class implements Wordle solver. It interacts with board.py.
The strategy is simple: at first I am trying to collect as much information
as possible. At first attempt I try a word that has the most vowels. At the 
second attempt try the word that has as little as possible letters that
were used in the word before.
At all later attempts, based on previous guesses, construct Regular Expression
and use it to narrow down dictionary. Then pick the most used word based on the
count from the dictionary.

Dictionary.txt has words and counts next to them. This dictionary was compiled by:
https://github.com/jonhoo/roget

The idea two pick two opposite words with the most vowels is from here
https://www.nytimes.com/2022/02/10/crosswords/best-wordle-tips.html'''

import pygame

from .constants import COLS, GREEN, GREY, ROWS

class Solver:
    def __init__(self, board):
        self.board = board
        self.surface = board.board
        self.regEx = ""

    def print(self):
        print("Solver things attempt is: " + str(self.board.get_attempt()))

    def build_regex(self):
        attempt = self.board.get_attempt()
        #what do I know about the word?
        word = ""
        #what do I know about the letter?
        permanent_letters = [""]*COLS
        wrong_pos_letters = [""]*COLS

        if not attempt:
            return
        
        #iterate over the board over attempt number of rows
        for row in range(attempt):
            for col in range(COLS):
                sq = self.surface[row][col]
                curr_letter = sq.get_letter().lower()

                #if green -> hard wire in that position
                if sq.get_back_color() == GREEN:
                    permanent_letters[col] = '[' + curr_letter + ']'
                elif sq.get_back_color() == GREY:
                    #print(sq.get_letter() +" Yo")
                    #if grey -> word is not there
                    to_add = '(?!.*'  + curr_letter + ')'
                    if to_add not in word:
                        word += to_add
                else:
                    #if orange -> somewhere else but not in that position
                    to_add = '(?=.*' + curr_letter + ')'
                    if to_add not in word:
                        word += to_add
                    if curr_letter not in wrong_pos_letters[col]:
                        wrong_pos_letters[col] += curr_letter

        #print(str(permanent_letters) + "Perm letters")
        #print(str(wrong_pos_letters) + "Wrong pos let")

        self.regEx = word
        for i in range(COLS):
            if permanent_letters[i]:
                self.regEx += permanent_letters[i]
            elif wrong_pos_letters[i]:
                self.regEx += '[^' + wrong_pos_letters[i] + ']'
            else:
                self.regEx += '[a-z]'
        self.regEx += "\s\d+"
        
        print(self.regEx)
        

    def sort_dictionary(self):
        pass

    def pick_guess(self):
        pass


    def make_suggestion(self):
        '''This method will make suggestion based on attempt'''
        attempt = self.board.get_attempt()
        if attempt == 0:
            print("Solver suggests ADIEU")
        elif attempt == 1:
            print("Solver suggests TRYST")
        else:
            print("WORK IN PROGRESS")

        self.print()
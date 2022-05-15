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

class Solver:
    def __init__(self, board):
        self.board = board
        self.regEx = ""

    def print(self):
        print("Solver things attempt is: " + str(self.board.attempt))

    def build_regex(self):
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
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
https://www.nytimes.com/2022/02/10/crosswords/best-wordle-tips.html


TODO: * Pick second guess opposite of the first guess
* Deal with repeated letters
* Use better dictionaries
'''

import pygame, random
import re

from .constants import COLS, DICT_ADDRESS, GREEN, GREY, ROWS, YELLOW

class Solver:
    def __init__(self, board):
        self.board = board
        self.surface = board.board
        self.regEx = ""
        self.word_list = self.get_list()

        #rules for sifting letters
        self.green_letters_pos = [""]*COLS
        self.yellow_letters_pos = [""]*COLS
        self.grey_letters = ""
        self.yellow_letters = ""
        self.words_tried_list = [""]*ROWS
        
    def get_list(self) -> str:
        file = open("dictionaries/answers.txt", "r+")
        word_list = file.read().split()
        file.close()
        return word_list


    def build_sorting_rules(self):
        '''TO ADD: repeating letters
        
        This function collects information from user'''
        attempt = self.board.get_attempt()
        self.words_tried_list = [""]*ROWS
        for row in range(attempt):
            for col in range(COLS):
                sq = self.surface[row][col]
                curr_letter = sq.get_letter().lower()
                self.words_tried_list[row] += curr_letter

                #if green -> hard wire in that position
                if sq.get_back_color() == GREEN:
                    self.green_letters_pos[col] = curr_letter
                elif sq.get_back_color() == GREY and curr_letter not in self.green_letters_pos and curr_letter not in self.yellow_letters:
                    #if grey -> word is not there
                    if curr_letter not in self.grey_letters:
                        self.grey_letters += curr_letter
                elif sq.get_back_color() == YELLOW:
                    #if yellow -> somewhere else but not in that position
                    if curr_letter not in self.yellow_letters:
                        self.yellow_letters += curr_letter
                    if curr_letter not in self.yellow_letters_pos[col]:
                        self.yellow_letters_pos[col] += curr_letter
                else:
                    print("I'm skipping GREY letter that is repeated somewhere else in the word.")
                    #print("DO NOT EXPECT TO BE HERE. INFORM ME. I'm in collect_information()")
        
        #print("GREEN letter pos  "+str(self.green_letters_pos))
        #print("YELLOW letter pos "+str(self.yellow_letters_pos))
        #print("GREY letters      "+str(self.grey_letters))
        #print("YELLOW letters    "+str(self.yellow_letters))
        #print("Words tried list" + str(self.words_tried_list))


    def word_fits(self, word) -> bool:
        '''does word fit those descriptions'''
        if word in self.words_tried_list:
            return False
        for i in range(COLS):
            letter = word[i]
            #check if all green letters present
            if self.green_letters_pos[i] and self.green_letters_pos[i] != letter:
                return False
            #check if grey letters are absent
            elif letter in self.grey_letters:
                return False
            elif letter in self.yellow_letters_pos[i]:
                return False
        for yell_letter in self.yellow_letters:
            #check if yellow letters are present
            if yell_letter not in word:
                return False
        return True


    def narrow_down_words(self):
        word_list_temp = []
        for word in self.word_list:
            if self.word_fits(word):
                word_list_temp.append(word)
        self.word_list = word_list_temp


    def pick_a_word(self) -> str:
        #print(self.word_list)
        print(random.choice(self.word_list).upper())
        return random.choice(self.word_list).upper()


    def make_suggestion(self):
        '''This method will make suggestion based on attempt'''
        attempt = self.board.get_attempt()
        if attempt == 0:
            print("Solver suggests ADIEU")
        elif attempt == 1:
            print("Solver suggests TRYST")
        else:
            self.build_sorting_rules()
            self.narrow_down_words()
            self.pick_a_word()
            print("WORK IN PROGRESS")



### The rest of functions were depreciated

    def sort_dictionary_withRegEx(self):
        p = re.compile(self.regEx)
        self.dict = p.findall(self.dict)
        print(self.dict)
        self.dict = str(self.dict)
        f = open("dictionaries/sorted.txt", "w")
        f.write(str(self.dict))
        f.close()



    def build_regex(self):
        '''This fucntion was retired.'''
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

        self.regEx = word
        for i in range(COLS):
            if permanent_letters[i]:
                self.regEx += permanent_letters[i]
            elif wrong_pos_letters[i]:
                self.regEx += '[a-z^' + wrong_pos_letters[i] + ']'
            else:
                self.regEx += '[a-z]'
        #self.regEx += '\s'
        #self.regEx += "\s\d+"



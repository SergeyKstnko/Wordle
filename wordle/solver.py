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

from .constants import BLACK, COLS, DICT_ADDRESS, GREEN, GREY, ROWS, SOLVER_X, SOLVER_Y, SQUARE_SIZE, YELLOW, WHITE

class Solver:
    def __init__(self, board):
        self.board = board
        self.surface = board.board
        self.regEx = ""
        self.word_list = self.get_list()
        self.hinted_word = ""
        self.hinted_alternative_word = ""

        #rules for sifting letters
        self.green_letters_pos = [""]*COLS
        self.yellow_letters_pos = [""]*COLS
        self.grey_letters = ""
        self.yellow_letters = ""
        self.words_tried_list = [""]*ROWS
        
    def get_list(self) -> str:
        file = open(DICT_ADDRESS, "r+")
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
        self.hinted_word = random.choice(self.word_list).upper()
        self.hinted_alternative_word = self.hinted_word
        while self.hinted_alternative_word == self.hinted_word and len(self.word_list) >= 2:
            self.hinted_alternative_word = random.choice(self.word_list).upper()

        return random.choice(self.word_list).upper()


    def make_suggestion(self):
        '''This method will make suggestion based on attempt'''
        attempt = self.board.get_attempt()

        if attempt >= ROWS:
            return
        if attempt == 0:
            self.hinted_word = "GAYER"
        elif attempt == 1:
            self.hinted_word = "TRYST"
        else:
            self.build_sorting_rules()
            self.narrow_down_words()
            self.pick_a_word()


    def draw_hint(self, game_window):
        font = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 30)
        alt_hint = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 15)
        font_strategy = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 25)
        attempt = self.board.get_attempt()
        
        txt_intro = font.render("Stuck? Press SPACE for a hint.", True, GREY) 
        game_window.blit(txt_intro, (SOLVER_X, SOLVER_Y+10))

        if not self.hinted_word:
            tile_thickness = 2
            tile_color = GREY
        else:
            tile_thickness = 0
            tile_color = GREEN


        for col in range(COLS):
            next_tile_x = SOLVER_X+col*(SQUARE_SIZE/1.5+10)
            next_tile_y = SOLVER_Y+43
            #x,y, width, length
            tile = pygame.Rect(next_tile_x, next_tile_y, SQUARE_SIZE/1.5, SQUARE_SIZE/1.5)
            #window, color, object_to_draw, thickness
            pygame.draw.rect(game_window, tile_color, tile, tile_thickness)

            #If user didn't ask for hint
            if self.hinted_word:
                letter = self.hinted_word[col]
                txt_surface = font.render(letter, True, WHITE) 
                indent = 18 if letter == "I" else 13
                game_window.blit(txt_surface, (next_tile_x+indent, next_tile_y+12))

        
        if attempt:
            alt_hint_text = "You may also try: " + self.hinted_alternative_word
            txt_strategy = alt_hint.render(alt_hint_text, True, GREY)
            game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+96))

        text = ""
        text_2 = ""
        if self.hinted_word:
            if attempt == 0:
                text = "One strategy suggests to pick the first word that has the most vowels."
            elif attempt == 1:
                text = "The second pick should contain letters used in the first try."
            else:
                text = "For 3rd attempt and further, computer actually analizes information"
                text_2 = "received from previous tries and gives you a word that fits those criteria."
        
        
        txt_strategy = font_strategy.render(text, True, GREY)
        game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+110))
        if text_2:
            txt_strategy = font_strategy.render(text_2, True, GREY)
            game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+126))
    
        







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



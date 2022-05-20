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

from .constants import BLACK, BLUE, COLS, DICT_ADDRESS, GREEN, GREY, LIGHT_BLUE, ROWS, SOLVER_X, SOLVER_Y, SQUARE_SIZE, YELLOW, WHITE
from .api import Api

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

        self.text = ""
        self.text_2 = ""
        self.text_3 = ""
        self.text_4 = ""

        self.hint_definition = {}
        

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
            self.hinted_word = "QUEUE"
            self.hinted_alternative_word = "GAYER"
            #self.hinted_word = "WAACS"
        elif attempt == 1:
            self.hinted_word = "TRYST"
            self.hinted_alternative_word = "QUASH"
            #self.hinted_word = "ENEMA"
        else:
            self.build_sorting_rules()
            self.narrow_down_words()
            self.pick_a_word()

        def_api = Api(self.hinted_word)
        self.hint_definition = def_api.get_word_info(self.hinted_word)


    def change_message(self):
        attempt = self.board.get_attempt()
        if attempt == 0:
            self.text = "One strategy suggests to pick the first"
            self.text_2 = "word that has the most vowels."
        elif attempt == 1:
            self.text = "The second pick should not contain"
            self.text_2 = "letters used in the first try."
        else:
            self.text = "For 3rd attempt and further, computer"
            self.text_2 = "actually analizes information received"
            self.text_3 = "from previous tries and gives you a word"
            self.text_4 = "that fits those criteria."

    def draw_definitions(self, game_window):
        word_font = pygame.font.SysFont("fonts/NotoSans-ExtraBold.ttf", 40)
        partOfSpeech_font = pygame.font.SysFont("fonts/NotoSans-ExtraBold.ttf", 22)
        definitions_font = pygame.font.SysFont("fonts/NotoSans-ExtraBold.ttf", 22)
        #if user asked for hint
        indent_y = SOLVER_Y + 210

        if self.hinted_word:
            word = self.hint_definition['word']
            partOfSpeech = self.hint_definition['partOfSpeech']
            definitions = self.hint_definition['definitions']
            
            txt_word = word_font.render(word.lower(), True, BLACK)
            game_window.blit(txt_word, (SOLVER_X, indent_y))

            txt_partOfSpeech = partOfSpeech_font.render(partOfSpeech, True, LIGHT_BLUE)
            game_window.blit(txt_partOfSpeech, (SOLVER_X+100, indent_y+10))


            y_indent = indent_y+40
            for definition in definitions:
                while definition:
                    end = 45
                    while end < len(definition) and definition[end] != " ":
                        end += 1
                    if end == len(definition)-1:
                        end += 1
                    temp_text = definition[:end]
                    txt_def = definitions_font.render(temp_text, True, GREY)
                    game_window.blit(txt_def, (SOLVER_X, y_indent))
                    y_indent += 20
                    definition = definition[end:]
                
                y_indent += 3
                



    def draw_hint(self, game_window):
        stuck_font = pygame.font.SysFont("fonts/NotoSans-ExtraBold.ttf", 30)
        hint_font = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 30)
        strategy_font = pygame.font.Font("fonts/NotoSans-ExtraBold.ttf", 15)
        attempt = self.board.get_attempt()
        
        stuck_prompt = stuck_font.render("Stuck? Press SPACE for a hint.", True, GREY) 
        game_window.blit(stuck_prompt, (SOLVER_X, SOLVER_Y+20))

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
                txt_surface = hint_font.render(letter, True, WHITE) 
                if letter in ["J", "I",]:
                    indent = 15
                elif letter in ["E","L","Y"]:
                    indent = 12
                elif letter == ["W","M"]:
                    indent = 0
                else:
                    indent = 10
                game_window.blit(txt_surface, (next_tile_x+indent, next_tile_y))


        if self.hinted_alternative_word:
            alt_hint_text = "You may also try: " + self.hinted_alternative_word
            txt_strategy = strategy_font.render(alt_hint_text, True, GREY)
            game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+83))
        
        if self.text:
            txt_strategy = strategy_font.render(self.text, True, GREY)
            game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+110))
        if self.text_2:
            txt_strategy = strategy_font.render(self.text_2, True, GREY)
            game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+126))
        if self.text_3:
            txt_strategy = strategy_font.render(self.text_3, True, GREY)
            game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+142))
        if self.text_4:
            txt_strategy = strategy_font.render(self.text_4, True, GREY)
            game_window.blit(txt_strategy, (SOLVER_X+10, SOLVER_Y+158))
    






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



'''This class will represent states of squares
where user will input words'''

from .constants import GREEN, GREY, BLACK, ORANGE, WHITE


class Square:
    def __init__(self):

        self.letter = ""
        self.back_color = GREY
        self.letter_color = BLACK
        self.thickness = 3

    def update_letter(self, letter):
        self.letter = letter

    def both_correct(self):
        self.back_color = GREEN
        self.letter_color = WHITE
        self.thickness = 0

    def correct_letter_only(self):
        self.back_color = ORANGE
        self.letter_color = WHITE
        self.thickness = 0

    def letter_not_in(self):
        self.back_color = GREY
        self.letter_color = WHITE
        self.thickness = 0

    def get_back_color(self) -> str:
        return self.back_color

    def get_letter(self) -> str:
        return self.letter



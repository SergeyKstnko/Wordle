'''This class will help retreave, format and return definitions
part of speech and phonetic for words.
This API does not allow to call server more than ones every
1,000ms. 

More info on API: https://dictionaryapi.dev/
'''


from requests import get
import pygame

#pprint is used solely for debuging purposes
#from pprint import PrettyPrinter


class Api:
    def __init__(self, word):
        self.word = word
        self.url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}"
        self.response = {}
        self.word_info = {}
        self.prev_call = 0

    def get_response(self):
        while self.prev_call >= pygame.time.get_ticks():
            print('API overload. BE NICE TO API')
            continue
        self.response = get(self.url)

        if self.response.status_code == 200:
            self.response = self.response.json()[0]
        else:
             print("\nAPI status: %d" % self.response.status_code)

        self.prev_call = pygame.time.get_ticks() + 1000
        #printer.pprint(self.response)

    def set_word(self, word):
        self.word = word

    def get_definitions(self) -> list:
        definitions = []
        l = len(self.response['meanings'][0]['definitions'])
        l = 3 if l >3 else l

        for i in range(l):
            definition = self.response['meanings'][0]['definitions'][i]['definition']
            definitions.append(str(i+1)+") "+definition)
        return definitions

    def get_part_of_speech(self) -> str: 
        return self.response['meanings'][0]['partOfSpeech']

    def get_phonetic(self) -> str:
        return self.response['phonetic']

    def get_word_info(self, word) -> dict:
        self.word = word
        self.get_response()

        self.word_info = {'word': self.word,
            'partOfSpeech': self.get_part_of_speech(),
            'definitions': self.get_definitions()
            }
            #'phonetic': self.get_phonetic(),
        return self.word_info
This game an implementation of the popular game Wordle.


Tech characteristics:
* a Python3 implementation of Wordle that includes suggested
guesses and word definitions retrieved via an API
* Implemented game using OOP design principles (specifically 
encapsulation principle)
* API
    * Call to a dictionary API to get definitions
    * Displaying definitions
    * Limiting number of calls to 1/1000ms at most
    not to overload API
* Easy extensibility
* GUI via Pygame
* Regular Expressions
* Fonts work on different opearation systems


Functionality (among others):
* checks if word user is trying to input is legitimate
* color code letters
* highlight if word is correct
* Picking new word each day
* Suggesting a new word based on previous guesses
* Shows message when "Word not in list" and "Not enough letters"


ToDO: (in the order of importance and interest):
* Use better dictionaries
* Suggest second guess opposite of the first one
* Update documentation
* Deal with repeated letters
* Add Keyboard
* Letter W is a little off to the right for some reason
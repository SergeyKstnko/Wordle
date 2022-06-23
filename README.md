![Main screenshot](https://user-images.githubusercontent.com/7826894/169595360-abcecc8c-7085-4b00-b7ad-359c309cd693.png)

**A Python3 implementation of Wordle that includes suggested guesses and word definitions retrieved via an API.**

Tech characteristics:
* Implemented game using OOP design principles (specifically 
encapsulation principle)
* Implemented calls to API:
    * Calls to a dictionary API to get definitions
    * Displays definitions of hints
    * Limits number of calls to 1/1000ms at most
    not to overload API
* Easy extensibility
* GUI via Pygame
* Fonts work on different operation systems
* Game gives you hint based on strategy offered by NYT:
   * For the first guess pick word with most vowels
   * For the second guess pick word that has no letters
   that were used in previous try
   * For the 3rd and all consecutive guesses, pick words
   based on the information you collected in all previous
   tries.
* Regular Expressions. Implemented at first but then eventually
retired as more elegant solution was found.


Functionality (among others): 
* Checks if word user is trying to input is legitimate and
displays corresponding message if not
* Color coded letters
* Highlight if word is correct
* Picking new word each day
* Suggesting a hint based on previous guesses
* Shows message when "Word not in list" and "Not enough letters"


ToDO: (in the order of importance and interest):
* Use better dictionaries
* Suggest second guess opposite of the first one
* Update documentation
* Deal with some nuances of repeated letters
* Add Keyboard
* Improve strategy to suggest new hints
* Letter W is a little off to the right for some reason

![Word not in list message](https://user-images.githubusercontent.com/7826894/169596343-01fd805f-92cd-4afd-a91f-6337433a70b8.png)
![Not enough letters message](https://user-images.githubusercontent.com/7826894/169596378-fe9f1ea3-a2df-492a-9d17-de1bbd0fe997.png)
![Using application with no hint.](https://user-images.githubusercontent.com/7826894/169596534-325a9bef-6a36-481b-a9e9-456bbf363458.png)



A Python3 implementation of Wordle that includes suggested guesses and word definitions retrieved via an API.

![Main screenshot](https://user-images.githubusercontent.com/7826894/169595360-abcecc8c-7085-4b00-b7ad-359c309cd693.png)


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
* Regular Expressions
* Fonts work on different opearation systems


Functionality (among others): 
* Checks if word user is trying to input is legitimate and
displayes corresponding message if not
* Color coded letters
* Highlight if word is correct
* Picking new word each day
* Suggesting a new word based on previous guesses
* Shows message when "Word not in list" and "Not enough letters"


ToDO: (in the order of importance and interest):
* Use better dictionaries
* Suggest second guess opposite of the first one
* Update documentation
* Deal with some nuances of repeated letters
* Add Keyboard
* Letter W is a little off to the right for some reason

![Word not in list message](https://user-images.githubusercontent.com/7826894/169596343-01fd805f-92cd-4afd-a91f-6337433a70b8.png)
![Not enough letters message](https://user-images.githubusercontent.com/7826894/169596378-fe9f1ea3-a2df-492a-9d17-de1bbd0fe997.png)
![Using application with no hint.](https://user-images.githubusercontent.com/7826894/169596534-325a9bef-6a36-481b-a9e9-456bbf363458.png)



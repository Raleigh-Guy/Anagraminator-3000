from bakery import assert_equal
from dataclasses import dataclass
import random
from drafter import *




    
@dataclass
class Word:
    name: str
    "Name of a word (Its original spelling)"
    length: int
    "The length of a word's alphabetization"
    alpha: str
    "The alphabetization of the word in all capitals"

@dataclass
class Translation:
    original: Word
    "A possibly recurring word in the original text"
    final: Word
    "The final word a word should become"
    rearanged: bool
    "Wether a word has been changed in translation"

@dataclass
class State:
    story_contents: str
    "contents of textbox to be translated"
    button_pushed: bool
    "If the mysterious button at the home page has been pushed"
    button_word: str
    "What the from the button says"
    added_translations: list[list[Translation]]
    "A list of the translations added by the user, such as the blacklist"
	
@dataclass
class Feature:
    case: str
    "The capitalization of the word"
    opening: str
    "Typically a {, (, or even ["
    punctuation: str
    "The punctuation coming directly after the string"

def alphabetize(word: str) -> str:
    """
    Create a list of letters in word not including special characters
    """
    organizer = []
    for letter in word:
        if letter not in """
                        `~!@#$%^&*()_+-={}[]|/:;"'<,>.?
                        """:
            organizer.append(letter.upper())
    """
    Reconstruct the word in all capitals and in alphabetical order
    """
    new_word = ""
    for number in sorted(organizer):
        new_word += number
    return new_word

assert_equal(alphabetize("Nickels"),"CEIKLNS")
assert_equal(alphabetize(""),"")
assert_equal(alphabetize("j az-z"),"AJZZ")


def encode_word_data(word: str) -> Word:
    """
    Encodes a word into a Word format
    """
    length = len(alphabetize(word))
    if length > 20:
        length = 21
    "take from the first up to the last non-special character"
    count = 0
    fcount1 = 0
    fcount2 = 0
    for letter in word:
        if not letter in """
		~!@#$%^&*()_+-={}[]|/:;"'<,>.?
        """:
            char = True
        else: char = False
        count += 1
        if char:
            fcount1 = count
        if not fcount1:
            fcount2 = count
    filtered = word[fcount2:fcount1]
    return Word(filtered, length, alphabetize(word))

assert_equal(encode_word_data(""), Word("", 0, ""))
assert_equal(encode_word_data("Joe Dan-forth"), Word("Joe Dan-forth", 11, "ADEFHJNOORT"))
assert_equal(encode_word_data("AAAAAAAAAAAAAAAAAAAA"), Word("AAAAAAAAAAAAAAAAAAAA", 20, "AAAAAAAAAAAAAAAAAAAA"))
assert_equal(encode_word_data("AAAAAAAAAAAAAAAAAAAABBBBB"), Word("AAAAAAAAAAAAAAAAAAAABBBBB", 21, "AAAAAAAAAAAAAAAAAAAABBBBB"))


def encode_list_data(words: list[str]) -> list[Word]:
    """
    from a list of strings, creates a list of Words with valuable data
    (using different variables than the helper functions)
    """
    new_list_of_words = []
    for each_word in words:
        new_list_of_words.append(encode_word_data(each_word))
    return new_list_of_words

assert_equal(encode_list_data(["", "Joe Dan-forth"]), [Word("", 0, ""), Word("Joe Dan-forth", 11, "ADEFHJNOORT")])


#Initiation
"This is the only code I specifically looked up; How to import the word library"
import requests
url = "https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words.txt"
response = requests.get(url)
data = response.text.splitlines()


"""
Create a list of lists of Words where the index of the list represents the length of the words
and the words are all in the word dataclasses inside the lists
"""

#Too large to be in the state dataclass
Library = [[],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           []
           ]
"""
Assembles using a for loop, but since no words are 0 characters long the first list will consistently be empty
"""
for term in data:
    Term = encode_word_data(term)
    if Term.length <= 20:
        Library[Term.length].append(Term)
    else:
        Library[21].append(Term)

assert_equal(find_anagrams(encode_word_data('coming')), [encode_word_data('gnomic')])
assert_equal(Library[0], [])

#Too large to be in the state dataclass
"""
WorkingLibrary is a list of all words that have already been translated used to significantly speed up
the translating process if there are many repeat words in a 'story'
"""
WorkingLibrary = [[],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           []
           ]

def find_anagrams(word: Word) -> list[Word]:
    """
    finds all non-auto anagrams of a word, find the unit test below the Library definition
    """
    new_list = []
    for wOrd in Library[word.length]:
        if wOrd.alpha == word.alpha and wOrd.name.lower() != word.name.lower():
            new_list.append(wOrd)
    return new_list

def find_continuity(word: Word) -> Word:
    """
    Intakes a Word type and checks if it already has a recorded anagram
    if it does: output that anagram's Word
    if it don't: assign an anagram to WorkingLibrary and output that anagram
    
    bobm is a wierd intermediate value which represents several pieces of useful information, so it is named to be wierd and thus stand out
    bobm will exist if there are anagrams OR if the word is in the dictionary
    if not bobm then the word IS NOT in the dictionary, and then is added to dictionary
    
    because of the random element, this function has been tested manually without unit tests.
    """
    for wOrd in WorkingLibrary[word.length]:
        if wOrd.original.name.upper() == word.name.upper():
            return wOrd.final
    bobm = find_anagrams(word)
    if bobm:
        working1 = bobm[random.randint(0, (len(bobm) - 1))]
        rearanged = True
    else:
        working1 = word
        Library[word.length].append(word)
        rearanged = False
    working2 = Translation(word, working1, rearanged)
    WorkingLibrary[word.length].append(working2)
    return working1

def collect_features(story: str) -> list[list[Feature]]:
    """
    Intakes a string and returns a list of each of its words' features
    organized by line
    
    Similar to 'find_continuity', this function was manually tested in a temporary space now lost to time but was very successful
    """
    features = []
    count = 0
    for line in story.splitlines():
        features.append([])
        for werd in line.split():
            """
            check casing and create variable case
            """
            if werd.lower() == werd:
                case = "lowercase"
            elif werd.title() == werd:
                case = "Titlecase"
            elif werd.upper() == werd:
                case = "UPPERCASE"
            else:
                case = "wEiRd"
            """
            check for opening special characters
            """
            if werd[0] in """
`							~!@#$%^&*()_+-={}[]|/:;"'<,>.?
                            """:
                intro = werd[0]
            else:
                intro = ""
            """
            check for punctuation (special characters) and also catches ellipses!
            """
            if werd[-3:] == "...":
                punct = werd[-3:]
            elif werd[-1] in """
`							~!@#$%^&*()_+-={}[]|/:;"'<,>.?
                            """:
                punct = werd[-1]
            else:
                punct = ""
            features[count].append(Feature(case, intro, punct))    
        count += 1
    return features

@route
def add_to_WL(state: State, word_from: str, word_to: str):
    """
    Intakes 2 strings and inserts into the WorkingLibrary a command to
    replace all instances of words that match the first string to
    become the second string
    """
    word_from = encode_word_data(word_from)
    word_to = encode_word_data(word_to)
    WorkingLibrary[word_from.length].append(Translation(word_from, word_to, True))
    state.added_translations[word_from.length].append(Translation(word_from, word_to, True))
    return to_set(state)
    

@route
def blacklist_from_WL(state: State, to_be_blacklisted: str):
    """
    Prevents a word from being anagramized by appending a translation from istelf to itself in the WorkingLibrary
    """
    for wOrd in encode_list_data(to_be_blacklisted.split(',')):
        if wOrd.name:
            WorkingLibrary[wOrd.length].append(Translation(wOrd, wOrd, False))
            state.added_translations[wOrd.length].append(Translation(wOrd, wOrd, False))
    return to_blacklist(state)

@route
def index(state: State) -> Page:
    """
    The home page of the drafter, includes a list of all blacklisted and pre-translated words
    in addition to a button for three other pages and one more button that puts a random translation from WorkingLibrary on screen
    """
    current_translations = ""
    for length in state.added_translations:
        for translation in length:
            if translation.rearanged:
                adder = translation.original.name + " -> " + translation.final.name + "\n"
            else:
                adder = translation.original.name + " has been blacklisted\n"
            current_translations += adder
    if not current_translations:
        current_translations += 'No translations yet!'
    current_translations = "\n" + current_translations
    if state.button_pushed:
        return Page(state, [
            """Home page \nWelcome to the 'Anigraminator 3000'!. From here you can go to 3 other pages: \n""",
            Button("Translation input", 'to_translate'),
            Button("Blacklist here", 'to_blacklist'),
            Button("Set your own translation", 'to_set'),
            Button("Have another!", 'random_translation_button'),
            state.button_word,
            current_translations
            ])
    return Page(state, [
        """Home page \nWelcome to the 'Anigraminator 3000'!. From here you can go to 3 other pages: \n""",
        Button("Translation input", 'to_translate'),
        Button("Blacklist here", 'to_blacklist'),
        Button("Set your own translation", 'to_set'),
        Button("Have a random anagram!", 'random_translation_button'),
        current_translations
        ])

@route
def to_translate(state: State) -> Page:
    """
    The page on which the 'story' is inputted into the system
    """
    return Page(state, [
        TextArea('user_story', state.story_contents),
        Button("Update contents by pushing this nifty button!", 'update_box'),
        Button("Finished translation over here!", 'to_translation'),
        Button("Back to home page?", 'index')
        ])

@route
def update_box(state: State, user_story: str) -> Page:
    """
    A function which updates the input textbox in to_translate so that it is part of the state
    not unit tested but has been tested thouroughly in the drafter website
    """
    state.story_contents = user_story
    return to_translate(state)

@route
def to_translation(state: State, user_story: str) -> Page:
    """
    The page that displays the translation, which is reconstructed every time the page is visited
    This function is much too reliant on collect_features, WorkingLibrary, and Library to be unit tested, so it has instead been
    tested manually, primarily through excerpts from the bee movie
    """
    new_story = ""
    features = collect_features(user_story)
    count_1 = 0
    for line in user_story.splitlines():
        new_story_line = ""
        count_2 = 0
        for werd in line.split():
            word = find_continuity(encode_word_data(werd)).name
            if features[count_1][count_2].case == "lowercase":
                word = word.lower()
            elif features[count_1][count_2].case == "Titlecase":
                word = word.title()
            elif features[count_1][count_2].case == "UPPERCASE":
                word = word.upper()
            new_story_line += features[count_1][count_2].opening + word + features[count_1][count_2].punctuation + " "
            count_2 += 1
        count_1 += 1
        new_story += new_story_line + "\n"
    return Page(state, [
        Button("Translation input", 'to_translate'),
        Button("Back to home page?", 'index'),
        "\n",
        new_story
        ])

@route
def to_blacklist(state: State) -> Page:
    """
    The blacklist page in which the user can stop words from being translated
    """
    return Page(state, [
        """Here you can blacklist certain words from being translated!\nPlease enter your words in a comma separated list. \n""",
        TextBox('to_be_blacklisted',""),
        Button("Apply changes", 'blacklist_from_WL'),
        Button("Back to home page?", 'index')
        ])

@route
def to_set(state: State) -> Page:
    """
    similar to to_blacklist but instead of stopping a word from being translated alltogether, you can customize what it becomes
    """
    return Page(state, [
        """Here you can set a certain word in the top box to translate to a certain word in the bottom box. \nOne word at a time, please! \n""",
        TextBox('word_from',""),
        TextBox('word_to',""),
        Button("Apply changes", 'add_to_WL'),
        Button("Back to home page?", 'index')
        ])

@route
def random_translation_button(state: State) -> Page:
    """
    A button in home (index) that returns a random translation from WorkingLibrary (already been used in the 'story')
    and also formats it to be displayed to the user
    """
    state.button_pushed = True
    for length in WorkingLibrary:
        for translation in length:
            if translation.rearanged:
                if random.randint(1,100) == 100:
                    state.button_word = translation.original.name + " --> " + translation.final.name
    return index(state)

assert_equal(index(State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])),
             Page(State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]),[
        """Home page \nWelcome to the 'Anigraminator 3000'!. From here you can go to 3 other pages: \n""",
        Button("Translation input", 'to_translate'),
        Button("Blacklist here", 'to_blacklist'),
        Button("Set your own translation", 'to_set'),
        Button("Have a random anagram!", 'random_translation_button'),
        '\nNo translations yet!'
        ]))

assert_equal(to_translate(State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])),Page(
                             State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])
    , [
        TextArea('user_story', "This is where you put your text-to-be-anagramized!"),
        Button("Update contents by pushing this nifty button!", 'update_box'),
        Button("Finished translation over here!", 'to_translation'),
        Button("Back to home page?", 'index')
        ]))

assert_equal(to_blacklist(State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])), Page(
                             State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]), [
        """Here you can blacklist certain words from being translated!\nPlease enter your words in a comma separated list. \n""",
        TextBox('to_be_blacklisted',""),
        Button("Apply changes", 'blacklist_from_WL'),
        Button("Back to home page?", 'index')
        ]))

assert_equal(to_set(State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])),Page(
                             State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]), [
        """Here you can set a certain word in the top box to translate to a certain word in the bottom box. \nOne word at a time, please! \n""",
        TextBox('word_from',""),
        TextBox('word_to',""),
        Button("Apply changes", 'add_to_WL'),
        Button("Back to home page?", 'index')
        ]))

assert_equal(random_translation_button(State("This is where you put your text-to-be-anagramized!", False, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])), index(
                             State("This is where you put your text-to-be-anagramized!", True, "",
                         [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])))

start_server(State("This is where you put your text-to-be-anagramized!", False, "", [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]))

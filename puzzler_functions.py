'''Phrase Puzzler: functions'''

import random


# Phrase Puzzler constants

DATA_FILE = 'puzzles.txt'

HIDDEN = '^'

VOWEL_PRICE = 1
CONSONANT_BONUS = 2

# Game types
HUMAN = '1'
HUMAN_HUMAN = '2'
HUMAN_COMPUTER = '3'

# Computer difficulty levels
EASY = 'E'
HARD = 'H'

# Players' names
PLAYER_ONE = 'Player One'
PLAYER_TWO = 'Player Two'

# Consonant and vowel sets
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWELS = 'aeiou'

# Menu options
CONSONANT = 'C'
VOWEL = 'V'
SOLVE = 'S'
QUIT = 'Q'

# The order in which a computer player, hard difficulty, will guess consonants.
PRIORITY_CONSONANTS = 'tnrslhdcmpfgybwvkqxjz'


# Define your functions here.

def is_win(puzzle, view):
    '''(str, str) -> bool

    Return True iff puzzle is the same as view.


    >>> is_win('banana', 'banana')
    True
    >>> is_win('b^^^^^', 'banana')
    False
    '''
    # put the function body here
    return puzzle == view




def game_over(puzzle, view, current_selection):
    '''(str, str, str) -> bool

    Return True iff puzzle is the same as view or current_selection is QUIT.


    >>> game_over('banana', 'banana', 'C')
    True
    >>> game_over('b^^^^^', 'banana', 'C')
    False
    >>> game_over('b^^^^^', 'banana', 'Q')
    True
    '''

    return (puzzle == view or current_selection == QUIT)



def get_view(puzzle):
    '''(str) -> str

    Return puzzle with every letter replaced by the HIDDEN character.


    >>> get_view('won't'):
    ^^^'^
    >>> get_view('a 9'):
    '^ 9'
    '''

    #Constructs view by adding characters from puzzle, except for when the
    #character is an alphabet, in which case it adds HIDDEN.
    view = ''
    for ch in puzzle:
        if ch in (CONSONANTS + VOWELS):
            view += HIDDEN
        else:
            view += ch
    return view



def update_view(puzzle, view, guessed_letter):
    '''(str, str, str) -> str

    For all guessed_letter in puzzle, reveal it in view.


    >>> update view('apple', '^^^l^', 'p')
    '^ppl^'
    >>> update view('apple', '^^^l^', 'f')
    '^^^l^'
    '''

    #Constructs update_view by adding characters from view, but adds
    #guessed_letter everytime it shows up in puzzle.
    updated_view = ''
    for ch in range(len(puzzle)):
        if guessed_letter == puzzle[ch]:
            updated_view += guessed_letter
        else:
            updated_view += view[ch]
    return updated_view
            
            



def make_guessed(unguessed_consonants, unguessed_vowels, guessed_letter):
    '''(str, str, str) -> tuple of (str, str)

    Return unguessed_consonants and unguessed_vowels with guessed_letter
    removed from each.


    >>> make_guessed('sdfjkl', 'au', 'l')
    ('sdfjk', 'au')
    >>> make_guessed('sd', 'au', 'a')
    ('sd', 'u')
    '''

    return (unguessed_consonants.replace(guessed_letter, ''), \
            unguessed_vowels.replace(guessed_letter, ''))



def calculate_score(current_score, occurences_of_letter, guessed_letter_type):
    '''(int, int, str) -> int

    Increase current_score by occurences_of_letter if guessed_letter_type is a
    consonant. Decrease current_score by VOWEL_PRICE if it is a vowel.


    >>> calculate_score(3, 2, 'C')
    5
    >>> calculate_score(3, 4, 'V')
    2
    '''

    if guessed_letter_type == VOWEL:
        return current_score - VOWEL_PRICE
    elif guessed_letter_type == CONSONANT:
        return current_score + occurences_of_letter


    

def finalize_score(puzzle, view, unguessed_consonants, current_score):
    '''(str, str, str, int) -> int

    Return the final score by adding CONSONANT_BONUS to current_score for
    each letter in view that's also in unguessed_consonants, but is
    hidden in view.


    >>> finalize_score('banana', 'ba^a^a', 'npr', 3)
    7
    >>> finalize_score('santiago', 'santiago', 'rp', 2)
    2
    '''
    
    for ch in range(len(puzzle)):
        if puzzle[ch] in unguessed_consonants:
            current_score += CONSONANT_BONUS
    return current_score


    

def update_score(player_one_score, player_two_score, new_score,\
                 current_player):
    '''(int, int, int, str) -> tuple of (int, int)

    Return player_one_score and player_two_score updated with
    current_player's new score, new_score.


    >>> update_score(6, 3, 5, 'Player_One')
    (5, 3)
    >>> update_score(3, 3, 6, 'Player_Two')
    (3, 6)
    '''

    if current_player == PLAYER_ONE:
        player_one_score = new_score
    else:
        player_two_score = new_score

    return (player_one_score, player_two_score)

    

    
    

    



def next_player(current_player, letter_occurences):
    '''(str, int) -> str

    Return the next player depending on current_player and if letter_occurence
    is atleast one.


    >>> next_player('Player_One', 2)
    'Player_one'
    >>> next_player('Player_One', 0)
    'Player_two'
    '''

    if letter_occurences > 0:
        return current_player
    elif current_player == PLAYER_ONE:
        return PLAYER_TWO
    elif current_player == PLAYER_TWO:
        return PLAYER_ONE

    

def guess_letter(unguessed_consonants, difficulty_level):
    '''(str, str) -> str

    Return a consonant from unguessed_consonants to be guessed next by
    the computer player. If difficulty_level is EASY, return a random consonant
    from unguessed_consonants. If difficulty_level is HARD, return the first
    consonants in PRIORITY_CONSONANTS that occurs in unguessed_consonants.


    >>> guess_letter('pssng', 'H')
    's'
    '''

    #Computer on hard difficulty uses the first letter that hasn't been
    #guessed from a prioritized list of consonants.
    if difficulty_level == EASY:
        return random.choice(unguessed_consonants)

    elif difficulty_level == HARD:
        for ch in range(len(PRIORITY_CONSONANTS)):
            if PRIORITY_CONSONANTS[ch] in unguessed_consonants:
                return PRIORITY_CONSONANTS[ch]



def half_revealed(view):
    '''(str) -> bool

    Return True iff at least half the letters in view are revealed.


    >>> half_revealed('app^^')
    True
    >>> half_revealed('a^^^^')
    False
    '''

    #First finds the number of revealed letters and the total amount of letters
    #in the view. Then determines if the revealed letters make up atleast
    #half the view.
    total_revealed = 0
    for ch in view:
        if ch in (CONSONANTS + VOWELS):
            total_revealed += 1

    total_letters = 0
    for ch in view:
        if ch in (HIDDEN + CONSONANTS + VOWELS):
            total_letters += 1
            
    return total_revealed >= (total_letters/2)
            




def is_match(puzzle, view):
    '''(str, str) -> bool

    Return True iff it seems like view could be puzzle.


    >>> is_match('apple', 'app^^')
    True
    >>> is_match('apple', 'b^^')
    False
    '''

    #First checks if the view and the puzzle are the same length.
    #When a letter is revealed in view, it checks if all the occurences
    #of the same letter in puzzle is also revealed in view.
    #If a letter is hidden in view, it checks if it is also hidden everytime
    #it occurs in puzzle.
    #Finally, if a character in puzzle isn't a letter, it checks if it appears
    #in view.
    if len(puzzle) == len(view):
        for ch in range(len(puzzle)):
            if puzzle[ch] in (CONSONANTS + VOWELS) and view[ch] != HIDDEN:
                for char in range(len(puzzle)):
                    if (puzzle[char] == puzzle[ch] and \
                     puzzle[char] != view[char]):
                        return False
            elif puzzle[ch] in (CONSONANTS + VOWELS) and view[ch] == HIDDEN:
                for char in range(len(puzzle)):
                    if (puzzle[char] == puzzle[ch] and view[char] != HIDDEN):
                        return False
            elif puzzle[ch] not in (CONSONANTS + VOWELS):
                if puzzle[ch] != view[ch]:
                    return False

    else:
        return False
                    
    return True


            


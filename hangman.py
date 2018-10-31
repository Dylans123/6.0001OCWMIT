# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    word_guess = []
    for x in secret_word:
        if x in letters_guessed:
                word_guess.append(x)
    return bool(len(word_guess) == len(secret_word))


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    for x in secret_word:
        if x not in letters_guessed:
            secret_word = secret_word.replace(x, "_ ")
        else:
            secret_word = secret_word
    return secret_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase
    for x in available_letters:
        if x in letters_guessed:
            available_letters = available_letters.replace(x, "")
        else:
            available_letters = available_letters
    return available_letters
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    available_letters = string.ascii_lowercase
    unique_letters = []
    for x in secret_word:
        if x not in unique_letters:
            unique_letters.append(x)
    guesses = 6
    warnings = 3
    vowels = "aeiou"
    letters_guessed = []
    secret_word = choose_word(wordlist)
    print("Welcome to the game of Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long")
    while guesses > 0 and is_word_guessed(secret_word, letters_guessed) != True:
        print("--------")
        print(get_guessed_word(secret_word, letters_guessed))        
        print("You have ", guesses," guesses left")
        print(get_available_letters(letters_guessed))
        guess = input("Please guess a letter: ")
        guess = guess.lower()
        if guess in secret_word:
            letters_guessed.append(guess)
            print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
        elif guess not in available_letters:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                warnings = 3
            print("Oops! That is not a valid letter. You have ",warnings,"warnings left: ", get_guessed_word(secret_word, letters_guessed))
        elif guess in vowels and guess not in secret_word and guess not in letters_guessed:
            print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
            guesses -= 2 
        elif guess in letters_guessed:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                warnings = 3
            print("You already guessed that letter! You have ",warnings,"warnings left. Try again.")
        else:
            print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
            guesses -= 1
        letters_guessed.append(guess)
    if is_word_guessed(secret_word, letters_guessed) == True:
        guesses_remaining = guesses
        total_score = guesses_remaining * len(unique_letters)
        print("Congratulations you won!")
        print("Your total score for this game is: ", total_score)
    else:
        print("Sorry you ran out of guesses. The word was: ", secret_word)



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_with_no_spaces = ""
    letters_guessed = []
    for char in my_word:
        if char != " ":
            my_word_with_no_spaces += char
        if char.isalpha():
            letters_guessed.append(char)
    if len(my_word_with_no_spaces.strip()) != len(other_word.strip()):
        return False
    for i in range(len(my_word_with_no_spaces)):
        current_letter = my_word_with_no_spaces[i]
        other_letter = other_word[i]
        if current_letter.isalpha():
            has_same_letter = current_letter == other_letter
            if not has_same_letter:
                return False
        else: 
            if current_letter == "_" and other_letter in letters_guessed:
                    return False
    return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    word_list = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            word_list.append(word)
    if len(word_list) > 0:
        for word in word_list:
            print(word, " ")
    else:
        print("no matches found")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    available_letters = string.ascii_lowercase
    unique_letters = []
    for x in secret_word:
        if x not in unique_letters:
            unique_letters.append(x)
    guesses = 6
    warnings = 3
    vowels = "aeiou"
    letters_guessed = []
    secret_word = choose_word(wordlist)
    print("Welcome to the game of Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long")
    while guesses > 0 and is_word_guessed(secret_word, letters_guessed) != True:
        print("--------")
        print(get_guessed_word(secret_word, letters_guessed))        
        print("You have ", guesses," guesses left")
        print(get_available_letters(letters_guessed))
        guess = input("Please guess a letter: ")
        guess = guess.lower()
        if guess in secret_word:
            letters_guessed.append(guess)
            print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
        elif guess == "*":
            print("Possible word matches are: ")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        elif guess not in available_letters:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                warnings = 3
            print("Oops! That is not a valid letter. You have ",warnings,"warnings left: ", get_guessed_word(secret_word, letters_guessed))
        elif guess in vowels and guess not in secret_word and guess not in letters_guessed:
            print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
            guesses -= 2 
        elif guess in letters_guessed:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                warnings = 3
            print("You already guessed that letter! You have ",warnings,"warnings left. Try again.")
        else:
            print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
            guesses -= 1
        letters_guessed.append(guess)
    if is_word_guessed(secret_word, letters_guessed) == True:
        guesses_remaining = guesses
        total_score = guesses_remaining * len(unique_letters)
        print("Congratulations you won!")
        print("Your total score for this game is: ", total_score)
    else:
        print("Sorry you ran out of guesses. The word was: ", secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
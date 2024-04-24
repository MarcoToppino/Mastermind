from random import randint
import time,sys

"""
Declare Global Variables
"""
turn = 0




def typingPrint(text):
    """
    Typewriting effect for Print method
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
  
def typingInput(text):
    """
    Typewriting effect for Input method
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    value = input()  
    return value


def ask_player_name():
    """
    Ask for the player name and print a welcome message
    """
    player_name = typingInput("Please login with your name:  ")
    typingPrint(f"\nGood morning {player_name}:\n\n")
    typingPrint(f"Shall we play a game?\n")
    typingPrint(f"What about a nice round at Mastermind?\n\n")
    typingPrint(f"I will play with you...my name is Joshua.\n\n")
    typingPrint(f"The game is very simple: we will both try to crack a secret code\n\n")
    typingPrint(f"The code is made of 4 digits, between 0 and 9\n")
    typingPrint(f"If we guess a digit in the right place of the code, it will show up in the feedback\n")
    typingPrint(f"If it is there, but in the wrong place, an X will appear, instead\n\n")
    typingPrint(f"Let's see who will crack the code first....and launch the missiles!\n\n")
    return player_name

def prepare_board(player_name):
    """
    Builds the two empty Boards, CPU on the left, player on the right
    """
    typingPrint(f"   Joshua          {player_name}\n")
    for row in range(1,10):
        print(f"|....| |....| - |....| |....|\n")
  
def create_random_code():
    """
    Creates a 4 digit code with integers 0-9
    """
    secret = []
    for num in range(4):
        secret.append(randint(1,9))
            
    return secret

def input_player_guess ():
    """
    Ask the player to input a guess for the code
    """
    player_guess = typingInput("Guess the ccode: ")
    return player_guess




player_name = ask_player_name()
turn = prepare_board(player_name)
secret_cpu = create_random_code()
secret_player = create_random_code()
player_guess = input_player_guess()
print(secret_cpu)
print(secret_player)
print(turn)
print(player_guess)

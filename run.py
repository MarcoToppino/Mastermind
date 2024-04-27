from random import randint
import time,sys

"""
Declare Global Variables
"""
turn = 0
history = []
feedback_cpu=[]
feedback_player = []

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
    typingPrint(f"The code is made of 4 digits, between 1 and 9\n")
    typingPrint(f"If we guess a digit in the right place of the code,\nit will show up in the feedback\n")
    typingPrint(f"If it is there, but in the wrong place, an X will appear\n\n")
    typingPrint(f"Let's see who will crack the code first....and launch the missiles!\n\n")
    return player_name

def prepare_board(player_name):
    """
    Builds the two empty Boards, CPU on the left, player on the right
    """
    typingPrint(f"       Joshua               {player_name}\n")
    typingPrint(f"   Code   Feedback      Code    Feedback\n")
    for row in range(1,10):
        print  (f"|. . . .| |. . . .| - |. . . .| |. . . .|\n")
  
def create_random_code():
    """
    Creates a 4 digit code with integers 0-9
    """
    secret = []
    for num in range(4):
        secret.append(randint(1,9))
            
    return secret


def validate_guess(guess):
    """
    Validate the imput guess from the player
    It must ba 4 digits (integers)
    Inside the try, converts the string value into integer.
    Raises ValueError if string cannot be converted into int,
    or if there aren't exactly 4 characters.
    """
    try:
        int(guess)
        if len(guess) != 4:
            raise ValueError(
                f"Exactly 4 digits required, you provided {len(guess)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def input_player_guess ():
    """
    Ask the player to input a guess for the code
    Continue to ask if the input is not valid
    """
    while True:
        player_guess = typingInput("Guess the code: ")
        if validate_guess(player_guess):
            typingPrint(f"Checking your code....\n")
            time.sleep(1)
            typingPrint(f"I'm also trying my code.... \n")
            time.sleep(1)
            typingPrint(f"Here is our feedback.... \n")
            break
            
    return player_guess


def evaluate_guess(player, guess, secret):
    """
    Converts the guess into a list
    Evaluate the guess against the corresponding code (player or CPU)
    creates the feedback
    """
    list_guess = [int(char) for char in guess]
    feedback = []
    for num in range(4):
        if list_guess[num] == secret[num]:
            feedback.append(list_guess[num])
        elif list_guess[num] != secret[num] and list_guess[num] in secret:
            feedback.append("X")
        else:
            feedback.append(".")
    return feedback


def cpu_almost_random_guess():
    """
    Creates the guess for the cpu.
    random integer for the unkonown digits,
    random, but avoiding the already known, for the known
    """
    if turn == 0:
        #first round (turn = 0) is pure random
        cpu_guess = create_random_code()
    elif feedback_cpu == [".",".",".","."]:
        #no digits found is pure random 
        cpu_guess = create_random_code()
    else:
        for num in range(4):
            if feedback_cpu[num] == ".":
                #digit not found is random
                cpu_guess.append(randint(1,9))
            elif feedback_cpu[num] == "X":
                #digit wrong place is random            
                cpu_guess.append(randint(1,9))
            else:
                #digit found right is the same digit
                cpu_guess.append(feedback_cpu[num])
    return cpu_guess

def make_string(list):
        string = " ".join(str(e) for e in list)
        return string


def create_history(player_guess, feedback_player, cpu_guess, feedback_cpu):
    """
    Creates a string for a full turn of the board
    add it to the list that represents the board
    """
    #takes every variable and convert to a string, so that can be created the full line as a string
    str_player_guess = make_string(player_guess)
    print(str_player_guess)
    str_feedback_player = make_string(feedback_player)
    print(str_feedback_player)
    str_cpu_guess = make_string(cpu_guess)
    print(str_cpu_guess)
    str_feedback_cpu = make_string(feedback_cpu)
    print(str_feedback_cpu)    


    line = "|" + str_cpu_guess + "| |" + str_feedback_cpu + "| - |" + str_player_guess + "| |" + str_feedback_player + "|"
    return line

"""
Sequence of activities to prepare the game
"""
player_name = ask_player_name()
prepare_board(player_name)
secret_cpu = create_random_code()
secret_player = create_random_code()
print(f"Secret_player {secret_player}")
print(f"Secret_cpu {secret_cpu}")

player_guess = input_player_guess()
validate_guess(player_guess)


"""
Sequence of activities to execute the game
evaluate the guess against the secret and create the feedback
create a guess for the CPU
evaluate the guess against the secret and create the feedback
store the values in the history list
if the code is same as secret, evaluate victory (cpu or player).
print the board with the history + the remaining empty turns
increase turns
if the turnes are fininshed...evaluate victory
"""
feedback_player = evaluate_guess("Player", player_guess, secret_player)
print(f"feedback_player {feedback_player}")
cpu_guess = cpu_almost_random_guess()
print(f"cpu_guess {cpu_guess}")
feedback_cpu = evaluate_guess("CPU", cpu_guess, secret_cpu)
print(f"feedback_cpu {feedback_cpu}")
line = create_history(player_guess, feedback_player, cpu_guess, feedback_cpu)
print(line)
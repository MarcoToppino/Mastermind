from random import randint
import time,sys
import os

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
    player_name = typingInput(" Please login with your name:  ")
    typingPrint(f"\n Good morning {player_name}:\n\n")
    typingPrint(f" Shall we play a game?\n")
    typingPrint(f" What about a nice round at Mastermind?\n\n")
    typingPrint(f" I will play with you...my name is Joshua.\n\n")
    typingPrint(f" The game is very simple: we will both try to crack a secret code\n\n")
    typingPrint(f" The code is made of 4 digits, between 0 and 9\n")
    typingPrint(f" If we guess a digit in the right place of the code,\n it will show up in the feedback\n")
    typingPrint(f" If it is there, but in the wrong place, an X will appear\n\n")
    typingPrint(f" Let's see who will crack the code first....and launch the missiles!\n\n")
    time.sleep(2)
    return player_name

def prepare_board(player_name):
    """
    Builds the two empty Boards, CPU on the left, player on the right
    """
    typingPrint(f"       Joshua               {player_name}\n")
    typingPrint(f"   Code   Feedback      Code    Feedback\n")
    for row in range(0,10):
        print  (f"|. . . .| |. . . .| - |. . . .| |. . . .|")
  
def create_random_code():
    """
    Creates a 4 digit code with integers 0-9
    """
    secret = []
    for num in range(4):
        secret.append(randint(0,9))
            
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
        player_guess = typingInput(f" {player_name}, guess your code: ")
        if validate_guess(player_guess):
            os.system("clear")
            typingPrint(f" Checking your code, {player_name}....\n\n")
            time.sleep(1)
            typingPrint(f" I'm also trying my code....\n\n")
            time.sleep(1)
            typingPrint(f" Here is our feedback....\n\n")
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
                cpu_guess.append(randint(0,9))
            elif feedback_cpu[num] == "X":
                #digit wrong place is random            
                cpu_guess.append(randint(0,9))
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
    add it to the history list that represents the board
    """
    #takes every variable and convert to a string, so that can be created the full line as a string
    str_player_guess = make_string(player_guess)
    str_feedback_player = make_string(feedback_player)
    str_cpu_guess = make_string(cpu_guess)
    str_feedback_cpu = make_string(feedback_cpu)
    line = "|" + str_cpu_guess + "| |" + str_feedback_cpu + "| - |" + str_player_guess + "| |" + str_feedback_player + "|"
    history.append(line)
    return history

def board_update():
    """
    Update the board with the different lines in the history list
    fills the remaining turns with empty lines
    """
    typingPrint(f"       Joshua               {player_name}\n")
    typingPrint(f"   Code   Feedback      Code    Feedback\n")
    for row in range(len(history)):
        typingPrint(f"{str(history[row])}\n")
    for row in range(turn+1,10):
        print  (f"|. . . .| |. . . .| - |. . . .| |. . . .|")

def evaluate_victory(guess, secret, player):
    """
    Evaluate the guess vs the secret
    If the code is fully found, depending of the player (CPU-Player)
    Prepares a victory-loosing message
    If the code is almost there (1 missing), depending of the player
    Prepare an "almost there" message
    If not found, send for a new turn of guess
    """    
    list_guess = [int(char) for char in guess]
    count = 0
    for num in range(4):
        if list_guess[num] == secret[num]:
            count = count +1
    
    if count == 4:
        print("Code found!")
    elif count == 3 and player == "CPU":
        print("I'm almost there....better you call the President....Defcon 1")
    elif count == 3 and player == "Player":
        print("You're almost there....we're not playing 'Global Thermonuclear War', or are we?...")
    elif player == "CPU" and count <4:
        global turn
        turn = turn + 1
"""
Sequence of activities to prepare the game
"""
player_name = ask_player_name()
prepare_board(player_name)
secret_cpu = create_random_code()
secret_player = create_random_code()
print(f"Secret_player {secret_player}")
print(f"Secret_cpu {secret_cpu}")



def play_game():
    """
    Sequence of activities to execute the game
    ask and validate input from the player
    evaluate the guess against the secret and create the feedback
    create a guess for the CPU
    evaluate the guess against the secret and create the feedback
    store the values in the history list
    print the board with the history + the remaining empty turns
    if the code is same as secret, evaluate victory (cpu or player).
    if only one number is missing for cpu...special message
    increase turns and ask for a new input
    if the turns are fininshed...evaluate victory
    """
    player_guess = input_player_guess()
    validate_guess(player_guess)
    feedback_player = evaluate_guess("Player", player_guess, secret_player)
    cpu_guess = cpu_almost_random_guess()
    feedback_cpu = evaluate_guess("CPU", cpu_guess, secret_cpu)
    create_history(player_guess, feedback_player, cpu_guess, feedback_cpu)
    board_update()
    print(f"Secret_player {secret_player}")
    print(f"Secret_cpu {secret_cpu}")
    evaluate_victory(player_guess, secret_player, "Player")
    evaluate_victory(cpu_guess, secret_cpu, "CPU")
    """
    If there are more turns to play asks for a new guess
    """
    if turn <= 9:
        play_game()
    else:
        print("game finished")

play_game()
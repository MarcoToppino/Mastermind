from random import randint
import time
import sys
import os
from pyfiglet import Figlet

# Declare Global Variables
turn = 0
history = []
feedback_cpu = []
choice = ""
secret_player = []
secret_cpu = []
player = ""
new = False


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
    #loop for a valid name (no empty)
    while True:
        player_name = typingInput(" Please login with your name:  ")
        if len(player_name) > 0:
            break

    typingPrint(f"\n Greetings {player_name}:\n\n")
    typingPrint(f" Shall we play a game?\n")
    typingPrint(f" How about a nice game of Mastermind?\n\n")
    typingPrint(f" I will play with you...my name is Joshua.\n\n")
    typingPrint(f" The game is very simple:\n")
    typingPrint(f" we will both try to crack a secret code\n\n")
    typingPrint(f" The code is made of 4 digits, between 0 and 9\n")
    typingPrint(f" If we guess a digit in the right place of the code,\n")
    typingPrint(f" it will show up in the feedback\n")
    typingPrint(
        f" If it is there, but in the wrong place, an X will appear\n\n"
        )
    typingPrint(f" Let's see who will crack the code first....\n\n")
    typingPrint(f" ...and launch the missiles!\n\n")
    time.sleep(2)
    return player_name


def prepare_board(player_name):
    """
    Builds the two empty Boards, CPU on the left, player on the right
    """
    typingPrint(f"       Joshua               {player_name}\n")
    typingPrint(f"   Code   Feedback      Code    Feedback\n")
    for row in range(0, 10):
        print(f"|. . . .| |. . . .| - |. . . .| |. . . .|")


def create_random_code():
    """
    Creates a 4 digit code with integers 0-9
    """
    secret = []
    for num in range(4):
        secret.append(randint(0, 9))

    return secret


def validate_guess(guess):
    """
    Validate the imput guess from the player
    It must ba 4 digits (integers)
    Inside the try, converts the string value into integer.
    Raises ValueError if string cannot be converted into int,
    or if there aren't exactly 4 characters.
    """
    if str(guess).isnumeric() is True and len(guess) == 4:
        return True
    else:
        typingPrint(
            f" The code must contain only 4 numbers. Please try again\n"
            )
        return False


def input_player_guess():
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
    cpu_guess = []
    if turn == 0:
        # first round (turn = 0) is pure random
        cpu_guess = create_random_code()
    elif make_string(feedback_cpu) == ["...."]:
        # no digits found is pure random
        cpu_guess = create_random_code()
    else:
        for num in range(4):
            if feedback_cpu[num] == ".":
                # digit not found is random
                cpu_guess.append(randint(0, 9))
            elif feedback_cpu[num] == "X":
                # digit wrong place is random
                cpu_guess.append(randint(0, 9))
            else:
                # digit found right is the same digit
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
    # takes every variable and convert to a string,
    # so that can be created the full line as a string
    str_player_guess = make_string(player_guess)
    str_feedback_player = make_string(feedback_player)
    str_cpu_guess = make_string(cpu_guess)
    str_feedback_cpu = make_string(feedback_cpu)
    line1 = "|" + str_cpu_guess + "| |" + str_feedback_cpu
    line2 = "| - |" + str_player_guess + "| |" + str_feedback_player + "|"
    line = line1 + line2
    history.append(line)
    return history


def board_update():
    """
    Update the board with the different lines in the history list
    fills the remaining turns with empty lines
    The first lines are printed fast
    """
    typingPrint(f"       Joshua               {player_name}\n")
    typingPrint(f"   Code   Feedback      Code    Feedback\n")
    for row in range(len(history)-1):
        print(f"{str(history[row])}")

    typingPrint(f"{str(history[-1])}\n")

    for row in range(turn+1, 10):
        print(f"|. . . .| |. . . .| - |. . . .| |. . . .|")


def evaluate_victory(guess, secret, player):
    """
    Evaluate the guess vs the secret
    If the code is fully found ends the game
    If the code is almost there (1 missing), depending of the player
    Prepare an "almost there" message
    If not yet found, check for turns and send for a new turn of guess
    """
    list_guess = [int(char) for char in guess]
    count = 0
    for num in range(4):
        if list_guess[num] == secret[num]:
            count = count + 1

    if count == 4:
        # exits the game when code found
        game_end(player)
    elif count == 3 and player == "CPU":
        print(f"I'm almost there....\n")
        print(f"better you call the President....I'm moving to Defcon 1\n")
    elif count == 3 and player == "Player":
        print(f"You're almost there....\n")
        print(f"we're not playing 'Global Thermonuclear War', or are we?...\n")

    global turn
    if player == "CPU":
        turn = turn + 1

    if turn == 10:
        game_end(player)
    else:
        play_game


def keep_playing():
    """
    Prompts for a new round
    """
    global new
    while True:
        time.sleep(1)
        choice = typingInput(
            f"\n How about another round?   (Y/N)     "
            ).upper()
        if choice == "Y":
            new = True
            new_game()
            play_game()
        elif choice == "N":
            typingPrint(f"\n Thank you for playing with me.\n")
            print("(To restart the game, please press 'RUN PROGRAM'")
            exit()
        else:
            print(" Please enter Yes[Y] or No[N].")
            continue
        break


def game_end(player):
    """
    Depending of the condition, there is a different end
    CPU wins:
    Player wins:
    no more turns:
    After the sequence: propose a new round
    """
    global turn
    if turn < 10 and player == "Player":
        time.sleep(2)
        f = Figlet(font='slant')
        print(f.renderText("YOU WON !"))
        time.sleep(1)
        print(f.renderText("YOU'RE LAUNCHING"))
        time.sleep(0.5)
        print(f.renderText("YOUR MISSILES !"))
        time.sleep(2)
        os.system("clear")
        time.sleep(2)
        typingPrint(f" Greetings {player_name}\n")
        time.sleep(1)
        typingPrint(f" A very strange game...\n")
        time.sleep(1)
        typingPrint(
            f" You won, but no one can really win launching missiles...\n"
            )
        time.sleep(1)
        typingPrint(f" The only winning move is not to play...\n")
        keep_playing()

    elif turn < 10 and player == "CPU":
        time.sleep(2)
        f = Figlet(font='slant')
        print(f.renderText("JOSHUA WON !"))
        time.sleep(1)
        print(f.renderText("I'M LAUNCHING"))
        time.sleep(0.5)
        print(f.renderText("MY MISSILES !"))
        time.sleep(2)
        os.system("clear")
        time.sleep(2)
        typingPrint(f" Greetings {player_name}\n")
        time.sleep(1)
        typingPrint(f" A very strange game...\n")
        time.sleep(1)
        typingPrint(
            f" You won, but no one can really win launching missiles...\n"
            )
        time.sleep(1)
        typingPrint(f" The only winning move is not to play...\n")
        keep_playing()

    elif turn == 10:
        typingPrint(
            f"\n\n No one of us seems to be able to find the code...\n"
            )
        keep_playing()


def new_game():
    """
    Sequence of activities to prepare the game
    """
    global secret_cpu
    global secret_player
    global history
    global turnLucidchart
    global new
    if new is True:
        history.clear()
        turn = 0
    prepare_board(player_name)
    secret_cpu = create_random_code()
    secret_player = create_random_code()


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
    if only one number is missing for cpu or player...special message
    increase turns and ask for a new input
    if the turns are fininshed...evaluate exit
    """
    global feedback_cpu
    global secret_player
    global secret_cpu
    global new
    global turn
    player_guess = input_player_guess()
    validate_guess(player_guess)
    feedback_player = evaluate_guess("Player", player_guess, secret_player)
    cpu_guess = cpu_almost_random_guess()
    feedback_cpu = evaluate_guess("CPU", cpu_guess, secret_cpu)
    create_history(player_guess, feedback_player, cpu_guess, feedback_cpu)
    board_update()
    evaluate_victory(player_guess, secret_player, "Player")
    evaluate_victory(cpu_guess, secret_cpu, "CPU")


# main sequence
player_name = ask_player_name()
new_game()
# infinite loop, unless broken directly in the code with exit()
while True:
    play_game()

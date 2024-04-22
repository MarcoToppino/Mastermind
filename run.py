from random import randint

def ask_player_name():
    """
    Ask for the player name and print a welcome message
    """
    player_name = input("Please input your name:  ")
    print(f"\nGood morning {player_name}: what about a nice game at Mastermind?\n")
    print(f"I will play with you...my name is Joshua.\n")
    print(f"The game is simple: we will both try to crack a secret code")
    print(f"The code is made of 4 digits, between 0 and 9")
    print(f"If we guess a digit in the right place of the code, it will show up in the feedback")
    print(f"If it is there, but in the wrong place, an X will appear in the feedback")
    print(f"Let's see who will crack the code first....and launch the missiles!\n")
    return player_name

def prepare_board(player_name):
    """
    Builds the two empty Boards, CPU on the left, player on the right
    """
    print(f"   Joshua          {player_name}")
    for row in range(1,10):
        print(f"|....| |....| - |....| |....|")

def create_random_code():
    """
    Creates a 4 digit code with integers 0-9
    """
    secret = []
    for num in range(4):
        secret.append(randint(1,9))
    return secret

player_name = ask_player_name()
prepare_board(player_name)
secret_cpu = create_random_code()
secret_player = create_random_code()
print(secret_cpu)
print(secret_player)

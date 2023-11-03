"""
ABSFUYU
-------
Game

Contain some game that can be played on terminal
"""

# Module level
##############################################################
__all__ = [
    "game_escapeLoop", "game_RockPaperScissors",
]



# Library
##############################################################
from random import choice as __randChoice




# Default games
##############################################################
def game_escapeLoop():
    """Try to escape the infinite loop"""
    
    init = True
    welcome_messages = [
        "Congrats! You are now stuck inside an infinite loop.",
        "Do you want to escape this loop?"
    ]

    num1 = __randChoice([2,3,4,5,6,7,8,9,10,11,12])
    num2 = __randChoice([2,3,4,5,6,7,8,9,10,11,12])
    hidden_answer = str(num1 * num2)

    game_messages = [
        "Are you sure about this?",
        "Don't leave me =((",
        "I can't believe you did this to me!",
        "Are you very much sure?",
        "I'll be sad. Pick again please.",
        "I still don't believe you.", 
        "Choose again.",
        "You actually have to answer the correct keyword",
        "I think you need to choose again.",
        "Last chance!",
        "Okay okay, i believe you ;)",
        "Almost there.",
        "I can do this all day", 
        "So close!",
        "You can't escape from me.",
        "How are you still here, just to suffer?",
        "Never gonna give you up",
        "Never gonna let you down",
        f"Hint 01: The keyword is: {num1}",
        f"Hint 02: *{num2}",
    ]

    congrats_messages = [
        "Congratulation! You've escaped."
    ]
    
    while True:
        # Welcome
        if init:
            for x in welcome_messages:
                print(x)
            answer = str(input())
            init = False
        
        # Random text
        mess = __randChoice(game_messages)
        print(mess)

        # Condition check
        answer = str(input())
        if answer == hidden_answer:
            for x in congrats_messages:
                print(x)
            break
    pass


def game_RockPaperScissors(hard_mode=False):
    """Rock Paper Scissors"""
    
    state_dict = {
        0: "rock",
        1: "paper",
        2: "scissors"
    }
    
    init = True

    end_message = "end"

    welcome_messages = [
        "Welcome to Rock Paper Scissors",
        f"Type '{end_message}' to end",
    ]

    game_messages = [
        "Pick one option to begin:",
    ]

    game_summary = {
        "Win": 0,
        "Draw": 0,
        "Lose": 0
    }
    
    while True:
        # Welcome
        if init:
            for x in welcome_messages:
                print(x)
            init = False
        
        # Game start
        print("")
        for x in game_messages:
            print(x)
        print(state_dict)
        
        # Player's choice
        answer = input()

        # Condition check
        if answer == end_message:
            print(game_summary)
            break
        
        elif answer not in ["0","1","2"]:
            print("Invalid option. Choose again!")
        
        else:
            # Calculation
            answer = int(answer)
            if hard_mode:
                if answer == 0:
                    game_choice = __randChoice([0,1])
                if answer == 1:
                    game_choice = __randChoice([1,2])
                if answer == 2:
                    game_choice = __randChoice([0,2])
            else:
                game_choice = __randChoice([0,1,2])
            print(f"You picked: {state_dict[answer]}")
            print(f"BOT picked: {state_dict[game_choice]}")
            
            if answer == 2 and game_choice == 0:
                print("You Lose!")
                game_summary["Lose"] += 1
            elif answer == 0 and game_choice == 2:
                print("You Win!")
                game_summary["Win"] += 1
            elif answer == game_choice:
                print("Draw Match!")
                game_summary["Draw"] += 1
            elif answer > game_choice:
                print("You Win!")
                game_summary["Win"] += 1
            else:
                print("You Lose!")
                game_summary["Lose"] += 1

    return game_summary
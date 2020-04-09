import json, random, time

from PIL import Image
from thermalprinter import *

import board, busio, serial
import RPi.GPIO as GPIO

class Game:
    stage = 0 # Default
    button_pressed = None # 0:left / 1:right / 2:reset
    games = None
    """
    # games_dict = {game_number:{stage_number:{text,button}}
    games_dict = {0:{0:{"text":"You wake up and as you blink your bleary eyes, you...",
                        "button":(None, None, None)},
                    1:{"text":"You hear a sound...like a [thump]...",
                        "button":("You fall out of bed... ouch!","You find your glasses. \"Oh, that is better! Now what?", None)},
                    2:{"text":"Well, now that I'm awake, it was just all a dream. Thanks for playing.\n\n",
                        "button":("You pick up your phone.", "I just need coffee...\n\n", None)},
                    },
                  1:{0:{"text":"This is game number two",
                        "button":(None, None, None)},
                     1:{"text":"STAGE 2: Meow mewo meow meow, what's your next choice?",
                        "button":("meow1 yellow choice 1", "meow2 blue choice", None)},
                     2:{"text":"next is game over\n\n",
                        "button":("No more Mews for you", "Meowthing to see here. but thank you for playing\n\n", None)}
                    }
    }
    """
    num_of_games = 0
    game_number = 0

def print_welcome_message(printer):
    ''' Prints the welcome message when game starts'''
    # The Dublin Maker logo at the top
    printer.image(Image.open("dm-bw.png"))

    # Welcome message and instructions to start game
    printer.out("Welcome to Vicky's print and play your own text-based adventure game",
                double_height = True,
                underline = 2)
    printer.feed(2)
    printer.out("Push a button to start playing.", bold=True)
    print_button_choices_text()

def print_endgame_message():
    printer.out("Made by Vicky Twomey-Lee", justify="C")
    printer.out("Maker Advocate", double_width=True)
    printer.out("Dublin Maker Festival", bold=True, justify="C")
    printer.out("Summer 2021", bold=True, justify="C")
    printer.out("DublinMaker.ie", bold=True, justify="C")
    printer.feed(1)
    printer.out("Inspired by Der Choosatron found at Berlin Game Science Center", justify="L")
    printer.feed(5)

def print_game_text(game_choice):
    current_game = game_choice.games[game_choice.game_number].get("game_stage")[game_choice.stage]

    try:
        if game_choice.button_pressed != 2:
            button_choice_text = current_game.get("button")[game_choice.button_pressed]
            print(button_choice_text)
            printer.out(button_choice_text)
    except:
        pass

    print(current_game.get("text"))
    printer.out(current_game.get("text"))

    print(f">game_choice.stage {game_choice.stage}")
    if game_choice.stage < 2:
        print_button_choices_text()


def print_button_choices_text():
    printer.out(" "*5 + "|" + " "*20 + "|")
    printer.out("[yellow/left]" + " "*7 + "[blue/right]")
    printer.out("|", justify="C")
    printer.out("|", justify="C")
    printer.out("[black/reset]", justify="C")
    printer.feed(3)


def pick_a_game(json_data):
    a_game = Game()
    a_game.games = json_data
    a_game.num_of_games = len(a_game.games)

    # Set up to pick a random game
    a_game.game_number = random.randint(0, a_game.num_of_games-1)
    return a_game


# Setting up and where the code starts
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

games = {0:"Fun game 1", 1:"Fun game 2"}
game_picked = False

printer = ThermalPrinter(port="/dev/serial0")

# Print welcome message
print_welcome_message(printer)

# Load the JSON file called games.json
with open("games.json", "r") as f:
    data = f.read()

# We now have the json data
# List of games (dictionaries)
#   - each game dict has a list of stages that contains
#   ---- text displayed at end of each stage
#   ---- text depending if player pressed yellow or blue button
#   ---- Black button only resets game, no texts
json_data = json.loads(data)

try:
    a_game = pick_a_game(json_data)

    print(f"> a_game.num_of_games: {a_game.num_of_games}")
    print(f">a_game.game_number: {a_game.game_number}")
    print(f"> GAME STARTS. STAGE {a_game.stage}")

    while True:
        blue_button_state = GPIO.input(16)
        yellow_button_state = GPIO.input(23)
        black_button_state = GPIO.input(26)

        if not blue_button_state:
            print("> Blue button pressed <")
            a_game.button_pressed = 1
            print_game_text(a_game)
            a_game.stage += 1
            time.sleep(0.2)
        elif not yellow_button_state:
            print("> Yellow button pressed <")
            a_game.button_pressed = 0
            print_game_text(a_game)
            a_game.stage += 1
            time.sleep(0.2)
        elif not black_button_state or a_game.stage == 3:
            a_game = Game()
            if not black_button_state:
                print(">GAME TO RESET")
                printer.out("Ok, let's restart the game!")
                print_welcome_message(printer)
            else:
                print(">END OF GAME, THANKS FOR PLAYING")
                printer.feed(1)
                printer.out("Thanks for playing!", double_height=True, justify="C")
                printer.out("To reset game,", justify="C")
                printer.out("hit the black button!", justify="C")
                printer.feed(2)

                print_endgame_message()
            a_game = pick_a_game(json_data)
except:
    GPIO.cleanup()
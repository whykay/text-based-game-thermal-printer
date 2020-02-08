
import adafruit_thermal_printer
import board
import busio
import serial

import RPi.GPIO as GPIO

import random
import time

class Game:
    stage = 0 # Default
    button_pressed = None # 0:left / 1:right / 2:reset

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

    num_of_games = len(games_dict)
    game_number = random.randint(0, num_of_games-1)

def print_welcome_message(printer):
    ''' Prints the welcome message when game starts'''
    printer.feed(2)
    printer.double_height = True
    printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
    printer.print("Welcome to Vicky's print and play your own text-based adventure game")
    printer.double_height = False
    printer.underline = None

    printer.feed(2)
    printer.bold = True
    printer.print("Push a button to start playing.")
    printer.bold = False
    printer.feed(2)

    printed = False
    print_button_choices_text()

def print_endgame_message():
    printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
    printer.double_height = True
    printer.print("Thanks for playing!")
    printer.double_height = False

    printer.print("Made by Vicky Twomey-Lee")

    printer.double_width = True
    printer.print("Maker Advocate\n\n")
    printer.double_width = False

    printer.bold = True
    printer.print("Dublin Maker Festival\nSat Jun 27, Herbert Park, Dublin\nDublinMaker.ie\n\n")
    printer.bold = False

    printer.print("Inspired by Der Choosatron found at Berlin Game Science Center")
    printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
    printer.feed(5)

def print_game_text(game_choice):
    current_game = game_choice.games_dict[game_choice.game_number]
    print(current_game[a_game.stage]["button"])
    print

    try:
        if game_choice.button_pressed != None:
            button_choice_text = current_game[a_game.stage]["button"][game_choice.button_pressed]
            printer.print(button_choice_text)
    except:
        pass

    printer.print(current_game[a_game.stage]["text"])

    if a_game.stage < 2:
        print_button_choices_text()

def print_button_choices_text():
    printer.print("\t\t|\t\t\t|")
    printer.print("\t\t|\t\t\t|")
    printer.print("[yellow/left]\t\t[blue/right]")
    printer.feed(3)

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

games = {0:"Fun game 1", 1:"Fun game 2"}
game_picked = False

ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
RX = board.RX
TX = board.TX

uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
printer = ThermalPrinter(uart, auto_warm_up=False)
printer.warm_up()

# Print welcome message
print_welcome_message(printer)

try:
    a_game = Game()
    print(f">>> GAME STARTS. STAGE {a_game.stage}")

    while True:
        blue_button_state = GPIO.input(16)
        yellow_button_state = GPIO.input(23)

        if not blue_button_state:
            print("Blue button pressed")
            a_game.button_pressed = 1
            print_game_text(a_game)
            a_game.stage += 1
            time.sleep(0.2)
        elif not yellow_button_state:
            print("Yellow button pressed")
            a_game.button_pressed = 0
            print_game_text(a_game)
            a_game.stage += 1
            time.sleep(0.2)
        elif a_game.stage == 3:
            a_game = Game()
            print(">GAME TO RESET")
            print(">END OF GAME, THANKS FOR PLAYING")
            print_endgame_message()
            print_welcome_message(printer)
except:
    GPIO.cleanup()
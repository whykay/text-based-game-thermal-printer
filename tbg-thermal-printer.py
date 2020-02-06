import random

class Game:
    stage = 0 # Default
    button_pressed = None # 0:left / 1:right / 2:reset

    # games_dict = {game_number:{stage_number:{text,button}}
    games_dict = {0:{0:{"text":"You wake up and as you blink your bleary eyes, you... \nPick <yellow> or <blue>",
                        "button":(None, None, None)},
                    1:{"text:":"You hear a sound...like a <thump>... \nPick <yellow> or <blue>",
                        "button":("You fall out of bed... ouch!","You find your glasses. \"Oh, that's better!\"\nNow what?", None)},
                    2:{"text":"Ok, I heard something, better check it out. You pick up a...",
                        "button":("You pick up your phone.", "I just need coffee...", None)},
                    },
                  1:{0:{"text":"This is game number two", 
                        "button":(None, None, None)},
                     1:{"text":"one to stage 2",
                        "button":("meow1", "meow2", None)},
                     2:{"text":"next is game over",
                        "button":("meowmeow1", "meow2meow2", None)}
                    }
    }

    num_of_games = len(games_dict)
    game_number = random.randint(0, num_of_games-1)

def welcome():
    print("Welcome to Vicky's print and play text-based adventure game.")

def start_game():
    a_game = Game()
    a_game.button_colour = button

    # Start game message
    current_game = a_game.games_dict[a_game.game_number]
    print(current_game[a_game.stage]["text"])

    while True:
        picked = int(input())
        a_game.stage += 1
        if a_game.stage > 2:
            return

        button_picked = current_game[a_game.stage]["button"][picked]
        if not button_picked:
            print("RESETTING")
            return
        print(current_game[a_game.stage]["button"][picked])


if __name__ == "__main__":
    button = "yellow"
    welcome()
    start_game()
    print("\nGAME OVER\n")
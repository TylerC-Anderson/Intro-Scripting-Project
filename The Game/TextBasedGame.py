### ESCAPE FROM XENON-5 ###
 ## By Tyler C Anderson ##

# Game Main

"""
PURPOSE: Contains the main script for the game, including the play loop and a
module for printing in a user friendly way. Also contains win conditions,
decision branching for those win cons and error messages.

INPUTS: Accepts user input for navigation and grabbing items.

OTHER MODULES: game_utils.py -- contains the rooms dictionary, rooms tuples and
the functions, navigate and grab_item. The remaining modules are imported for
the delayed print function, and for accepting room descriptions from text files.
"""

# import the game_utils module, which contains the rooms dictionary and the
# navigate and grab_item functions.
import game_utils
import sys,time
from pathlib import Path

# initialize the error codes and valid inputs for the game
COMMANDS = ['Move', 'Grab', 'Examine']
DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = COMMANDS + [EXIT_COMMAND]
INVALID_COMMAND = f"That is not a valid command. You need to enter one of the following commands: {str(VALID_INPUTS)}.\nIf you enter a move command, it must be in one of the following directions: {str(DIRECTIONS)}.\n If you are trying to grab an item, you need to enter the items name with your grab command."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing!"
EXIT_ROOM_SENTINEL = "exit"
NOT_VISITED_OR_GRABBED = "You don't see that item anywhere in here, or you are not in that room. Please try again."

# initialize the win conditions and best ending conditions and sort them for
# easier comparison
WIN_CON = [
    'Universal Translator', 'Hangar Key',
    'Ship Map', 'Space Suit',
    'Cloaking Device', 'Baton',
    ]
BEST_ENDING = WIN_CON + ['Voice Activated Navigator']
WIN_CON.sort()
BEST_ENDING.sort()

# initialize the rooms dictionary from game_utils for readability and the
# description document
rooms = game_utils.rooms_dict()
desc_doc = ''

# initialize the parent directory for the description documents
parent_dir = Path(__file__).parent.resolve() / 'Descriptions'
# parent_dir = Path(__file__).parent.resolve() / 'Test Descriptions' # uncomment to test with the test descriptions


def main():
    """
    Contains the loop that will run the game until the exit condition is satisfied. Starts in the Start room and prints a welcome message.
    """

    # initialize the starting conditions for the game
    current_room = 'Start'
    player_inventory = []
    was_here = []
    err_msg = ''
    command = ''
    item_or_direction = ''
    desc_doc = "Start_room.txt"
    doc_path = parent_dir /  desc_doc

    # Test for win condition, uncomment desired Win-con (best or standard) to
    # test
    # player_inventory = WIN_CON  # for testing purposes
    # player_inventory = BEST_ENDING  # for testing purposes

    # starting welcome message
    doc_reader(doc_path)
    delprint('\n\nWelcome to the game.\n\n')

    # Adding start to the was_here list
    was_here.append(current_room)

    # Game loop running while exit conditions are not satisfied
    while current_room != EXIT_ROOM_SENTINEL:

        # Sort players inventory for easier comparison
        player_inventory = sorted(player_inventory)

        # Prompt message, using the delayed print function below to print the
        # prompt in a more user friendly way.
        delprint(
            f"Current room: {rooms[current_room].name}\nCurrent inventory: {player_inventory}\nYou see the: {rooms[current_room].item}\n\nValid commands: {VALID_INPUTS}.\nValid directions: {DIRECTIONS}.\nExamine will redisplay an item or room description.\n\nWhat would you like to do?\n\n")
        user_input = input()
        
        # Checking if the user input is valid and splitting it into a command
        if len(user_input) > 0:
            if user_input.title() != 'Exit':
                split_input = user_input.title().strip().split()
                command = split_input[0]
                item_or_direction = ' '.join(split_input[1:])

            else:
                item_or_direction = user_input.title().strip()

        # If the user input is not valid, print an error message.
        else:
            delprint(f'{INVALID_COMMAND}\n\n')

        # Passing the current room and user_input to the navigate function below
        # and changing the current room variable and error message equal to its
        # output.

        if command == 'Move' or item_or_direction == EXIT_COMMAND:
            current_room, err_msg = game_utils.navigate(current_room, item_or_direction)
            if not err_msg:
                delprint(f"You move to {rooms[current_room].name}\n\n")

                # If the current room has been visited before, print a message, otherwise
                # print the description of the room and add it to the was_here list.
                if rooms[current_room].name in was_here:
                    delprint(f"You have been here before.\n\n")
                    continue
                else:
                    was_here.append(rooms[current_room].name)
                    desc_doc = f"{rooms[current_room].name}_room.txt"
                    doc_path = parent_dir /  desc_doc
                    doc_reader(doc_path)
                    print('\n\n')

        # If the command is grab, pass the item_or_direction and current room to the
        # grab_item function below and update the player inventory. Print error message
        # if there is one.
        elif command == 'Grab':
            player_inventory, err_msg = game_utils.grab_item(item_or_direction, player_inventory, current_room)

            # If there is no error, print a message and the description of the item
            if not err_msg:
                delprint(f"You pick up the {rooms[current_room].item}\n\n")
                desc_doc = f"{rooms[current_room].item}_item.txt"
                doc_path = parent_dir /  desc_doc
                doc_reader(doc_path)
                print('\n\n')

        # If the player wishes to Examine, print the description of the item or direction
        # again for the player.
        elif command == 'Examine':

            # If the player is examining a room they are in or have been to,
            # print the room description again.
            if item_or_direction in was_here or item_or_direction == rooms[current_room].name:
                desc_doc = f"{current_room}_room.txt"
                doc_path = parent_dir /  desc_doc
                doc_reader(doc_path)
                print('\n\n')

            # If the player is examining an item they have in inventory or is in the room,
            # print the item description again.
            elif item_or_direction in player_inventory or item_or_direction == rooms[current_room].item:
                desc_doc = f"{item_or_direction}_item.txt"
                doc_path = parent_dir /  desc_doc
                doc_reader(doc_path)
                print('\n\n')

            # Otherwise, print an error message.
            else:
                delprint(f'{NOT_VISITED_OR_GRABBED}\n\n')

        # If there is any error message, print it out using delprint.
        # Also prints game over message when exit condition occurs.
        if err_msg:
            delprint(f'{err_msg}\n\n')

        # If the player has the win condition items in their inventory, print the
        # win message and break the loop.

        # I think it's because the lists are in different orders. Need to sort them
        # before comparing.
        if (player_inventory == WIN_CON or player_inventory == BEST_ENDING) and rooms[current_room].name == rooms['Hangar'].name:

            # If the player has the best ending items in their inventory, print the
            # best ending message and break the loop.
            if player_inventory == BEST_ENDING:
                desc_doc = "Best_Win.txt"
                doc_path = parent_dir /  desc_doc
                doc_reader(doc_path)
                print('\n')
                delprint(F'{GAME_OVER}!!')
                current_room = EXIT_ROOM_SENTINEL

            # If the player has the standard ending items in their inventory, print the
            # standard ending message and break the loop.
            else:
                desc_doc = "Win_Msg.txt"
                doc_path = parent_dir /  desc_doc
                doc_reader(doc_path)
                print('\n')
                delprint(F'{GAME_OVER}!!')
                current_room = EXIT_ROOM_SENTINEL
        



def delprint(text,delay_time=1e-150):
    """
    Short for delayed print. Prints character by character instead of printing
    all output to terminal at once. Makes for a nicer user experience.
    Courtesy of @Muffinlavania/The Slow Print on replit.
    """
    for character in text:      
        sys.stdout.write(character) 
        sys.stdout.flush()
        time.sleep(delay_time)


def doc_reader(file_path):
    """
    Reads the description documents for each room and prints them to the terminal
    using delprint for user friendly terminal readouts.
    """
    with file_path.open(mode='r', encoding='utf-8') as doc_file:
        for lines in doc_file:
            delprint(lines)

main()
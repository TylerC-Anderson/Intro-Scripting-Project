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
import os,platform

# initialize the valid inputs for the game
COMMANDS = ['Move', 'Grab', 'Examine']
DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = COMMANDS + [EXIT_COMMAND]
EXIT_ROOM_SENTINEL = "exit"
GAME_OVER = "Thanks for playing! I hope you enjoyed the game."
PLAYER_DEATH = 'You turned the corner and saw The Captain too late...\nIt pulls out a strange looking implement and you see a brilliant blue flash for the briefest moment before you die.\n\nGAME OVER\n\n'
END_CREDITS = 'Created by Tyler Anderson, 2023\n\nIncludes modules from @Muffinlavania/The Slow Print on replit and from u/GeorgeBoca.'

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

# initialize the rooms dictionary and the error messages dictionary from the
# game_utils module. Also initialize the description document variable.
rooms = game_utils.rooms_dict()
err_list = game_utils.errors_search
desc_doc = ''
best_ending_check = False

# initialize the delay print default value based on the OS
if platform.system() == "Windows":
    del_print_default = 1e-250
else: 
    del_print_default = 0.01

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
    

    # initialize the parent directory for the description documents
    parent_dir = Path(__file__).parent.resolve() / 'Descriptions'
    
    # parent_dir = Path(__file__).parent.resolve() / 'Test Descriptions' # uncomment to test with the test descriptions

    ## Test for win condition, uncomment desired Win-con (best or standard) to
    ## test. Remember to comment out testing prompt immediately below to skip
    ## test mode prompting.
    # player_inventory = WIN_CON  # for testing purposes
    # player_inventory = BEST_ENDING  # for testing purposes

    # starting welcome message
    delprint('\n\nWelcome to the game.\n\n')

    # prompts user for play or test mode, and for god mode if test mode is
    # selected, and for best ending if god mode is enabled. Comment out if you want to skip prompting.
    delprint("Press enter for Play mode, or T for test mode. Test mode uses short test descriptions for all items and rooms.\n")
    test_mode_input = input().lower().strip()

    # first checking for length of user input. If it is empty, then play mode is selected.
    # will also repeat this syntax for all other user testing input prompts.
    if len(test_mode_input) == 0:
        pass

    # sets the parent directory to the test descriptions if test mode is
    # selected, and sets the player inventory to the win con if god mode is
    # selected, or best ending if also selected.
    elif test_mode_input[0] == 't':
        delprint("Test mode enabled.\n")
        parent_dir = Path(__file__).parent.resolve() / 'Test Descriptions'
        
        delprint("Press Y to use god mode (all items in inventory, WinCon ready). Enter to not enable god mode.\n")
        test_mode_input = input().lower().strip()
        if len(test_mode_input) == 0:
            pass
        elif test_mode_input[0] == 'y':
            delprint("God mode enabled.\n")
            
            delprint("Press Y for best ending. Press enter for standard ending.\n")
            test_mode_input = input().lower().strip()
            if len(test_mode_input) == 0:
                player_inventory = WIN_CON
                pass
            elif test_mode_input[0] == 'y':
                delprint("Best ending enabled.\n")
                player_inventory = BEST_ENDING
            else:
                player_inventory = WIN_CON

    # finish setting full doc path
    doc_path = parent_dir /  desc_doc

# waits for user input to continue
    input("Press enter to continue.")
    clear_screen()
    doc_reader(doc_path)
    print('\n')


    # Adding start to the was_here list
    was_here.append(current_room)

    # Game loop running while exit conditions are not satisfied
    while current_room != EXIT_ROOM_SENTINEL:

        # Sort players inventory for easier comparison
        player_inventory = sorted(player_inventory)
        previous_room = current_room

        # Prompt message, using the delayed print function below to print the
        # prompt in a more user friendly way.
        delprint(
            f"Current room: {rooms[current_room].name}\nCurrent inventory: {player_inventory}\nValid commands: {VALID_INPUTS}.\nValid directions: {DIRECTIONS}.\nExamine will redisplay an item or room description.\n",delay_time=del_print_default*1e-5)
        
        if rooms[current_room].item not in player_inventory and rooms[current_room].item != None:
            delprint(f'\nYou see the: {rooms[current_room].item}\n',delay_time=1e-340)
        
        # Displays if user is in test mode, providing directions and a disclaimer
        if parent_dir == Path(__file__).parent.resolve() / 'Test Descriptions':
            delprint(f'Possible directions: {rooms[current_room].possible_directions}\n\n')
            delprint(f'You are currently in test mode. The descriptions you see are not the actual descriptions for the rooms. To see the actual descriptions, restart game and enter T for test mode.\nWhat would you like to do?\n\n',delay_time=1e-320)
        
        # Displays if user is not in test mode, standard user prompt
        else:
            delprint(f'\nWhat would you like to do?\n\n',delay_time=1e-320)
        
        # waits for user input, then clears screen after input is received
        user_input = input()
        clear_screen()

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
            delprint(f'{game_utils.errors_search("INVALID_COMMAND")}\n\n')

        # Passing the current room and user_input to the navigate function below
        # and changing the current room variable and error message equal to its
        # output.

        if command == 'Move' or item_or_direction == EXIT_COMMAND:
            current_room, err_msg = game_utils.navigate(current_room, item_or_direction)
            if not err_msg:
                delprint(f"You move {item_or_direction} to {rooms[current_room].name}\n\n")

                # If the current room has been visited before, print a message, otherwise
                # print the description of the room and add it to the was_here list.
                if rooms[current_room].name in was_here:
                    delprint(f"You have been here before.\n")
                    continue
                else:
                    was_here.append(rooms[current_room].name)
                    desc_doc = f"{rooms[current_room].name}_room.txt"
                    doc_path = parent_dir /  desc_doc
                    doc_reader(doc_path)
                    print('\n')
                    # If the player does not have the right items in their inventory to be
                    # in the current room, print the feedback and game over message
                    if rooms[current_room].required_items != None and player_inventory != BEST_ENDING:
                        for item in rooms[current_room].required_items:
                            if item not in player_inventory:
                                fail_condition = game_utils.items_required(current_room, player_inventory)
                        
                                delprint(F'{fail_condition}\n')
                                delprint(F'{PLAYER_DEATH}Would you like to try again? (Y/N)\n')
                                user_input = input().strip().lower()

                                # If the player wants to try again, respawn them in the previous room
                                # and remove the current room from the was_here list. Otherwise, print
                                # the game over message and break the loop.
                                if user_input == 'y':
                                    if rooms[previous_room].name != 'Start':
                                        delprint(F'You have respawned back in {rooms[previous_room].name}.\n')
                                        was_here.remove(rooms[current_room].name)
                                        current_room = previous_room
                                    elif rooms[previous_room].name == 'Start':
                                        delprint(F'You have respawned back in {rooms[previous_room].name}.\n')
                                        current_room = previous_room
                                elif user_input == 'n':
                                    delprint(F'{GAME_OVER}\n')
                                    command = 'Exit'
                                    current_room = EXIT_ROOM_SENTINEL

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
                print('\n')

        # If the player wishes to Examine, print the description of the item or direction
        # again for the player.
        elif command == 'Examine':

            # If the player is examining a room they are in or have been to,
            # print the room description again.
            if item_or_direction == rooms[current_room].name or item_or_direction == 'Room':
                desc_doc = f"{current_room}_room.txt"
                doc_path = parent_dir /  desc_doc
                examine_reader(doc_path)
                print('\n')

            # If the player is examining an item they have in inventory or is in the room,
            # print the item description again.
            elif item_or_direction in player_inventory or item_or_direction == rooms[current_room].item or item_or_direction == 'Item':
                if rooms[current_room].item == None:
                    delprint(f'You see nothing in this room.\n\n')
                elif item_or_direction == 'Item':
                    desc_doc = f"{rooms[current_room].item}_item.txt"
                    doc_path = parent_dir /  desc_doc
                    doc_reader(doc_path)
                    print('\n')
                else:
                    desc_doc = f"{item_or_direction}_item.txt"
                    doc_path = parent_dir /  desc_doc
                    doc_reader(doc_path)
                    print('\n')

            # Otherwise, print an error message.
            else:
                delprint(f'{err_list("NOT_VISITED_OR_GRABBED")}\n\n')

        # If there is any error message, print it out using delprint.
        # Also prints game over message when exit condition occurs.
        if err_msg:
            delprint(f'{err_msg}\n\n')

        # If the player has the win condition items in their inventory, print the
        # win message and break the loop.
        if command != 'Exit':
            if (player_inventory == WIN_CON or player_inventory == BEST_ENDING) and rooms[current_room].name == rooms['Hangar'].name:

                # If the player has the best ending items in their inventory, print the
                # best ending message and break the loop.
                if player_inventory == BEST_ENDING:
                    desc_doc = "Best_Win.txt"
                    doc_path = parent_dir /  desc_doc
                    doc_reader(doc_path)
                    print('\n')
                    delprint(F'{GAME_OVER}!!\n\n')
                    delprint(F'{END_CREDITS}\n\n')
                    input(F'Press enter to exit the game.\n\n')
                    current_room = EXIT_ROOM_SENTINEL

                # If the player has the standard ending items in their inventory, print the
                # standard ending message and break the loop.
                else:
                    desc_doc = "Win_Msg.txt"
                    doc_path = parent_dir /  desc_doc
                    doc_reader(doc_path)
                    print('\n')
                    delprint(F'{GAME_OVER}!\n\n')
                    delprint(F'{END_CREDITS}\n\n')
                    current_room = EXIT_ROOM_SENTINEL

def delprint(text, delay_time=del_print_default):
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

def examine_reader(file_path):
    """
    Reads the description documents for each room and prints them to the terminal
    using delprint for user friendly terminal readouts. Faster delprint speed since
    user is not reading the description for the first time.
    """
    with file_path.open(mode='r', encoding='utf-8') as doc_file:
        for lines in doc_file:
            delprint(lines,delay_time=del_print_default*0.5)

def clear_screen():
    """
    Clears the terminal screen. Courtesy of u/GeorgeBoca/the following reddit post.
    https://www.reddit.com/r/learnpython/comments/qjooa7/how_to_auto_erase_previous_text_in_terminal_text/
    """
    CLEAR = "cls" if platform.system() == "Windows" else "clear"
    os.system(CLEAR)

main()

# GAME UTILS
"""
Contains both main functions for user commands within the game.
"""

## Grab Item
"""
PURPOSE: For allowing the player to grab items in the game.

INPUTS: Item's name the player wishes to grab, and the current room.
"""

from collections import namedtuple
import sys,time

# initialize the error codes and valid inputs for the game
COMMANDS = ['Move', 'Grab', 'Examine']
DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = COMMANDS + [EXIT_COMMAND]
EXIT_ROOM_SENTINEL = "exit"
GAME_OVER = "Thanks for playing! I hope you enjoyed the game."

# initialize the win condition items and the best ending items and sort them
WIN_CON = [
    'Universal Translator', 'Hangar Key',
    'Ship Map', 'Space Suit',
    'Cloaking Device', 'Baton',
    ]
WIN_CON.sort()
BEST_ENDING = WIN_CON + ['Voice Activated Navigator']
BEST_ENDING.sort()

# initialize the error messages, also includes a search function for the error codes.
NOT_IN_ROOM = "You don't see that item anywhere in here. Please try again."
ALREADY_GRABBED = "You check your pockets... Yes, that item is still there. You don't think you need another one."
INVALID_COMMAND = f"That is not a valid command. You need to enter one of the following commands: {str(VALID_INPUTS)}.\nIf you enter a move command, it must be in one of the following directions: {DIRECTIONS}.\n If you are trying to grab an item, you need to enter the items name with your grab command."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
NOT_VISITED_OR_GRABBED = "You don't see that item anywhere in here, or you are not in that room. Please try again."
MISSING_ITEM = "You think you need an item you don't have yet to get there. Please try again."

def errors_search(error_code):
    """
    Returns the error message associated with the error code. Allows accessiblity from
    other modules.
    """
    errors_dict = {
        'NOT_IN_ROOM':NOT_IN_ROOM,
        'ALREADY_GRABBED':ALREADY_GRABBED,
        'INVALID_COMMAND':INVALID_COMMAND,
        'CANNOT_GO_THAT_WAY':CANNOT_GO_THAT_WAY,
        'NOT_VISITED_OR_GRABBED':NOT_VISITED_OR_GRABBED,
        'MISSING_ITEM':MISSING_ITEM
    }
    error_message_text = errors_dict[error_code]

    return error_message_text

# setting the fields for the tuple in a variable for modularization
room_fields = [
'name', 'item', 
'possible_directions',
'required_items']

# initialize the tuple category, rooms
RoomsTuple = namedtuple(
                'Room',
                room_fields,
                )

# actually make the rooms tuples
start = RoomsTuple(
    name='Start',
    possible_directions={'East':'Cell Blocks'},
    item = None,
    required_items = None)
cell_blocks = RoomsTuple(
    name='Cell Blocks', 
    possible_directions={
        'North':'West EVA', 'South':'South Junction',
        'East':'North Junction'},
    item='Universal Translator',
    required_items = None)
flight_control = RoomsTuple(
    name='Flight Control',
    possible_directions={'East':'South Junction'},
    item='Hangar Key',
    required_items = ['Ship Map'])
south_junction = RoomsTuple(
    name='South Junction',
    possible_directions={
        'North':'Cell Blocks', 'West':'Flight Control',
        'East':'Empty Hall'},
    item='Ship Map',
    required_items = ['Universal Translator'])
empty_hall = RoomsTuple(
    name='Empty Hall',
    possible_directions={
        'South':'Hidden Room', 'West':'South Junction',
        'East':'Armory'},
    item=None,
    required_items = None)
hidden_room = RoomsTuple(
    name='Hidden Room',
    possible_directions={
        'North':'Empty Hall'},
    item='Voice Activated Navigator',
    required_items = None)
armory = RoomsTuple(
    name='Armory',
    possible_directions={
        'North':'Arsenal', 'West':'Empty Hall'},
    item='Cloaking Device',
    required_items = ['Ship Map'])
arsenal = RoomsTuple(
    name='Arsenal',
    possible_directions={
        'South':'Armory', 'West':'North Junction'},
    item='Baton',
    required_items = ['Ship Map', 'Cloaking Device'])
north_junction = RoomsTuple(
    name='North Junction',
    possible_directions={
        'North':'East EVA', 'East':'Arsenal',
        'West':'Cell Blocks'},
    item='Ship Map',
    required_items = ['Universal Translator', 'Cloaking Device'])
east_eva = RoomsTuple(
    name='East EVA',
    possible_directions={
        'North':'Hangar', 'South':'North Junction',
        'West':'West EVA'},
    item='Space Suit',
    required_items = ['Hangar Key', 'Cloaking Device', 'Baton', 'Universal Translator', 'Ship Map'])
west_eva = RoomsTuple(
    name='West EVA',
    possible_directions={
        'North':'Hangar', 'South':'Cell Blocks',
        'East':'East EVA'},
    item='Space Suit',
    required_items = ['Hangar Key', 'Cloaking Device', 'Baton', 'Universal Translator', 'Ship Map'])
hangar = RoomsTuple(
    name='Hangar',
    possible_directions={
        'East':'East EVA', 'West':'West EVA'},
    item=None,
    required_items=WIN_CON)

def rooms_dict():
    """Simple lookup function for the rooms list."""
    rooms = {
    'Start':start,
    'Cell Blocks':cell_blocks,
    'Flight Control':flight_control,
    'South Junction':south_junction,
    'Empty Hall':empty_hall,
    'Hidden Room':hidden_room,
    'Armory':armory,
    'Arsenal':arsenal,
    'North Junction':north_junction,
    'East EVA':east_eva,
    'West EVA':west_eva,
    'Hangar':hangar
    }
    return rooms

def items_required(current_room, player_inventory: list):
    """
    Returns item responses when player enters a room without the required item.
    """
    no_item = {
        'Ship Map':'No map, you have gotten lost on the way.',
        'Universal Translator':'You cannot understand the language of the ship. You have taken a wrong turn.',
        'Hangar Key':'This door needs a Key. You try to open the door without the key. The door refuses to open and an alarm sounds.',
        'Cloaking Device':'There was no place to hide here. You have been spotted by one of the aliens.',
        'Baton':'There was only one guard here, but without a weapon you were not able to stealthily dispatch it. The alien sounded an alarm.',
        'Space Suit':'You were able to reach an escape pod, but wasted too much time looking for a space suit for the journey. An alien has spotted you and raised the alarm.'
    }

    for item in rooms[current_room].required_items:
        if item not in player_inventory:
            return no_item[item]

rooms = rooms_dict()

def grab_item(item_choice: str, player_inventory: list, current_room):
    """
    Given an item_choice, player_inventory, and current_room; return the
    player_inventory updated with the item choice and err_msg (if there is one).
    """
    err_msg = ''

    # if the item chosen exists in this room
    if item_choice == rooms[current_room].item:

        # and the player does not already have the item
        # add item to player inventory
        if item_choice not in player_inventory:
            player_inventory.append(item_choice)
        
        # for when the item chosen is already in player inventory
        else:
            err_msg = ALREADY_GRABBED

    # for when the item doesn't exist in this room
    else:
        err_msg = NOT_IN_ROOM

    # best_ending_check(player_inventory)

    return player_inventory, err_msg

def navigate(current_room: str, user_input: str):
    """
    Given a current_room in rooms and a user_input, return a tuple (next_room, err_msg) with
    next_room -- where you are after or EXIT_ROOM_SENTINEL
    err_msg -- message to print, if any, empty, GAME_OVER, INVALID_DIRECTION, or CANNOT_GO_THAT_WAY
    """

    # initialize next_room and err_msg
    next_room = current_room
    err_msg = ''
    rooms = rooms_dict()

    # First checking if command links to valid input
    if user_input in DIRECTIONS or user_input == EXIT_COMMAND:
        
        # Then checking for exit command, and printing GAME_OVER message and moving
        # next room to the exit state.
        if user_input.lower() == EXIT_COMMAND.lower():
            delprint("Are you sure you'd like to exit?\n")
            delprint("Progress is NOT saved.\n\n")
            certainty_check = ''

            # While loop to ensure the player is certain about their choice to
            # exit the game, after informing them there is no save.
            while certainty_check not in ('y','n'):
                delprint("Type y for yes or n for no.\n")
                certainty_check = input()
                certainty_check.lower().strip()
                certainty_check = certainty_check[0]
                if certainty_check == 'y':
                    err_msg = GAME_OVER
                    next_room = EXIT_ROOM_SENTINEL
                elif certainty_check == 'n':
                    pass
                else:
                    delprint("Invalid input, please try again.\n\n")
                    continue

        # Then checking if the valid command is a valid direction the room has
        # then moving player according to their command if so
        elif user_input in rooms[current_room].possible_directions:
            next_room = rooms[current_room].possible_directions[user_input]
            return next_room, err_msg

        # If the input is valid, but the direction given is not exit or a direction
        # the room has, we are assuming the player can't go that way. Output
        # CANNOT_GO_THAT_WAY message
        else:
            err_msg = CANNOT_GO_THAT_WAY

    # Then checking if the user_input links is not a valid input, assigning
    # appropriate error message.
    else:
        err_msg = INVALID_COMMAND
    return next_room, err_msg

def delprint(text,delay_time = 0.0025):
    """
    Short for delayed print. Prints character by character instead of printing
    all output to terminal at once. Makes for a nicer user experience.
    Courtesy of @Muffinlavania/The Slow Print on replit.
    """
    for character in text:      
        sys.stdout.write(character) 
        sys.stdout.flush()
        time.sleep(delay_time)


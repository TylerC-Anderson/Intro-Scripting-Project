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
NOT_IN_ROOM = "You don't see that item anywhere in here. Please try again."
ALREADY_GRABBED = "You check your pockets... Yes, that item is still there. You don't think you need another one."
COMMANDS = ['Move', 'Grab']
DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = COMMANDS + [EXIT_COMMAND]
INVALID_COMMAND = f"That is not a valid command. You need to enter one of the following commands: {str(VALID_INPUTS)}.\nIf you enter a move command, it must be in one of the following directions: {DIRECTIONS}.\n If you are trying to grab an item, you need to enter the items name with your grab command."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing."
EXIT_ROOM_SENTINEL = "exit"

# setting the fields for the tuple in a variable for modularization
fields = [
'name', 'item', 
'possible_directions',
'is_end_room']

# initialize the tuple category, rooms
RoomsTuple = namedtuple(
                'Room',
                fields,
                )

# actually make the rooms tuples
start = RoomsTuple(
    name='Start',
    possible_directions={'East':'Cell Blocks'},
    item = None,
    is_end_room = False)
cell_blocks = RoomsTuple(
    name='Cell Blocks', 
    possible_directions={
        'North':'West EVA', 'South':'South Junction',
        'East':'North Junction'},
    item='Universal Translator',
    is_end_room = False)
flight_control = RoomsTuple(
    name='Flight Control',
    possible_directions={'East':'South Junction'},
    item='Hangar Key',
    is_end_room = False)
south_junction = RoomsTuple(
    name='South Junction',
    possible_directions={
        'North':'Cell Blocks', 'West':'Flight Control',
        'East':'Empty Hall'},
    item='Ship Map',
    is_end_room = False)
empty_hall = RoomsTuple(
    name='Empty Hall',
    possible_directions={
        'South':'Hidden Room', 'West':'South Junction',
        'East':'Armory'},
    item=None,
    is_end_room = False)
hidden_room = RoomsTuple(
    name='Hidden Room',
    possible_directions={
        'North':'Empty Hall'},
    item='Voice Activated Navigator',
    is_end_room = False)
armory = RoomsTuple(
    name='Armory',
    possible_directions={
        'North':'Arsenal', 'West':'Empty Hall'},
    item='Cloaking Device',
    is_end_room = False)
arsenal = RoomsTuple(
    name='Arsenal',
    possible_directions={
        'South':'Armory', 'West':'North Junction'},
    item='Baton',
    is_end_room = False)
north_junction = RoomsTuple(
    name='North Junction',
    possible_directions={
        'North':'East EVA', 'East':'Arsenal',
        'West':'Cell Blocks'},
    item='Ship Map',
    is_end_room = False)
east_eva = RoomsTuple(
    name='East EVA',
    possible_directions={
        'North':'Hangar', 'South':'North Junction',
        'West':'West EVA'},
    item='Space Suit',
    is_end_room = False)
west_eva = RoomsTuple(
    name='West EVA',
    possible_directions={
        'North':'Hangar', 'South':'Cell Blocks',
        'East':'East EVA'},
    item='Space Suit',
    is_end_room = False)
hangar = RoomsTuple(
    name='Hangar',
    possible_directions={
        'East':'East EVA', 'West':'West EVA'},
    item=None,
    is_end_room=True)

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

    return player_inventory, err_msg

## Move Room
"""
PURPOSE: For allowing the player to move between rooms in the game.

INPUTS:
- current_room -- the room the player is currently in
- user_input -- the command the player entered.
- rooms -- the dictionary of rooms and their connections
"""

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


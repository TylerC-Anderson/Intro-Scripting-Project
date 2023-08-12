# Move Room function

"""
PURPOSE: For allowing the player to move between rooms in the game.

INPUTS:
- current_room -- the room the player is currently in
- user_input -- the command the player entered.
- rooms -- the dictionary of rooms and their connections
"""

import game_map

DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = DIRECTIONS + [EXIT_COMMAND]
INVALID_DIRECTION = "That is not a valid direction. You need to enter one of: " +\
    str(VALID_INPUTS) + "."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing."
EXIT_ROOM_SENTINEL = "exit"

def navigate(current_room: str, user_input: str, rooms: list):
    """
    Given a current_room in rooms and a user_input, return a tuple (next_room, err_msg) with
    next_room -- where you are after or EXIT_ROOM_SENTINEL
    err_msg -- message to print, if any, empty, GAME_OVER, INVALID_DIRECTION, or CANNOT_GO_THAT_WAY
    """
    next_room = current_room
    err_msg = ''

    # First checking if command links to valid input
    if user_input in VALID_INPUTS:
        # Then checking for exit command, and printing GAME_OVER message and moving
        # next room to the exit state.
        if user_input.lower() == EXIT_COMMAND.lower():
            err_msg = GAME_OVER
            next_room = EXIT_ROOM_SENTINEL

        # Then checking if the valid command is a valid direction the room has
        # then moving player according to their command if so

        # TODO Fix this so that it works with the new rooms list and namedtuples
        elif user_input in game_map.rooms_list(current_room):
            next_room = game_map.mapping(current_room, user_input)

        # If the input is valid, but the direction given is not exit or a direction
        # the room has, we are assuming the player can't go that way. Output
        # CANNOT_GO_THAT_WAY message
        else:
            err_msg = CANNOT_GO_THAT_WAY

    # Then checking if the user_input links is not a valid input, assigning
    # appropriate error message.
    else:
        err_msg = INVALID_DIRECTION
    return next_room, err_msg

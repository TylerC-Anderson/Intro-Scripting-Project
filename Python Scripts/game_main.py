# Game Main
"""
PURPOSE: Contains the main script for the game, including the play loop and a
module for printing in a user friendly way.

INPUTS: Accepts user input for navigation and grabbing items.
"""

import move_room
import grab_item
import sys,time

# initialize the conditions for the game
COMMANDS = ['Move', 'Grab']
DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = COMMANDS + [EXIT_COMMAND]
INVALID_COMMAND = f"That is not a valid command. You need to enter one of the following commands: {str(VALID_INPUTS)}.\nIf you enter a move command, it must be in one of the following directions: {str(DIRECTIONS)}.\n If you are trying to grab an item, you need to enter the items name with your grab command."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing."
EXIT_ROOM_SENTINEL = "exit"

rooms = move_room.rooms_dict()
player_inventory = []

def main():
    """
    Contains the loop that will run the game until the exit condition is satisfied. Starts in the Start room and prints a welcome message.
    """
    current_room = 'Start'

    # starting welcome message
    delprint(
        f'Welcome to the game.\nYou have woken up in the {rooms[current_room].name}.\n\n')

    # Game loop running while exit conditions are not satisfied
    while current_room != EXIT_ROOM_SENTINEL:

        # Prompt message, using the delayed print function below to print the
        # prompt in a more user friendly way.
        delprint(
            f"Current room: {rooms[current_room].name}\nCurrent inventory: {player_inventory}\n\nWhat would you like to do?\nYou may enter any of the following: {VALID_INPUTS}.\n\n")
        user_input = input()
        user_input = user_input.title().strip().split
        command = user_input[0]
        item_or_direction = user_input[1]

        # Passing the current room and user_input to the navigate function below
        # and changing the current room variable and error message equal to its
        # output.

        if command == 'Move' or command == EXIT_ROOM_SENTINEL:
            current_room, err_msg = move_room.navigate(current_room, item_or_direction)

        elif command == 'Grab':
            player_inventory, err_msg = grab_item(item_or_direction, player_inventory, current_room)

        # If there is any error message, print it out using delprint.
        # Also prints game over message when exit condition occurs.
        if err_msg:
            delprint(f'{err_msg}\n')

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

main()
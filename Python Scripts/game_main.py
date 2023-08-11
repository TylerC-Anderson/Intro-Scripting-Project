import sys
import time
from collections import namedtuple
import move_room

# initialize the tuple category, rooms
Rooms = namedtuple('Room', ['name', ['possible_directions'], 'Items', 'description', 'is_end_room'], defaults=None)

# initialize the rooms
Start = Rooms('Start', ['East'], None)
cell_blocks = Rooms('Cell Blocks', ['North', 'South', 'East'], 'universal_translator')
flight_control = Rooms('Flight Control', ['east'], 'hangar_key')
south_junction = Rooms('South Junction', ['North', 'East', 'West'], 'map')
empty_hall = Rooms('Empty Hall', ['South', 'East', 'West'], None)
hidden_room = Rooms('Hidden Room', ['North'], 'va_nav')
armory = Rooms('Armory', ['North', 'West'], 'cloaking_device')
arsenal = Rooms('Arsenal', ['South', 'West'], 'baton')
north_junction = Rooms('North Junction', ['North', 'East', 'West'], 'map')
east_eva = Rooms('East EVA', ['North', 'South', 'West'], 'space_suit')
west_eva = Rooms('West EVA', ['North', 'South', 'East'], 'space_suit')
hangar = Rooms('Hangar', ['North', 'South', 'West'], 'space_suit', is_end_room=True)

DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = DIRECTIONS + [EXIT_COMMAND]
INVALID_DIRECTION = "That is not a valid direction. You need to enter one of: " +\
    str(VALID_INPUTS) + "."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing."
EXIT_ROOM_SENTINEL = "exit"

rooms_dict = {
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
    'Hangar':hangar,
    'Start':Start
}

def main():
    """
    Contains the loop that will run the game until the exit condition is
    satisfied. Starts in the Bedroom and prints a welcome message
    """
    current_room = 'Bedroom'
    delprint(f'Welcome to the game.\nYou have woken up in the {current_room}.\n\n', 0.0025)

    # Game loop running while exit conditions are not satisfied
    while current_room != EXIT_ROOM_SENTINEL:

        # Prompt message, using the delayed print function below to print the
        # prompt in a more user friendly way.
        delprint(f"You are currently in the: {current_room}\n\nWhere would you like to go?\nYou may enter any of the following: {VALID_INPUTS}. \n\n", 0.0025)
        user_input = input()
        user_input = user_input.title().strip()

        # Passing the current room and user_input to the navigate function below
        # and changing the current room variable and error message equal to its
        # output.
        current_room, err_msg = move_room.navigate(current_room, user_input, rooms_dict)

        # If there is any error message, print it out using delprint.
        # Also prints game over message when exit condition occurs.
        if err_msg:
            delprint(f'{err_msg}\n', 0.0025)

def delprint(text,delay_time):
    """
    Short for delayed print. Prints character by character instead of printing
    all output to terminal at once. Makes for a nicer user experience.
    Courtesy of @Muffinlavania/The Slow Print on replit.
    """
    for character in text:      
        sys.stdout.write(character) 
        sys.stdout.flush()
        time.sleep(delay_time)

import sys
import time
from collections import namedtuple
import move_room

# initialize the tuple category, rooms
Rooms = namedtuple('Room', ['name', {'possible_directions':'connection'}, 'Items', 'description', 'is_end_room'], defaults=None)

# initialize the rooms, so python isn't upset while we're making the namedtuples
cell_blocks = None
flight_control = None
south_junction = None
empty_hall = None
hidden_room = None
armory = None
arsenal = None
north_junction = None
east_eva = None
west_eva = None
hangar = None
Start = None

# initialize the rooms list to pass to the move_room module
rooms_list = [
    Start,
    cell_blocks,
    flight_control,
    south_junction,
    empty_hall,
    hidden_room,
    armory,
    arsenal,
    north_junction,
    east_eva,
    west_eva,
    hangar
    ]

# actually make the rooms tuples
Start = Rooms(
    'Start',
    {'East':cell_blocks})
cell_blocks = Rooms(
    'Cell Blocks', 
    {'North':east_eva, 'South':south_junction, 'East':north_junction},
    'universal_translator')
flight_control = Rooms(
    'Flight Control',
    {'East':south_junction},
    'hangar_key')
south_junction = Rooms(
    'South Junction',
    {'North':cell_blocks, 'East':flight_control, 'West':empty_hall},
    'map')
empty_hall = Rooms(
    'Empty Hall',
    {'South':hidden_room, 'East':south_junction, 'West':armory},
    'va_nav')
hidden_room = Rooms(
    'Hidden Room',
    {'North':empty_hall},
    'va_nav')
armory = Rooms(
    'Armory',
    {'North':arsenal, 'West':empty_hall},
    'cloaking_device')
arsenal = Rooms(
    'Arsenal',
    {'South':armory, 'West':north_junction},
    'baton')
north_junction = Rooms(
    'North Junction',
    {'North':east_eva, 'East':cell_blocks, 'West':arsenal},
    'map')
east_eva = Rooms(
    'East EVA',
    {'North':hangar, 'South':north_junction, 'West':west_eva},
    'space_suit')
west_eva = Rooms(
    'West EVA',
    {'North':hangar, 'South':cell_blocks, 'West':east_eva},
    'space_suit')
hangar = Rooms(
    'Hangar',
    {'North', 'South', 'West'},
    'space_suit',
    is_end_room=True)

# initialize the conditions for the game
DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = DIRECTIONS + [EXIT_COMMAND]
INVALID_DIRECTION = "That is not a valid direction. You need to enter one of: " +\
    str(VALID_INPUTS) + "."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing."
EXIT_ROOM_SENTINEL = "exit"

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
        current_room, err_msg = move_room.navigate(current_room, user_input, rooms_list)

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

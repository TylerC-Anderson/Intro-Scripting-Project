# Game Map

"""
Contains mapping calls and the lookup lists for the game.
"""
from collections import namedtuple

fields = [
    'name', 'item', 
    'possible_directions', 'description',
    'is_end_room']

# initialize the tuple category, rooms
Rooms = namedtuple('Room',
                fields,
                defaults=[None, ] * len(fields))

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

# # initialize the rooms list to pass to the move_room module
# rooms_dict = [
#     Start,
#     cell_blocks,
#     flight_control,
#     south_junction,
#     empty_hall,
#     hidden_room,
#     armory,
#     arsenal,
#     north_junction,
#     east_eva,
#     west_eva,
#     hangar
#     ]

# actually make the rooms tuples
start = Rooms(
    'Start',
    possible_directions={'East':cell_blocks})
cell_blocks = Rooms(
    'Cell Blocks', 
    possible_directions={'North':east_eva, 'South':south_junction, 'East':north_junction},
    item='universal_translator')
flight_control = Rooms(
    'Flight Control',
    possible_directions={'East':south_junction},
    item='hangar_key')
south_junction = Rooms(
    'South Junction',
    possible_directions={'North':cell_blocks, 'East':flight_control, 'West':empty_hall},
    item='map')
empty_hall = Rooms(
    'Empty Hall',
    possible_directions={'South':hidden_room, 'East':south_junction, 'West':armory},
    item='va_nav')
hidden_room = Rooms(
    'Hidden Room',
    possible_directions={'North':empty_hall},
    item='va_nav')
armory = Rooms(
    'Armory',
    possible_directions={'North':arsenal, 'West':empty_hall},
    item='cloaking_device')
arsenal = Rooms(
    'Arsenal',
    possible_directions={'South':armory, 'West':north_junction},
    item='baton')
north_junction = Rooms(
    'North Junction',
    possible_directions={'North':east_eva, 'East':cell_blocks, 'West':arsenal},
    item='map')
east_eva = Rooms(
    'East EVA',
    possible_directions={'North':hangar, 'South':north_junction, 'West':west_eva},
    item='space_suit')
west_eva = Rooms(
    'West EVA',
    possible_directions={'North':hangar, 'South':cell_blocks, 'West':east_eva},
    item='space_suit')
hangar = Rooms(
    'Hangar',
    possible_directions={'North', 'South', 'West'},
    item='space_suit',
    is_end_room=True)

def rooms_dict(current_room):
    """Simple lookup function for the rooms list."""
    rooms = {
    'start':start,
    'cell_blocks':cell_blocks,
    'flight_control':flight_control,
    'south_junction':south_junction,
    'empty_hall':empty_hall,
    'hidden_room':hidden_room,
    'armory':armory,
    'arsenal':arsenal,
    'north_junction':north_junction,
    'east_eva':east_eva,
    'west_eva':west_eva,
    'hangar':hangar
    }
    

    return rooms[current_room]

def mapping(current_room: str, user_input: str):
    """This function takes the current room and the user input and returns the next room.""" 
    # initialize output variable
    next_room = None
    next_room = current_room.possible_directions[user_input]
    return next_room

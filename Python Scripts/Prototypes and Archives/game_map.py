# Game Map

"""
Contains mapping calls and the lookup lists for the game.
"""
from collections import namedtuple

    # initialize the rooms, so python isn't upset while we're making the dictionary
    
fields = [
'name', 'item', 
'possible_directions', 'description',
'is_end_room']

# initialize the tuple category, rooms
Rooms = namedtuple(
                'Room',
                fields,
                )
# initialize the rooms, so python isn't upset while we're making the namedtuples
cell_blocks = ()
flight_control = ()
south_junction = ()
empty_hall = ()
hidden_room = ()
armory = ()
arsenal = ()
north_junction = ()
east_eva = ()
west_eva = ()
hangar = ()
start = ()

# actually make the rooms tuples
start = Rooms(
    name='Start',
    possible_directions={'East':cell_blocks},
    description = None,
    item = None,
    is_end_room = False)
cell_blocks = Rooms(
    name='Cell Blocks', 
    possible_directions={'North':east_eva, 'South':south_junction, 'East':north_junction},
    item='universal_translator',
    description = None,
    is_end_room = False)
flight_control = Rooms(
    name='Flight Control',
    possible_directions={'East':south_junction},
    item='hangar_key',
    description = None,
    is_end_room = False)
south_junction = Rooms(
    name='South Junction',
    possible_directions={
        'North':cell_blocks, 'East':flight_control,
        'West':empty_hall},
    item='map',
    description = None,
    is_end_room = False)
empty_hall = Rooms(
    name='Empty Hall',
    possible_directions={
        'South':hidden_room, 'East':south_junction,
        'West':armory},
    item='va_nav',
    description = None,
    is_end_room = False)
hidden_room = Rooms(
    name='Hidden Room',
    possible_directions={
        'North':empty_hall},
    item='va_nav',
    description = None,
    is_end_room = False)
armory = Rooms(
    name='Armory',
    possible_directions={
        'North':arsenal, 'West':empty_hall},
    item='cloaking_device',
    description = None,
    is_end_room = False)
arsenal = Rooms(
    name='Arsenal',
    possible_directions={'South':armory, 'West':north_junction},
    item='baton',
    description = None,
    is_end_room = False)
north_junction = Rooms(
    name='North Junction',
    possible_directions={
        'North':east_eva, 'East':cell_blocks,
        'West':arsenal},
    item='map',
    description = None,
    is_end_room = False)
east_eva = Rooms(
    name='East EVA',
    possible_directions={
        'North':hangar, 'South':north_junction,
        'West':west_eva},
    item='space_suit',
    description = None,
    is_end_room = False)
west_eva = Rooms(
    name='West EVA',
    possible_directions={
        'North':hangar, 'South':cell_blocks,
        'West':east_eva},
    item='space_suit',
    description = None,
    is_end_room = False)
hangar = Rooms(
    name='Hangar',
    possible_directions={
        'East':east_eva, 'West':west_eva},
    item='space_suit',
    description = None,
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

# def mapping(current_room: str, user_input: str):
#     """This function takes the current room and the user input and returns the next room.""" 
#     rooms = rooms_dict()
#     next_room = rooms[current_room].possible_directions[user_input]
#     return next_room

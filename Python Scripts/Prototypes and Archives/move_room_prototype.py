from collections import namedtuple

# initialize the tuple category, rooms
rooms = namedtuple('Room', ['name', 'possible_directions'])

# room tuples
Lobby = rooms('Lobby', {'east':'Foyer', 'north':'Attic'})
Foyer = rooms('Foyer', {'west':'Lobby'})
Attic = rooms('Attic', {'south':'Lobby'})

# dictionary mapping rooms to their strings as names
rooms_dict = {
    'Lobby':Lobby,
    'Foyer':Foyer,
    'Attic':Attic,
}

# initializing player without choices and in starting location, the lobby in 
# this case
choice = ''
current_room = Lobby


def move_room(move_choice):
    """ This function allows a player to move in any direction, provided the game
        has a namedtuple and a dictionary containing the string and tuple
        pairs for the room in that direction. It will switch the current_room
        to the tuple version of the next room by accessing the dictionary
        within the room's tuple for that direction, getting the string held as a
        value there which is the room's name. Then it will identify
        which room is in that direction by seeking the string/tuple pairs dictionary
        for a matching string as a key, and assign the current_room to that key's
        value, which is the tuple version of that room.
     """

    # get the global variable, current_room
    global current_room

    # seek through current_room's possible_directions dictionary for a matching
    # direction
    for directions in current_room.possible_directions:

        # if found
        if directions == move_choice:

            # move current room to tuple version of that room, accessed through
            # the rooms_dict and uses the string contained in the namedtuple
            # as a key to access that room's value
            current_room = rooms_dict[current_room.possible_directions[move_choice]]
            print(f'You have moved to {current_room.name}')
            return current_room
               
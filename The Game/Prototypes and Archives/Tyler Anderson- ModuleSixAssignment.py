# Tyler Anderson
# Submission to Module 6 Assignment

# Modules for the delayed printing function
import sys,time

# A dictionary for the simplified dragon text game
# The dictionary links a room to other rooms.
rooms = {
    'Great Hall': {'South': 'Bedroom'},
    'Bedroom': {'North': 'Great Hall', 'East': 'Cellar'},
    'Cellar': {'West': 'Bedroom'}
}

# list of directions, different inputs and outputs we are accepting from
# the player or are relaying back to the player, as well as definining the
# exit conditions
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
        current_room, err_msg = navigate(current_room, user_input)

        # If there is any error message, print it out using delprint.
        # Also prints game over message when exit condition occurs.
        if err_msg:
            delprint(f'{err_msg}\n', 0.0025)

def navigate(current_room: str, user_input: str):
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
        elif user_input in rooms[current_room]:
            next_room = rooms[current_room][user_input]

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

main()
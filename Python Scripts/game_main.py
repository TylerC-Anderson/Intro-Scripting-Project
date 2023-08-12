import move_room
import sys,time

# initialize the conditions for the game
DIRECTIONS = ['North', 'South', 'East', 'West']
EXIT_COMMAND = "Exit"
VALID_INPUTS = DIRECTIONS + [EXIT_COMMAND]
INVALID_DIRECTION = "That is not a valid direction. You need to enter one of: " +\
    str(VALID_INPUTS) + "."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing."
EXIT_ROOM_SENTINEL = "exit"

rooms = move_room.rooms_dict()

def main():
    """
    Contains the loop that will run the game until the exit condition is
    satisfied. Starts in the Bedroom and prints a welcome message
    """
    current_room = 'Start'

    delprint(
        f'Welcome to the game.\nYou have woken up in the {rooms[current_room].name}.\n\n')

    # Game loop running while exit conditions are not satisfied
    while current_room != EXIT_ROOM_SENTINEL:

        # Prompt message, using the delayed print function below to print the
        # prompt in a more user friendly way.
        delprint(
            f"You are currently in the: {rooms[current_room].name}\n\nWhere would you like to go?\nYou may enter any of the following: {VALID_INPUTS}. \n\n")
        user_input = input()
        user_input = user_input.title().strip()

        # Passing the current room and user_input to the navigate function below
        # and changing the current room variable and error message equal to its
        # output.
        current_room, err_msg = move_room.navigate(current_room, user_input)

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
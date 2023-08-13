# Grab Item
"""
PURPOSE: For allowing the player to grab items in the game.

INPUTS: Item's name the player wishes to grab, and the current room.
"""

import move_room

NOT_IN_ROOM = "You don't see that item anywhere in here. Please try again."
ALREADY_GRABBED = "You check your pockets... Yes, that item is still there. You don't think you need another one."

rooms = move_room.rooms_dict()
err_msg = ''

def grab_item(item_choice: str, player_inventory: list, current_room):
    """   
    """

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

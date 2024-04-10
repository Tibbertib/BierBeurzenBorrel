import pickle
import time
import matplotlib.pyplot as plt
from drink import Drink

plt.ion()

# balance = 0
inventory = {}
time_stamps = [time.time()]

def initialise_inventory():
    """
    This will later be changed to read input from a csv file to improve usability
    """
    inventory[0] = Drink("Hertog Jan", 0, 80, 100, 90, 50, True)
    inventory[1] = Drink("Heineken", 1, 75, 90, 80, 100, True)


# def display_balance() -> None:
    # print(f"Current balance: €{balance}")


def print_valid_stock() -> None:
    for value in inventory.values():
        print(value)


def update_prices(drink: Drink, amount: int):
    """
    Updates all prices of the drinks based on the latest sale.
    Parameter drink (Drink) is the drink that is sold, hence its price increases.
    All other prices must decrease, as they are not sold in the latest transaction
    """
    price_change = 10
    for value in inventory.values():
        if value == drink:
            value.modify_price(True, price_change, amount)
        else:
            value.modify_price(False, price_change, 0)


def sell_drink(drink: Drink, amount: int):
    """
    Function used to sell a drink. Used to show the sell price to
    the user (i.e. how much somebody needs to pay for their order),
    and updates the borrel balance
    """
    time_stamps.append(time.time())
    sell_price = (drink.current_price * amount) / 100
    # profit = (drink.current_price - drink.starting_price) * amount
    # balance += profit
    print(f"\nSold for €{drink.current_price/100:.2f} per bottle")
    print(f"Sell price is €{sell_price:.2f}")
    print("\n --------------------------- \n")


def reset() -> None:
    """
    Resets all drink prices in the inventory to their default value,
    which is stored in the Drink object associated with the drink
    """
    for value in inventory.values():
        value.reset()


def quit() -> None:
    """
    Used to properly shutdown the borrel at the end. Useful to determine how much of each drink has been sold.
    """
    with open("finalInventory.pkl", "wb") as f:
        pickle.dump(inventory, f)
    print("Final results of drinks sold written to file")
    plt.close("all")

def safe_parse(prompt: str) -> tuple[int, bool]:
    """
    Used to make sure that we can properly parse inputs to integers.
    Additionally, performs checks for other possible commands and calls
    the functions associated with these commands when needed.
    Returns the parsed result when appropiate, along with a flag that indicates
    whether the program needs to continue running.
    """
    result = input(prompt)
    if result == "quit":
        return quit(), False
    while result.isdigit() == False:
        print("Input must be an integer \n")
        result = input(prompt)
    return int(result), True


"""
Main control loop that takes care of running the borrel. Includes functionality
to parse input (orders) and update the inventory based on the input.
"""

initialise_inventory()
# Keep track of a boolean flag that indicates when the program should be terminated
running = True

while running:
    id, running = safe_parse("ID of the drink sold: >> ")
    if running == False:
        break

    # Continue until a valid ID is entered. ID entered must be associated with a drink
    while id not in inventory:
        print("That input is not valid, please use a valid ID")
        print_valid_stock()
        id, running = safe_parse("ID of the drink sold: >> ")
        if running == False:
            break
    drink = inventory[id]

    amount, running = safe_parse("Number of drinks sold: >> ")
    if running == False:
        break

    # Continue until user enters a valid amount of drinks to be ordered
    while (
        drink.can_sell_amount(amount) == False
    ):  # is possible to sell 0 drinks
        print("You can not sell this amount of drinks")
        print(f"You can sell at most {drink.nr_drinks} bottles")
        amount, running = safe_parse("Number of drinks sold: >> ")
        if running == False:
            break

    sell_drink(drink, amount)
    update_prices(drink, amount)
    print_valid_stock()


import pickle
import random
import time
import matplotlib.pyplot as plt
from drink import Drink

plt.ion()

balance = 0
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


def update_prices(drink: Drink, amount: int, balance):
    """
    Updates all prices of the drinks based on the latest sale.
    Parameter drink (Drink) is the drink that is sold, hence its price increases.
    All other prices must decrease, as they are not sold in the latest transaction
    """
    price_change = random.gauss(10,2)
    for value in inventory.values():
        if value == drink:
            value.modify_price(True, price_change, amount)
        else:
            value.modify_price(False, price_change, 0)
    if balance > 500:
        for value in inventory.values():
            value.steer_price(-price_change)
    if balance < 500:
        for value in inventory.values():
            value.steer_price(price_change)


def sell_drink(drink: Drink, amount: int, balance):
    """
    Function used to sell a drink. Used to show the sell price to
    the user (i.e. how much somebody needs to pay for their order),
    and updates the borrel balance
    """
    time_stamps.append(time.time())
    sell_price = (drink.current_price * amount) / 100
    profit = (drink.current_price - drink.starting_price) * amount
    balance += profit
    print(f"\nSold for €{drink.current_price/100:.2f} per bottle")
    print(f"Sell price is €{sell_price:.2f}")
    print(f"Current balance is: €{balance/100:.2f}")
    print("\n --------------------------- \n")
    return balance


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
Main control loop that takes care of running the borrel. 
"""
initialise_inventory()
# Keep track of a boolean flag that indicates when the program should be terminated
running = True

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
plots = []
for i, drank in enumerate(inventory.values()):
    lines, = ax.plot([],[])
    plots.append(lines)
ax.set_ylim(0, 280)
plt.xlabel('Time')
plt.ylabel('Price in cents')


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

    balance = sell_drink(drink, amount,balance)
    update_prices(drink, amount, balance)
    print_valid_stock()

    for i,drink in enumerate(inventory.values()):
        plots[i].set_xdata(time_stamps)
        plots[i].set_ydata(drink.historic_prices)
        label = f"{drink.name} :: (€{drink.current_price/100:.2f})"
        plots[i].set_label(label)
    ax.set_xlim(time_stamps[0], time_stamps[-1])
    ax.get_xaxis().set_ticks([])
    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
    fig.canvas.draw()
    fig.canvas.flush_events()
    print('\n')


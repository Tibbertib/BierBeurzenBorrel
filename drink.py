from dataclasses import dataclass, field


@dataclass(repr=True)
class Drink:
    """
    Contains all logic related to individual Drinks. This class should be used to modify individual drinks based on information received from
    another method that runs the main loop of the borrel.

    TODO: implement functionality for crashing the price
    """

    name: str = field(repr=True)
    id: int
    min_price: int
    max_price: int
    starting_price: int
    nr_drinks: int
    for_sale: bool = True
    historic_prices: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.initial_nr_drinks = self.nr_drinks
        self.historic_prices.append(self.starting_price)
        self.current_price = self.starting_price

    def modify_price(self, is_sold: bool, price_change: int, drinks_sold: int) -> None:
        """
        Used to update the price of all drinks. Because we update both the
        price of the drink sold, and all drinks that weren't sold in this
        transaction, we use the is_sold flag. We update the price according
        to some external specification and decrease the number of available
        drinks by the number ordered.
        """
        if is_sold:
            self.nr_drinks -= drinks_sold
            if self.nr_drinks <= 0:
                self.for_sale = False
            self.current_price = min(self.current_price + price_change, self.max_price)
            self.historic_prices.append(self.current_price)
        else:
            self.current_price = max(self.current_price - price_change, self.min_price)
            self.historic_prices.append(self.current_price)

    def can_sell_amount(self, amount: int) -> bool:
        """
        Used to check whether an ordered amount of drinks does not exceed current inventory.
        Also possible to order 0 drinks, which may be useful when user accidentally enters the wrong ID
        """
        return self.for_sale and self.nr_drinks - amount >= 0 and amount >= 0

    def reset(self) -> None:
        """
        Return sell price to initial price
        """
        self.current_price = self.starting_price
    
    def steer_price(self, price_change, decrease: bool) -> None:
        """"
        Used to only modify the price of a drink, for example to steer balance in preferred direction
        """
        if self.for_sale == False:
            return
        if decrease:
            self.current_price -= price_change
        else:
            self.current_price += price_change
        self.current_price = min(self.current_price, self.max_price)
        self.current_price = max(self.current_price, self.min_price)

    def increase_drinks_nr(self, amount: int) -> None:
        """
        Add additional drinks to the inventory
        """
        self.nr_drinks += amount

    def __repr__(self) -> str:
        if self.for_sale:
            return f"{self.id} : {self.name}, current price = €{self.current_price/100:.2f}, drinks remaining = {self.nr_drinks}, drinks sold = {self.initial_nr_drinks - self.nr_drinks}"
        else:
            return f"{self.id} {self.name} IS SOLD OUT"

from dataclasses import dataclass, field

@dataclass(repr=True)
class Drink:
    """
    Contains all logic related to individual Drinks. This class should be used to modify individual drinks based on information received from
    another method that runs the main loop of the borrel.

    TODO: implement functionality for crashing the price
    """

    name: int = field(repr=True)
    id: int
    min_price: int
    max_price: int
    starting_price: int
    nr_drinks: int
    for_sale: bool = True
    historic_price: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.historic_price.append(self.starting_price)

    def modify_price(
        self, is_sold: bool, price_change: float, drinks_sold: int, Drink=None
    ) -> None:
        # Because this function is used to both increase and decrease the price of Drinks, we must check whether the product was sold in the last transaction
        if is_sold:
            self.nr_drinks -= drinks_sold
            if self.nr_drinks <= 0:
                self.for_sale = False
            self.current_price += price_change
            self.historic_price.append(self.current_price)
        else:
            self.current_price -= price_change
            self.historic_price.append(self.current_price)

    def can_sell_amount(self, amount: int) -> bool:
        return self.nr_drinks - amount >= 0 and amount >= 0

    def reset(self) -> None:
        self.current_price = self.starting_price

    def increase_drinks_nr(self, amount: int) -> None:
        self.nr_drinks += amount

    def identifier(self) -> str:
        return f"{self.id} : {self.name}"
    
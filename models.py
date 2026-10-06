"""ByteBites backend models, following the class diagram in bytebites_design.md."""


class Item:
    """A food or beverage product with a name, price, category and popularity rating."""

    def __init__(self, name: str, price: float, category: str, popularity_rating: float):
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty")
        if price < 0:
            raise ValueError("Item price cannot be negative")
        if not category or not category.strip():
            raise ValueError("Item category cannot be empty")
        if not 0 <= popularity_rating <= 5:
            raise ValueError("Popularity rating must be between 0 and 5")
        self._name = name.strip()
        self._price = float(price)
        self._category = category.strip()
        self._popularity_rating = float(popularity_rating)

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def get_category(self) -> str:
        return self._category

    def get_popularity_rating(self) -> float:
        return self._popularity_rating

    def __repr__(self) -> str:
        return f"Item({self._name!r}, ${self._price:.2f}, {self._category!r}, {self._popularity_rating})"


class Menu:
    """The catalog of all Items, filterable by category."""

    def __init__(self):
        self._items: list[Item] = []

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def remove_item(self, item: Item) -> None:
        if item not in self._items:
            raise ValueError("Item is not on the menu")
        self._items.remove(item)

    def get_all_items(self) -> list[Item]:
        return list(self._items)

    def filter_by_category(self, category: str) -> list[Item]:
        wanted = category.strip().lower()
        return [i for i in self._items if i.get_category().lower() == wanted]


class Transaction:
    """A customer's grouped selection of Items, with a computed total cost."""

    def __init__(self, customer: "Customer"):
        self._customer = customer
        self._selected_items: list[Item] = []

    def add_item(self, item: Item) -> None:
        self._selected_items.append(item)

    def remove_item(self, item: Item) -> None:
        if item not in self._selected_items:
            raise ValueError("Item is not in this transaction")
        self._selected_items.remove(item)

    def calculate_total(self) -> float:
        return round(sum(i.get_price() for i in self._selected_items), 2)


class Customer:
    """A ByteBites user with a name and a purchase history."""

    def __init__(self, name: str):
        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty")
        self._name = name.strip()
        self._purchase_history: list[Transaction] = []

    def get_name(self) -> str:
        return self._name

    def get_purchase_history(self) -> list[Transaction]:
        return list(self._purchase_history)

    def add_transaction(self, t: Transaction) -> None:
        self._purchase_history.append(t)

    def is_verified(self) -> bool:
        """A customer is verified if they have a name and at least one past purchase."""
        return bool(self._name) and len(self._purchase_history) > 0


if __name__ == "__main__":
    # Scenario: build a menu, sort and filter it, then place an order.
    burger = Item("Spicy Burger", 8.50, "Mains", 4.7)
    soda = Item("Large Soda", 2.75, "Drinks", 3.9)
    shake = Item("Chocolate Shake", 4.25, "Drinks", 4.5)
    brownie = Item("Fudge Brownie", 3.00, "Desserts", 4.8)

    menu = Menu()
    for item in (burger, soda, shake, brownie):
        menu.add_item(item)
    print("All items:", menu.get_all_items())

    by_popularity = sorted(menu.get_all_items(), key=Item.get_popularity_rating, reverse=True)
    print("By popularity:", [i.get_name() for i in by_popularity])
    by_price = sorted(menu.get_all_items(), key=Item.get_price)
    print("By price:", [i.get_name() for i in by_price])

    print("Drinks:", [i.get_name() for i in menu.filter_by_category("drinks")])
    print("Desserts:", [i.get_name() for i in menu.filter_by_category("Desserts")])
    print("Sides:", menu.filter_by_category("Sides"))

    alice = Customer("Alice")
    print("Verified before purchase:", alice.is_verified())

    order = Transaction(alice)
    order.add_item(burger)
    order.add_item(soda)
    order.add_item(soda)
    print("Total (burger + 2 sodas):", order.calculate_total())
    order.remove_item(soda)
    print("Total after removing a soda:", order.calculate_total())

    alice.add_transaction(order)
    print("Verified after purchase:", alice.is_verified())
    print("History size:", len(alice.get_purchase_history()))

    menu.remove_item(brownie)
    print("Menu size after removing brownie:", len(menu.get_all_items()))

    for bad in (lambda: Item("Free Lunch", -1, "Mains", 3), lambda: Item("X", 1, "Mains", 9), lambda: Customer(" ")):
        try:
            bad()
        except ValueError as e:
            print("Rejected:", e)
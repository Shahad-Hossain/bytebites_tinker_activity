"""ByteBites backend models (empty skeletons, see bytebites_design.md)."""


class Customer:
    """A ByteBites user with a name and a purchase history."""


class Item:
    """A food or beverage product with a name, price, category and popularity rating."""


class Menu:
    """The catalog of all Items, filterable by category."""


class Transaction:
    """A customer's grouped selection of Items, with a computed total cost."""

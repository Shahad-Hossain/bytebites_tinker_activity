## Class Diagram
Paste into [mermaid.live](https://mermaid.live) to render.

```mermaid
classDiagram
    direction LR

    class Customer {
        -str name
        -list~Transaction~ purchase_history
        +get_name() str
        +get_purchase_history() list
        +add_transaction(t: Transaction) None
        +is_verified() bool
    }

    class Item {
        -str name
        -float price
        -str category
        -float popularity_rating
        +get_name() str
        +get_price() float
        +get_category() str
        +get_popularity_rating() float
    }

    class Menu {
        -list~Item~ items
        +add_item(item: Item) None
        +remove_item(item: Item) None
        +get_all_items() list
        +filter_by_category(category: str) list
    }

    class Transaction {
        -Customer customer
        -list~Item~ selected_items
        +add_item(item: Item) None
        +remove_item(item: Item) None
        +calculate_total() float
    }

    Menu "1" o-- "*" Item : contains
    Transaction "*" --> "1" Customer : made by
    Transaction "1" o-- "1..*" Item : includes
    Customer "1" o-- "*" Transaction : purchase history
```

## Design Notes
- **Category** is a plain string on `Item`, to stay within the four-class rule. `Menu.filter_by_category` handles case-insensitive matching.
- **Verification** is simple: `Customer.is_verified()` returns true when the customer has a name and at least one past transaction. No authentication logic.
- **Open question:** the spec has no quantity. For now, buying two burgers means adding the item twice. Worth confirming with the client.
- **Open question:** `Transaction` references live `Item` prices, so changing a price changes old totals. Consider copying the price at purchase time if that matters.

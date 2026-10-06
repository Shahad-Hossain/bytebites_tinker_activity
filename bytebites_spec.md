Client Feature Request
We need to build the backend logic for the ByteBites app. The system needs to manage our customers, tracking their names and their past purchase history so the system can verify they are real users.

These customers need to browse specific food items (like a "Spicy Burger" or "Large Soda"), so we must track the name, price, category, and popularity rating for every item we sell.

We also need a way to manage the full collection of items — a digital list that holds all items and lets us filter by category such as "Drinks" or "Desserts".

Finally, when a user picks items, we need to group them into a single transaction. This transaction object should store the selected items and compute the total cost.

Candidate Classes:

Customer: Represents the users of the ByteBites app, storing their personal details (name) and maintaining their purchase history for verification.

Item: Represents the individual food or beverage products (e.g., "Spicy Burger") available for sale, tracking attributes like price, category, and popularity rating.

Menu: Serves as the catalog or collection container that holds all the individual Items, providing the ability to filter them by category.

Transaction: Represents the grouped selection of items a customer is purchasing, responsible for storing those items and calculating the final total cost.
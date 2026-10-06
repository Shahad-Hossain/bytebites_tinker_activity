"""Tests for models.py. Run with: python3 -m unittest test_bytebites -v"""
import unittest

from models import Customer, Item, Menu, Transaction


def make_items():
    return {
        "burger": Item("Spicy Burger", 8.50, "Mains", 4.7),
        "soda": Item("Large Soda", 2.75, "Drinks", 3.9),
        "shake": Item("Chocolate Shake", 4.25, "Drinks", 4.5),
        "brownie": Item("Fudge Brownie", 3.00, "Desserts", 4.8),
    }


class TestItem(unittest.TestCase):
    def test_getters_return_constructor_values(self):
        item = Item("Spicy Burger", 8.50, "Mains", 4.7)
        self.assertEqual(item.get_name(), "Spicy Burger")
        self.assertEqual(item.get_price(), 8.50)
        self.assertEqual(item.get_category(), "Mains")
        self.assertEqual(item.get_popularity_rating(), 4.7)

    def test_name_and_category_are_stripped(self):
        item = Item("  Soda  ", 1, "  Drinks ", 3)
        self.assertEqual(item.get_name(), "Soda")
        self.assertEqual(item.get_category(), "Drinks")

    def test_numbers_are_stored_as_floats(self):
        item = Item("Fries", 3, "Sides", 4)
        self.assertIsInstance(item.get_price(), float)
        self.assertIsInstance(item.get_popularity_rating(), float)

    def test_zero_price_allowed(self):
        self.assertEqual(Item("Free Water", 0, "Drinks", 3).get_price(), 0.0)

    def test_rating_boundaries_allowed(self):
        self.assertEqual(Item("A", 1, "X", 0).get_popularity_rating(), 0.0)
        self.assertEqual(Item("B", 1, "X", 5).get_popularity_rating(), 5.0)

    def test_empty_or_blank_name_rejected(self):
        for bad in ("", "   ", "\t\n", None):
            with self.subTest(name=bad):
                with self.assertRaises(ValueError):
                    Item(bad, 1, "Mains", 3)

    def test_empty_or_blank_category_rejected(self):
        for bad in ("", "  ", None):
            with self.subTest(category=bad):
                with self.assertRaises(ValueError):
                    Item("Burger", 1, bad, 3)

    def test_negative_price_rejected(self):
        for bad in (-0.01, -1, -100):
            with self.subTest(price=bad):
                with self.assertRaises(ValueError):
                    Item("Burger", bad, "Mains", 3)

    def test_rating_out_of_range_rejected(self):
        for bad in (-0.1, 5.01, 6, 100, float("nan")):
            with self.subTest(rating=bad):
                with self.assertRaises(ValueError):
                    Item("Burger", 1, "Mains", bad)

    def test_nan_price_rejected(self):
        with self.assertRaises(ValueError):
            Item("Burger", float("nan"), "Mains", 3)

    def test_infinite_price_rejected(self):
        with self.assertRaises(ValueError):
            Item("Burger", float("inf"), "Mains", 3)

    def test_repr_contains_name_and_price(self):
        text = repr(Item("Soda", 2.5, "Drinks", 4))
        self.assertIn("Soda", text)
        self.assertIn("2.50", text)


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.items = make_items()
        self.menu = Menu()
        for item in self.items.values():
            self.menu.add_item(item)

    def test_new_menu_is_empty(self):
        self.assertEqual(Menu().get_all_items(), [])

    def test_add_item_preserves_insertion_order(self):
        self.assertEqual(self.menu.get_all_items(), list(self.items.values()))

    def test_remove_item(self):
        self.menu.remove_item(self.items["brownie"])
        self.assertNotIn(self.items["brownie"], self.menu.get_all_items())
        self.assertEqual(len(self.menu.get_all_items()), 3)

    def test_remove_missing_item_raises(self):
        with self.assertRaises(ValueError):
            self.menu.remove_item(Item("Pizza", 9, "Mains", 4))

    def test_remove_from_empty_menu_raises(self):
        with self.assertRaises(ValueError):
            Menu().remove_item(self.items["burger"])

    def test_remove_same_item_twice_raises(self):
        self.menu.remove_item(self.items["soda"])
        with self.assertRaises(ValueError):
            self.menu.remove_item(self.items["soda"])

    def test_equal_but_distinct_item_is_not_the_same_item(self):
        twin = Item("Large Soda", 2.75, "Drinks", 3.9)
        with self.assertRaises(ValueError):
            self.menu.remove_item(twin)

    def test_get_all_items_returns_a_copy(self):
        listing = self.menu.get_all_items()
        listing.clear()
        self.assertEqual(len(self.menu.get_all_items()), 4)

    def test_duplicate_add_removes_one_at_a_time(self):
        self.menu.add_item(self.items["soda"])
        self.menu.remove_item(self.items["soda"])
        self.assertIn(self.items["soda"], self.menu.get_all_items())

    def test_filter_by_category(self):
        drinks = self.menu.filter_by_category("Drinks")
        self.assertEqual(drinks, [self.items["soda"], self.items["shake"]])

    def test_filter_is_case_insensitive(self):
        for query in ("drinks", "DRINKS", "dRiNkS"):
            with self.subTest(query=query):
                self.assertEqual(len(self.menu.filter_by_category(query)), 2)

    def test_filter_ignores_surrounding_whitespace(self):
        self.assertEqual(len(self.menu.filter_by_category("  Drinks ")), 2)

    def test_filter_unknown_category_returns_empty_list(self):
        self.assertEqual(self.menu.filter_by_category("Sides"), [])

    def test_filter_empty_string_returns_empty_list(self):
        self.assertEqual(self.menu.filter_by_category(""), [])

    def test_filter_requires_exact_match_not_substring(self):
        self.assertEqual(self.menu.filter_by_category("Drink"), [])

    def test_filter_on_empty_menu(self):
        self.assertEqual(Menu().filter_by_category("Drinks"), [])

    def test_filter_does_not_modify_menu(self):
        self.menu.filter_by_category("Drinks")
        self.assertEqual(len(self.menu.get_all_items()), 4)

    def test_filter_after_removal(self):
        self.menu.remove_item(self.items["soda"])
        self.assertEqual(self.menu.filter_by_category("drinks"), [self.items["shake"]])

    def test_sorting_menu_items_by_popularity_and_price(self):
        by_pop = sorted(self.menu.get_all_items(), key=Item.get_popularity_rating, reverse=True)
        self.assertEqual([i.get_name() for i in by_pop][0], "Fudge Brownie")
        by_price = sorted(self.menu.get_all_items(), key=Item.get_price)
        self.assertEqual(by_price[0], self.items["soda"])
        self.assertEqual(by_price[-1], self.items["burger"])


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.items = make_items()
        self.customer = Customer("Alice")
        self.order = Transaction(self.customer)

    def test_empty_transaction_total_is_zero(self):
        self.assertEqual(self.order.calculate_total(), 0)

    def test_total_of_single_item(self):
        self.order.add_item(self.items["burger"])
        self.assertEqual(self.order.calculate_total(), 8.50)

    def test_total_of_multiple_items(self):
        self.order.add_item(self.items["burger"])
        self.order.add_item(self.items["soda"])
        self.assertEqual(self.order.calculate_total(), 11.25)

    def test_same_item_added_twice_counts_twice(self):
        self.order.add_item(self.items["soda"])
        self.order.add_item(self.items["soda"])
        self.assertEqual(self.order.calculate_total(), 5.50)

    def test_remove_item_updates_total(self):
        self.order.add_item(self.items["burger"])
        self.order.add_item(self.items["soda"])
        self.order.remove_item(self.items["soda"])
        self.assertEqual(self.order.calculate_total(), 8.50)

    def test_remove_one_of_two_duplicates(self):
        self.order.add_item(self.items["soda"])
        self.order.add_item(self.items["soda"])
        self.order.remove_item(self.items["soda"])
        self.assertEqual(self.order.calculate_total(), 2.75)

    def test_remove_item_not_in_transaction_raises(self):
        with self.assertRaises(ValueError):
            self.order.remove_item(self.items["burger"])

    def test_remove_all_items_returns_total_to_zero(self):
        self.order.add_item(self.items["burger"])
        self.order.remove_item(self.items["burger"])
        self.assertEqual(self.order.calculate_total(), 0)

    def test_total_is_rounded_to_cents(self):
        # 0.1 + 0.2 is 0.30000000000000004 in floating point
        self.order.add_item(Item("A", 0.1, "X", 3))
        self.order.add_item(Item("B", 0.2, "X", 3))
        self.assertEqual(self.order.calculate_total(), 0.3)

    def test_free_items_do_not_change_total(self):
        self.order.add_item(Item("Water", 0, "Drinks", 3))
        self.order.add_item(self.items["soda"])
        self.assertEqual(self.order.calculate_total(), 2.75)

    def test_many_items(self):
        for _ in range(1000):
            self.order.add_item(Item("Cookie", 0.99, "Desserts", 4))
        self.assertEqual(self.order.calculate_total(), 990.00)

    def test_total_is_recomputed_not_cached(self):
        self.order.add_item(self.items["soda"])
        first = self.order.calculate_total()
        self.order.add_item(self.items["soda"])
        self.assertNotEqual(first, self.order.calculate_total())

    def test_two_transactions_are_independent(self):
        other = Transaction(Customer("Bob"))
        self.order.add_item(self.items["burger"])
        self.assertEqual(other.calculate_total(), 0)


class TestCustomer(unittest.TestCase):
    def test_name_is_stripped(self):
        self.assertEqual(Customer("  Alice ").get_name(), "Alice")

    def test_empty_or_blank_name_rejected(self):
        for bad in ("", "   ", None):
            with self.subTest(name=bad):
                with self.assertRaises(ValueError):
                    Customer(bad)

    def test_new_customer_has_no_history(self):
        self.assertEqual(Customer("Alice").get_purchase_history(), [])

    def test_new_customer_is_not_verified(self):
        self.assertFalse(Customer("Alice").is_verified())

    def test_add_transaction_adds_to_history(self):
        alice = Customer("Alice")
        order = Transaction(alice)
        alice.add_transaction(order)
        self.assertEqual(alice.get_purchase_history(), [order])

    def test_customer_with_purchase_is_verified(self):
        alice = Customer("Alice")
        alice.add_transaction(Transaction(alice))
        self.assertTrue(alice.is_verified())

    def test_history_keeps_order_of_purchases(self):
        alice = Customer("Alice")
        first, second = Transaction(alice), Transaction(alice)
        alice.add_transaction(first)
        alice.add_transaction(second)
        self.assertEqual(alice.get_purchase_history(), [first, second])

    def test_get_purchase_history_returns_a_copy(self):
        alice = Customer("Alice")
        alice.add_transaction(Transaction(alice))
        alice.get_purchase_history().clear()
        self.assertEqual(len(alice.get_purchase_history()), 1)
        self.assertTrue(alice.is_verified())

    def test_histories_are_not_shared_between_customers(self):
        alice, bob = Customer("Alice"), Customer("Bob")
        alice.add_transaction(Transaction(alice))
        self.assertEqual(bob.get_purchase_history(), [])
        self.assertFalse(bob.is_verified())

    def test_history_total_matches_transaction_total(self):
        alice = Customer("Alice")
        order = Transaction(alice)
        order.add_item(Item("Burger", 8.5, "Mains", 4))
        alice.add_transaction(order)
        self.assertEqual(alice.get_purchase_history()[0].calculate_total(), 8.5)


class TestEndToEnd(unittest.TestCase):
    def test_full_ordering_flow(self):
        items = make_items()
        menu = Menu()
        for item in items.values():
            menu.add_item(item)

        alice = Customer("Alice")
        self.assertFalse(alice.is_verified())

        order = Transaction(alice)
        for item in menu.filter_by_category("drinks"):
            order.add_item(item)
        order.add_item(items["brownie"])
        self.assertEqual(order.calculate_total(), 10.0)

        alice.add_transaction(order)
        self.assertTrue(alice.is_verified())

    def test_removing_item_from_menu_does_not_change_existing_order(self):
        items = make_items()
        menu = Menu()
        menu.add_item(items["soda"])
        alice = Customer("Alice")
        order = Transaction(alice)
        order.add_item(items["soda"])
        menu.remove_item(items["soda"])
        self.assertEqual(order.calculate_total(), 2.75)


if __name__ == "__main__":
    unittest.main()

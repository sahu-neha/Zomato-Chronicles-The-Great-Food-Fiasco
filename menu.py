import sys
from re import match
from termcolor import colored
from tabulate import tabulate

# Initial menu data
menu = {
    "1": {"name": "Pasta", "price": 10.99, "availability": True, "stock": 20},
    "2": {"name": "Burger", "price": 8.99, "availability": True, "stock": 15},
    "3": {"name": "Pizza", "price": 12.99, "availability": False, "stock": 0},
}

orders = []


# Display the menu
def display_menu():
    if len(menu) == 0:
        print(colored("No Dishes in menu!", "red"))
        return
    else:
        menu_data = []
        for dish_id, dish in menu.items():
            availability = (
                colored("Available", "green")
                if dish["availability"]
                else colored("Not Available", "red")
            )
            menu_data.append(
                [
                    colored(dish_id, "yellow"),
                    colored(dish["name"], "cyan"),
                    colored(dish["price"], "blue"),
                    availability,
                    colored(dish["stock"], "magenta"),
                ]
            )

        print(
            tabulate(
                menu_data,
                headers=[
                    colored("ID", "yellow"),
                    colored("Name", "cyan"),
                    colored("Price", "blue"),
                    colored("Availability", "green"),
                    colored("Stock", "magenta"),
                ],
                tablefmt="grid",
            )
        )

        print(colored("\n*** Orders ***", "yellow"))
        if len(orders) == 0:
            print(colored("No orders placed yet!", "red"))
        else:
            order_data = []
            for order in orders:
                order_data.append(
                    [
                        colored(order["order_id"], "yellow"),
                        colored(order["customer_name"], "cyan"),
                        colored(order["order_status"], "green"),
                    ]
                )
            print(
                tabulate(
                    order_data,
                    headers=[
                        colored("Order ID", "yellow"),
                        colored("Customer", "cyan"),
                        colored("Status", "green"),
                    ],
                    tablefmt="grid",
                )
            )


# Add a new dish to the menu
def add_dish():
    id = str(len(menu) + 1)
    if id not in menu:
        id = str(len(menu) + 1)
    else:
        id = str(len(menu))

    dish_name = input(colored("Enter the Dish name: ", "blue"))
    price = input(float(colored("Enter the Dish price: ", "blue")))
    stock_count = int(input(colored("Enter the stock count: ", "blue")))

    availability = stock_count > 0  # Set availability based on stock count

    dish = {
        "dish_id": id,
        "dish_name": dish_name,
        "price": price,
        "stock_count": stock_count,
        "availability": availability,
    }

    menu[id] = dish

    if stock_count == 0:
        print(f"{dish_name} added successfully to the menu. Availability: No")
    else:
        print(f"{dish_name} added successfully to the menu. Availability: Yes")


# Remove a dish from the menu
def remove_dish():
    dish_id = input(colored("Enter the Dish ID: ", "blue"))

    if dish_id in menu:
        dish_name = menu[dish_id]["name"]
        del menu[dish_id]
        print(f"Dish '{dish_name}' with ID '{dish_id}' has been removed from the menu.")
    else:
        print("Invalid dish ID. The dish does not exist in the menu.")


# Update details of a dish in the menu
def update_dish():
    dish_id = input(colored("Enter the Dish ID: ", "blue"))

    if dish_id in menu:
        dish_name = menu[dish_id]["name"]
        dish_price = input(float(colored("Enter the Dish price: ", "blue")))
        dish_stock = int(input(colored("Enter the stock count: ", "blue")))
        dish_availability = dish_stock > 0  # Set availability based on stock count

        menu[dish_id] = {
            "name": dish_name,
            "price": dish_price,
            "availability": dish_availability,
            "stock": dish_stock,
        }

        print(
            colored(
                f"Dish '{dish_name}' with ID '{dish_id}' has been updated.", "green"
            )
        )
    else:
        print(colored("Invalid dish ID. The dish does not exist in the menu.", "red"))


# Take a customer order
def take_order():
    customer_name = input("Enter customer name: ")
    dish_ids = input("Enter dish IDs (comma-separated): ").split(",")

    # Check if all dishes in the order are available and deduct stock count
    for dish_id in dish_ids:
        dish = menu.get(dish_id)
        if dish:
            if dish["availability"]:
                if dish["stock"] > 0:
                    dish["stock"] -= 1  # Deduct 1 from the stock count
                    if dish["stock"] == 0:
                        dish["availability"] = False  # Update availability to "no"
                else:
                    print(f"Sorry, {dish['dish_name']} is out of stock.")
                    return
            else:
                print(f"{dish['dish_name']} is currently unavailable.")
                return
        else:
            print(f"Dish with ID {dish_id} does not exist.")
            return

    # Create a new order with a unique order ID
    order_id = len(orders) + 1
    order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "dishes": dish_ids,
        "order_status": "received",  # Set initial order status as "received"
    }

    # Add the order to the list of orders
    orders.append(order)

    print(f"Order {order_id} placed successfully.")


# Update the status of an order
def update_order_status():
    order_id = int(input("Enter the order ID: "))
    for order in orders:
        if order["order_id"] == order_id:
            print(f"Current order status: {order['order_status']}")
            new_status = input("Enter the new order status: ")
            order["order_status"] = new_status
            print(f"Order {order_id} status updated to {new_status}.")
            return

    print(f"Order with ID {order_id} not found.")


# Main program execution
def main():
    while True:
        print()
        print("========================")
        print("Welcome to Zesty Zomato!")
        print("1. Display menu")
        print("2. Add a dish")
        print("3. Remove a dish")
        print("4. Update dish details")
        print("5. Take an order")
        print("6. Update order status")
        print("7. Exit")
        print("========================")
        print()

        choice = input("Enter your choice: ")

        if choice == "1":
            display_menu()
        elif choice == "2":
            add_dish()
        elif choice == "3":
            remove_dish()
        elif choice == "4":
            update_dish()
        elif choice == "5":
            take_order()
        elif choice == "6":
            update_order_status()
        elif choice == "7":
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

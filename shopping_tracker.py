# Shopping List Price Tracker — with QR Code Scanning!
# Cardozo Education Campus | AP Computer Science Principles

from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import os

# Starter shopping list (parallel lists: items[i] matches prices[i])
items = ["Milk", "Eggs", "Bread", "Chicken", "Rice"]
prices = [3.99, 2.50, 4.25, 8.99, 5.49]


# This function:
# - Reads the QR code from an image file
# - Pulls out the item name and price
# - Adds them to our shopping list
def scan_qr_code(image_path, item_list, price_list):
    # Open the QR code image
    image = Image.open(image_path)
    # Decode reads the text hidden inside the QR code
    decoded = decode(image)

    if len(decoded) == 0:
        print("Could not read the QR code. Try another image.")
        return

    # The text inside our QR codes looks like:  Milk,3.99
    qr_text = decoded[0].data.decode("utf-8")
    parts = qr_text.split(",")
    item_name = parts[0]
    item_price = float(parts[1])

    # Add the scanned item to the shopping list
    item_list.append(item_name)
    price_list.append(item_price)
    print("Scanned: " + item_name + " - $" + str(item_price))


# This function makes a QR code image for one item
# so students can print them and use them at the expo
def make_qr_code(item_name, item_price):
    qr_text = item_name + "," + str(item_price)
    qr = qrcode.make(qr_text)
    filename = "qr_" + item_name + ".png"
    qr.save(filename)
    print("Saved QR code: " + filename)


# This function:
# - Displays the items that fit within the budget
# - Compares the budget with the item prices
def find_items(item_list, price_list, max_budget):
    found = []
    total = 0
    for i in range(len(item_list)):
        # Check if this item fits in what's left of the budget
        if price_list[i] <= max_budget and total + price_list[i] <= max_budget:
            found.append(i)
            total = total + price_list[i]
    if len(found) == 0:
        print("Nothing fits your budget.")
    else:
        for i in found:
            print("  " + item_list[i] + " - $" + str(price_list[i]))
        print("  Total: $" + str(round(total, 2)))
    return found


# Main program loop
running = True
while running:
    print("\n=== SHOPPING LIST TRACKER ===")
    print("1. View shopping list")
    print("2. Add an item manually")
    print("3. Scan QR code to add an item")
    print("4. Find items within budget")
    print("5. Generate QR codes for all items")
    print("6. Quit")
    choice = input("Choose (1-6): ")

    # View the current shopping list
    if choice == "1":
        for i in range(len(items)):
            print(str(i + 1) + ". " + items[i] + " - $" + str(prices[i]))

    # Add a new item by typing it in
    elif choice == "2":
        new_item = input("Item name: ")
        new_price = float(input("Price: "))
        items.append(new_item)
        prices.append(new_price)
        print(new_item + " added!")

    # Scan a QR code from a saved image file
    elif choice == "3":
        path = input("Enter the QR code filename (example: qr_Milk.png): ")
        scan_qr_code(path, items, prices)

    # Run the budget checker
    elif choice == "4":
        budget = float(input("Enter your max budget: $"))
        find_items(items, prices, budget)

    # Create printable QR codes for every item on the list
    elif choice == "5":
        for i in range(len(items)):
            make_qr_code(items[i], prices[i])
        print("All QR codes saved!")

    # Quit the program
    elif choice == "6":
        print("Goodbye!")
        running = False

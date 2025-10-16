"""
Inventory Management System Module.

This module provides functions to manage stock data, including adding, removing,
loading, and saving inventory items.
"""
import json
import logging
from datetime import datetime


# Global variable
stock_data = {}


def addItem(item="default", qty=0, logs=None):
    """Adds a specified quantity of an item to the global stock data."""
    if logs is None:
        logs = []

    # Validation added for robustness (Addresses original TypeError)
    if not isinstance(qty, int):
        logging.warning(f"Attempted to add non-integer quantity: {qty}")  # W1203 fixed
        return

    if not item:
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))


def removeItem(item, qty):
    """Removes a specified quantity of an item from the global stock data."""
    # Fixed bare except: with specific exception handling
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # W1203 fixed
        logging.info(f"Attempted to remove non-existent item: {item}")
    except Exception as e:
        # W0718 mitigated by specific catches, and W1203 fixed
        logging.error(f"An unexpected error occurred: {e}")


def getQty(item):
    """Retrieves the current stock quantity for an item, defaulting to 0."""
    return stock_data.get(item, 0)


def loadData(file="inventory.json"):
    """Loads inventory data from a specified JSON file."""
    # FIX R1732, W1514: Use 'with open' and explicit encoding
    with open(file, "r", encoding='utf-8') as f:
        global stock_data
        stock_data = json.loads(f.read())
    # f is automatically closed outside the 'with' block


def saveData(file="inventory.json"):
    """Saves the current inventory data to a specified JSON file."""
    # FIX R1732, W1514: Use 'with open' and explicit encoding
    with open(file, "w", encoding='utf-8') as f:
        f.write(json.dumps(stock_data))
    # f is automatically closed outside the 'with' block


def printData():
    """Prints a formatted report of all items and their quantities."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(item, "->", qty)


def checkLowItems(threshold=5):
    """Returns a list of items whose stock quantity is below the given threshold."""
    result = []
    for item in stock_data:
        if stock_data[item] < threshold:
            result.append(item)
    return result


def main():
    """Main execution function to run inventory operations."""
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()


main()

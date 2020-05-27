"""
The program lets the user enter the data of existing products with their prices and quantities
And track the quantity and price if they need to be change:
    - delete if the product is sold out
    - update the quantity is some of the product is sold
    - stock up and add more inventory
    - display the whole table of the existing products and it's priced
    - look up the whole information of the product using it's name
"""
import pickle
from colorama import init, Fore, Back, Style
from termcolor import colored

init(autoreset=True)
init(convert=True)


def check_if_valid_price(price_of_product):
    """
    :param price_of_product: entered data for the price of the product
    :return: the valid price of the new product
    """

    valid_price = 0
    # print(not price_of_product.replace('.', '', 1).isdigit())
    while not price_of_product.replace('.', '', 1).isdigit():
        # print("HERE")
        print(Fore.RED + "Please enter the valid price for your new product: " + Style.RESET_ALL, end="")
        price_of_product = input()
        # print(price_of_product.replace('.', '', 1).isdigit())
        valid_price = price_of_product
        # print(type(valid_price))
    valid_price = float(valid_price)
    # print(type(valid_price))
    return valid_price


def check_if_valid_quantity(quantity_of_product):
    """
    :param quantity_of_product: entered quantity of new product
    :return: the valid quantity of the new product
    """
    valid_quantity = 0
    while not quantity_of_product.isdigit():
        print(Fore.RED + "Please enter the valid whole number for the quantity of your new product: " + Style.RESET_ALL, end="")
        quantity_of_product = input()
        valid_quantity = quantity_of_product
    valid_quantity = int(valid_quantity)
    return valid_quantity


def add_new_product(inventory):
    """
    :return: the new list including the product name, it's price and stock-up quantity
    """
    single_product_data = []  # empty list to hold whole info about single product
    product_details = {}  # empty object for price and quantity store of a single product

    name_of_product = input("Please enter the product name. Must be unique. ")
    if_exist = if_product_exists(inventory, name_of_product)
    while if_exist:
        name_of_product = input(
            "Product with such name already exists in the inventory. Please enter another unique product name. ")
        if_exist = if_product_exists(inventory, name_of_product)
    price_of_product = (input("Please enter the price of single item of your new product in $: "))
    # Check if the entered price is valid number
    valid_price = check_if_valid_price(price_of_product)
    quantity_of_product = (input("Please enter the quantity for stock-up of your new product: "))
    # Check if the entered quantity is valid number
    valid_quantity = check_if_valid_quantity(quantity_of_product)

    product_details["price"] = valid_price  # price_of_product
    product_details["quantity"] = valid_quantity  # quantity_of_product

    print(product_details["price"])
    print(product_details["quantity"])
    single_product_data.append(name_of_product)
    single_product_data.append(product_details)
    print("")

    return single_product_data


def print_inventory(inventory):
    # we print the whole inventory object detailed product by product
    print("")
    print(colored("Here is the whole list of the inventory:", "green", attrs=['bold']))
    for item in inventory:
        print("---------------------")
        print(colored((item + ":"), "green"))
        for details in inventory[item]:
            print(details + ": " + str(inventory[item][details]))


def print_single_product_data(inventory, product_name):
    # print("")
    for product in inventory:
        if product == product_name:
            # print("")
            print("--------------------------")
            print(colored(product_name + ":", "green"))
            for details in inventory[product_name]:
                print(details + ": " + str(inventory[product_name][details]))
            print("--------------------------")
            # print("")


def print_menu():
    print("")
    print("==========================================")
    print(colored("Please pick an option you want to do now:", "blue", attrs=['bold']))
    print("-1- to see the whole list of inventory")
    print("-2- to see the list of low stock products")
    print("-3- to delete the specified product")
    print("-4- to add new product")
    print("-5- for pull up all data for specified product")
    print("-6- to modify the quantity of specified product")
    print("-7- to exit the program")
    print("==========================================")
    print("")

    print(Fore.BLUE + "Please enter your choice: " + Style.RESET_ALL, end="")
    user_choice = input()
    # print((user_choice.isdigit()))
    while not user_choice.isdigit():
        user_choice = input("Please type the number for one of the options from the menu: ")
    return user_choice


def change_the_given_product_quantity(inventory, product_to_change_quantity):
    """
    :param inventory: all the data from the whole inventory
    :param product_to_change_quantity: the name of the product we need to change quantity
    :return: the updated new version of quantity of given product name
    """

    for product in inventory:
        if product == product_to_change_quantity:
            print("Here is current quantity for " + product_to_change_quantity + ": " + str(
                inventory[product]["quantity"]))
            quantity_to_change = int(input("Please add new quantity for the " + product + " product: "))
            # check_if_valid_quantity(quantity_to_change)
            inventory[product]["quantity"] = quantity_to_change
            print("Here is the new quantity for " + product_to_change_quantity + ": " + str(
                inventory[product]["quantity"]))
            pickle.dump(inventory, open("save.p", "wb"))


def delete_the_product(inventory, product_to_delete):
    """
    :param inventory: all the inventory data
    :param product_to_delete: the name of the product we need to delete
    :return: the updated new version of the inventory without the product which we deleted
    """
    print("")
    print(colored("Here is the all available data for your chosen product.", "red"))
    print_single_product_data(inventory, product_to_delete)
    if_delete = input("Are you sure, you want to delete it? y/n: ")

    # using while loop to make sure user picks the y - Yes to delete or n - No, changed his mind
    while True:
        if if_delete == "y":
            del inventory[product_to_delete]
            pickle.dump(inventory, open("save.p", "wb"))
            print(colored("You've just deleted all the data for " + product_to_delete + " from your inventory", "red"))
            break
        elif if_delete == "n":
            print("You've change your mind - no product data will be deleted")
            break
        else:
            if_delete = input("Please enter 'y' for Yes - to delete, 'n' for No - not to delete: ")


def show_low_stock_products(inventory):
    """
    :param inventory: all the inventory data
    :return: the data of only low stock quantity products (where quantity <20)
    """
    # print(inventory.items())
    print("")
    print(colored("Here is the list of all the products in the inventory which quantity is lower then 20 pc:", "red",
                  attrs=['bold']))

    for name, data in inventory.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        # function data.get(key) – Returns value associated with key in dictionary.
        num = data.get("quantity")
        if num < 20:
            print_single_product_data(inventory, name)
    # print_menu()


def if_product_exists(inventory, product_name):
    """
    Function to check if the user's product name is exist in our inventory DB. Name has to be unique.
    :param product_name: product name to check
    :param inventory: all the inventory data
    :return: True if product with such name exists or False if not.
    """
    return product_name in inventory


def main():
    while True:
        # print the options / menu of choices for the user
        user_choice = int(print_menu())
        # load up our DB
        all_data = pickle.load(open("save.p", "rb"))

        # if user picks to look up at the whole list of the inventory
        if user_choice == 1:
            print_inventory(all_data)

        # if user picks to add new product
        elif user_choice == 4:
            while True:
                inventory = all_data
                keep_adding_new_product = input("Do you want to add new product? y/n: ")
                print("")
                # when user choose to add new product
                if keep_adding_new_product == "y":
                    single_product_data = add_new_product(inventory)
                    # print(single_product_data)
                    # if_product_exists(all_data, single_product_data[0])
                    # saving new product data to our inventory DB
                    # the key of dict is the name of product
                    inventory[single_product_data[0]] = single_product_data[1]
                    print("------------------------------------------------")
                    print(colored("You have successfully added your new product data into the inventory ", "blue"))
                    print("------------------------------------------------")
                    print("")
                # when user choose to stop adding new products
                elif keep_adding_new_product == "n":
                    break
                # when user choose something else then y for "Yes" or n for "No"
                else:
                    print("Please enter 'y' or 'n' to add new product for 'y' or 'n' if you are all done ")

            print("")
            pickle.dump(inventory, open("save.p", "wb"))

        # if user choose to find out the data for the specific product name
        elif user_choice == 5:
            user_choice_of_single_product = input("Please enter the name of the product you want to look at: ")
            while user_choice_of_single_product not in all_data:
                print(
                    "Sorry, there is no such product in the inventory, please enter the product using all small letters")
                user_choice_of_single_product = input("Please enter the name of the product you want to look at: ")
            print("")
            print(colored("Here is the whole data for your " + user_choice_of_single_product + ":", "yellow"))
            print_single_product_data(all_data, user_choice_of_single_product)

        # if user choose to change the quantity of the certain specified product name
        elif user_choice == 6:
            product_to_change_quantity = input(
                "Please enter the name of the product you want to change the quantity at: ")
            while product_to_change_quantity not in all_data:
                print(
                    "Sorry, there is no such product in the inventory, please enter the product using all small letters")
                product_to_change_quantity = input(
                    "Please enter the name of the product you want to change the quantity at: ")
            change_the_given_product_quantity(all_data, product_to_change_quantity)

        # if user wants to delete the specified product and it's all data from the inventory
        elif user_choice == 3:
            product_to_delete = input("Please enter the product name you want to delete: ")
            while product_to_delete not in all_data:
                print(
                    "Sorry, there is no such product in the inventory, please enter the product using all small letters")
                product_to_delete = input("Please enter the name of the product you want to delete: ")
            delete_the_product(all_data, product_to_delete)

        # if user wants to see the list of low locked products
        elif user_choice == 2:
            show_low_stock_products(all_data)

        elif user_choice == 7:
            break

        else:
            print(colored("Please pick the number from the menu: ", "red"))
            user_choice = int(print_menu())


if __name__ == '__main__':
    main()

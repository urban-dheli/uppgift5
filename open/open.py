import csv
import os
import locale
from time import sleep
import uuid

def load_data(filename): 
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(        #list
                {                    #dictionary
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

#gör en funktion som hämtar en produkt

def add_products(products, name, desc, price, quantity):

    max_id = max(products, key = lambda x: x['id'])
    new_id = max_id['id'] + 1

    new_product = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }

    products.append(new_product)

    with open('open/db_products.csv', 'a') as fd:
        fd.write(f"\n{new_id},{name},{desc},{price},{quantity}")

    return f"Du la till produkt {name} med id: {new_id}"

def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break  # Avsluta loopen så snart produkten hittas

    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"

def edit_product(products, id, name, desc, price, quantity):
    edit = None

    for product in products:
        if product['id'] == id:
            edit = product
            break

    if edit != None:
        edit['name'] = name
        edit['desc'] = desc
        edit['price'] = price
        edit['quantity'] = quantity

    return f"Produkt med id: {id}, har ändrats"

def view_product(products, id):
    # Go through each product in the list
    for product in products:
        # Check if the product's id matches the given id
        if product["id"] == id:
            # If it matches, return the product's name and description
            return f"Visar produkt: {product['name']} {product['desc']}"
    
    # If no matching product is found, return this message
    return "Produkten hittas inte"


def view_products(products):
    product_list = []
    for index, product in enumerate(products,1 ):
        product_info = f"{index}) (#{product['id']}) {product['name']} \t {product['desc']} \t {locale.currency(product['price'], grouping=True)}"
        product_list.append(product_info)
    
    return "\n".join(product_list)

def get_product(products, id):
    for product in products:
        if product["id"] == id:
            return product
        
    return "Produkten finns ej"

#TODO: gör om så du slipper använda global-keyword (flytta inte "product = []")
#TODO: skriv en funktion som returnerar en specifik produkt med hjälp av id


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('open/db_products.csv')
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))  # Show ordered list of products

        choice = input("Vill du (L)ägga till, (Ä)ndra, (V)isa eller (T)a bort en produkt? ").strip().upper()

        if choice == "L":

            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))

            print(add_products(products, name, desc, price, quantity))
            sleep(1)

        elif choice in ["Ä", "V", "T"]:
            try:
                index = int(input("Enter product ID: "))

            except ValueError:
                print("Välj produkt-id med siffror")
                sleep(1)
                continue

            if 1 <= index <= len(products):
                selected_product = products[index - 1]
                id = selected_product['id']

            if choice == "Ä":
                placeholder = get_product(products, id)

                name = input(f"Nytt namn: ({placeholder['name']})   ")
                desc =  input(f"Ny beskrivning på produkten: ({placeholder['desc']}) ")
                price = float(input(f"Nytt pris: ({placeholder['price']})   "))
                quantity = int(input(f"Ny mängd av produkten: ({placeholder['quantity']})    "))

                edit_product(products, id, name, desc, price, quantity)

            if choice == "V":   #visa
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product
                    print(view_product(products, id))  # Remove product using the actual ID
                    done = input()
                    
                else:
                    print("Ogiltig produkt")
                    sleep(1)

            elif choice == "T": #ta bort
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product

                    print(remove_product(products, id))  # Remove product using the actual ID
                    sleep(1)            

                else:
                    print("Ogiltig produkt")
                    sleep(1)
        
    except ValueError:
        print("Välj en produkt med siffor")
        sleep(1)

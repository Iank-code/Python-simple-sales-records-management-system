import csv
import os
import sys

customers = {}
sales = []
next_cust_id = 100000
next_trans_id = 100000000

def normalize_headers(headers):
    return [header.strip().lower() for header in headers]

def load_customers(file_path):
    global customers, next_cust_id
    customers = {}
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            reader.fieldnames = normalize_headers(reader.fieldnames)
            for row in reader:
                cust_id = int(row['cust_id'])
                customers[cust_id] = {
                    'name': row['name'],
                    'postcode': row.get('postcode', ''),
                    'phone': row.get('phone', '')
                }
                next_cust_id = max(next_cust_id, cust_id + 1)
    except KeyError as e:
        print(f"Error: Missing expected column in customers CSV: {e}")
    except Exception as e:
        print(f"An error occurred while loading customers: {e}")

def load_sales(file_path):
    global sales, next_trans_id
    sales = []
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            reader.fieldnames = normalize_headers(reader.fieldnames)
            for row in reader:
                trans_id = int(row['trans_id'])
                sales.append({
                    'date': row['date'],
                    'trans_id': trans_id,
                    'cust_id': int(row['cust_id']),
                    'category': row['category'],
                    'value': float(row['value'])
                })
                next_trans_id = max(next_trans_id, trans_id + 1)
    except KeyError as e:
        print(f"Error: Missing expected column in sales CSV: {e}")
    except Exception as e:
        print(f"An error occurred while loading sales: {e}")

def save_customers(file_path):
    try:
        with open(file_path, mode='w', newline='') as file:
            fieldnames = ['cust_id', 'name', 'postcode', 'phone']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for cust_id, data in customers.items():
                writer.writerow({
                    'cust_id': cust_id,
                    'name': data['name'],
                    'postcode': data['postcode'],
                    'phone': data['phone']
                })
        print(f"Customer records saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving customers: {e}")

def save_sales(file_path):
    try:
        with open(file_path, mode='w', newline='') as file:
            fieldnames = ['date', 'trans_id', 'cust_id', 'category', 'value']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for sale in sales:
                writer.writerow(sale)
        print(f"Sales records saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving sales: {e}")

def add_customer():
    global next_cust_id
    name = input("Enter customer name: ")
    postcode = input("Enter customer postcode (optional): ")
    phone = input("Enter customer phone number (optional): ")
    customers[next_cust_id] = {'name': name, 'postcode': postcode, 'phone': phone}
    print(f"Customer added with ID: {next_cust_id}")
    next_cust_id += 1

def add_sales_record():
    global next_trans_id
    cust_id = int(input("Enter customer ID: "))
    if cust_id not in customers:
        print("Customer ID not found.")
        return
    date = input("Enter date of sale (YYYY-MM-DD): ")
    category = input("Enter sale category: ")
    value = float(input("Enter sale value: "))
    sales.append({'date': date, 'trans_id': next_trans_id, 'cust_id': cust_id, 'category': category, 'value': value})
    print(f"Sales record added with transaction ID: {next_trans_id}")
    next_trans_id += 1
def search_customers(query):
    query = query.lower()
    results = []
    for cust_id, data in customers.items():
        print(f"Checking customer: {data}")  # Debug statement
        if (query in data['name'].lower() or
            query in data['postcode'].lower() or
            query in data['phone'].lower()):
            results.append(data)  # Append only the data without cust_id
    print(f"Search results: {results}")  # Debug statement
    return results

def search_sales(query):
    query = query.lower()
    results = []
    for sale in sales:
        if (query in str(sale['cust_id']).lower() or
            query in sale['date'].lower() or
            query in sale['category'].lower() or
            query in str(sale['value']).lower()):
            results.append(sale)  # Append the entire sale data
    return results


def display_sales_by_customer(cust_id):
    results = [sale for sale in sales if sale['cust_id'] == cust_id]
    return results

def delete_sales_record(trans_id):
    global sales
    sales = [sale for sale in sales if sale['trans_id'] != trans_id]

def delete_customer(cust_id):
    global customers, sales
    if cust_id in customers:
        del customers[cust_id]
        sales = [sale for sale in sales if sale['cust_id'] != cust_id]

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Load customer and sales records from CSV files")
        print("2. Save all customer records to a CSV file")
        print("3. Save all sales records to a CSV file")
        print("4. Add a new customer")
        print("5. Add a new sales record")
        print("6. Search for customers")
        print("7. Search for sales records")
        print("8. Display all sales records for a customer")
        print("9. Delete a sales record")
        print("10. Delete a customer")
        print("11. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            load_data()
        elif choice == '2':
            save_data('customer')
        elif choice == '3':
            save_data('sales')
        elif choice == '4':
            add_customer()
        elif choice == '5':
            add_sales_record()
        elif choice == '6':
            query = input("Enter search query: ")
            results = search_customers(query)
            if results:
                for cust_id, data in results:
                    print(f"ID: {cust_id}, Name: {data['name']}, Postcode: {data['postcode']}, Phone: {data['phone']}")
            else:
                print("No matching customers found.")
        elif choice == '7':
            query = input("Enter search query: ")
            results = search_sales(query)
            if results:
                for sale in results:
                    print(f"Date: {sale['date']}, Transaction ID: {sale['trans_id']}, Customer ID: {sale['cust_id']}, Category: {sale['category']}, Value: {sale['value']}")
            else:
                print("No matching sales records found.")
        elif choice == '8':
            cust_id = int(input("Enter customer ID: "))
            results = display_sales_by_customer(cust_id)
            if results:
                for sale in results:
                    print(f"Date: {sale['date']}, Transaction ID: {sale['trans_id']}, Category: {sale['category']}, Value: {sale['value']}")
            else:
                print("No sales records found for this customer.")
        elif choice == '9':
            trans_id = int(input("Enter transaction ID: "))
            delete_sales_record(trans_id)
            print(f"Sales record with transaction ID {trans_id} deleted.")
        elif choice == '10':
            cust_id = int(input("Enter customer ID: "))
            delete_customer(cust_id)
            print(f"Customer with ID {cust_id} and their sales records deleted.")
        elif choice == '11':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

def load_data():
    global customers, sales
    folder_path = input("Enter the folder path where the CSV files are located: ")
    cust_file = input("Enter the customer records file name (e.g., customers.csv): ")
    sales_file = input("Enter the sales records file name (e.g., sales.csv): ")

    cust_file_path = os.path.join(folder_path, cust_file)
    sales_file_path = os.path.join(folder_path, sales_file)

    try:
        load_customers(cust_file_path)
        load_sales(sales_file_path)
        print("Customer and sales records loaded successfully.")
    except Exception as e:
        print(f"An error occurred while loading the files: {e}")

def save_data(data_type):
    if data_type == 'customer' and not customers:
        print("No customer records in memory.")
        return
    if data_type == 'sales' and not sales:
        print("No sales records in memory.")
        return

    file_path = input(f"Enter the file path to save the {data_type} records: ")
    if os.path.exists(file_path):
        overwrite = input("File exists. Overwrite? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("Operation cancelled.")
            return

    try:
        if data_type == 'customer':
            save_customers(file_path)
        else:
            save_sales(file_path)
        print(f"{data_type.capitalize()} records saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the files: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            load_customers(sys.argv[1])
            load_sales(sys.argv[2])
            print("Customer and sales records loaded from command line arguments.")
        except Exception as e:
            print(f"An error occurred while loading the files from command line: {e}")

    main_menu()

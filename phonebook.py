import psycopg2

# Connection Setup
conn = psycopg2.connect(
    host="localhost",
    database="phonebook2_db",
    user="postgres",
    password="1234"
)
cur = conn.cursor()

# 1. Function: Search by pattern
def search_pattern(pattern):
    cur.execute("SELECT * FROM search_pattern(%s);", (pattern,))
    results = cur.fetchall()
    for row in results:
        print(row)

# 2. Procedure: Insert or update one user
def insert_or_update_user(name, phone):
    cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    conn.commit()
    print("User inserted or updated.")

# 3. Procedure: Insert many users (with validation)
def insert_many_users():
    n = int(input("How many users do you want to insert? "))
    names = []
    phones = []
    for _ in range(n):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        names.append(name)
        phones.append(phone)
    cur.execute("CALL insert_many_users(%s, %s);", (names, phones))
    conn.commit()
    print("Batch insert attempted. Invalid entries were shown in pgAdmin if any.")

# 4. Function: Pagination
def get_paginated():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    cur.execute("SELECT * FROM get_users_paginated(%s, %s);", (limit, offset))
    results = cur.fetchall()
    for row in results:
        print(row)

# 5. Procedure: Delete by name or phone
def delete_by_name_or_phone():
    name = input("Enter name (leave empty if unknown): ")
    phone = input("Enter phone (leave empty if unknown): ")
    cur.execute("CALL delete_by_name_or_phone(%s, %s);", (name, phone))
    conn.commit()
    print("Deleted matching records.")

# Menu loop
def menu():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Search by pattern")
        print("2. Insert or update user")
        print("3. Insert many users with validation")
        print("4. Get users with pagination")
        print("5. Delete by name or phone")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            pattern = input("Enter pattern to search: ")
            search_pattern(pattern)
        elif choice == '2':
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_or_update_user(name, phone)
        elif choice == '3':
            insert_many_users()
        elif choice == '4':
            get_paginated()
        elif choice == '5':
            delete_by_name_or_phone()
        elif choice == '0':
            break
        else:
            print("Invalid option. Try again.")

    cur.close()
    conn.close()
    print("Goodbye!")

# Start the menu
menu()

import sqlite3

def create_database():
    # Connect to the database
    conn = sqlite3.connect('mydatabases.db')
    cursor = conn.cursor()

    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            productname TEXT,
            material TEXT,
            size INTEGER,
            price INTEGER,
            quantity INTEGER,
            color TEXT
        )
    ''')

    # Create Stock table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            id INTEGER PRIMARY KEY,
            fabricname TEXT
        )
    ''')

    # Create FabrickProperty table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FabrickProperty (
            id INTEGER PRIMARY KEY,
            fabricId INTEGER,
            color TEXT,
            numRoll INTEGER,
            date TEXT,
            sizes TEXT,
            FOREIGN KEY (fabricId) REFERENCES Stock(id)
        )
    ''')

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT,
            phone INTEGER
        )
    ''')

    # Create Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            firstname TEXT,
            lastname TEXT,
            email TEXT,
            phone INTEGER,
            gender TEXT
        )
    ''')

    # Create Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    ''')

    # Create Cart table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cart (
            id INTEGER PRIMARY KEY,
            productId INTEGER,
            customerId INTEGER,
            payment TEXT,
            quantity INTEGER,
            date TEXT,
            FOREIGN KEY (productId) REFERENCES Products(id),
            FOREIGN KEY (customerId) REFERENCES Customers(id)
        )
    ''')

    # Create Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Expenses (
            id INTEGER PRIMARY KEY,
            employeeId INTEGER,
            amount INTEGER,
            expensename TEXT,
            date TEXT,
            FOREIGN KEY (employeeId) REFERENCES Employees(id)
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print('Database and tables created successfully.')

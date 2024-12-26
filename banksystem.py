import sqlite3
import os
import time

def start():
    os.system("clear")
    print("Banking system")
    print("1. Log into account\n2. Sign in\n3. Forgot password?\n4. Exit")
    choice = int(input("Enter an option: "))
    match (choice):
        case 1:
            login()
        case 2:
            signin()
        case 3:
            forgot()
        case 4: 
            os.system("clear")
            print("Thank for using this program")
            exit()

def login():
    os.system("clear")
    print("Login system")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM userlist WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    if result:
        os.system("clear")
        print("Login successful")
        time.sleep(2)
        useraccount(username, password)
    else:
        os.system("clear")
        print("Login failed")
        time.sleep(2)
        start()
        


def signin():
    os.system("clear")
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute ( """ 
        CREATE TABLE IF NOT EXISTS userlist(
            username VARCHAR(20) PRIMARY KEY,
            password VARCHAR(50),
            bal DECIMAL(100000000000000,2)
    )
                    """)
    print("Sign in system")
    username = input("Enter your username: ")
    cursor.execute ("SELECT username from userlist WHERE username = ?", (username,))
    result = cursor.fetchone()
    if (result):
        os.system("clear")
        print("Username already exists")
        choice = int(input("1. Main page\n2. Try again\nEnter an option: "))
        match (choice):
            case 1:
                start()
            case 2:
                signin()
    else:
        password = input("Enter your password: ")
        cursor.execute( """
            INSERT INTO userlist(username, password, bal)
            VALUES (?, ?, ?) """, (username, password, 0)
       )

    database.commit()
    database.close()
    
def forgot():
    os.system("clear")
    print("Forgot system")

def useraccount(username, password):
    os.system("clear")
    print("Account: ", username)
    print("1. Deposit\n2. Withdraw\n3. Check balance\n4. Logout")
    choice = int(input("Enter an option: "))
    match (choice):
        case 1:
            deposit(username)
        case 2:
            withdraw(username)
        case 3:
            checkbalance(username)
        case 4:
            start()

def deposit(username):
    amt = int(input("Enter amount to deposit: "))
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT bal FROM userlist WHERE username = ?",(username,))
    result = cursor.fetchone()
    curbal = result[0]
    newbal = curbal + amt
    cursor.execute("UPDATE userlist SET bal = ? WHERE username = ?" , (newbal, username))
    print("Successfully depositted RM", amt)
    database.commit()
    database.close()

def withdraw(username):
    amt = int(input("Enter amount to withdraw: "))
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT bal FROM userlist WHERE username = ?",(username,))
    result = cursor.fetchone()
    curbal = result[0]
    if (curbal < amt):
        print("You dont have enough money to withdraw: ")
        start()
    else:
        newbal = curbal - amt
        cursor.execute("UPDATE userlist SET bal = ? WHERE username = ?" , (newbal, username))
        print("Successfully withdraw RM", amt)
        database.commit()
        database.close()
def checkbalance(username):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute ("SELECT bal FROM userlist WHERE username = ?", (username,))
    result = cursor.fetchone()
    curbal = result[0]
    print("Current balance: RM", curbal)

start()

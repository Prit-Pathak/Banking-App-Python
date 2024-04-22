from bankAccount import *
from debitCard import *
import pyodbc
from pyodbc import *
from flask import *
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

bankAccounts = []
validate_user_choice_flag = True

def validate_user_choice():
    if invalid_choice:
        print("We're sorry but you have run out of attempts to access our online banking system for the next hour. Please try again later.")
    else:
        if user_choice == 1:
            print("Great, let's go ahead and deposit your money. Please enter your debit card number first so we can find your account.") 
            card_number_entry = input()
            message = "There is no account registered with this card. Please contact customer service for further assistance. Good bye!"
            for i in bankAccounts:
                if i.debitCardNumber == card_number_entry:
                    message = "We found your account!"
                    print(message)
                    print("Please enter in the amount you'd like to deposit in this transaction. Remember, the deposit limit is $200 per transaction.")
                    depositAmount = int(input())
                    i.depositMoney(depositAmount)
                    break
            if message != "We found your account!":
                print(message)
        elif user_choice == 2:
            print("Alright, let's withdraw money from your account. Please enter your debit card number first so we can find your account.")
            card_number_entry = input()
            message = "There is no account registered with this card. Please contact customer service for further assistance. Good bye!"
            for i in bankAccounts:
                if i.debitCardNumber == card_number_entry:
                    message = "We found your account!"
                    print(message)
                    print("Please enter in the amount you'd like to withdraw in this transaction. Remember, the withdrawal limit is $100 per transaction.")
                    withdrawalAmount = int(input())
                    i.withdrawMoney(withdrawalAmount)
                    break
            if message != "We found your account!":
                print(message)
        elif user_choice == 3:
            print("Ok, so you want to know your account balance. Please enter your debit card number first so we can find your account.")
            card_number_entry = input()
            message = "There is no account registered with this card. Please contact customer service for further assistance. Good bye!"
            for i in bankAccounts:
                if i.debitCardNumber == card_number_entry:
                    message = "We found your account!"
                    print(message)
                    i.checkAccountBalance()
                    break
            if message != "We found your account!":
                print(message)
        elif user_choice == 4:
            print("A new customer, welcome!!\n Please enter the following details one by one so we can set up your account in our system.")
            account = bankAccount()
            account.createAccount()
            bankAccounts.append(account)
        elif user_choice == 5:
            print("Let's show you your most recent transactions to help you keep account of your saving tendencies. Please enter your debit card number first so we can find your account.")
            card_number_entry = input()
            message = "There is no account registered with this card. Please contact customer service for further assistance. Good bye!"
            for i in bankAccounts:
                if i.debitCardNumber == card_number_entry:
                    message = "We found your account!"
                    print(message)
                    print(i.transactions)
                    break
            if message != "We found your account!":
                print(message)
        elif user_choice == 6:
            print("Oh, you've asked for customer support, so here are some details to help you get started on the process of reaching our banking representatives via chat or phone.\n")
            print("Online Banking Customer Service Hours: 8:00 AM - 8:00 PM EST\n\nContact Number: 567-890-1234\n\nTo Chat With Our Representatives: www.chat-with-online-banking-reps.com\n\n")
            print("We hope we've been able to be of service to you today! Thank you for using our system!")

def loadSecrets():
    keyVaultName = "madhu-test-vault-v1"
    key_vault_url = f"https://{keyVaultName}.vault.azure.net/"
    load_dotenv("variables.env")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    secretName = "Test-server-password"
    db_server_password = client.get_secret(secretName).value
    return db_server_password
def create_table():
    db_server_password = loadSecrets()
    with pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:banking-records-v1.database.windows.net,1433;Database=banking_records_v1;Encrypt=yes;Uid=test;Pwd=' + db_server_password) as connection_object:
        with connection_object.cursor() as cursor:
            cursor.execute("IF  NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[banking_transaction_records]') AND type in (N'U')) CREATE TABLE banking_transaction_records(Customer_Name varchar(50), Date varchar(25), Type varchar(50), Amount varchar(25))")
# Connect to SQL function
def connect_to_sql():
    db_server_password = loadSecrets()
    with pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:banking-records-v1.database.windows.net,1433;Database=banking_records_v1;Encrypt=yes;Uid=test;Pwd=' + db_server_password) as connection_object:
        with connection_object.cursor() as cursor:
            for i in bankAccounts:
                customer_name = i.accountHolderName
                for j in i.transactions_data:
                    transaction_date = j[0]
                    transaction_type = j[1]
                    transaction_amount = j[2]
                    cursor.execute("INSERT INTO [dbo].[banking_transaction_records](Customer_Name, Date, Type, Amount) VALUES ('" + customer_name + "', '" + transaction_date + "', '" + transaction_type + "', '" + transaction_amount + "')")


create_table()
while validate_user_choice_flag:
    print("Welcome to our online banking system. Please choose from the following menu options so we can better assist you. \n 1) Deposit Money \n 2) Withdraw Money \n 3) Retrieve My Account Balance \n 4) I Am A New Customer \n 5) Show Me My Recent Transactions\n 6) Customer Support\n")
    count = 0
    user_choice = int(input())
    invalid_choice = True
    while count < 3:
        if user_choice not in [1, 2, 3, 4, 5, 6]:
            print("You entered an invalid option. Please try again.")
            user_choice = int(input())
            count += 1
        else:
            if user_choice == 6:
                validate_user_choice_flag = False
            invalid_choice = False
            break
    validate_user_choice()

connect_to_sql()

# Here the tangible objects are a bank account, a customer, and possibly a credit card.
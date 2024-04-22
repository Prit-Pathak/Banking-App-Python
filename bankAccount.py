import regex as re
from random import randint
from debitCard import *
from datetime import date
class bankAccount:
    accountNumber = 'xxxxxxxx'
    accountHolderName = ''
    accountBalance = 0
    address = ''
    salary = ''
    debitCardNumber = ""
    debitCardExpiryDate = ""
    debitCardCVV = ""
    transactions = []
    transactions_data = []
    exit_GUI_flag = False
    def createAccount(self):
        name = input("Your name: ")
        ssn = input("Your Social Security Number: ")
        address = input("Your street address: ")
        salary = input("Your annual salary: ")
        self.transactions = []
        self.transactions_data = []
        if len(ssn) != 11:
            print("You've not provided a valid social security number. Exiting the application....")
            self.exit_GUI_flag = True
        else:
            ssn_search = re.compile(r'(\d\d\d-\d\d-\d\d\d\d)*')
            mo = ssn_search.search(ssn)
            print(mo.group())
            if mo.group() == '':
                print("You've not provided a valid social security number. Exiting the application....")
                self.exit_GUI_flag = True
        if self.exit_GUI_flag == False:
            print("Thank you for providing your details. We have been able to generate an account for you based off of your credentials.")
            self.accountHolderName = name
            self.accountNumber = str(randint(10000000, 99999999))
            self.address = address
            self.salary = salary
            self.accountBalance = 0
            print("Your account number is " + self.accountNumber + ". You will now be provisioned a debit card that is associated with this account.")
            newDebitCard = debitCard(self.accountHolderName)
            newDebitCard.printCardDetails()
            self.debitCardNumber = newDebitCard.cardNumber
            self.debitCardExpiryDate = newDebitCard.cardExpiryDate
            self.debitCardCVV = newDebitCard.cardCVV
            self.transactions.append("Date: " + str(date.today()) + ", Type: Created New Account" + ", Amount: $0")
            self.transactions_data.append([str(date.today()), "Created New Account", "0"])
    def depositMoney(self, amount_to_deposit):
        if amount_to_deposit > 200:
            print("That is more than the allowed deposit amount per transaction. Please try again later. Exiting the application...")
        else:
            self.accountBalance += amount_to_deposit
            print("You have deposited $" + str(amount_to_deposit) + " into your account. Thank you for using our system!" )
            self.transactions.append("Date: " + str(date.today()) + ", Type: Deposited Money" + ", Amount: $" + str(amount_to_deposit))
            self.transactions_data.append([str(date.today()), "Deposited Money", str(amount_to_deposit)])
        self.exit_GUI_flag = True
    def withdrawMoney(self, amount_to_withdraw):
        if amount_to_withdraw > 100:
            print("That is more than the allowed withdrawal amount per transaction. Please try again later. Exiting the application...")
        else:
            if (self.accountBalance >= amount_to_withdraw):
                self.accountBalance -= amount_to_withdraw
                print("You have withdrawn $" + str(amount_to_withdraw) + " from your account. Thank you for using our system!")
                self.transactions.append("Date: " + str(date.today()) + ", Type: Withdrew Money" + ", Amount: $" + str(amount_to_withdraw))
                self.transactions_data.append([str(date.today()), "Withdrew Money", str(amount_to_withdraw)])
            else:
                print("You are attempting to withdraw more than your account's current balance. Please try again later. Exiting the application...")
    def checkAccountBalance(self):
        amount_involved = 0
        print("You have a current account balance of $" + str(self.accountBalance))
        self.transactions.append("Date: " + str(date.today()) + ", Type: Checked Account Balance" + ", Amount: $0")
        self.transactions_data.append([str(date.today()), "Checked Account Balance", "0"])

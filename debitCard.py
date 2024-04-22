from random import randint
from datetime import date
from bankAccount import *
class debitCard:
    cardNumber = ''
    cardHolderName = ''
    cardCVV = ''
    cardExpiryDate = ''
    def __init__(self, customerName):
        self.cardHolderName = customerName
        self.cardNumber = str(randint(1000,9999)) + str(randint(1000,9999)) + str(randint(1000,9999)) + str(randint(1000,9999))
        self.cardCVV = str(randint(100, 999))
        current_date = str(date.today())
        current_month = current_date.split('-')[1]
        current_year = current_date.split('-')[0]
        self.cardExpiryDate = current_month + "/" + str(int(current_year) + 5)
        print("Your debit card has now been created and entered into the system. You will receive the physical card via mail in the next two weeks.")
    def printCardDetails(self):
        print("Your card number is " + self.cardNumber + " and your CVV and card expiry date are respectively " + self.cardCVV + " and " + self.cardExpiryDate)
        
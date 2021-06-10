from datetime import date, timedelta
from textwrap import dedent

class Person:
    def __init__(self, name, percent, bank, rent, auto_loan,
                 auto_in, cable, phone, card,
                 util, renter_in):
        
        self.name = name
        self.balance = 1391.09
        self.savings = 0
        self.score = 2486.74
        self.due = []
        self.paid = []
        self.checks_pending = []
        self.payments_pending = []
        self.job = Job(int(percent))
        self.bank = bank
        self.rent = rent 
        self.auto_loan = auto_loan
        self.auto_in = auto_in
        self.cable = cable 
        self.phone = phone 
        self.card = card
        self.util = util 
        self.renter_in = renter_in
        self.student_loan = Vendor('student loan', 
                                   265.78,
                                   timedelta(days=30),
                                   date(2021, 3, 21),
                                   0,
                                   timedelta(days=8),
                                   50,
                                   30)

        # used to check when vendors will charge the person
        self.vendors = [self.rent, self.auto_loan, self.auto_in, self.cable,
                        self.phone, self.util, self.renter_in, self.student_loan]

    # given a day, it will return if in that day there will be any charges by the vendors inside person.vendors
    # should return a list of all the charges as Charge objects
    # Job used to be a charge, but I created a new function to check when the person gets paid
    def check_charges(self, today):
        charges = []
        for vendor in self.vendors:
            since_first_day = today-vendor.first_day
            
            # this is an exception to the rent vendor because on the first day of the simulation, even though it isnt the first_day, first_charge is charged
            if today == date(2021, 3, 4):
                if vendor.name == 'rent 1' or vendor.name == 'rent 2':
                    charges.append(Charge(vendor.name, vendor.first_charge, today+timedelta(days=7), None))

            if since_first_day < timedelta(days=0):
                pass

            # instead of checking if date is greater than vendor.first_day, just cehck if since_first_day is negative
            # if the vendor has a frequency of monthly
            elif vendor.freq == timedelta(days=30):
                # check if today's date is greater than vendor.first_day and if today's date is the same day as vendor.first_day.day
                # doing this because not every month has 30 days
                if today >= vendor.first_day and today.day == vendor.first_day.day:
                    charges.append(Charge(vendor.name,
                                         (vendor.amount if today != vendor.first_day or vendor.name == 'card' or 'rent' in vendor.name else vendor.amount + vendor.first_charge),
                                          today+vendor.due,
                                          None))

            # if vendor has a frequency of semianually
            elif vendor.freq == timedelta(days=183):
                # check if today's date is greater than vendors.first_day, if todays date is the same day as vendors.first_day, and if today's month minus vendors.first_day month is a multiple of 6
                if today >= vendor.first_day and today.day == vendor.first_day.day and today.month-vendor.first_day.month%6 == 0:
                    charges.append(Charge(vendor.name,
                                         (vendor.amount if today != vendor.first_day else vendor.amount + vendor.first_charge),
                                          today+vendor.due,
                                          None))

            # if vendor has a frequency of anually
            elif vendor.freq == timedelta(days=365):
                # check if todays date day and month are the same as vendorst.first_day day and month
                if today.day == vendor.first_day.day and today.month == vendor.first_day.month:
                    charges.append(Charge(vendor.name, vendor.amount, today+vendor.due, None))

            elif since_first_day%vendor.freq == timedelta(days=0):
                charges.append(Charge(vendor.name,
                                     (vendor.amount if today != vendor.first_day else vendor.amount + vendor.first_charge),
                                      today+vendor.due,
                                      None))

        return charges

    # given a day, it will check if the person will be payed that day
    def check_payment(self, today):
        since_first_day = today-self.job.first_day
        if since_first_day%self.job.freq == timedelta(days=0):
            return Payment(self.job.amount, today)

    # only runs when the person opens the program at first
    # will loop through all days since the beginning till today and check the charges received
        # the function compares the charges with charges already paid
        # the function compares the charges with pending checks
    def check_past_charges(self):
        start = date(year=2021, month=3, day=4)
        end = date.today()
        delta = timedelta(days=1)

        while start <= end:
            charges = self.check_charges(start)
            for charge in charges:
                charge_paid = False
                for paid in self.paid:
                    if charge.name == paid.name and charge.due == paid.due:
                        charge_paid = True
                
                for check_pending in self.checks_pending:
                    if charge.name == check_pending.paid_for and charge.due == check_pending.due:
                        charge_paid = True
                        self.payments_pending.append(charge)

                if not charge_paid:
                    self.due.append(charge)

            start += delta

    # I could first ask who is the check for and then check if it matches the vendor
    # might be too extra
    # this function requires the today paremeter because when I am creating a person, I have to assume that todays date is the first day of the simulation
    # for this function to function normally, do not enter anything for "today"
    def write_check(self, today=date.today()):
        while True:
            due = input('Due date of the bill\nmm/dd/yyyy e.g. 03/04/2021\n>>> ')
            post_date = input('Check post date\nmm/dd/yyyy e.g. 03/04/2021\n>>> ')
            check_amount = input('Check amount:\n>>> $')
            paid_for = input('Check is for\nCheck can be for: rent, auto loan, auto ins, cable, phone, card, utilities, renter ins, student loan\n>>> ')
            print('To confirm your information is correct, re-type it')
            due_2 = input('Due date of the bill\nmm/dd/yyyy e.g. 03/04/2021\n>>> ')
            post_date2 = input('Check post date\nmm/dd/yyyy e.g. 03/04/2021\n>>> ')
            check_amount2 = input('Check amount:\n>>> $')
            paid_for2 = input('Check is for\n>>> ')

            if due != due_2:
                print('The due date did not match, try again')
                continue

            elif post_date != post_date2:
                print('Your post dates did not match, try again')
                continue

            elif check_amount != check_amount2:
                print('Your check amount did not match, try again')
                continue

            elif paid_for != paid_for2:
                print('Your check recipient did not match, try again')
                continue

            else:
                print('The information is correct')
                
                due = due.split('/')
                due = date(year=int(due[2]), month=int(due[0]), day=int(due[1]))
                # converting all the inputs to the correct format I need them in
                post_date = post_date.split('/')
                post_date = date(year=int(post_date[2]), month=int(post_date[0]), day=int(post_date[1]))
                # check if post_date is valid
                if post_date < today+timedelta(days=2):
                    print(f'You cannot write a check for the {post_date}, must be at least two days after today')
                    continue

                check_amount = float(check_amount) + self.bank.per_check
                # getting the actual vendor name given the name inputted by the user 
                for vendor in self.vendors:
                    if paid_for in vendor.name:
                        paid_for = vendor.name

                break

        # create a loop from today to the day that the check will be posted and see if the person will have enough money by that day
        start = today
        end = post_date
        delta = timedelta(days=1)
        future_balance = self.balance

        while start <= end:
            payment = self.check_payment(start)
            if payment:
                future_balance += payment.amount
            
            start += delta

        if future_balance < check_amount:
            print(f'You will not have enough money by the {post_date} to pay ${check_amount} to {paid_for}')

        # the person can write a check, so I have to add that to the pending checks
        # All i have to do is add this to the list of Person.checks_pending and when the program closes it will write to the file
        else:
            self.checks_pending.append(Check(paid_for, check_amount, due, post_date))
            # since I just wrote a check, I wanna make sure that it is taken in consideration when determining what is actually due now
            for charge in self.due:
                if charge.name == paid_for and charge.due == due:
                    self.due.remove(charge)

    def add_to_balance(self):
        while True:
            amount = input('Enter how much should be added to your checkings\n>>> ')
            print('Enter that same amount again to confirm')
            amount_2 = input('Enter how much should be added to your checkings again\n>>> ')

            try:
                amount = float(amount)
                amount_2 = float(amount)

            except Exception:
                print('That is not a valid amount, try again')

            if amount != amount_2:
                print('The amount did not match, try again')

            else:
                self.balance += amount
                print('Balance updated succesfully')
                break

    def transfer_to_savings(self):
        while True:
            amount = input("Enter the amount to transfer\n>>> $")
            amount_2 = input("Confirm the amount\n>>> $")

            try:
                amount = float(amount)
                amount_2 = float(amount_2)

            except Exception:
                print('That is not a valid amount')
                continue
            
            if amount != amount_2:
                print('The amount did not match')
                continue

            elif amount > self.balance:
                print(f'You do not have ${amount} to transfer')
                continue

            break

        self.balance -= amount
        self.savings += amount
        print('Transfer made succesfully')        

    def __str__(self):
        result = dedent(f"""
                         Checking Balance: {self.balance}
                         Savings Balance: {self.savings}
                         401k Score: {self.score}
                         401k Percent: {self.job.percent}% or ${self.job.saved}
                         Credit Card Usage: {self.card.amount}

                         Due:
                         {'-'*15}""")

        for due_charge in self.due:
            result += '\n' + str(due_charge)

        #result += f'\n\nPaid\n{"-"*15}'
        #for paid_charge in self.paid:
        #    result += '\n' + str(paid_charge)

        result += f'\nChecks Pending\n{"-"*15}'
        for check_pending in self.checks_pending:
            result += '\n' + str(check_pending)

        return result

# taxes breakdown
# Federal: 142.57-(401k*1.93)
# Soc Sec: 96.59
# Medicare: 22.59
# State: 38.92
# State: 38.92
# Health Ins: 50.04
# 401k Contribution: 1608*(percent/100)
# The person also gets a 100% match up to 5% on 401k
class Job:
    def __init__(self, percent):
        self.percent = percent
        self.amount = 1608-1608*(percent/100)-(142.57-percent*1.93)-96.59-22.59-38.92-50.04
        # on top of saving the percentage I contribute, my employer always contributes 5 percent
        self.saved = 1608*(percent/100)+1608*(5/100)
        self.freq = timedelta(days=14)
        self.first_day = date(2021, 3, 11)
        self.name = 'job'

    def update_percent(self):
        while True:
            percent = input('Enter the percentage\n>>> ')
            print('To confirm, re-enter the same percentage')
            percent_2 = input('Enter the percentage again\n>>> ')
            
            try:
                percent = int(percent)
                percent_2 = int(percent_2)

            except Exception:
                print('That is not a valid percentage, try again')
                continue

            if percent != percent_2:
                print('The percentage did not match, try again')
                continue

            elif percent < 5 or percent > 42:
                print('Your percentage should not be less than 5% or more than 42%, try again')
                continue

            else:
                self.percent = percent
                self.amount = 1608-1608*(percent/100)-(142.57-percent*1.93)-96.59-22.59-38.92-50.04
                self.saved = 1608*(percent/100)+1608*(5/100)
                print('Percentage changed successfully')
                break

class Card:
    def __init__(self, freq, first_day, due, late, minimum_payment,
                 limit, minimum_finance, interest, over_credit, bounce):
        
        self.amount = 0
        self.freq = freq
        self.first_day = first_day
        self.due = due
        self.late = late
        self.minimum_payment = minimum_payment
        self.limit = limit
        self.minimum_finance = minimum_finance
        self.interest = interest
        self.over_credit = over_credit
        self.bounce = bounce
        self.name = 'card'

    def update_usage(self):
        while True:
            amount = input('Enter usage amount\n>>> $')
            print('To confirm, enter the same amount')
            amount_2 = input('Enter usage amount again\n>>> $')

            try:
                amount = float(amount)
                amount_2 = float(amount_2)
    
            except Exception:
                print('That is not a valid amount, try again')
                continue

            if amount != amount_2:
                print('Amount did not match, try again')
                continue

            self.amount += amount
            print('Usage was entered succesfully')
            break 

class Bank:
    def __init__(self, unsufficient, over_draft, over_draft_per_use,
                 per_check, minimum, below_minimum, negative, interest):

        self.unsufficient = unsufficient
        self.over_draft = over_draft
        self.over_draft_per_use = over_draft_per_use
        self.per_check = per_check
        self.minimum = minimum
        self.below_minimum = below_minimum
        self.negative = negative
        self.interest = interest
        self.statement = timedelta(days=17)
        self.name = 'bank'

# most vendors have "interest"
class Vendor:
    def __init__(self, name, amount, freq, first_day, first_charge, due, late, bounce):
        self.name = name
        self.amount = amount
        self.freq = freq
        self.first_day = first_day
        self.first_charge = first_charge
        self.due = due
        self.late = late
        self.bounce = bounce

class Charge:
    def __init__(self, name, amount, due, date_paid):
        self.name = name
        self.amount = amount
        # due will not be a timedelta object, it will be a date
        # that date is equal to the date the charge was issued plus the due period
        self.due = due
        self.date_paid = date_paid

    def __str__(self):
        if self.date_paid:
            return f'For: {self.name} Amount: {self.amount} Due by: {self.due} Paid on: {self.date_paid}'

        else:
            return f'For: {self.name} Amount: {self.amount} Due by: {self.due}'

# I craeted this objeect because the Job payments used to be a charge object
# But i decided to separate them
# This payment object will be used to display events to the user
# It will also be used to check
class Payment:
    def __init__(self, amount, date_received):
        self.amount = amount
        self.date_received = date_received

    def __str__(self):
        # I am not sure if I should include the date_received when printing it
        # When I do print this, I will be printing it on the main file with the main function, so the day will already be there
        info = f'Job Payment Amount: {self.amount}'
        width = len(info)+2
        result = dedent(f"""
                        +{'-'*width}+
                        |{info:^{width}}|
                        +{'-'*width}+
                        """)

        return result

class CardStatement:
    def __init__(self, person, due):
        pass

    def __str__(self):
        pass

class Check:
    def __init__(self, paid_for, amount, due, post_date):
        self.paid_for = paid_for
        self.amount = amount
        # due stands for the day the charge for which the check was written is due
        self.due = due
        self.post_date = post_date

    def __str__(self):
        return f'For: {self.paid_for} Amount: {self.amount} Post Date: {self.post_date}'
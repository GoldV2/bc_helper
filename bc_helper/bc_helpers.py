from datetime import time, timedelta
from bc_objects import *
from bc_options import *

nl = '\n'
vendor_names = ['bank', 'rent', 'auto loan', 'auto ins', 'cable', 'phone', 'credit card', 'utility', 'renter ins']
vendors = [banks, rents, auto_loans, auto_ins, cables, phones, cards, utils, renter_ins]

def readline(file):
    return file.readline().strip('\n')

def create_person():
    # asks for user name and options picked
    name = input('Enter your name\n>>> ')
    while True:
        try:
            parameters = [name]
            selections = []

            # the 401k percentage cant be combined with the others because it would make the lists vendor_names and vendors
            # have different lengths
            percentage = input('Enter your initial 401k percentage\n>>> ')
            parameters.append(percentage)
            selections.append(percentage)

            for vendor_name, vendor in zip(vendor_names, vendors):
                selection = input(f'Enter your {vendor_name} option\n>>> ')
                parameters.append(vendor[selection])
                selections.append(selection)

            person = Person(*parameters)
            break

        except Exception:
            print('You entered an invalid option, try again')

    # asking for credit card usage and how much they have transfered to savings
    while True:
        usage = input('Enter your current credit card usage\n>>> $')
        savings = input('Enter how much you have transferred to your savings\n>>> $')
        print('Re-enter the same amounts to confirm')
        usage_2 = input('Enter your current credit card usage again\n>>> $')
        savings_2 = input('Enter how much you have transferred to your savings again\n>>> $')

        try:
            usage = float(usage)
            usage_2 = float(usage_2)
            savings = float(savings)
            savings_2 = float(savings_2)
        
        except Exception:
            print('Your input is invalid, try again')
        
        if usage != usage_2:
            print('Credit card usage did not match, try again')

        elif savings != savings_2:
            print('Savings amount did not match, try again')

        else:
            person.card.amount = usage
            person.savings = savings
            person.balance -= savings
            break

    # asking the person to enter every single check they have written so far
    print('Enter all checks you have written')
    while True:
        again = input('Enter "1" to write a check, enter "0" to stop writing checks\n>>> ')

        if again == '0':
            break
        
        elif again == '1':
            person.write_check(today=date(year=2021, month=3, day=4))

        else:
            print('Your answer is not valid, try again')

    # starts creating the file. The file design can be found above the analyze_file() function
    filename = f'Projects/bc_helper/bc_helper/{name.lower()}_bc.txt'
    file = open(filename, 'w')

    for selection in selections:
        file.write(selection + ', ')

    file.write(str(person.balance) + ', ')
    file.write(str(person.savings) + ', ')
    file.write(str(person.score) + ', ')
    file.write(str(person.card.amount) + ', ')

    # creating the section for payment made, checks due, and last visit
    file.write(', ')
    file.write(', ')
    file.write(str(date(year=2021, month=3, day=4)))

    file.close()

    return person

# analyzes text file to gather past information about the person
# file design
    # 1: 401k percent, bank, rent, auto loan, auto ins, cable, phone, credit card, utility, renter ins,
    # 1: checkings balance, savings balance, 401K score, credit card usage, "payments made" name,amount,due,date_paid/name,amount,due,date_paid, "checks pending" paid for,amount,due,post_date, last visit
def analyze_file(name=''):
    if not name:
        name = input('Enter your name\n>>> ')
    filename = f'Projects/bc_helper/bc_helper/{name.lower()}_bc.txt'
    file = open(filename, 'r+')

    options = file.readline().split(', ')

    person = Person(name,
                    int(options[0]),
                    banks[options[1]],
                    rents[options[2]],
                    auto_loans[options[3]],
                    auto_ins[options[4]],
                    cables[options[5]],
                    phones[options[6]],
                    cards[options[7]],
                    utils[options[8]],
                    renter_ins[options[9]])

    person.balance = float(options[10])
    person.savings = float(options[11])
    person.score = float(options[12])
    person.card.amount = float(options[13])

    # the 14 item will have the made payments, and they have the format name,amount,due_date,date_paid and are separated by a /
    # converting the text to a Charge object
    paids = options[14].split('/')
    if paids != ['']:
        for paid in paids:
            paid = paid.split(',')
            date_due = list(map(int, paid[2].split('-')))
            date_paid = list(map(int, paid[3].split('-')))
            person.paid.append(Charge(paid[0], float(paid[1]),
                                      date(year=date_due[0], month=date_due[1], day=date_due[2]),
                                      date(year=date_paid[0], month=date_paid[1], day=date_paid[2]),))

    # the 15 item will have the pending checks, and they have the format paid_for,amount,due,post_date and are separated by a /
    # converting the text to a Check object
    # due stands for the day the charge which the check was written to is due
    checks_pending = options[15].split('/')
    if checks_pending != ['']:
        for check in checks_pending:
            check = check.split(',')
            due = list(map(int, check[2].split('-')))
            post_date = list(map(int, check[3].split('-')))
            person.checks_pending.append(Check(check[0], float(check[1]),
                                               date(year=due[0], month=due[1], day=due[2]),
                                               date(year=post_date[0], month=post_date[1], day=post_date[2])))

    last_visit = list(map(int, options[16].split('-')))
    last_visit = date(year=last_visit[0], month=last_visit[1], day=last_visit[2])

    if last_visit <= date.today():
        validate(person, last_visit)

    # this function will compare the charges received up to today with charges paid and pending checks
    person.check_past_charges()

    file.close()

    return person

# this function will loop from the day the person last visited up to today and validate any new payments
# or if any pending check they had has been paid off
# this function will not check for new charges because there is a function that does that already Person.check_past_charges
def validate(person, last_visit):
    start = last_visit
    end = date.today()
    delta = timedelta(days=1)

    while start < end:
        payment = person.check_payment(start)
        if payment:
            person.balance += payment.amount
            person.score += person.job.saved

        for check in person.checks_pending:
            if check.post_date == start:
                person.balance -= check.amount
                if 'card' in check.paid_for:
                    # I have to subtract the per_check because that fee is not removed from my credit card usage
                    person.card.amount -= check.amount-person.bank.per_check
                person.paid.append(Charge(check.paid_for, check.amount, check.due, check.post_date))
                person.checks_pending.remove(check)

        start += delta

def update_file(person):
    filename = 'Projects/bc_helper/bc_helper/' + person.name + '_bc.txt'
    file = open(filename, 'r+')
    information = file.readline().split(', ')

    information[0] = str(person.job.percent)
    information[10] = str(round(person.balance, 2))
    information[11] = str(round(person.savings, 2))
    information[12] = str(round(person.score, 2))
    information[13] = str(round(person.card.amount, 2))
    information[14] = ''
    for charge in person.paid:
        information[14] += f'{charge.name},{charge.amount},{charge.due},{charge.date_paid}/'
    # I need to remove the last character because it will be a / and i cant have it there
    information[14] = information[14][:-1]

    information[15] = ''
    for check_pending in person.checks_pending:
        information[15] += f'{check_pending.paid_for},{check_pending.amount},{check_pending.due},{check_pending.post_date}/'
    information[15] = information[15][:-1]

    information[16] = str(date.today())

    file.truncate(0)
    # I have to go back to the first byte else, the file is gonna be filled with NULL characters after writing
    file.seek(0)
    file.write(', '.join(information))
    file.close()

def predict(person):
    ahead = int(input('How many days ahead to predict?\n>>> '))
    today = date.today()
    end_date = today+timedelta(days=ahead)
    delta = timedelta(days=1)

    calendar = []
    while today <= end_date:
        charges = person.check_charges(today)
        payment = person.check_payment(today)

        day = [today]

        # only append if there is a payment
        if payment:
            day.append(payment)

        for charge in charges:
            # day will be a list where the first item is the day, and the rest are charges for that day
            day.append(charge)

        # only append if there is an event that date
        if len(day) > 1:
            calendar.append(day)
        
        today += delta

    return calendar

def help_budget(person):
    ahead = int(input('Enter how many payments ahead you would like to budget\n>>> '))

    # first I need to find all charges the person has received at most 11 days before
    # 11 days because that is the longest due period
    start = date.today()-timedelta(days=30)
    delta = timedelta(days=1)
    # i need this variable because if the person inputs multiple weeks I want to keep track
    # of the predicted_balance for all weeks
    predicted_balance = person.balance
    for i in range(ahead):
        all_charges = []
        while True:
            daily_charges = person.check_charges(start)
            all_charges += daily_charges

            payment = person.check_payment(start)
            if payment and payment.date_received > date.today():
                total_due = 0
                width = len(f'Period between {payment.date_received} and {payment.date_received+timedelta(days=14)}')+2
                print(dedent(f"""
                             +{width*'-'}+
                             |{f'Period between {payment.date_received} and {payment.date_received+timedelta(days=14)}':^{width}}|
                             +{width*'-'}+
                             """))

                for charge in all_charges:
                    # In this if statement I have to somehow check the charges that I have right now and include them in my calculation
                    # I also have to check if that charge isn't already gonna be charged normally 
                    if payment.date_received <= charge.due and charge.due <= payment.date_received + timedelta(days=14):
                        total_due += charge.amount
                        print(charge)

                predicted_balance += payment.amount - total_due
                print(f'Total money due: ${total_due} Predicted balance: {predicted_balance}')
                start += delta
                break

            start += delta

# probably wont use
def create_file(calendar):
    user = os.path.expanduser('~')
    filename = f'{user}\\Desktop\\Budget Challenge.xls'
    file = open(filename, 'w')
    for day in calendar:
        for item in day:
            file.write(str(item) + '\t')

        file.write('\n')

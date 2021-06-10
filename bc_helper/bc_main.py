from bc_objects import *
from bc_options import *
from bc_helpers import *
from os import system

def start():
    while True:
        choice = input('Enter "0" to register. Enter "1" if already registered\n>>> ')

        if choice == '0':
            person = create_person()

            # after creating a person and sending them to the main menu
            # I want to make sure that they see the correct and most current info
            update_file(person)
            person = analyze_file(name=person.name)


        elif choice == '1':
            person = analyze_file()

        else:
            print('Not a valid input. Try again')
            continue

        break

    try:
        while True:
            main(person)
    
    finally:
        update_file(person)

def main(person):
    print('\n1: View information',
          '\n2: View future events',
          '\n3: Budget future payments',
          '\n4: Write Check',
          '\n5: Input credit card usage',
          '\n6: Update 401k percentage',
          '\n7: Transfer funds to savings',
          '\n8: Add money to checkings',
          '\n0: Exit')

    choice = input('>>> ')
    system('cls')

    if choice == '0':
        exit()

    elif choice == '1':
        print(person)

    elif choice == '2':
        calendar = predict(person)

        for day in calendar:
            # if the date isnt today, print that date, but if it is today, print 'Today'
            print(str(day[0]) if day[0] != date.today() else 'Today')
            print(15*"-")
            for event in day[1:]:
                print(event)
                
            print()

    elif choice == '3':
        help_budget(person)

    elif choice == '4':
        person.write_check()

    elif choice == '5':
        person.card.update_usage()

    elif choice == '6':
        person.job.update_percent()

    elif choice == '7':
        person.transfer_to_savings()
    
    elif choice == '8':
        person.add_to_balance()

start()

# add a way to check credit card statements
# for my account, i need to change my 401k score
# the program is updating the person's payments and checking their charges
# for new users
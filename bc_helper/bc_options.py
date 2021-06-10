from bc_objects import *

# the due attribute does not include grace periods
# coding all the options
percents = range(5, 43)

banks = {'1': Bank(39.95, 0, 0, 0.5, 0, 0, 3, 0),
         '2': Bank(39.95, 3.95, 10, 0.5, 0, 0, 3, 0),
         '3': Bank(39.95, 0, 10, 0, 250, 9.95, 3, 0),
         '4': Bank(39.95, 0, 10, 0, 400, 9.95, 3, 2)}

# rents have a "daily fee for negative balance"
rents = {'1': Vendor('rent 1', 600, timedelta(days=30), date(2021, 4, 1), 941.94, timedelta(days=7), 25, 30),
         '2': Vendor('rent 2', 500, timedelta(days=30), date(2021, 4, 1), 1001.61, timedelta(days=7), 25, 30)}

# auto loans have a "interest rate" and "term length" (doesn't matter)
auto_loans = {'1': Vendor('auto loan 1', 360.48, timedelta(days=30), date(2021, 3, 15), 25, timedelta(days=8), 360.48*0.1, 30),
              '2': Vendor('auto loan 2', 369.44, timedelta(days=30), date(2021, 3, 15), 0,timedelta(days=8), 369.44*0.1, 30)}

# frequency is semianually (don't know how many days exactly)
# auto_ins have a "insurance deductible"
auto_ins = {'1': Vendor('auto ins 1', 645.59, timedelta(days=183), date(2021, 4, 29), 0, timedelta(days=10), 24.95, 30),
            '2': Vendor('auto ins 2', 618.59, timedelta(days=183), date(2021, 4, 29), 0, timedelta(days=10), 24.95, 30)}

# cables have a "monthly set-top box insurance"
cables = {'1': Vendor('cable 1',49.5, timedelta(days=30), date(2021, 3, 18), 0, timedelta(days=10), 9.95, 30),
          '2': Vendor('cable 2',53.2, timedelta(days=30), date(2021, 3, 18), 0, timedelta(days=10), 9.95, 30)}

phones = {'1': Vendor('phone 1', 75, timedelta(days=30), date(2021, 3, 8), 50, timedelta(days=9), 10, 30),
          '2': Vendor('phone 2', 65, timedelta(days=30), date(2021, 3, 4), 0, timedelta(days=9), 10, 30)}

# cards cycle day is the same day that the challenge starts
cards = {'1': Card(timedelta(days=30), date(2021, 3, 4), timedelta(days=9), 19.95, 15, 1000, 2, 0.21, 19.95, 30),
         '2': Card(timedelta(days=30), date(2021, 3, 4), timedelta(days=9), 39.95, 15, 1000, 2, 0.14, 39.95, 30)}

# utilities have a "management fee"
utils = {'1': Vendor('utilities 1', 93, timedelta(days=30), date(2021, 3, 28), 0, timedelta(days=11), 5, 30),
             '2': Vendor('utilities 2', 95, timedelta(days=30), date(2021, 3, 28), 0, timedelta(days=11), 5, 30)}

# renter_ins have a "deductible"
renter_ins = {'1': Vendor('renter ins 1', 195, timedelta(days=365), date(2021, 3, 5), 0, timedelta(days=9), 45, 30),
              '2': Vendor('renter ins 2', 250, timedelta(days=365), date(2021, 3, 5), 0, timedelta(days=9), 45, 30)}

# student loan, since there is only one option, it is created whenever a person is created
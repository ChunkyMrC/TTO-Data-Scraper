from datetime import date, timedelta, datetime
import re

###################### TTO USERNAME & PASSWORD ####################

while True:
    username = input("Enter your the email address you use for TTO: ")
    reg = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(reg, username):
        print("Valid email.")
        break
    else:
        print("Invalid email.")

while True:
    password = input("Enter your TTO password: ")
    if isinstance(password, str) and len(password) >= 4:
        print("Valid password.")
        break
    else:
        print("Invalid password.")

######################### Start and End Dates #########################

while True:
    start_dt = input("Enter the start date (DD/MM/YY): ")
    try:
        input_date = datetime.strptime(start_dt, "%d/%m/%y")
        print("Start date valid")
        start_dt = input_date.date()
        break
    except ValueError:
        print("Start date invalid")

while True:
    end_dt = input("Enter the end date (DD/MM/YY): ")
    try:
        input_date = datetime.strptime(end_dt, "%d/%m/%y")
        print("End date valid")
        end_dt = input_date.date()
        break
    except ValueError:
        print("End date invalid")

delta = timedelta(days=1)
dates_to_search = set()
dates_to_search.add(end_dt)

while start_dt <= end_dt:
    dates_to_search.add(start_dt)
    start_dt += delta


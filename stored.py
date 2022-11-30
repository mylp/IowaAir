import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb"
)

cursor = mydb.cursor()

def bookFlight(first_name, last_name, email, phone, flight_id, seat_id):
    cursor.callproc('bookFlight', (first_name, last_name, email, phone, flight_id, seat_id))

def manageTrip(passenger_id):
    cursor.callproc('manageTrip', (passenger_id))

def checkFlightStatus(departure_city, arrival_city, departure_date):
    cursor.callproc('checkFlightStatus', (departure_city, arrival_city, departure_date))

def displayScreen():
    print("Welcome to the flight booking system")
    print("1. Book a flight")
    print("2. Manage Trip/Check-in")
    print("3. Check flight status")
    print("4. Exit")
    print("Please enter your choice: ", end="")
    choice = int(input())
    return choice

def main():
    choice = displayScreen()
    while choice != 4:
        if choice == 1:
            bookFlight()
        elif choice == 2:
            manageTrip()
        elif choice == 3:
            checkFlightStatus()
        else:
            print("Invalid choice")
        choice = displayScreen()

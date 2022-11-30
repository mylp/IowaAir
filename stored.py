import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PepeSilvia1259#12!",
    database="mydb"
)

cursor = mydb.cursor()

def generateRandomPassengers():
    pass

def generateRandomFlights():
    pass
        
# How are transactions handled in Python?
# Should they be handled in the stored procedures?

def bookFlight(first_name, last_name, email, phone, flight_id, seat_id):
    cursor.callproc('bookFlight', (first_name, last_name,
                    email, phone, flight_id, seat_id))


def manageTrip(passenger_id):
    cursor.callproc('manageTrip', (passenger_id))

# Need support for checking flight status with flight id
def checkFlightStatus(departure_city, arrival_city, departure_date):
    cursor.callproc('checkFlightStatus',
                    (departure_city, arrival_city, departure_date))


def displayScreen():
    print("------------------------------------")
    print("Welcome to Iowa Air Booking System")
    print("1. Book a flight")
    print("2. Manage Trip/Check-in")
    print("3. Check flight status")
    print("4. Exit\n")
    print("Please enter your choice: ", end="")
    choice = int(input())
    print()
    return choice


def main():
    choice = displayScreen()
    while choice != 4:

        if choice == 1:
            first = input("Enter your first name: ")
            last = input("Enter your last name: ")
            email = input("Enter your email: ")
            phone = input("Enter your phone number: ")
            flight = input("Enter the flight number: ")
            seat = input("Enter the seat number: ")
            bookFlight(first, last, email, phone, flight, seat)

        elif choice == 2:
            passenger = input("Enter your passenger id: ")
            manageTrip(passenger)

        elif choice == 3:
            departure = input("Enter the departure city: ")
            arrival = input("Enter the arrival city: ")
            date = input("Enter the departure date: ")
            checkFlightStatus(departure, arrival, date)

        else:
            print("Invalid choice")

        choice = displayScreen()
    
    cursor.execute("SELECT * FROM airport")
    a = cursor.fetchall()
    if a:
        for i in a:
            print(i)
    print()


if __name__ == "__main__":
    main()

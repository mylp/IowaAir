import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb"
)

cursor = mydb.cursor()


def generateRandomPassengers():
    pass


def generateRandomFlights():
    pass


def bookFlight():
    round_trip = input("Is this a round trip? (y/n): ")
    departure_city = input("Enter the departure city: ")
    arrival_city = input("Enter the arrival city: ")
    departure_date = input("Enter the departure date: (yyyy/mm/dd)")
    if round_trip == 'y':
        return_date = input("Enter the return date: (yyyy/mm/dd)")
    
    passenger_count = int(input("Enter the number of passengers: "))
    
    flights = cursor.callproc('getFlights', (departure_city, arrival_city, departure_date, return_date, passenger_count))
    if flights:
        print("Available flights: ")
        for flight in flights:
            print(flight)
    else:
        print("No flights available")

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
            bookFlight()

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
    queries = cursor.fetchall()
    if queries:
        for query in queries:
            print(query)
    print()


if __name__ == "__main__":
    main()

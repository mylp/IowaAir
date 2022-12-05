import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PepeSilvia1259#12!",
    database="mydb"
)

cursor = mydb.cursor()

def calculateCost(seats):
    cost = 0
    for seatID in seats:
        cost  += cursor.callproc('getSeatCost', seatID)
    return cost 

def bookFlight():
    round_trip = input("Is this a round trip? (y/n): ")
    departure_city = input("Enter the departure city: ")
    arrival_city = input("Enter the arrival city: ")
    departure_date = input("Enter the departure date: (yyyy/mm/dd)")
    if round_trip == 'y':
        return_date = input("Enter the return date: (yyyy/mm/dd)")
    passenger_count = int(input("Enter the number of passengers: "))

    # Get all flights that match and have seats available
    flights = cursor.callproc('getFlights', (departure_city,
                              arrival_city, departure_date, return_date, passenger_count))

    # Get all return flights that match and have seats available
    #return_flights = cursor.callproc('getReturnFlights', (departure_city,
    #                                      arrival_city, departure_date, return_date, passenger_count))
    
    if flights:
        print("Available flights: ")
        for flight in flights:
            print(flight)

        # Need to handle the case with return flights
        selection = int(input("Enter the flight ID you want to book: "))
        selected = flights[selection]

        seatID = None

        # Need to handle passenger seat selections
        passengers = []
        for _ in range(passenger_count):
            first_name = input("Enter your first name: ")
            middle_name = input("Enter your middle name: ")
            last_name = input("Enter your last name: ")
            email = input("Enter your email: ")
            phone = input("Enter your phone number: ")
            dob = input("Enter your date of birth: (yyyy/mm/dd)")
            gender = input("Enter gender: (M/F)")
            country = input("Enter your country: ")

            passengers.append(
                (first_name, middle_name, last_name, email, phone, dob, gender, country))

        for passenger in passengers:
            cursor.callproc('insertPassenger', passenger)
        
        # Need to handle seat selection
        seats = []

        # Split this to separate transaction function
        totalCost = calculateCost(seats)
        fName = input("Enter your first name: ")
        lName = input("Enter your last name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        dob = input("Enter your date of birth: (yyyy/mm/dd)")
        billing = input("Enter your billing address: ")
        ccNo = input("Enter your credit card number: ")
        ccExp = input("Enter your credit card expiration date: (yyyy/mm/dd)")
        cardType = input("Enter your credit card type: ")
        ccCVV = input("Enter your credit card CVV: ")

        customerID = cursor.callproc(  # Assume this returns passenger ID
            'insertCustomer', (fName, lName, email, phone, dob, billing, ccNo, ccExp, cardType, ccCVV))

        transaction = cursor.callproc(  # Assume this returns tranasction ID
            'createTransaction', (0, totalCost, ccNo, ccExp, cardType, ccCVV, customerID))

        cursor.callproc('updateBookingWithTransaction', transaction)

        confirmation = None
        print("Your confirmation number is: ", confirmation)

    else:
        print("No flights available")
        bookFlight()


def manageTrip():
    print("1. Cancel flight")
    print("2. Check-in")
    print("3. Exit\n")
    print("Please enter your choice: ", end="")
    choice = int(input())
    match choice:
        case 1:
            print("Please enter the transaction ID to cancel a flight")
            transID = int(input())
            # Get all bookings with the transID
            # Get all passengers with the bookingID
            # Get all seatIDs with passengerID
            # Unmark all seats with seatIDs
            # Locate and delete all bookings with the given transaction ID
            cancellation = cursor.callproc('cancelFlight', transID)
            if cancellation:
                print("Successfully cancelled flight.")
        case 2:
            pass
        case 3:
            pass


def checkFlightStatus():
    print("Enter your flight ID to check the status: ", end="")
    flightID = int(input())
    status = cursor.callproc('getFlightStatus', flightID)
    print("Flight status: ", status)


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

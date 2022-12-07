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
        cost += cursor.callproc('getSeatCost', seatID)
    return cost


def create_transaction(seats, return_seats):
    totalCost = calculateCost(seats+return_seats)
    print("Total cost: ", totalCost)
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

    return transaction


def getPassengerInfo(pcount):
    passengers = []
    for _ in range(pcount):
        first_name = input("Enter your first name: ")
        middle_name = input("Enter your middle name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        dob = input("Enter your date of birth: (yyyy/mm/dd)")
        gender = input("Enter gender: (M/F)")
        country = input("Enter your country: ")
        passengers.append((first_name, middle_name, last_name,
                          email, phone, dob, gender, country))
    return passengers


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
    return_flights = cursor.callproc('getReturnFlights', (arrival_city,
                                                          departure_city, return_date, departure_date, passenger_count))
    # What if there are no return flights?
    # What if there are no flights?
    if flights and return_flights:
        print("Available departure flights: ")
        for flight in flights:
            print(flight)
        depart_flight = int(
            input("Enter the departure flight ID you want to book: "))
        
        print("Available return flights: ")
        for flight in return_flights:
            print(flight)
        return_flight = int(
            input("Enter the return flight ID you want to book: "))

        passengers = getPassengerInfo(passenger_count)

        # Need to handle passenger seat selections
        for passenger in passengers:
            
            # Need to make sure the seat is available
            print("Select the depart seat: ")
            # Get all seats for the flight
            seats = cursor.callproc('getSeats', depart_flight)
            for seat in seats:
                print(seat)
            seatID = int(input("Enter the seat ID you want to book: "))
            # Mark seat as taken
            cursor.callproc('markSeatTaken', seatID)
            
            print("Select the return seat: ")
            # Get all seats for the flight
            seats = cursor.callproc('getSeats', return_flight)
            for seat in seats:
                print(seat)
            seatID = int(input("Enter the seat ID you want to book: "))
            # Mark seat as taken
            cursor.callproc('markSeat', seatID, 1)

        # What about seat selection?
        for passenger in passengers:
            cursor.callproc('insertPassenger', passenger)

        seats = []
        return_seats = []

        transaction = create_transaction(seats, return_seats)
        cursor.callproc('updateBookingWithTransaction', transaction)
        print("Your transaction number is: ", transaction)

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
            cancellation = cursor.callproc('cancelFlight', transID)
            seats = [] # Get seats from transaction
            for seatID in seats:
                cursor.callproc('markSeat', seatID, 0)
            if cancellation:
                print("Successfully cancelled flight.")


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

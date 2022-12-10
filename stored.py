import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PepeSilvia1259#12!",
    database="mydb"
)
cursor = mydb.cursor()
mydb.autocommit = True

def calculateCost(seatIDs):
    cost = 0
    for seatID in seatIDs:
        cursor.callproc('get_seatcost', (seatID,))
        for result in cursor.stored_results():
            tup = result.fetchall()
            for x in tup:
                cost += sum(x)
    return cost

def create_transaction(totalCost):
    fName = input("Enter your first name: ")
    lName = input("Enter your last name: ")
    dob = input("Enter your date of birth (yyyy-mm-dd): ")
    gender = input("Enter your gender:")
    phone = input("Enter your phone number: ")
    streetAddress = input("Enter your billing street address (Do not include State or ZIP Code): ")
    state = input("Enter your state: ")
    country = input("Enter your country: ")
    zipcode = input("Enter your zipcode: ")
    email = input("Enter your email: ")
    ccNo = input("Enter your credit card number: ")
    ccExp = input("Enter your credit card expiration date (yyyy-mm): ") + "-00"
    cardType = input("Enter your credit card type: ")
    ccCVV = input("Enter your credit card CVV: ")

    cursor.callproc(  # Assume this returns passenger ID
        'add_customer', (fName, lName, dob, gender, phone, streetAddress, state, country, zipcode, email, 0))
    customerID = getColumn(0)[0]
    print(customerID)

    cursor.callproc(  # Assume this returns tranasction ID
        'add_transaction', (totalCost, ccNo, ccExp, cardType, ccCVV, customerID))
    transaction = getColumn(0)[0]

    print("Your transaction ID is: ", transaction)
    return transaction
    

def getPassengerInfo(pcount):
    passengers = []
    for _ in range(pcount):
        print("Passenger " + str(_ + 1))
        first_name = input("Enter your first name: ")
        middle_name = input("Enter your middle name: ")
        last_name = input("Enter your last name: ")
        dob = input("Enter your date of birth (yyyy-mm-dd): ")
        gender = input("Enter gender (M/F): ")
        country = input("Enter your country: ")
        passengers.append([first_name, last_name, middle_name, 
                          dob, gender, country])
    return passengers

def getColumn(index):
    printThese = []
    for result in cursor.stored_results():
        tup = result.fetchall()
        for x in tup:
            printThese.append(x[index])
    return printThese

def bookFlight():
    round_trip = input("Is this a round trip? (y/n): ")
    departure_city = input("Enter the departure city: ")
    arrival_city = input("Enter the arrival city: ")
    departure_date = input("Enter the departure date (yyyy-mm-dd): ")
    if round_trip == 'y':
        return_date = input("Enter the return date (yyyy-mm-dd): ")
    passenger_count = int(input("Enter the number of passengers: "))

    # Get all flights that match and have seats available
    cursor.callproc('get_flights', (departure_city,
                              arrival_city, departure_date, passenger_count))
    flights = []
    for flight in cursor.stored_results():
        tup = flight.fetchall()
        for x in tup:
            flights.append(x[0])
    
    # Get all return flights that match and have seats available
    cursor.callproc('get_flights', (arrival_city, departure_city, return_date, passenger_count))
    return_flights = []
    for flight in cursor.stored_results():
        tup = flight.fetchall()
        for x in tup:
            return_flights.append(x[0])
    
    if flights and return_flights:
        print("Available departure flights: ")
        for flight in flights:
            print(flight)
        depart_flight_id = int(
            input("Enter the departure flight ID you want to book: "))
        
        print("Available return flights: ")
        for flight in return_flights:
            print(flight)
        return_flight_id = int(
            input("Enter the return flight ID you want to book: "))

        passengers = getPassengerInfo(passenger_count)

        cursor.callproc('get_available_seats', (depart_flight_id,))
        seats_available = getColumn(0)
        
        cursor.callproc('get_available_seats', (return_flight_id,))
        return_seats_available = getColumn(0)
        
        seat_selection = []
        return_seat_selection = []

        for i, passenger in enumerate(passengers):
            
            # Need to make sure the seat is available
            print("Select the depart seat: ")
            print("Available seats: ", seats_available)
            seatID = int(input("Passenger " + str(i+1) + ", Enter the seat ID you want to book: "))
            if seatID in seats_available:
                seat_selection.append(seatID)
                seats_available.remove(seatID)
            else:
                print("Seat not available")
        
        for i, passenger in enumerate(passengers):
            print("Select the return seat: ")
            
            print("Available seats: ", return_seats_available)
            returnseatID = int(input("Passenger " + str(i+1) + ", Enter the seat ID you want to book: "))
            if returnseatID in return_seats_available:
                return_seat_selection.append(returnseatID)
                return_seats_available.remove(returnseatID)
            else:
                print("Seat not available")
        
        # Calculate total cost
        totalCost = calculateCost(seat_selection) + calculateCost(return_seat_selection)
        print("Total Cost = $" + str(totalCost))
        transactionID = create_transaction(totalCost)

        for i in range(len(passengers)):
            passengers[i].append(seat_selection[i])
            cursor.callproc('add_passenger', tuple(passengers[i]))
            passengerID = getColumn(0)[0]
            cursor.callproc('add_booking', (passengerID, depart_flight_id, transactionID))
        
        for i in range(len(passengers)):
            passengers[i].pop()
            passengers[i].append(return_seat_selection[i])
            cursor.callproc('add_passenger', tuple(passengers[i]))
            passengerID = getColumn(0)[0]
            cursor.callproc('add_booking', (passengerID, return_flight_id, transactionID))
        
        for seatID in seat_selection:
            cursor.callproc('mark_seat', (seatID, 1))
        cursor.callproc('update_passenger_count', (depart_flight_id, len(passengers)))

        for seatID in return_seat_selection:
            cursor.callproc('mark_seat', (seatID, 1))
        cursor.callproc('update_passenger_count', (return_flight_id, len(passengers)))

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
            transactionID = int(input())
            cursor.callproc('cancel_flight', transactionID)
            print("Flight cancelled")


def checkFlightStatus():
    print("Enter your flight ID to check the status: ", end="")
    flightID = int(input())
    cursor.callproc('check_flight_status', (flightID,))
    printThese = []
    for result in cursor.stored_results():
        tup = result.fetchall()
        for x in tup:
            printThese.append(x)
    print("Depart Date: " + str(printThese[0][0]) + "\n"
        + "Arrival Date: " + str(printThese[0][1]) + "\n"
        + "Aircraft ID: " + str(printThese[0][2]))
        
    cursor.callproc('get_airport', (flightID,))
    printThese = []
    for result in cursor.stored_results():
        tup = result.fetchall()
        for x in tup:
            printThese.append(x)
    print("Depart Airport: " + str(printThese[0][0]) + "\n" + "Arrival Airport: " + str(printThese[1][0]))

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
            checkFlightStatus()
        else:
            print("Invalid choice")
        choice = displayScreen()

if __name__ == "__main__":
    main()

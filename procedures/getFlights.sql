DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `getFlights`(
departure_city VARCHAR(45),
arrival_city VARCHAR(45), 
departure_date DATE, 
return_date DATE, 
passenger_count INT)
BEGIN
	SELECT * FROM flight
    WHERE flightID in (
		SELECT flightID FROM airport_has_flight
        WHERE departureID in (
			SELECT airportID from airport
            WHERE city = departure_city
		) AND arrivalID in (
			SELECT airportID from airport
            WHERE city = arrival_city
		)
    ) AND passengerCount + passenger_count <= (
		SELECT seatCount FROM aircraft
        WHERE aircraftID = Aircraft_aircraftID
    );
END$$
DELIMITER ;

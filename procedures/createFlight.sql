CREATE DEFINER=`root`@`localhost` PROCEDURE `createFlight`(
	departAirport VARCHAR(45), 
    arrivalAirport VARCHAR(45),
    departDate DATETIME, 
    arrivalDate DATETIME, 
    employeeID INT, 
    aircraftID INT)
BEGIN
	INSERT INTO flight
    VALUES (0, 0, departDate, arrivalDate, employeeID, aircraftID);
    
    CALL createSeats(LAST_INSERT_ID(), 10); 
    
    INSERT INTO airport_has_flight
    VALUES (departAirport, LAST_INSERT_ID(), arrivalAirport);
    
END
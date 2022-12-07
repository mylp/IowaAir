CREATE DEFINER=`root`@`localhost` PROCEDURE `createSeats`(fID INT, cost INT)
BEGIN
    
    # CALLED BY createFlight to generate seats
    SET @i = 0;
	SET @seatCount = (
		SELECT seatCount FROM aircraft
        WHERE aircraftID in (
			SELECT aircraftID FROM flight
            WHERE flightID = fID
        )
	);
    
    WHILE @i < @seatCount DO
		INSERT INTO seat
        VALUES (0, 0, "Economy", fID, cost, 0);
        SET @i = @i + 1;
    END WHILE;
END
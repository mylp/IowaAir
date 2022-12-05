DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `cancelFlight`(transactionID INT)
BEGIN
	# Update occupancies based on transactionID
    UPDATE seat
    SET occupancy = 0
    WHERE seatID IN (
		SELECT seatID FROM passenger
		WHERE passengerID in (
			SELECT passengerID FROM booking
			WHERE Transaction_transactionID = transactionID
		)
	);
    
    DELETE FROM booking
    WHERE Transaction_transactionID = transactionID;
    
    DELETE FROM `transaction`
    WHERE transactionID = transactionID;
END$$
DELIMITER ;

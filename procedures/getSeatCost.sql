DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `getSeatCost`(seatID INT)
BEGIN
	SELECT cost, additional_cost FROM seat
    WHERE seatID = seatID;
END$$
DELIMITER ;

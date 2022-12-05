DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertCustomer`(
`customerID` INT,
`fName` VARCHAR(45),
`lName` VARCHAR(45),
`dob` DATE,
`gender` VARCHAR(45),
`phoneNo` VARCHAR(45),
`streetAddress` VARCHAR(45),
`state` VARCHAR(45),
`country` VARCHAR(45),
`zipcode` INT,
`email`  VARCHAR(45),
`username` VARCHAR(45),
`password` VARCHAR(45),
`rewardMiles` INT)
BEGIN

INSERT INTO customer
VALUES (0, fName, lName, dob, gender, phoneNo, streetAddress, state, country, zipcode, email, username, `password`, rewardMiles);
END$$
DELIMITER ;

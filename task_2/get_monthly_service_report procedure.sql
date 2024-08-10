DELIMITER //
CREATE PROCEDURE get_monthly_services_report(IN start_date DATE)
BEGIN
    DECLARE end_date DATE;
    SET end_date = LAST_DAY(start_date);

    CREATE TEMPORARY TABLE monthly_services_report AS
    SELECT
		u.name AS user_name,
		u.login AS user_login,
		s.name AS service_name,
        u.contract_start_date,
		u.contract_expiration_date,
		s.cost AS original_cost,
		COALESCE(d.name, '-') AS discount_name,
		COALESCE(d.discount, 0) AS discount,
		s.cost - COALESCE(d.discount, 0) AS total_cost
	FROM users u
	INNER JOIN services s
		ON s.user_id = u.user_id
	LEFT JOIN discounts d
		ON d.service_id = s.service_id
		AND s.timefrom BETWEEN d.timefrom AND d.timeto
	WHERE
		s.timefrom >= start_date 
		AND s.timeto <= end_date;

    SELECT * FROM monthly_services_report;
    DROP TEMPORARY TABLE IF EXISTS monthly_services_report;
END //

DELIMITER ;
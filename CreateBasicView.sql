DROP VIEW IF EXISTS 'BasicView';
CREATE VIEW 'BasicView' AS
SELECT 
	knights.first_name || ' ' || 
	knights.last_name AS 'Name',
	knights.address AS 'Address',
	knights.city AS 'City', 
	knights.email AS 'Email',
	knights.primary_phone AS 'Phone',
	councils.council_number AS 'Council'
FROM knights
INNER JOIN councils ON councils.id = knights.council_id;
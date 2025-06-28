DROP VIEW IF EXISTS "DistrictsView";
CREATE VIEW "DistrictsView" as SELECT 
    d.number,
    k.first_name || ' ' || k.last_name AS "Name",
	group_concat(c.council_number || ': ' || c.city, ', ') as "Councils"
FROM districts d
LEFT JOIN knights k ON d.dd_id = k.id
LEFT JOIN councils c ON c.district_id = d.id
GROUP BY d.number;
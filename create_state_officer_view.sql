DROP VIEW IF EXISTS "main"."State Officers";
CREATE VIEW "State Officers" AS 
	select k.first_name || ' ' || k.last_name as "full_name",
	k.wife as "wife",
	k.address as "address",
	k.city || ', ' || "STATE" || ' ' || k.zipcode as "city_state_zip",
	k.primary_phone as "phone",
	k.email as "email",
	c.council_number as "council",
	group_concat(r.role, ', ') as "role"
from knights k

inner join knights_roles kr on k.id = kr.knight_id 
inner join roles r on kr.role_id = r.id

inner join knights_councils kc on k.id = kc.knight_id
inner join councils c on kc.council_id = c.id

where role_id <= 10
group by k.id, k.first_name, k.last_name, k.email
order by r.id
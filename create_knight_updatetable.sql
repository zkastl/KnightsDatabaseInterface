DROP TABLE IF EXISTS "State_Officers_Editable";
CREATE TABLE "State_Officers_Editable" AS 
	select 
		k.id as knight_id,
		group_concat(kr.role_id, ',') as role_ids, -- Store actual role IDs
		group_concat(r.role, ', ') as "Roles",
		k.first_name || ' ' || k.last_name as "Name",
		k.wife as "wife",
		--c.council as "council",
		k.primary_phone as "phone",
		k.address as "address",
		k.city || ', ' || "STATE" || ' ' || k.zipcode as "city_state_zip",
		k.email as "Email"
	from knights k 
	inner join knights_roles kr on k.id = kr.knight_id 
	inner join roles r on kr.role_id = r.id
	inner join knights_councils kc on k.id = kc.knight_id
	inner join councils c on kc.council_id = c.id
	where kr.role_id <= 10
	group by k.id, k.first_name, k.last_name, k.email
	order by MIN(r.id);
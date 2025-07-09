DROP VIEW IF EXISTS "main"."StateOfficerView";
CREATE VIEW "StateOfficerView" AS 
	select k.first_name || ' ' || k.last_name as "full_name",
	k.wife as "wife",
	k.address as "address",
	k.city || ', ' || k.state || ' ' || k.zipcode as "city_state_zip",
	k.primary_phone as "phone",
	k.email as "email",
	k.council as "council",
	r.id as "role_id",
	group_concat(r.role, ', ') as "role"
from knights k

left join knights_roles kr on k.id = kr.knight_id 
left join roles r on kr.role_id = r.id
left join councils c on k.council = c.id

where role_id <=10 OR role_id=71
group by k.id, k.first_name, k.last_name, k.email
order by min(r.id)
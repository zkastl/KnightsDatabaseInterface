DROP VIEW IF EXISTS "ProgramDirectorView";
CREATE VIEW "ProgramDirectorView" AS

select r.role, k.first_name || ' ' || k.last_name as "name", k.council, k.email, k.primary_phone from roles r

left join knights_roles kr on r.id = kr.role_id
left join knights k on kr.knight_id = k.id

where r.role COLLATE NOCASE in
(
"State Program Director",
"Life Director",
"Silver Rose Chairman",
"March 4 Life Chairman - OKC",
"March 4 Life Chairman - Tulsa",
"Intellectual Disabilities Chairman",
"Special Olympics Chairman",
"Ultrasound Initiative Chairman",
"Center of Family Love Support Chairman",
"Faith Director",
"Icons Chairman",
"Keep Christ in Christmas Chairman",
"RSVP Chairman - OKC",
"RSVP Chairman - Tulsa",
"Community Director",
"State Golf Tournament Chairman",
"Coats 4 Kids Chairman",
"State Free Throw Tournament Chairman",
"Soccer Challenge Chairman",
"Disaster Response Chairman",
"Family Director",
"Family of the Month Chairman",
"Food 4 Families Chairman"
)
ORDER BY
CASE r.role COLLATE NOCASE
	WHEN "State Program Director" THEN 1
	WHEN "Life Director" THEN 2
	WHEN "Silver Rose Chairman" THEN 3
	WHEN "March 4 Life Chairman - OKC" THEN 4
	WHEN "March 4 Life Chairman - Tulsa" THEN 5
	WHEN "Intellectual Disabilities Chairman" THEN 6
	WHEN "Special Olympics Chairman" THEN 7
	WHEN "Ultrasound Initiative Chairman" THEN 8
	WHEN "Center of Family Love Support Chairman" THEN 9
	WHEN "Faith Director" THEN 10
	WHEN "Icons Chairman" THEN 11
	WHEN "Keep Christ in Christmas Chairman" THEN 12
	WHEN "RSVP Chairman - OKC" THEN 13
	WHEN "RSVP Chairman - Tulsa" THEN 14
	WHEN "Community Director" THEN 15
	WHEN "State Golf Tournament Chairman" THEN 16
	WHEN "Coats 4 Kids Chairman" THEN 17
	WHEN "State Free Throw Tournament Chairman" THEN 18
	WHEN "Soccer Challenge Chairman" THEN 19
	WHEN "Disaster Response Chairman" THEN 20
	WHEN "Family Director" THEN 21
	WHEN "Family of the Month Chairman" THEN 22
	WHEN "Food 4 Families Chairman" THEN 23
	ELSE 99
END;
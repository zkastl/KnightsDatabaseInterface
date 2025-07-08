BEGIN TRANSACTION;

-- TABLES SECTION

-- COUNCILS
DROP TABLE IF EXISTS "councils";
CREATE TABLE "councils" (
	"id"	INTEGER NOT NULL UNIQUE,
	"council_number"	INTEGER,
	"council_name"	TEXT,
	"parish"	TEXT,
	"address"	TEXT,
	"city"	TEXT,
	"meeting_time"	TEXT,
	"district_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- DISTRICTS
DROP TABLE IF EXISTS "districts";
CREATE TABLE "districts" (
	"id"	INTEGER NOT NULL UNIQUE,
	"number"	INTEGER NOT NULL,
	"dd_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("dd_id") REFERENCES "knights"("id") ON DELETE SET NULL
);

-- KNIGHTS
DROP TABLE IF EXISTS "knights";
CREATE TABLE "knights" (
	"id"	INTEGER,
	"first_name"	TEXT,
	"middle_name"	TEXT,
	"last_name"	TEXT,
	"wife"	TEXT,
	"address"	TEXT,
	"city"	TEXT,
	"zipcode"	INTEGER,
	"primary_phone"	TEXT,
	"secondary_phone"	TEXT,
	"email"	TEXT,
	"deceased"	INTEGER,
	"state"	text,
	"council"	NUMERIC,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- KNIGHTS_ROLES JUNCTION
DROP TABLE IF EXISTS "knights_roles";
CREATE TABLE "knights_roles" (
	"knight_id"	INTEGER,
	"role_id"	INTEGER,
	PRIMARY KEY("knight_id","role_id"),
	FOREIGN KEY("knight_id") REFERENCES "knights"("id"),
	FOREIGN KEY("role_id") REFERENCES "roles"("id")
);
DROP TABLE IF EXISTS "roles";
CREATE TABLE "roles" (
	"id"	INTEGER NOT NULL UNIQUE,
	"role"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- VIEWS SECTION

-- DISTRICTS VIEW
DROP VIEW IF EXISTS "DistrictsView";
CREATE VIEW "DistrictsView" as
SELECT 
    d.number,
    k.first_name || ' ' || k.last_name AS "district_deputy",
	k.address || "|" || k.city || "|" || k.state || "|" || k.zipcode as "address",
	k.primary_phone as "phone",
    k.email as "email",
	k.council as "home_council",
	group_concat(c.council_number || ',' || c.city, '|') as "councils",
	k.wife as "wife"
FROM districts d
LEFT JOIN knights k ON d.dd_id = k.id
INNER JOIN councils c ON c.district_id = d.id
GROUP BY d.number;

-- KNIGHTS VIEW
DROP VIEW IF EXISTS "KnightsView";
CREATE VIEW "KnightsView" AS 
select 
	k.first_name || ' ' || k.last_name as "Name",
	k.wife as "Wife",
	k.address as "Address",
	k.city as "City",
	k.state as "State",
	k.zipcode as "Zip Code",
	k.primary_phone as "Phone",
	k.email as "Email",
	c.district_id as "District",
	group_concat(r.role, ', ') as "Roles"
from knights k
left join knights_roles kr on k.id = kr.knight_id 
inner join roles r on kr.role_id = r.id
left join councils c on k.council = c.council_number

where k.deceased != 1

group by k.last_name
order by min(r.id);

-- PROGRAM DIRECTORS VIEW
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

-- STATE OFFICERS VIEW
DROP VIEW IF EXISTS "StateOfficerView";
CREATE VIEW "StateOfficerView" AS 
	select k.first_name || ' ' || k.last_name as "full_name",
	k.wife as "wife",
	k.address as "address",
	k.city || ', ' || k.state || ' ' || k.zipcode as "city_state_zip",
	k.primary_phone as "phone",
	k.email as "email",
	c.council_number as "council",
	r.id as "role_id",
	group_concat(r.role, ', ') as "role"
from knights k

left join knights_roles kr on k.id = kr.knight_id 
left join roles r on kr.role_id = r.id
left join councils c on k.council = c.id

where role_id <=10
group by k.id, k.first_name, k.last_name, k.email
order by min(r.id);

-- INSERT DATA INTO ROLES (PERMANENT SO CAN PUT HERE)
INSERT INTO "roles" ("id","role") VALUES
 (1,'State Chaplain'),
 (2,'State Deputy'),
 (3,'Immediate Past State Deputy'),
 (4,'State Secretary'),
 (5,'State Treasurer'),
 (6,'State Advocate'),
 (7,'State Warden'),
 (8,'Vice Supreme Master - 4th Degree'),
 (9,'District Master - 4th Degree'),
 (10,'Regional Growth Director'),
 (11,'District Deputy'),
 (12,'Executive Secretary'),
 (13,'State Membership Director'),
 (14,'Assistant State Membership Director - East'),
 (15,'Assistant State Membership Director - West'),
 (16,'State Online Director'),
 (17,'State Online Chairman - East'),
 (18,'State Online Chairman - West'),
 (19,'State Membership Retention Director'),
 (20,'State Reactivation Chairman'),
 (21,'State New Council Development Chairman'),
 (22,'State Retention and Round Table Chairman'),
 (23,'Hispanic Chairman'),
 (24,'Hispanic Coordinator - East'),
 (25,'Hispanic Coordinator - West'),
 (26,'Ceremonials and Protocol Director'),
 (27,'State Program Director'),
 (28,'Faith Director'),
 (29,'RSVP Chairman - OKC'),
 (30,'RSVP Chairman - Tulsa'),
 (31,'Pilgrim Icon Program'),
 (32,'Go Life Liaison - East'),
 (33,'Pennies for Heaven / 365 Club Chairman'),
 (34,'Spiritual Reflection Program Chairman'),
 (35,'Community Director'),
 (36,'Intellectual Disabilities Chairman'),
 (37,'Soccer Challenge Chairman'),
 (38,'State Free Throw Tournament Chairman'),
 (39,'Disaster Response Chairman'),
 (40,'Coats 4 Kids Chairman'),
 (41,'State Golf Tournament Chairman'),
 (42,'Keep Christ in Christmas Chairman'),
 (43,'Family Director'),
 (44,'Food 4 Families Chairman'),
 (45,'Family of the Month Chairman'),
 (46,'Life Director'),
 (47,'Ultrasound Initiative Chairman'),
 (48,'Silver Rose Chairman'),
 (49,'Special Olympics Chairman'),
 (50,'Novena for Life Chairman'),
 (51,'Annual Go Life Gala Committee (K of C Liaison)'),
 (52,'Center of Family Love Support Chairman'),
 (53,'Center of Family Love Support Directors Co-Chairman - Tulsa'),
 (54,'Catholic Education Support Director'),
 (55,'Awards/Report Forms Director'),
 (56,'Father McGivney Guild Chairman'),
 (57,'Knights on Bikes - Oklahoma President'),
 (58,'Knights on Bikes Director - OKC'),
 (59,'Knights on Bikes Director - Tulsa'),
 (60,'Marketing & Public Relations Chairman'),
 (61,'Oklahoma Knight Editor'),
 (62,'State Training Director'),
 (63,'State Directory Chairman'),
 (64,'Past State Deputy'),
 (65,'Former State Chaplain'),
 (68,'Icons Chairman'),
 (69,'March 4 Life Chairman - OKC'),
 (70,'March 4 Life Chairman - Tulsa');

-- COMMIT
COMMIT;

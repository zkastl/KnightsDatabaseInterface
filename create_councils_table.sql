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
)
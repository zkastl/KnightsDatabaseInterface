CREATE TABLE "districts" (
	"id"	INTEGER NOT NULL UNIQUE,
	"number"	INTEGER NOT NULL,
	"dd_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("dd_id") REFERENCES "knights"(id) ON DELETE SET NULL
)
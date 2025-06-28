drop table if exists "knights_councils";

CREATE TABLE "knights_councils" (
	"knight_id"	INTEGER,
	"council_id"	INTEGER,
	PRIMARY KEY("knight_id","council_id"),
	FOREIGN KEY("knight_id") REFERENCES "knights"("id"),
	FOREIGN KEY("council_id") REFERENCES "councils"("id")
);
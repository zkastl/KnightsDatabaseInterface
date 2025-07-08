CREATE TABLE "knights_roles" (
	knight_id	INTEGER,
	role_id	INTEGER,
	PRIMARY KEY (knight_id, role_id),
	FOREIGN KEY (knight_id) REFERENCES knights (id),
	FOREIGN KEY (role_id) REFERENCES roles (id)
)
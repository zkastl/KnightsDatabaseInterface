import csv
import sqlite3

CSV_FILENAME = './entry_script.csv'
DB_FILENAME = './ok_knights_directory.db'

SELECT_KNIGHTS = "SELECT * FROM knights"
SELECT_KR = 'SELECT * from knights_roles ORDER BY role_id'

SELECT_THREE = """SELECT k.id, 
       c.council_number, 
       k.last_name, 
       r.role
FROM knights k
INNER JOIN knights_roles kr ON k.id = kr.knight_id 
INNER JOIN roles r ON kr.role_id = r.id
LEFT JOIN councils c ON k.council = c.council_number
WHERE kr.role_id IN (75, 77)
order by council_number
"""

INSERT_FOUR = """
UPDATE \"councils\"
SET gk_id = (
    SELECT k.id FROM knights k
    INNER JOIN knights_roles kr on k.id = kr.knight_id
    WHERE kr.role_id = 75 AND k.council = councils.council_number
)
WHERE EXISTS (
    SELECT 1 FROM knights k
    INNER JOIN knights_roles kr on k.id = kr.knight_id
    WHERE kr.role_id = 75 AND k.council = councils.council_number
)"""


INSERT_FIVE = """
UPDATE \"councils\"
SET fs_id = (
    SELECT k.id 
    FROM knights k
    INNER JOIN knights_roles kr ON k.id = kr.knight_id
    WHERE kr.role_id = 77 
      AND k.council = councils.council_number
)
WHERE EXISTS (
    SELECT 1 
    FROM knights k
    INNER JOIN knights_roles kr ON k.id = kr.knight_id
    WHERE kr.role_id = 77 
      AND k.council = councils.council_number
)
"""

INSERT_KNIGHTS = "INSERT INTO \"knights\" (first_name, middle_name,\
    last_name, address, city, state, zipcode, email, primary_phone,\
    council, deceased) VALUES "

INSERT_KR = "INSERT INTO \"knights_roles\" (knight_id, role_id) VALUES "


# grab and process text from insert file
raw_text = []
knights = []
with open(CSV_FILENAME, 'r', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in rows:
        raw_text.append(row)

value_text = []
for text in raw_text:
    value_text.append('(' + ','.join(['null' if e == '' \
        else f"\'{e}\'" if i not in [9,10] else e for i,e \
        in enumerate(text[:-1])]) + ')')

knights_insert_text = ','.join(value_text)

# process entries for roles
# 500 - 515: 76
# 516 - 526: 77
# 527 - 542: 75
value_text = []
for x in range(500, 543):
    value_text.append('(' + ','.join([str(x), '76' \
        if x < 516 else '77' if x < 527 else '75']) + ')')
    
role_insert_text = ','.join(value_text)

# connect to database
con = sqlite3.connect(DB_FILENAME)
cur = con.cursor()
# _ = cur.execute(INSERT_KNIGHTS + knights_insert_text)
# _ = cur.execute(INSERT_KR + role_insert_text)
_ = cur.execute(INSERT_FIVE)


# COMMIT: DO NOT UNCOMMENT THIS LINE UNTIL YOU'RE READY
#con.commit()

# Verify, run a select query
out = cur.execute("SELECT * from CouncilsView where fs_name is not null")
for o in out.fetchall():
    print(o)
print('')

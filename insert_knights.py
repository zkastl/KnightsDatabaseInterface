import csv
import sqlite3

CSV_FILENAME = './entry_script.csv'
DB_FILENAME = './ok_knights_directory.db'

SELECT_TEXT = "SELECT * FROM knights"

INSERT_TEXT = "INSERT INTO \"knights\" (first_name, middle_name,\
    last_name, address, city, state, zipcode, email, primary_phone,\
    council, deceased) VALUES "

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

v = ','.join(value_text)

con = sqlite3.connect(DB_FILENAME)
cur = con.cursor()
_ = cur.execute(INSERT_TEXT + v)
#con.commit()

out = cur.execute(SELECT_TEXT)

for o in out.fetchall():
    print(o)
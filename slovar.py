import psycopg2

conn = psycopg2.connect(
        host="127.0.0.1",
        database="my_slovar",
        user="postgres",
        password="tashkent88",
        port=5432
    )

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS slovar (
    id SERIAL PRIMARY KEY,
    english_word VARCHAR(100),
    russian_word VARCHAR(100)
);
""")
conn.commit()

# cursor.execute("INSERT INTO slovar (english_word, russian_word) VALUES (%s, %s)", ('Hello', 'Привет'))
# conn.commit()


cursor.execute("SELECT * FROM slovar;")
records = cursor.fetchall()

for record in records:
    print(record)




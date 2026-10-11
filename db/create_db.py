import sqlite3

# اتصال به دیتابیس (اگر وجود نداشته باشد، ساخته می‌شود)
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# ساخت جدول فیلم‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER,
    genre TEXT NOT NULL,
    rating REAL NOT NULL
)
""")

# اطلاعات فیلم‌ها
movies = [
    ("The Shawshank Redemption", 1994, "Drama", 9.3),
    ("The Godfather", 1972, "Crime", 9.2),
    ("The Dark Knight", 2008, "Action", 9.0),
    ("The Lord of the Rings: The Return of the King", 2003, "Action", 9.0),
    ("Pulp Fiction", 1994, "Crime", 8.9),
    ("Schindler's List", 1993, "Drama", 9.0),
    ("Inception", 2010, "Sci-Fi", 8.8),
    ("The Matrix", 1999, "Sci-Fi", 8.7),
    ("Interstellar", 2014, "Sci-Fi", 8.7),
    ("Se7en", 1995, "Thriller", 8.6),
    ("The Silence of the Lambs", 1991, "Thriller", 8.6),
    ("Saving Private Ryan", 1998, "Drama", 8.6),
    ("City of God", 2002, "Crime", 8.6),
    ("Terminator 2: Judgment Day", 1991, "Action", 8.6),
    ("Gladiator", 2000, "Action", 8.5),
    ("The Prestige", 2006, "Thriller", 8.5),
    ("Whiplash", 2014, "Drama", 8.5),
    ("Alien", 1979, "Sci-Fi", 8.5),
    ("The Departed", 2006, "Crime", 8.5),
    ("Back to the Future", 1985, "Sci-Fi", 8.5),
    ("Joker", 2019, "Crime", 8.4),
    ("The Truman Show", 1998, "Drama", 8.2),
    ("Top Gun: Maverick", 2022, "Action", 8.2),
    ("Shutter Island", 2010, "Thriller", 8.2),
    ("A Quiet Place", 2018, "Thriller", 7.5),
    ("Arrival", 2016, "Sci-Fi", 7.9),
    ("Mad Max: Fury Road", 2015, "Action", 8.1),
    ("The Social Network", 2010, "Drama", 7.8),
    ("Knives Out", 2019, "Crime", 7.9),
    ("Edge of Tomorrow", 2014, "Sci-Fi", 7.9),
]

# وارد کردن فیلم‌ها به دیتابیس
cursor.executemany("""
INSERT INTO movies (title, year, genre, rating)
VALUES (?, ?, ?, ?)
""", movies)

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()

print("Database created successfully!")
print("30 movies added to movies.db")
import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("imdb-sqlite")

def get_db():
    return sqlite3.connect("./movies.db")

@mcp.tool()
def search_movies(genre: str, min_rating: float):
    conn = get_db()
    # قبل اجرا دستورات باید بزنی
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT title, year, genre, rating
        FROM movies
        WHERE genre = ? AND rating >= ?
        ORDER BY rating DESC
        LIMIT 5
        """,
        (genre, min_rating)
    )
    # دریافت نتایج
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "title": r[0],
            "year": r[1],
            "genre": r[2],
            "rating": r[3]
        }
        for r in rows
    ]

if __name__ == "__main__":
    mcp.run()
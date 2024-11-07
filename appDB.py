import sqlite3

# ---- Connecting the Database and Establishing it ----
conn = sqlite3.connect(":memory:")
c = conn.cursor()

# ---- Creating the Books Table ----
c.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY,  
        title TEXT NOT NULL,      
        author TEXT NOT NULL,     
        category TEXT NOT NULL,   
        status TEXT CHECK(status IN ('Want to Read', 'Currently Reading', 'Read')) DEFAULT 'Want to Read',  
        rating INTEGER CHECK(rating BETWEEN 1 AND 5)  
    )
""")

# ---- Function to Add a New Book to the Database ----
def addBook(title, author, category):
    with conn:
        c.execute(
            "INSERT INTO Books (title, author, category) VALUES (:title, :author, :category)", 
            {"title": title, "author": author, "category": category}
        )

# ---- Function to Update the Status of a Book ----
def updateStatus(bookID, newStatus):
    with conn:
        c.execute(
            "UPDATE Books SET status = :status WHERE id = :id", 
            {"status": newStatus, "id": bookID}
        )

# ---- Function to Add or Update the Rating of a Book ----
def addRating(bookID, rating):
    with conn:
        c.execute(
            "UPDATE Books SET rating = :rating WHERE id = :id", 
            {"rating": rating, "id": bookID}
        )

# ---- Function to Retrieve Books by Status ----
def bookByStatus(status):
    with conn:
        c.execute(
            "SELECT id, title, author, category, rating FROM Books WHERE status = :status", 
            {"status": status}
        )
        books = c.fetchall()
        return books

# ---- Function to Retrieve All Books ----
def getBooks():
    c.execute("SELECT * FROM Books")
    rows = c.fetchall()
    books = []

    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "category": row[3],
            "status": row[4],
            "rating": row[5]
        })
    return books

# ---- Function to Retrieve Details of a Specific Book by ID ----
def getBookDetails(bookID):
    c.execute("SELECT * FROM Books WHERE id = :id", {"id": bookID})
    book = c.fetchone()
    if book:
        return {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "category": book[3],
            "status": book[4],
            "rating": book[5]
        }
    return None
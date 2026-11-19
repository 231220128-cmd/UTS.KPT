import asyncio
from database import init_db, fetch_one, execute

BOOKS = [
    ("Laskar Pelangi", "Andrea Hirata", "Novel", 85000, 12),
    ("Bumi", "Tere Liye", "Fantasi", 92000, 10),
    ("Negeri 5 Menara", "Ahmad Fuadi", "Novel", 78000, 8),
    ("Filosofi Teras", "Henry Manampiring", "Pengembangan Diri", 99000, 15),
    ("Atomic Habits", "James Clear", "Pengembangan Diri", 115000, 9),
    ("Sapiens", "Yuval Noah Harari", "Sejarah", 145000, 7),
    ("The Psychology of Money", "Morgan Housel", "Keuangan", 105000, 11),
    ("Buku Pintar Python", "Budi Raharjo", "Teknologi", 125000, 6),
    ("Belajar FastAPI", "Andi Prasetyo", "Teknologi", 110000, 5),
    ("Dilan 1990", "Pidi Baiq", "Novel", 89000, 13),
]

async def main():
    await init_db()
    inserted = 0
    for title, author, category, price, stock in BOOKS:
        existing = await fetch_one("SELECT id FROM books WHERE title = ?", (title,))
        if existing:
            continue
        await execute(
            """INSERT INTO books (title, author, category, price, stock)
               VALUES (?, ?, ?, ?, ?)""",
            (title, author, category, price, stock),
        )
        inserted += 1
    print(f"Seed selesai. {inserted} buku baru ditambahkan.")

if __name__ == "__main__":
    asyncio.run(main())

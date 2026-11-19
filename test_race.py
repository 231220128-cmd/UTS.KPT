import asyncio
import httpx
from database import get_db, init_db

BASE_URL = "http://127.0.0.1:8000"

async def set_stock(book_id: int, stock: int):
    db = await get_db()
    try:
        await db.execute("UPDATE books SET stock = ? WHERE id = ?", (stock, book_id))
        await db.commit()
    finally:
        await db.close()

async def main():
    await init_db()
    book_id = int(input("Masukkan ID buku yang akan diuji: "))
    await set_stock(book_id, 1)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15) as client:
        payload = {"book_id": book_id, "quantity": 1}
        results = await asyncio.gather(
            client.post("/transactions/", json=payload),
            client.post("/transactions/", json=payload),
        )
        for index, response in enumerate(results, start=1):
            print(f"Request {index}: HTTP {response.status_code} - {response.text}")

    db = await get_db()
    try:
        cursor = await db.execute("SELECT stock FROM books WHERE id = ?", (book_id,))
        row = await cursor.fetchone()
        print("Sisa stok setelah pengujian:", row["stock"])
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())

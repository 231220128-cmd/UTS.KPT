from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routes.resource import router as books_router
from routes.transaction import router as transactions_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Toko Buku API",
    description="API CRUD buku dan transaksi menggunakan FastAPI, SQLite, aiosqlite, dan BackgroundTasks.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(books_router)
app.include_router(transactions_router)

@app.get("/")
async def root():
    return {"message": "Toko Buku API aktif", "docs": "/docs"}

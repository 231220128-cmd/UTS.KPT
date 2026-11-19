from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    author: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=60)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=150)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[str] = Field(default=None, min_length=1, max_length=60)
    price: Optional[float] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str
    price: float
    stock: int
    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(BaseModel):
    book_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class TransactionResponse(BaseModel):
    id: int
    book_id: int
    quantity: int
    total_price: float
    status: str
    created_at: Optional[datetime] = None

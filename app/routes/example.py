from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(tags=["examples"])

class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float

# In-memory storage for demo
items_db = []

@router.get("/items", response_model=List[Item])
async def get_items():
    return items_db

@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", response_model=Item)
async def create_item(item: Item):
    items_db.append(item)
    return item

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    item_index = next((i for i, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_index] = updated_item
    return updated_item

@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    item_index = next((i for i, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_index]
    return {"message": "Item deleted successfully"}

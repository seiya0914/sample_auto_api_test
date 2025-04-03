from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Sample API Server")

# データモデルの定義
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

class User(BaseModel):
    id: int
    name: str
    email: str

# インメモリデータストア
items_db = {
    1: Item(id=1, name="ノートパソコン", description="高性能ノートPC", price=150000.0),
    2: Item(id=2, name="スマートフォン", description="最新モデル", price=98000.0),
    3: Item(id=3, name="ワイヤレスイヤホン", description="ノイズキャンセリング機能付き", price=25000.0),
    4: Item(id=4, name="スマートウォッチ", description="健康管理機能搭載", price=35000.0),
    5: Item(id=5, name="タブレット", description="10インチディスプレイ", price=45000.0)
}

users = [
    User(id=1, name="John Doe", email="john@example.com"),
    User(id=2, name="Jane Smith", email="jane@example.com"),
    User(id=3, name="John Smith", email="john.smith@example.com"),
]

@app.get("/")
def read_root():
    return {"message": "Welcome to Sample API Server"}

@app.get("/items/", response_model=List[Item])
def read_items():
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.id] = item
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id != item.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"}

@app.get("/api/users", response_model=List[User])
def get_users():
    return users

@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/search", response_model=List[User])
def search_users(name: str = Query(..., description="The name to search for")):
    if not name:
        raise HTTPException(status_code=400, detail="Name parameter is required")
    
    matched_users = [user for user in users if name.lower() in user.name.lower()]
    return matched_users

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

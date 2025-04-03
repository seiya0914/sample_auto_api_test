from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Sample API Server")

# データモデルの定義
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: str

# インメモリデータストア
items_db = {
    1: Item(id=1, name="ノートパソコン", description="高性能ノートPC", price="100000.0"),
    2: Item(id=2, name="スマートフォン", description="最新モデル", price="80000.0"),
    3: Item(id=3, name="ワイヤレスイヤホン", description="ノイズキャンセリング機能付き", price="20000.0"),
    4: Item(id=4, name="スマートウォッチ", description="健康管理機能搭載", price="30000.0"),
    5: Item(id=5, name="タブレット", description="10インチディスプレイ", price="40000.0")
}

@app.get("/")
def read_root():
    return {"message": "Welcome to Sample API Server"}

@app.get("/api/items/", response_model=List[Item])
def read_items():
    return list(items_db.values())

@app.get("/api/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/api/items/", response_model=Item)
def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.id] = item
    return item

@app.put("/api/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id != item.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

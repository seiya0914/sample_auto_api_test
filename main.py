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
    price: float

# インメモリデータストア
items_db = {
    1: Item(id=1, name="ノートパソコン", description="高性能ノートPC", price=150000.0),
    2: Item(id=2, name="スマートフォン", description="最新モデル", price=98000.0),
    3: Item(id=3, name="ワイヤレスイヤホン", description="ノイズキャンセリング機能付き", price=25000.0),
    4: Item(id=4, name="スマートウォッチ", description="健康管理機能搭載", price=35000.0),
    5: Item(id=5, name="タブレット", description="10インチディスプレイ", price=45000.0)
}

@app.get("/")
def read_root():
    # 意図的なエラー: レスポンスの形式が異なる
    return "Welcome to Sample API Server"  # オブジェクトではなく文字列を返す

@app.get("/items/", response_model=List[Item])
def read_items():
    # 意図的なエラー: レスポンスの形式が異なる
    return [{"item": item} for item in items_db.values()]  # 余分なitemキーを追加

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    # 意図的なエラー: レスポンスの形式が異なる
    item = items_db[item_id]
    return {
        "id": str(item.id),  # 数値を文字列に変換
        "name": item.name,
        "description": item.description,
        "price": str(item.price)  # 数値を文字列に変換
    }

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    # 意図的なエラー1: 新規作成時のステータスコードを201ではなく200で返す
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.id] = item
    return item  # 201を返すべきところを200で返している

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    # 意図的なエラー2: IDの不一致チェックを省略
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    # item_idとitem.idの一致チェックを省略（OpenAPI仕様違反）
    items_db[item_id] = item
    # 意図的なエラー: レスポンスの形式が異なる
    return {
        "id": str(item.id),  # 数値を文字列に変換
        "name": item.name,
        "description": item.description,
        "price": str(item.price)  # 数値を文字列に変換
    }

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # 意図的なエラー3: 404エラーを返すべき場合に500エラーを返す
    if item_id not in items_db:
        raise HTTPException(status_code=500, detail="Internal server error")  # 本来は404を返すべき
    del items_db[item_id]
    # 意図的なエラー: レスポンスの形式が異なる
    return {"message": 200}  # 文字列ではなく数値を返す

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

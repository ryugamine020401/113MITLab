from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from models import TortoiseItem, StudentScoreItem
from tortoise.contrib.fastapi import register_tortoise
from config import TORTOISE_ORM
from dotenv import load_dotenv
import os
# 加載 .env 檔案
load_dotenv()

# 獲取環境變數
DB_PWD = os.getenv('DB_PASSWORD')
DB_URL = os.getenv('DB_URL')


# 定義 Pydantic 模型，用於請求驗證
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class PydanticItem(BaseModel):
    name : str
    description : Union[str, None] = None
    price : int

app = FastAPI()

@app.get("/")   # 定義 / path 的 get方法
async def read_root():
    return {"Hello": "World"}   # return一個JSON

# POST 方法，用於新增資料到資料庫
@app.post("/")
async def create_item(item: PydanticItem):
    # 使用 Tortoise ORM 創建記錄
    new_item = await TortoiseItem.create(
        name=item.name,
        description=item.description,
        price=item.price
    )
    return {"id": new_item.id, "message": "Item created successfully"}

@app.get("/items/{item_id}")    # 定義path /items/{item_id}
async def read_item(item_id: int, q: Union[str, None] = None):
    """
    item_id: int
    q: Union[str, None] = None  定義一個可選的查詢參數 q Type 是 str或None 預設None
    """
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    定義了/items/{item_id}的put方法
    item_id在url中
    item和上面加入的class有關
    分別定義了name, price和is_offer
    """
    return {"item_name": item.name, "item_id": item_id}


# ------------------------------ SQLite -------------------------
# register_tortoise(
#     app,
#     db_url="sqlite://db.sqlite3",       # 確保路徑正確，特別是在 Linux 上注意相對路徑
#     modules={"models": ["models"]},     # 確保模型模組路徑正確
#     generate_schemas=True,              # 自動生成資料表結構
#     add_exception_handlers=True,
# )

# -------------------------- MySQL ------------------------------
class StudentScoreItemPydantic(BaseModel):
    """
    Pydantic的Model
    """
    name : str
    subject : Union[str, None] = "Math"
    midterm_score : Union[float, None] = 0.0
    final_score : Union[float, None] = 0.0


@app.get("/score/")
async def list_score():
    """
    get列出所有內容
    """
    instance = await StudentScoreItem.all()
    return instance

@app.post("/score/")
async def uploadscore(item: StudentScoreItemPydantic):
    instance = await StudentScoreItem.create(
        name = item.name,
        subject = item.subject,
        midterm_score = item.midterm_score,
        final_score = item.final_score,
    )
    return {"id": instance.id, "message": "Item created successfully"}

register_tortoise(
    app,
    config = TORTOISE_ORM,
    # db_url=DB_URL,
    # modules={"models": ["models"]},
    generate_schemas = True,  # 自動生成資料表
    add_exception_handlers = True,
)

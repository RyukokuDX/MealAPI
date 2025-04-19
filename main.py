from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# データベースの設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/menu.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# モデルの定義
class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    restaurant = Column(String, index=True)
    menu_name = Column(String)
    description = Column(Text, nullable=True)

# データベースの作成
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MealAPI")

# データベースセッションの依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "MealAPIへようこそ"}

@app.get("/restaurants")
async def get_restaurants():
    return {
        "restaurants": [
            "22号館食堂",
            "清和館食堂",
            "青志館食堂",
            "4号館ミール&カフェ",
            "3号館フードコート"
        ]
    }

@app.get("/menu/{restaurant}")
async def get_menu(restaurant: str):
    db = SessionLocal()
    try:
        menus = db.query(Menu).filter(Menu.restaurant == restaurant).all()
        if not menus:
            raise HTTPException(status_code=404, detail="メニューが見つかりません")
        return {"restaurant": restaurant, "menus": menus}
    finally:
        db.close() 
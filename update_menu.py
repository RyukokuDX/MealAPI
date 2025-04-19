import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Menu, Base
import logging

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# データベースの設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/menu.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def update_menu():
    try:
        # 生協のサイトからデータを取得
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(
            "https://west2-univ.jp/sp/index.php?t=650521",
            headers=headers
        )
        response.raise_for_status()

        # HTMLの解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # データベースセッションの開始
        db = SessionLocal()
        
        # 既存のメニューを削除
        db.query(Menu).delete()
        
        # 新しいメニューを追加（ここで実際のスクレイピングロジックを実装）
        # 例としてダミーデータを追加
        restaurants = [
            "22号館食堂",
            "清和館食堂",
            "青志館食堂",
            "4号館ミール&カフェ",
            "3号館フードコート"
        ]
        
        for restaurant in restaurants:
            menu = Menu(
                restaurant=restaurant,
                menu_name="サンプルメニュー",
                description="メニューの説明"
            )
            db.add(menu)
        
        # 変更を保存
        db.commit()
        logging.info("メニューの更新が完了しました")
        
    except Exception as e:
        logging.error(f"メニューの更新中にエラーが発生しました: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_menu() 
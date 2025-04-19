#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import shutil
import logging

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def backup_database():
    """データベースファイルをバックアップする関数"""
    try:
        # 現在の日時を取得
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        # 元のDBファイルとバックアップ先のパス
        db_path = "/app/data/menu.db"
        backup_dir = "/app/data/backups"
        backup_path = f"{backup_dir}/menu_{timestamp}.db"
        
        # バックアップディレクトリが存在しない場合は作成
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # ファイルをコピー
        shutil.copy2(db_path, backup_path)
        
        # 古いバックアップを削除（7日以上経過したもの）
        clean_old_backups(backup_dir, days=7)
        
        logging.info(f"データベースバックアップが完了しました: {backup_path}")
        
    except Exception as e:
        logging.error(f"バックアップ中にエラーが発生しました: {str(e)}")

def clean_old_backups(backup_dir, days=7):
    """古いバックアップファイルを削除する関数"""
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=days)
    
    for filename in os.listdir(backup_dir):
        if filename.startswith("menu_") and filename.endswith(".db"):
            file_path = os.path.join(backup_dir, filename)
            file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mod_time < cutoff:
                os.remove(file_path)
                logging.info(f"古いバックアップを削除しました: {file_path}")

if __name__ == "__main__":
    backup_database() 
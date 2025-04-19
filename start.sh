#!/bin/bash

# cronサービスを開始
service cron start

# FastAPIアプリケーションを開始
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 
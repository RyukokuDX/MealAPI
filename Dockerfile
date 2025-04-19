FROM debian:bullseye

# 作業ディレクトリを設定
WORKDIR /app

# タイムゾーンの設定（JSTに確実に設定）
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && \
    rm -f /etc/localtime && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# 必要なパッケージのインストール
RUN apt-get install -y cron python3 python3-pip curl vim-tiny && \
    rm -rf /var/lib/apt/lists/*

# Pythonパッケージのインストール
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# アプリケーションのコピー
COPY . .

# cronの設定
COPY crontab /etc/cron.d/app-cron
RUN echo "" >> /etc/cron.d/app-cron && \
    chmod 0644 /etc/cron.d/app-cron && \
    crontab /etc/cron.d/app-cron

# ログファイルを作成
RUN touch /var/log/cron.log

# データベースディレクトリの作成
RUN mkdir -p /app/data

# 起動スクリプトの作成と権限設定
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# FastAPIアプリ用のポート
EXPOSE 8000

# 起動スクリプトを実行
CMD ["/app/start.sh"] 
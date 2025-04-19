# MealAPI
生協のメニューを返すapiで、apiの練習.
RDXのサーバーにdockerでwebサーバーを建て、
そこにapi経由でメッセンジャーボットから情報を取得する.
生協のサイト：
[生協のサイト](https://west2-univ.jp/sp/ryukoku.php)
から
``` bash
curl -A "Mozilla/5.0" "https://west2-univ.jp/sp/index.php?t=650521"
```
の様にしてhtmlファイルを取得、
それを解析してdbに
- 22号館食堂
- 清和館食堂
- 青志館食堂
- 4号館ミール&カフェ
- 3号館フードコート
のおすすめメニューを追加.

これをapiで読み取る.
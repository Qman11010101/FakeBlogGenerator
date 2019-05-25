from datetime import datetime
import os
import config
from requests_oauthlib import OAuth1Session

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#ファイルパスの合成
print("記事のタイトルを入力してください(記事に書いたものと同じにしてください)")
title_atc = input(">> ") #タイトル取得
current_time = datetime.now().strftime("%Y%m%d%H%M%S") #日付・時刻取得
crtimestr = str(current_time)

file_path = f"[ブログ全体が置いてあるディレクトリのパスに置き換えてください]/articles/{crtimestr}.html" #ファイルパス合成
file_code = f"./articles/{crtimestr}.html" #コード上のファイルパス文字列

#トップページの合成
day_str = str(datetime.now().strftime("%Y-%m-%d")) #yyyy-mm-dd形式で日付テキストを生成

index_path = "[ブログ全体が置いてあるディレクトリのパスに置き換えてください]/blog_index.html" #ファイル生成(初回)/上書き用パス
insert_code = '<hr><div class="list_content"><p>' + day_str + '</p><h1><a href="' + file_code + '">' + title_atc + '</a></h1></div>' #挿入するコード

# top1.html
with open("assets/top1.html", mode="r", encoding="utf-8") as f:
    top1 = f.read()

# insert_code
if os.path.isfile("assets/insert_code_file.html"):
    with open("assets/insert_code_file.html", mode="r", encoding="utf-8") as f:
        conv = f.read()
else:
    conv = ""

with open("assets/insert_code_file.html", mode="w", encoding="utf-8") as f:
    icf = insert_code + "\n" + conv
    f.write(icf)

# top2.html
with open("assets/top2.html", mode="r", encoding="utf-8") as f:
    top2 = f.read()

# 以上の順番で合成、改行は不要
# 合成したものをindex_pathに保存
with open(index_path, mode="w", encoding="utf-8") as f:
    f.write(top1 + icf + top2)


#記事の合成

# (article_base.htmlに記事そのまま書く)
# 以下の順番で合成、改行は不要
# 1.html
with open("assets/1.html", mode="r", encoding="utf-8") as f:
    t1 = f.read()

# title_atc

# 2.html
with open("assets/2.html", mode="r", encoding="utf-8") as f:
    t2 = f.read()

# article_base.html
with open("assets/article_base.html", mode="r", encoding="utf-8") as f:
    atc = f.read()

# 3.html
with open("assets/3.html", mode="r", encoding="utf-8") as f:
    t3 = f.read()

# 合成したものをfile_pathに保存
with open(file_path, mode="w", encoding="utf-8")as f:
    f.write(t1 + title_atc + t2 + atc + t3)

#Twitterに更新通知をツイートする
endpoint = "https://api.twitter.com/1.1/statuses/update.json"
tweet = "ブログを更新しました: " + title_atc + " [ブログが置いてあるディレクトリのURLに置き換えてください]/articles/" + crtimestr + ".html"
params = {"status": tweet}
twAuth = OAuth1Session(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
postReq = twAuth.post(endpoint, params = params)
if postReq.status_code != 200:
    print("HTTP Status Code:" + str(postReq.status_code))
    print("エラーが発生した可能性があります。")
    print("articleフォルダ内の最新記事とblog_index.htmlにある最新記事へのリンクを削除し、再試行してください。")
    print("もしくは、更新通知のみを手動で行ってください。")
    input("Enterを押すとプログラムが終了します。")
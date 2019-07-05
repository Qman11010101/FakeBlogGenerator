from datetime import datetime
import os
import configparser
import sys
from requests_oauthlib import OAuth1Session
from distutils.dir_util import copy_tree

# 現ディレクトリ
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# config.ini読み込み
config = configparser.ConfigParser()
config.read("config.ini")

# ファイルパス・Twitterトークン定義
blogpath = config["path"]["blog_folder"]
blogurl = config["path"]["blog_url"]
ckey = config["twitter"]["consumer_key"]
csec = config["twitter"]["consumer_secret"]
atkn = config["twitter"]["access_token"]
asec = config["twitter"]["access_secret"]

# ディレクトリ生成
os.chdir(blogpath)
os.makedirs("blog/", exist_ok=True)
os.chdir("blog/")
os.makedirs("articles/", exist_ok=True)
os.makedirs("pictures/", exist_ok=True)
os.chdir(os.path.dirname(os.path.abspath(__file__))) # 戻ってくる

# ファイルパスの合成
print("記事のタイトルを入力してください")
title_atc = input(">> ") # タイトル取得
current_time = datetime.now().strftime("%Y%m%d%H%M%S") # 日付・時刻取得
crtimestr = str(current_time) # 時間の文字列化
title_code = "<h1>{}</h1>\n".format(title_atc) # タイトル生成

file_path = f"{blogpath}blog/articles/{crtimestr}.html" # 記事ファイルパス合成
file_code = f"./articles/{crtimestr}.html" # コード上に挿入するファイルパス文字列

# トップページの合成
day_str = str(datetime.now().strftime("%Y-%m-%d")) # yyyy-mm-dd形式で日付テキストを生成

index_path = f"{blogpath}blog/blog_index.html" # ファイル生成(初回)/上書き用パス
insert_code = f'<hr><div class="list_content"><p>{day_str}</p><h1><a href="{file_code}">{title_atc}</a></h1></div>' # 挿入するコード

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

# 合成したものをindex_pathに保存
with open(index_path, mode="w", encoding="utf-8") as f:
    f.write(top1 + icf + top2)

# 記事の合成

# 1.html
with open("assets/1.html", mode="r", encoding="utf-8") as f:
    t1 = f.read()

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
    f.write(t1 + title_atc + t2 + title_code + atc + t3)

# 画像を移動
copy_tree("pictures", f"{blogpath}blog/pictures")

input("ファイルの準備ができました。サーバーへのアップロードが完了したら、キーを押して続行してください。Twitterに更新通知が投稿されます")

# Twitterに更新通知をツイートする
endpoint = "https://api.twitter.com/1.1/statuses/update.json"
tweet = "ブログを更新しました: " + title_atc + f" {blogurl}blog/articles/" + crtimestr + ".html"
params = {"status": tweet}
twAuth = OAuth1Session(ckey, csec, atkn, asec)
postReq = twAuth.post(endpoint, params = params)
if postReq.status_code != 200: # ここも自動化できたらうれしい
    print("HTTP Status Code:" + str(postReq.status_code))
    print("エラーが発生した可能性があります。")
    print("articleフォルダ内の最新記事とblog_index.htmlにある最新記事へのリンクを削除し、再試行してください。")
    print("もしくは、更新通知のみを手動で行ってください。")
    input("Enterを押すとプログラムが終了します。")
    sys.exit()
input("更新通知が正常に投稿されました。キーを押して終了します")
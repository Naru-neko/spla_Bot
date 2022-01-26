
import urllib
import codecs
from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
import http
from http.cookiejar import CookieJar
import json
import os
import pandas as pd

# 引数のJSONデータを戦績ごとにファイルに保存
def saveButtleResults(x_jsonData):

    # /api/results で取得した results 項目を取得
    p_jsonData = x_jsonData['results']

    # 改行コードを削除
    p_jsonData = json.dumps(p_jsonData, ensure_ascii=False).replace("\\n", "")

    # Data Frame に変換
    p_df = pd.read_json(p_jsonData)

    # battle_number を抜き出す
    p_bn = p_df['battle_number']

    '''
    p_battle_number = p_bn[0] #最新バトル
    # 取得する結果の API を作成
    p_api = "https://app.splatoon2.nintendo.net/api/results/" + str(p_battle_number)
    # 結果を取得
    p_results = getJson(p_api)
    # 出力ファイル名
    p_outputFilePath = "/home/shoma/Discord_Bot/result/" + str(p_battle_number) + ".json"
    # この戦績ファイルが既に存在するか確認、なかったら作成・書き込み
    if not(os.path.exists(p_outputFilePath)) :
        p_outputFile = codecs.open(p_outputFilePath, "w", encoding="utf-8")
        json.dump(p_results, p_outputFile, ensure_ascii=False, indent=4, sort_keys=True)
        p_outputFile.close()
    '''

    for p_battle_number in p_df['battle_number']:
        # 取得する結果の API を作成
        p_api = "https://app.splatoon2.nintendo.net/api/results/" + str(p_battle_number)
        # 結果を取得
        p_results = getJson(p_api)
        # 出力ファイル名
        p_outputFilePath = "/home/shoma/Discord_Bot/result/" + str(p_battle_number) + ".json"
        # この戦績ファイルが既に存在するか確認、なかったら作成・書き込み
        if not(os.path.exists(p_outputFilePath)) :
            p_outputFile = codecs.open(p_outputFilePath, "w", encoding="utf-8")
            json.dump(p_results, p_outputFile, ensure_ascii=False, indent=4, sort_keys=True)
            p_outputFile.close()

def getJson(x_url): # UrlにアクセスしJsonを取得
    # 自分のイカリングの API key を入力
    p_cookie = "iksm_session=297e59ec8b8e648b2ea0b4ff9ae4a1f2679c1228"
    p_opener = build_opener(HTTPCookieProcessor(CookieJar()))
    p_opener.addheaders.append(("Cookie", p_cookie))
    p_res = p_opener.open(x_url)
    return json.load(p_res)

saveButtleResults(getJson("https://app.splatoon2.nintendo.net/api/results"))
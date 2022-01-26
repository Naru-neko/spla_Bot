import urllib
import codecs
from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import json
import pandas as pd
import time
import discord
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#=============================================================================================-

client = discord.Client()

SPREADSHEET_KEY = '1MgryGoC-cnsdatYlMHR-EUH5Y2MaJLIOLSuS6ESbh64'

    
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('./spla-bot-spread.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログイン
gc = gspread.authorize(credentials)

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

TOKEN = worksheet.acell('B1').value


# 起動時に動作する処理
@client.event
async def on_ready():

    
    
    while True:

        RESULT_CHANNEL_ID = int(worksheet.acell('B2').value) #group or other channel
        AUTHOR_CHANNEL_ID = int(worksheet.acell('B3').value) #author self channel
        LAST_RESULT = int(worksheet.acell('B5').value)
        GROUP_FLAG = int(worksheet.acell('B6').value)

        if GROUP_FLAG == 0:
            result_channel = client.get_channel(AUTHOR_CHANNEL_ID) #send to author
        else:
            result_channel = client.get_channel(RESULT_CHANNEL_ID) #send to group

        author_channel = client.get_channel(AUTHOR_CHANNEL_ID)


        try:

            num = await get_num()

            if num > LAST_RESULT:
                worksheet.update_cell(5,2, str(num))
                await push_msg(result_channel)

            else:
                pass


        except urllib.error.HTTPError:
            if iksm_flag == 0:
                await author_channel.send('Probably iksm is changed.\nCheck it.')
                iksm_flag = 1
            continue

        except AttributeError:
            if channel_flag == 0:
                await author_channel.send('Probably channel_id is changed.\nCheck it.')
                channel_flag = 1
            continue

        else:
            iksm_flag = 0
            channel_flag = 0

        finally:
            time.sleep(5)



async def get_num():

    p_jsonData = await getJson("https://app.splatoon2.nintendo.net/api/results")
    p_jsonData = p_jsonData['results']
    p_jsonData = json.dumps(p_jsonData, ensure_ascii=False).replace("\\n", "")

    # Data Frame に変換
    p_df = pd.read_json(p_jsonData)
    #print(p_df)

    # battle_number を抜き出す
    p_bn = p_df['battle_number']
    p_battle_number = p_bn[0] #最新バトル
    return p_battle_number




async def make_list(data, mode):

    data_list = list()
    
    if mode == 0:
        for x in data:

            data_list.append(x['player']['nickname'])
            data_list.append(x['player']['player_rank'])
            data_list.append(x['kill_count'])
            data_list.append(x['assist_count'])
            data_list.append(x['death_count'])
            data_list.append(x['special_count'])
            data_list.append(x['game_paint_point'])

    else:
        data_list.append(data['player']['nickname'])
        data_list.append(data['player']['player_rank'])
        data_list.append(data['kill_count'])
        data_list.append(data['assist_count'])
        data_list.append(data['death_count'])
        data_list.append(data['special_count'])
        data_list.append(data['game_paint_point'])

    return data_list



async def push_msg(channel): 

    results = await get_result(await getJson("https://app.splatoon2.nintendo.net/api/results"))
    
    #myteam
    my_team_result = await make_list(results['my_team_members'],0)
    #print('MY_TEAM')

    my_result = await make_list(results['player_result'],1)

    #otherteam
    other_team_result = await make_list(results['other_team_members'],0)
    #print('OTHER_TEAM')


    if results['rule']['name'] == 'ナワバリバトル':
        my_team_score = results['my_team_percentage']
        other_team_score = results['other_team_percentage']
    else:
        my_team_score = results['my_team_count']
        other_team_score = results['other_team_count']




    text = '''
==================
[{}]
ルール：{}
ステージ：{}
カウント： {} vs {}
==================\n
[{}]
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)\n
[{}]
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)
● {}(RANK{})
    {}({})キル, {}デス, {}スペ, (塗り{}p)
'''.format(results['game_mode']['name'],
        results['rule']['name'],
        results['stage']['name'],
        my_team_score,
        other_team_score,
        results['my_team_result']['name'],
        my_team_result[0],
        my_team_result[1],
        my_team_result[2],
        my_team_result[3],
        my_team_result[4],
        my_team_result[5],
        my_team_result[6],
        my_team_result[7],
        my_team_result[8],
        my_team_result[9],
        my_team_result[10],
        my_team_result[11],
        my_team_result[12],
        my_team_result[13],
        my_team_result[14],
        my_team_result[15],
        my_team_result[16],
        my_team_result[17],
        my_team_result[18],
        my_team_result[19],
        my_team_result[20],
        my_result[0],
        my_result[1],
        my_result[2],
        my_result[3],
        my_result[4],
        my_result[5],
        my_result[6],
        results['other_team_result']['name'],
        other_team_result[0],
        other_team_result[1],
        other_team_result[2],
        other_team_result[3],
        other_team_result[4],
        other_team_result[5],
        other_team_result[6],
        other_team_result[7],
        other_team_result[8],
        other_team_result[9],
        other_team_result[10],
        other_team_result[11],
        other_team_result[12],
        other_team_result[13],
        other_team_result[14],
        other_team_result[15],
        other_team_result[16],
        other_team_result[17],
        other_team_result[18],
        other_team_result[19],
        other_team_result[20],
        other_team_result[21],
        other_team_result[22],
        other_team_result[23],
        other_team_result[24],
        other_team_result[25],
        other_team_result[26],
        other_team_result[27])


    await channel.send(text)



    #------------------------------------------------------------------------------------------

    '''
    出力イメージ

    [レギュラーマッチ]
    ルール：ガチヤグラ
    ステージ：モンガラ
    カウント： 56 vs 46
    
    [WIN!]
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)

    [LOSE...]
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)
    - PLAYER(R31)
        10(2)k, 5d, 3sp, (1000p)

    '''

    '''
    レギュラーマッチ
    dict_keys(['my_team_result', 'battle_number', 'player_rank', 'game_mode', 'star_rank',
     'win_meter', 'my_team_percentage', 'type', 'rule', 'other_team_result', 'my_team_members', 
     'weapon_paint_point', 'stage', 'start_time', 'other_team_percentage', 'player_result', 
     'other_team_members'])
    
    ガチマ
    dict_keys(['x_power', 'stage', 'elapsed_time', 'player_result', 'game_mode', 'crown_players', 
    'udemae', 'my_team_result', 'estimate_x_power', 'other_team_result', 'weapon_paint_point', 
    'battle_number', 'rank', 'start_time', 'my_team_members', 'other_team_count', 'other_team_members', 
    'player_rank', 'star_rank', 'rule', 'estimate_gachi_power', 'my_team_count', 'type'])

    '''
    #---------------------------------------------------------------------------------------------




# 引数のJSONデータを戦績ごとにファイルに保存
async def get_result(x_jsonData):

    # /api/results で取得した results 項目を取得
    p_jsonData = x_jsonData['results']

    # 改行コードを削除
    p_jsonData = json.dumps(p_jsonData, ensure_ascii=False).replace("\\n", "")

    # Data Frame に変換
    p_df = pd.read_json(p_jsonData)
    #print(p_df)

    # battle_number を抜き出す
    p_bn = p_df['battle_number']
    p_battle_number = p_bn[0] #最新バトル

    # 取得する結果の API を作成
    p_api = "https://app.splatoon2.nintendo.net/api/results/" + str(p_battle_number)
    

    # 結果を取得
    p_json_results = await getJson(p_api)

    return p_json_results



async def getJson(x_url): # UrlにアクセスしJsonを取得
    p_opener = build_opener(HTTPCookieProcessor(CookieJar()))
    IKSM = worksheet.acell('B4').value
    p_opener.addheaders.append(("Cookie", IKSM))
    p_res = p_opener.open(x_url)
    return json.load(p_res)


client.run(TOKEN)
import requests
import json
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials




SPREADSHEET_KEY = '1MgryGoC-cnsdatYlMHR-EUH5Y2MaJLIOLSuS6ESbh64'

    
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('./spla-bot-spread.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログイン
gc = gspread.authorize(credentials)

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

TOKEN = worksheet.acell('B1').value





def getStageInfo(index=0):
    '''
        ステージ情報
    '''
    links = ('gachi/now','gachi/next','league/now','leage/next','regular/now','regular/next')
    headers = {"User-Agent": "spla_stage_lool(twitter @waremono_0918)"}
    url = "https://spla2.yuu26.com/" + links[index]
    response = requests.get(url,headers=headers)
    dic = json.loads(response.text)
    dic = dic['result'][0]

    return "[ルール]\n{}\n[ステージ]\n● {}\n● {}".format(dic['rule'],dic['maps'][0],dic['maps'][1])

#clientオブジェクトの生成
client = discord.Client()

@client.event
async def on_ready():
    pass


@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.startswith('/コマンド一覧'):
        await message.channel.send('''/ガチマ\n現在のガチマのルール・ステ表示\n
/次ガチマ\n次のガチマのルール・ステ表示\n
/リグマ\n現在のリグマのルール・ステ表示\n
/次リグマ\n次のリグマのルール・ステ表示\n
/ナワバリ\n現在のナワバリのルール・ステ表示\n
/次ナワバリ\n次のナワバリのルール・ステ表示\n''')

    if message.content.startswith('/ガチマ'):
        m = getStageInfo(0)
        await message.channel.send(m)

    if message.content.startswith("/次ガチマ"):
        m = getStageInfo(1)
        await message.channel.send(m)

    if message.content.startswith("/リグマ"):
        m = getStageInfo(2)
        await message.channel.send(m)

    if message.content.startswith("/次リグマ"):
        m = getStageInfo(3)
        await message.channel.send(m)

    if message.content.startswith("/ナワバリ"):
        m = getStageInfo(4)
        await message.channel.send(m)

    if message.content.startswith("/次ナワバリ"):
        m = getStageInfo(5)
        await message.channel.send(m)

    if message.content.startswith("/channel_id"):
        await message.channel.send(str(message.channel.id))
    
    if message.content.startswith("/channel_author"):
        worksheet.update_cell(6,2, 0)
        await message.channel.send('changed result channel to author.')
    
    if message.content.startswith("/channel_group"):
        worksheet.update_cell(6,2, 1)
        await message.channel.send('changed result channel to group.')
    


client.run(TOKEN)
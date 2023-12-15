import discord
import datetime as dt


TOKEN = ''

# 接続に必要なオブジェクトを生成
client = discord.Client()

with open('./param.csv') as f:
    param = csv.reader(f)
    for row in param:
        if row[0] == 'TOKEN':
            TOKEN = row[1]
        elif row[0] == 'RESULT_CHANNEL_ID':
            RESULT_CHANNEL_ID = int(row[1])
        elif row[0] == 'AUTHOR_CHANNEL_ID':
            AUTHOR_CHANNEL_ID = int(row[1])
        elif row[0] == 'IKSM':
            IKSM = row[1]
        else:
            pass


# 起動時に動作する処理
@client.event
async def on_ready():

    while 1:
        await term()



async def term(): 

    channel = client.get_channel(AUTHOR_CHANNEL_ID)
    print('HOST_CONPUTER ' + str(dt.datetime.now()) + 'channel=' + str(AUTHOR_CHANNEL_ID),
          end='>')
    command = input()


    if command == 'say':
        await say(channel)
    elif command == 'help':
        await show_help()
    elif command == 'set_author_channel':
        await set_author_channel()
    elif command == 'show_author_channel':
        await show_author_channel()
    elif command == 
    else:
        pass



async def say(channel):
    
    text = input("Send message: ")
    print("Bot sent a message \'" + text + "\'\n")
    if text != None and text != '\n' and text != '^Z':
        await channel.send(text)
    else:
        pass



async def show_help():
    print('''
          say : change to sending message mode from bot\n
          help : show command list\n
          showchannel : show current channel ID\n
          setchannel : set new channel ID\n
          ''')



async def show_author_channel():
    print('current channel ID = ' + str(AUTHOR_CHANNEL_ID))



async def set_author_channel():

    print('current channel ID = ' + str(AUTHOR_CHANNEL_ID))
    AUTHOR_CHANNEL_ID = input('Enter the new channel ID: ')
    print('\n channel ID was chaneged to ' + str(AUTHOR_CHANNEL_ID)  + '\n')


client.run(TOKEN)

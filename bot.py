# @adityaraj7612

import os
from pyrogram import Client, filters
from pyrogram.types import *
from utils import *
import os.path
from urllib.request import urlopen, Request
import pytz
import time



Bot = Client(
    "Conan76-Simple-IPTV-m3u-to-Video-Bot",
    bot_token = "5561532834:AAEwk_vC8KmmcRKyPTe2XjZXC_1GG6DCaXk",
    api_id = 15668875,
    api_hash = "9126d3e935a1553bedf9bd822f3b4ad9"
)


START_TEXT = """<b><i>Hello</i></b> {}
<b><i>It's a Recording Bot Of Pokesensei.</i></b>

> `{}`

<b>Made by @PokeSensei</b>"""



HELP_TEXT = """<b><i>Hello</i></b> {}
<b><i>Here are The Commands which can be used in the BOT!</i></b>

> <b>Get This Help Module </b> <code>/help</code>

> <b>Get the List of Channels </b> <code>/channels</code>

> <b>Records Multi Audio TV Rips from streamLink </b> <code>/multirec CN 00:00:10 | Ben 10</code>

<b><i>Click on the Command to COPY</i></b>

<b>Made by @PokeSensei</b>"""





CHANNELS_TEXT = """<b>Here are the List of Channels : </b>

<code>{}</code>

<b>Usage : </b> <code>/multirec channelTitle duration | showTitle</code> 

<b>Example : </b> <code>/multirec Star Maa 00:00:10 | Movie</code> 
"""


SITE_BUTTON = [
    InlineKeyboardButton(
        text='WEBSITE',
        url='t.me/SushanthMachineni'
    )
]


@Bot.on_message(filters.private & filters.command(["channels"]))
def channel_list(bot, update):

    if update.from_user.id in config.AUTH_USERS:

        url = "https://vigorous-kirch-074e44.netlify.app/dark_night.json"
        response = urlopen(url)
        data_json = json.loads(response.read())

        channelsList = ""
        for i in data_json:
          channelsList += f"{i}\n"


        update.reply_text(
        text=CHANNELS_TEXT.format(channelsList),
        reply_markup=InlineKeyboardMarkup([SITE_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )


    else:
        update.reply_text(
        text="`You are not Allowed to access this Command`",
        reply_markup=InlineKeyboardMarkup([SITE_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )



@Bot.on_message(filters.private & filters.command(["start"]))
def start(bot, update):


    if update.from_user.id in config.AUTH_USERS:

        update.reply_text(
        text=START_TEXT.format(update.from_user.mention , "You are a Authorised User"),
        reply_markup=InlineKeyboardMarkup([SITE_BUTTON]),
        disable_web_page_preview=True,
        quote=True
        )

        print('--------')
        print(f'[USER] {update.from_user.first_name} - {update.from_user.id}\n[CMD] start')
        print('--------')
    
    elif update.from_user.id in config.ADMIN_USERS:

        update.reply_text(
        text=START_TEXT.format(update.from_user.mention , "You are in the list of ADMIN User"),
        reply_markup=InlineKeyboardMarkup([SITE_BUTTON]),
        disable_web_page_preview=True,
        quote=True
        )
        print('--------')
        print(f'[USER] {update.from_user.first_name} - {update.from_user.id}\n[CMD] start')
        print('--------')


    elif update.from_user.id not in config.ADMIN_USERS:

        update.reply_text(
        text=START_TEXT.format(update.from_user.mention , "You are not Allowed to access this BOT"),
        reply_markup=InlineKeyboardMarkup([SITE_BUTTON]),
        disable_web_page_preview=True,
        quote=True
        )
        print('--------')
        print(f'[USER] {update.from_user.first_name} - {update.from_user.id}\n[CMD] start')
        print('--------')


    


    




@Bot.on_message(filters.private & filters.command(["multirec"]))
def recording_multi_audio(bot, update):


    if update.from_user.id in config.AUTH_USERS:

        if len(update.command) > 1:

            url = "https://gist.githubusercontent.com/Uploader45/c50a746b3303cec0f3355f2e5c39c2b0/raw/TV"
            response = urlopen(url) 
            data_json = json.loads(response.read())


            if update.command[1] in data_json:

                channel = update.command[1]
                channel_json = data_json[channel][0]['title']
                recordingDuration = update.command[2]

                
                if len(update.command) > 2:

                    if '|' in update.command:
                        join = concatenate_list_data(update.command)
                        title = join.split('| ')
                        title = title[1]
                        # multirecNickJunior00:00:10|MashaTest
                    elif recordingDuration.split(':')[2] <= 50:
                        title = "Test"
                    else:
                        title = "No Title"



                    msg = update.reply_text(
                    text = f"<b><i>Recording in Progress...</b></i>",
                    disable_web_page_preview=True,
                    quote=True
                    )
                    print('--------')
                    print(f'[RECORDING] {channel_json} - {recordingDuration}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                    print('--------')

                    

                    audioList = audioListTitle(data_json[channel][0]['audio'])

                    try:
                        newfile = multi_rip(bot, update , streamUrl = data_json[channel][0]['link'] , channel = data_json[channel][0]['title'] , recordingDuration = recordingDuration , language = audioList , ripType = data_json[channel][0]['ripType'] , ripQuality = data_json[channel][0]['quality'] , fileTitle = title)
                        
                        if os.path.exists(newfile) == True:
                            msg.edit(text = f'<b><i>{channel_json} Recorded Successfully</i></b>' , disable_web_page_preview=True)

                            print('--------')
                            print(f'[RECORDING DONE] {channel_json} - {recordingDuration}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                            print('--------')




                            print('--------')
                            print(f'[UPLOAD] {newfile}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                            print('--------')
                            
                            

                            duration = get_duration(newfile)
                            width, height = get_width_height(newfile)

                            bot.send_video(video=newfile, chat_id = update.from_user.id , caption= f"<code>{newfile}</code>")

                                

                            
                            os.remove(newfile)

                            print('--------')
                            print(f'[REMOVE] {newfile}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                            print('--------')
                                

                                
                                



                        else:
                            msg.edit(text = f'<b><i>Recording Failed</b></i>' , disable_web_page_preview=True)

                    except Exception as e:
                        msg.edit(text = f'<code>{e}</code>' , disable_web_page_preview=True)




                    


                    

                else:

                    update.reply_text(
                    text = f"<b><i>No Duration Supplied for {update.command[1]}</b></i>",
                    disable_web_page_preview=True,
                    quote=True
                    )



                
            
            else:
                update.reply_text(
                text = f"<b><i>Requested Channel not Found in Database!</i></b>",
                disable_web_page_preview=True,
                quote=True
                )


            


            

        else:
            update.reply_text(
            text="<b><i>No Command from User...</i></b>",
            disable_web_page_preview=True,
            quote=True
            )

        

    else:
        update.reply_text(
        text="`You are not Allowed to access this Command`",
        reply_markup=InlineKeyboardMarkup([SITE_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )



    





Bot.run()

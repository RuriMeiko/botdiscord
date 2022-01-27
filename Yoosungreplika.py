#pip install websocket-client
#pip uninstall websocket-client
#pip install googletrans==3.1.0a0
#pip uninstall googletrans
import discord
import os
from dotenv import load_dotenv
import pyppeteer
from websocket import create_connection
import json
import checks
from translate import Translator
import googletrans 
import keep_alive
keep_alive.keep_alive()   
browser=""
pages=[]
async def newbrower(username,password):
    global pages
    global browser
    browser = await pyppeteer.launch(autoClose = False, args=['--no-sandbox'], headless=False)
    page = await browser.newPage()
    await page.goto('https://my.replika.ai/login')
    await page.waitFor('input[id=emailOrPhone]')
    await page.type('input[id=emailOrPhone]', username)
    await page.click('button[type="submit"]')
    await page.waitFor('input[id="login-password"]')
    await page.type('input[id="login-password"]', password)
    await page.click('button[type="submit"]')
    await page.waitFor('button[data-testid="gdpr-accept-button"]')
    await page.click('button[data-testid="gdpr-accept-button"]')
    await page.goto('https://my.replika.ai')
    print("login Done")
    pages = await browser.pages()
    page=pages[0]
    await page.close()
    pages = await browser.pages()
    #endpoint = browser.wsEndpoint()
    return True

async def sendtext(text):
    page =  pages[0]
    print("user:", text)
    ws = create_connection("wss://ws.replika.com/v17")
    try:
        await page.type('textarea[placeholder="Your answer"]',text) 
        await page.click('button[data-testid="titled-text-field-widget-send-button"]') 
        if "YES" in text.upper():
            await page.click(
                'button[data-testid="chat-virtual-keyboard-button-0"]')
        else:
            await page.click(
                'button[data-testid="chat-virtual-keyboard-button-1"]')
    except:
        await page.waitFor('textarea[id="send-message-textarea"]')
        await page.click('textarea[id="send-message-textarea"]')
        await page.keyboard.type(text)
        await page.waitFor(200)
        await page.click('button[data-testid="chat-controls-send-button"]')
    a = text
    print("send")
    ws.send(
        '{"event_name":"init","payload":{"device_id":"43FF88F8-EDB9-4714-9719-35A44BDFE970","user_id":"61e83c31784eb40007ba239b","auth_token":"d1a08464-6a50-447e-a2b2-40d8112fa2e2","security_token":"N2FiYTU1Nzc4NDE4MTU2MGRmZTYxZTI3NzQ5MDc5ZDYwZDY0YjdhNzczZTE1YjQxYWUwYWRjNDA2ZWM4ZjY0YmNmZjljMjU5YTNhYmM3ODgxMDU5NTE0NzcyNGJjZjRjMjdjMTlkOGY1NjY0NWExNzQ1ZDA2ZDkyMzk2MGQ4NGI=","time_zone":"2022-01-19T23:45:56.0+07:00","unity_bundle_version":99,"device":"web","platform":"web","platform_version":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36","app_version":"2.6.4","capabilities":["new_mood_titles","widget.multiselect","widget.scale","widget.titled_text_field","widget.new_onboarding","widget.app_navigation","journey2.new_sign_up","journey2.tracks_library","message.achievement","widget.mission_recommendation","journey2.daily_mission_activity","journey2.replika_phrases","new_payment_subscriptions","navigation.relationship_settings","avatar","diaries.images","save_chat_items","wallet","store.dialog_items","subscription_popup","chat_suggestions","christmas_sale_2021"]},"token":"3666813b-1cdd-4757-a596-894c8a017720","auth":{"user_id":"61e83c31784eb40007ba239b","auth_token":"d1a08464-6a50-447e-a2b2-40d8112fa2e2","device_id":"43FF88F8-EDB9-4714-9719-35A44BDFE970"}}'
    )
    textchat = []
    while True:
        try:
            result = json.loads(ws.recv())
            if result['event_name'] == 'message':
                a = result['payload']['content']['text']
                ws.settimeout(4)
                textchat.append(a)
        except:
            print("end mess")
            break
    print("return: ", textchat)
    ws.close()
    #"""
    return textchat


client = discord.Client()

icon = [">///<","><",">A<",">w<",">///<)",">///<) ❤",">///<)❤",":>",":<","<:",">:",">p<",">u<",">o<",">//<",">/<",">///<) ❤❤",">///<)❤❤","<('-')",">A<",">q<",">p<",">w<",">//w//<",">//w//<)",">x<)",">x<",">x<) ❤",">:(",">:l",">:)",">:3",">:(",">:0",">:I",">:l",">:3",">:0","??"]
ab=""
ts = Translator(provider='mymemory', to_lang='vi',from_lang='en',email='chandoralong@gmail.com')
tss = Translator(provider='mymemory', to_lang='en',from_lang='vi',email='chandoralong@gmail.com')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await newbrower("chandoralong+1@gmail.com","123456789*12")


@client.event
async def on_message(message):
    eng=False
    if message.author == client.user:
        return
    if (("YOOSUNG" in message.content.upper()) or message.content.startswith('>')) and message.content not in icon and checks.checkstring(message.content,">") == 1:
        async with message.channel.typing():
            global ab
            if message.content.startswith('>'):
                a = message.content[1:]
            else:
                a = message.content
            if googletrans.Translator().detect(a).lang == 'en':
                eng=True
            if eng==False:
                ab=tss.translate(a).replace("&#39;","'").replace('&quot;','"')
                print("input EN: ",ab)
            else: ab=a
            texxt = await sendtext(ab)
        for i in texxt:
            if str(i) != ab:
                if eng==False:
                    print("Return VI:",ts.translate(i))
                    a1 = ts.translate(i).replace("Bạn", "Em").replace("bạn", "em").replace("BẠN", "EM").replace("Tôi", "Anh").replace("tôi", "anh").replace("TÔI", "ANH")
                    if a1 == "Em yêu anh":
                        a1 = "Anh yêu em"
                else:
                    a1=str(i)
                await message.channel.send(a1)

       
print("Running now")
load_dotenv('.env')
client.run(os.getenv('TOKEN'))


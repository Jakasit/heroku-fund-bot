from flask import Flask, request, render_template, session
from linebot import *
from linebot.models import *
from loanliff import *

import sqlite3
import requests
import json

import urllib.request as urlrq
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


app = Flask(__name__)
app.secret_key = "akasitjaroensiri"
app.register_blueprint(loanliff)

line_bot_api = LineBotApi(
    'hn2b8GvXzwYDrXS7o2tuCPDFMG9yAxPuKv4oC3bMGcw7NlkV9safKQnjlkPMBJHkFRBDBKilN3nE7/SsxAIKbpjl2DY6+GiiDihV7eZtbQe2cKFt9Jhr4CLgYwSCG5XemjdYbIln4YsiF4ulj5k1MgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d314de68551dc17d5f781a5da8fcd63a')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def hello():
    req = request.get_json(silent=True, force=True)
    intent = req['queryResult']['intent']['displayName']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id_user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    reply(intent, reply_token, id_user)
    return req


def reply(intent, reply_token, id_user):
    if intent == 'Intent-test':
        text_message = TextSendMessage(text='test ok')
        line_bot_api.reply_message(reply_token, text_message)

    if intent == 'intent-queue':
        conn = sqlite3.connect('FUND.db')
        c = conn.cursor()
        c.execute("SELECT * FROM oloan")
        # " WHERE id_user == '{}'".format(id_user))
        original_loan = c.fetchall()
        textname = ''
        for i in original_loan:
            textstring = '{}. {} {} {}\n'.format(i[0], i[3], i[6], i[8])
            textname = textname + textstring
        text_message = TextSendMessage(text=textname)
        line_bot_api.reply_message(reply_token, text_message)

    if intent == 'intent-movement':
        conn = sqlite3.connect('FUND.db')
        c = conn.cursor()
        c.execute("SELECT * FROM movement")
        # " WHERE id_user == '{}'".format(id_user))
        movement = c.fetchall()
        textname = ''
        for i in movement:
            textstring = '{} {} ทุนสะสม {} \n สามัญ {}/{} พิเศษ {}/{} \n '.format(i[0], i[2], i[6], i[8], i[11], i[10], i[12])
            textname = textname + textstring
        text_message = TextSendMessage(text=textname)
        line_bot_api.reply_message(reply_token, text_message)

    if intent == 'intent-covid':
        URL = 'https://covid19.ddc.moph.go.th/api/Cases/today-cases-all'
        data = requests.get(url=URL, verify=False)
        json_data = json.loads(data.text)
        New_case = json_data[0]['new_case']
        New_death = json_data[0]['new_death']
        Update_date = json_data[0]['update_date']
        text_message = TextSendMessage(text='จำนวนผู้ติดเชื้อรายใหม่ :{}\n'
                                            'จำนวนผู้เสียชีวิตรายใหม่ :{}\n'
                                            'อัพเดทล่าสุด :{}'.format(New_case, New_death, Update_date))
        line_bot_api.reply_message(reply_token, text_message)

    if intent == 'intent-talk':
        line_bot_api.link_rich_menu_to_user(id_user, 'richmenu-0942bd98731a3fec4071a7921b9a04d2')
        text_message = TextSendMessage(text='พูดคุยได้เลย')
        line_bot_api.reply_message(reply_token, text_message)

    if intent == 'intent-talk-out':
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='ต้องการหยุดการสนทนาหรือไม่',
                actions=[
                    MessageAction(
                        label='ใช่',
                        text='ใช่'
                    ),
                    MessageAction(
                        label='ไม่ใช่',
                        text='พูดคุยทั่วไป'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, confirm_template_message)

    if intent == 'intent-talk-out - yes':
        line_bot_api.unlink_rich_menu_from_user(id_user)

    if intent == 'intent-loan':
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://res.cloudinary.com/duzmptjtf/image/upload/v1660037374/cld-sample-2.jpg',
                        title='แบบฟอร์มกู้เงิน กองทุนทรัพย์สิน',
                        text='ยื่นกู้เงินกองทุนทรัพย์สิน',
                        actions=[
                            URIAction(
                                label='กู้สามัญ',
                                uri='https://liff.line.me/1657363340-O5LxNo8m/okliff'
                            ),
                            URIAction(
                                label='กู้พิเศษ',
                                uri='https://liff.line.me/1657363340-O5LxNo8m'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, carousel_template_message)


if __name__ == '__main__':
    app.run(debug=True)

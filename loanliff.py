from flask import Flask, request, render_template, session, Blueprint
from linebot import *
from linebot.models import *
import sqlite3
from datetime import date, datetime
import json


loanliff = Blueprint('loanliff', __name__)

line_bot_api = LineBotApi(
    'hn2b8GvXzwYDrXS7o2tuCPDFMG9yAxPuKv4oC3bMGcw7NlkV9safKQnjlkPMBJHkFRBDBKilN3nE7/SsxAIKbpjl2DY6+GiiDihV7eZtbQe2cKFt9Jhr4CLgYwSCG5XemjdYbIln4YsiF4ulj5k1MgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d314de68551dc17d5f781a5da8fcd63a')
#iduser1 = "U85faece44b8902064843d0a1641f3146"


@loanliff.route('/okliff', methods=['POST', 'GET'])
def okliff():
    if request.method == 'POST':
        id_user = request.form['userId']
        displayName = request.form['displayName']
        conn = sqlite3.connect('FUND.db')
        c = conn.cursor()
        c.execute("SELECT * FROM personal INNER JOIN movement ON personal.id_pea = movement.id_pea "
                  "WHERE personal.id_user == '{}' ORDER BY id DESC LIMIT 1".format(id_user))
        rows = c.fetchall()
        print(rows)
        if len(rows) == 0:
            return render_template('newiduser.html')
        else:
            return render_template('loanliff.html', datas=rows)
    else:
        return render_template('okliff.html')


@loanliff.route('/oknewuser', methods=['POST', 'GET'])
def oknewuser():
    if request.method == 'POST':
        id_user = request.form['userId']
        id_pea = request.form['idpea']
        birth_day = request.form['birthday']
        birth_day_text = datetime.strptime(birth_day, "%Y-%m-%d").strftime("%d-%m-%Y")
        conn = sqlite3.connect('FUND.db')
        c = conn.cursor()
        c.execute("SELECT * FROM personal WHERE id_pea == '{}' AND birth_day == '{}'".format(id_pea, birth_day_text))
        rows = c.fetchall()
        print(rows)
        if len(rows) > 0:
            c1 = conn.cursor()
            c1.execute("UPDATE personal SET id_user = '{}' WHERE id_pea == '{}' AND birth_day == '{}'".format(id_user, id_pea, birth_day_text))
            conn.commit()
            return render_template('okliff.html')
        else:
            return render_template('newiduser.html')


@loanliff.route('/loanliff', methods=['POST', 'GET'])
def myliff():
    if request.method == 'POST':
        id_user = request.form['userId']
        displayName = request.form['displayName']
        today = date.today()
        post_date = today.strftime("%d-%m-%Y")
        id_pea = request.form['idpea']
        net_stock = request.form['netstock']
        o_loan = request.form['oloan']
        o_install = request.form['oinstall']
        o_status = "wait"

        id = None
        conn = sqlite3.connect('FUND.db')
        c = conn.cursor()
        c.execute("""INSERT INTO oloan VALUES(?,?,?,?,?,?,?,?,?)""",
                  (id, post_date, id_user, displayName, id_pea, net_stock, o_loan, o_install, o_status))
        conn.commit()
        text_message = TextSendMessage(text='ได้รับเรื่องกู้เรียบร้อยแล้ว')
        line_bot_api.push_message(id_user, text_message)
        return render_template('close.html')
    else:
        #id_user = request.form['userId']

        id_user = session.get('username')
        #print(id_user, "AAAAAAAAAAAAA")
        #reply(intent, reply_token, id_user)
        #id_user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
        conn = sqlite3.connect('FUND.db')
        c = conn.cursor()
        c.execute("SELECT * FROM personal WHERE id_user == '{}'".format(id_user))
        rows = c.fetchall()
        print(rows)
        return render_template('loanliff.html', datas=rows)




  #  if request.method == 'POST':
  #      id_user = request.form['userId']
  #      today = date.today()
   #     post_date = today.strftime("%d-%m-%Y")
   #     displayName = request.form['displayName']

   #     id = None
   #     conn = sqlite3.connect('FUND.db')
   #     c = conn.cursor()
   #     c.execute("""INSERT INTO oloan VALUES(?,?,?,?,?,?,?,?)""",
   #               (id, post_date, id_user, displayName, id_pea, net_stock, o_loan, o_install, o_net_install))
   #     conn.commit()
   #     return render_template('close.html')
   # else:
   #      return render_template('loanliff.html')

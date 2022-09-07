channel_access_token ='hn2b8GvXzwYDrXS7o2tuCPDFMG9yAxPuKv4oC3bMGcw7NlkV9safKQnjlkPMBJHkFRBDBKilN3nE7/SsxAIKbpjl2DY6+GiiDihV7eZtbQe2cKFt9Jhr4CLgYwSCG5XemjdYbIln4YsiF4ulj5k1MgdB04t89/1O/w1cDnyilFU='
import json
from urllib import response
import requests

richdata = {
  "size": {
    "width": 2500,
    "height": 843
  },
  "selected": True,
  "name": "Rich Menu 1",
  "chatBarText": "กดเพื่อดูเมนู",
  "areas": [
    {
      "bounds": {
        "x": 1225,
        "y": 466,
        "width": 1271,
        "height": 372
      },
      "action": {
        "type": "message",
        "text": "ออกจากการสนทนา"
      }
    }
  ]
}


def RegisRich(Rich_json,channel_access_token):
    url = 'https://api.line.me/v2/bot/richmenu'
    Rich_json = json.dumps(Rich_json)
    Authorization = 'Bearer {}'.format(channel_access_token)
    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': Authorization}
    response = requests.post(url, headers=headers, data=Rich_json)
    print(str(response.json()['richMenuId']))
    return str(response.json()['richMenuId'])


def CreateRichMenu(ImageFilePath, Rich_json, channel_access_token):
    richId = RegisRich(Rich_json=Rich_json, channel_access_token=channel_access_token)
    url = 'https://api-data.line.me/v2/bot/richmenu/{}/content'.format(richId)
    Authorization = 'Bearer {}'.format(channel_access_token)
    headers = {'Content-Type': 'image/jpeg',
               'Authorization': Authorization}
    img = open(ImageFilePath, 'rb').read()
    response = requests.post(url, headers=headers, data=img)
    print(response.json())


CreateRichMenu(ImageFilePath='img_richmenu/talkbot.jpg', Rich_json=richdata,
               channel_access_token=channel_access_token)


# richmenu-0942bd98731a3fec4071a7921b9a04d2
# เอาไปใช้ใน link_rich_menu_to_user
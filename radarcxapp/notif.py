
"""
Notification module

Since there were some issues in Najva's package (najva_api_client.najva),
We will note use their package directly.

Those bugs were, namely,
+ incompatible timezone (Iran time zone required)
+ out-of-date syntax of josn (needed json_parder)
+ using "api-key" instead of "api_key" (underline)
+ using token instead of self.tokens
+ not having guildline for how to return sw.js and manifest.json
+ And many more issues there were on thier website
"""
import requests
import json as json_parser
from datetime import datetime, timedelta # for iranTimeZone func

def UTC_to_IR_TimeZone(delay = 3):
    # time should be in this format :"%Y-%m-%dT%H:%M:%S"
    # Notice: by our settings Heroku uses UTC tim zone
    # iran = UTC + 270 minuts
    # send time = irantime + 3 min delay
    sent_time = datetime.now() + timedelta(minutes=270+delay)
    #najva has asked to send in the following format but they actually do that in their code!(line66)
    #sent_time = sent_time.strftime("%Y-%m-%dT%H:%M:%S")
    return sent_time

def send_to_users(apikey= "9e48e9f0-41e1-4f0a-a3d0-dd34b8313f03",
    token= "6e83d4164baf569f345ab556b01347b1178776c5" ,
    title="Notification for your triggered condition",
    body,
    url="https://radarcx.herokuapp.com/",
    icon="https://png.pngtree.com/element_our/md/20180515/md_5afb099d307d3.jpg",
    subscriber_tokens,
    onclick='open-link',
    image="https://png.pngtree.com/element_our/md/20180515/md_5afb099d307d3.jpg",
    content=None,
    json=None,
    sent_time=None):

    urlNajva = 'https://app.najva.com/notification/api/v1/notifications/'

    if sent_time==None:
        sent_time = datetime.now() + timedelta(minutes=3)


    body = {
        'api_key': apikey,
        'title': title,
        'body': body,
        'onclick-action': onclick,
        'url': url,
        'content': content,
        'json': '"%s"' % json,
        'icon': icon,
        'image': image,
        'sent_time': sent_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'subscriber_tokens': subscriber_tokens
    }

    headers = {
        'authorization': "Token %s" % token,
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request(method="POST", url=urlNajva, data = json_parser.dumps(body), headers= headers)

    return response.text

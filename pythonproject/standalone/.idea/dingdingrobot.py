import urllib2,urllib,json

url='https://oapi.dingtalk.com/robot/send?access_token=275bc50f9dbf247ebd1b6faf0b134f4a618200cb2e11c462e5442d3c6fc35b82'
value={"msgtype": "text",
    "text": {
        "content": "muma!"
     },
    "at": {
        "atMobiles": ["18992868907"],
        "isAtAll": False
    }
  }
headers={'Content-Type':'application/json'}
data=json.dumps(value)
request=urllib2.Request(url,data,headers)
res=urllib2.urlopen(request)
print res.read()

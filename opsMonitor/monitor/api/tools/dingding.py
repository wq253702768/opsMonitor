#!/usr/bin/env python
#coding: utf-8
from urllib import parse, request
import json


class DingdingAPI(object):
    def __init__(self, http_url, message):
        self.http_url = http_url
        self.message = message

    def run(self):
        HEADERS = {
            "Content-Type": "application/json ;charset=utf-8 ",
            "Charset": "UTF-8"
        }
        String_textMsg = {
            "msgtype": "text",
            "text": {"content": self.message},
            "atMobiles": [
                "15850590916"  # 如果需要@某人，这里写他的手机号
            ],
            "at": {
                "isAtAll": False
            }
        }

        # 对请求的数据进行json封装
        sendData = json.dumps(String_textMsg)
        sendData = sendData.encode("utf-8")

        # 发送请求
        req = request.Request(url=self.http_url, data=sendData, headers=HEADERS)
        # 将请求发回的数据构建成为文件格式
        opener = request.urlopen(req)
        result = opener.read().decode(encoding="utf-8")
        return eval(result)

if __name__ == "__main__":
    print (DingdingAPI(http_url="https://oapi.dingtalk.com/robot/send?access_token=a5a81391a31889885e40f39f936bf674115cbae21e58f217d81d36103ae434c2",message ='测试').run())

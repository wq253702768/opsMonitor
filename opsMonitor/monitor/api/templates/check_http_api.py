#!/usr/bin/env python
# coding: utf-8
import requests
import socket


class CheckHttpInterface(object):
    def __init__(self, http_host,port,interface=None,**kwargs):
        self.http_host = http_host
        self.port = port
        self.interface = interface

    def check_http_api(self):
        try:
            print ("http://%s:%s/%s" % (self.http_host, self.port,self.interface))
            response = requests.get("http://%s:%s/%s" % (self.http_host, self.port,self.interface), timeout=5)
            response_data = eval(response.content.decode(encoding="utf-8"))
            if response_data:
                component_status = response_data['status']
                redis_status = response_data['details']['redis']['status']
                mongodb_status = response_data['details']['mongo']['status']
                if component_status in ["UP"] and redis_status in ["UP"] and mongodb_status in ["UP"]:
                    data = {
                        'result': True,
                        'message': '[http://%s:%s/%s] [访问成功]' % (self.http_host, self.port, self.interface)
                    }
                else:
                    data = {
                        'result': False,
                        'message': '[http://%s:%s/%s] [访问失败] [%s]，请及时检查' % (self.http_host, self.port, self.interface, response_data)
                    }
        except Exception as e:
            data = {
                'result': False,
                'message': '[http://%s:%s/%s] [访问失败] [%s]，请及时检查' % (self.http_host, self.port, self.interface, e)
            }

        return data

    def check_port(self, socket_timeout=2):
        socket.setdefaulttimeout(socket_timeout)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个基于网络通信的TCP协议的socket对象
        try:
            re_socker = server.connect_ex((self.http_host, self.port))
            if re_socker == 0:
                result = True
                message = "端口检测成功"
            else:
                result = False
                message = "[%s:%s] 端口检测不同 [返回code号: %s]" % (self.http_host, self.port, re_socker)
        except Exception as e:
            print(e)
            result = False
            message = "[%s:%s] 端口检测不同 [%s]" % (self.http_host, self.port, e)
        finally:
            server.close()

        return {'result': result, 'message': message}

    def run(self):
        if self.interface:
            return self.check_http_api()

        else:
            return self.check_port()


if __name__ == "__main__":
    interface=''
    print (CheckHttpInterface(http_host="172.19.184.203",port=8084,interface=interface).run())



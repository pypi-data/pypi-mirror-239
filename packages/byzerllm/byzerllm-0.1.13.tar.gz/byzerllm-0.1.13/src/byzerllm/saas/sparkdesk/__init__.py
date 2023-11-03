import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from typing import List, Tuple,Dict
import time
import queue

import websocket

reponse_queue = queue.Queue()

class SparkDeskAPIParams(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

class SparkDeskAPI:

    def __init__(self,appid, api_key, api_secret,params:Dict[str,str]={}) -> None:
        appid = appid if appid else params.get("saas.appid","")
        api_key = api_key if api_key else params.get("saas.api_key","")
        api_secret = api_secret if api_secret else params.get("saas.api_secret","")
        gpt_url = params.get("gpt_url","ws://spark-api.xf-yun.com/v1.1/chat")
        self.config = SparkDeskAPIParams(appid, api_key, api_secret, gpt_url)
    
    @staticmethod
    def on_error(ws, error):
        pass


    @staticmethod
    def on_close(ws,a,b):        
        pass


    @staticmethod
    def on_open(ws):
        thread.start_new_thread(SparkDeskAPI.run, (ws,))

    @staticmethod
    def run(ws, *args):
        # 8192
        data = {
            "header": {
                "app_id": ws.appid,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": "general",
                    "random_threshold": ws.temperature,
                    "max_tokens": ws.max_length,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": ws.question
                }
            }
        }
        data = json.dumps(data)
        ws.send(data)

   
    @staticmethod
    def on_message(ws, message):
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:            
            reponse_queue.put(f'请求错误: {code}, {data}')
            reponse_queue.put(None)
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]            
            reponse_queue.put(content)
            if status == 2:
                reponse_queue.put(None)
                ws.close()
    

    def stream_chat(self,tokenizer,ins:str, his:List[Tuple[str,str]]=[],  
        max_length:int=4096, 
        top_p:float=0.7,
        temperature:float=0.9): 

        q = [] 
        for item in his:
           q.append({"role": "user", "content": item[0]})
           q.append({"role": "assistant", "content": item[1]})


        q.append({"role": "user", "content": ins})        
        websocket.enableTrace(False)
        wsUrl = self.config.create_url()
        ws = websocket.WebSocketApp(wsUrl, 
                                    on_message=SparkDeskAPI.on_message, 
                                    on_error=SparkDeskAPI.on_error, 
                                    on_close=SparkDeskAPI.on_close, 
                                    on_open=SparkDeskAPI.on_open)
        ws.appid = self.config.APPID
        ws.question = q
        ws.max_length = max_length
        ws.top_p = top_p
        ws.temperature = temperature        
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
        result = []

        t  = reponse_queue.get(timeout=30)
        while t is not None:
            result.append(t)
            t  = reponse_queue.get(timeout=30)
           

        return [("".join(result),"")]

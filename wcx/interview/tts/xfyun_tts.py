# tts/xfyun_tts.py
# -*- coding:utf-8 -*-
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import ssl
import os
import threading
from time import mktime
from wsgiref.handlers import format_date_time
from datetime import datetime


class WsTTSParam:
    def __init__(self, app_id, api_key, api_secret, text):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.text = text

        self.CommonArgs = {"app_id": self.app_id}
        self.BusinessArgs = {
            "aue": "raw",
            "auf": "audio/L16;rate=16000",
            "vcn": "xiaoyan",
            "tte": "utf8"
        }
        self.Data = {
            "status": 2,
            "text": base64.b64encode(self.text.encode('utf-8')).decode('utf-8')
        }

    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = f"host: ws-api.xfyun.cn\ndate: {date}\nGET /v2/tts HTTP/1.1"
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        return url + '?' + urlencode({
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        })


def synthesize_text(text, app_id, api_key, api_secret, output_path="./output.pcm"):
    ws_param = WsTTSParam(app_id, api_key, api_secret, text)
    result_path = output_path
    if os.path.exists(result_path):
        os.remove(result_path)

    def on_message(ws, message):
        try:
            data = json.loads(message)
            audio = data['data']['audio']
            audio = base64.b64decode(audio)
            with open(result_path, 'ab') as f:
                f.write(audio)
            if data["data"]["status"] == 2:
                ws.close()
        except Exception as e:
            print("❌ 合成错误：", e)

    def on_error(ws, error):
        print("❌ WebSocket 错误:", error)

    def on_close(ws, a=None, b=None):
        print(f"✅ 合成完成，音频已保存到：{result_path}")

    def on_open(ws):
        def run():
            d = {
                "common": ws_param.CommonArgs,
                "business": ws_param.BusinessArgs,
                "data": ws_param.Data
            }
            ws.send(json.dumps(d))

        threading.Thread(target=run).start()

    ws_url = ws_param.create_url()
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(ws_url,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

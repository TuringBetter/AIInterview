# recorder/xfyun_asr.py
# -*- coding:utf-8 -*-
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
import pyaudio
import threading
from wsgiref.handlers import format_date_time
from time import mktime
from datetime import datetime

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2


class WsParam:
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

        self.CommonArgs = {"app_id": self.APPID}
        self.BusinessArgs = {
            "domain": "iat",
            "language": "zh_cn",
            "accent": "mandarin",
            "vinfo": 1,
            "vad_eos": 10000
        }

    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = f"host: ws-api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        return url + '?' + urlencode({
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        })


class ASRClient:
    def __init__(self, app_id, api_key, api_secret):
        self.ws_param = WsParam(app_id, api_key, api_secret)
        self.final_result = ""
        self.ws = None

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if data.get("code", 0) != 0:
                print(f"❌ Error: {data.get('message')} (code {data.get('code')})")
            else:
                result = ""
                for item in data["data"]["result"]["ws"]:
                    for w in item["cw"]:
                        result += w["w"]
                print("📝 识别结果：", result)
                self.final_result += result
        except Exception as e:
            print("❌ 解析错误:", e)

    def on_error(self, ws, error):
        print("❌ WebSocket 错误:", error)

    def on_close(self, ws, a=None, b=None):
        print("🔒 连接关闭")

    def on_open(self, ws):
        def run(*args):
            pa = pyaudio.PyAudio()
            stream = pa.open(format=pyaudio.paInt16,
                             channels=1,
                             rate=16000,
                             input=True,
                             frames_per_buffer=8000)

            status = STATUS_FIRST_FRAME
            print("🎤 开始说话，按 Ctrl+C 停止")

            try:
                while True:
                    buf = stream.read(8000, exception_on_overflow=False)

                    if status == STATUS_FIRST_FRAME:
                        d = {
                            "common": self.ws_param.CommonArgs,
                            "business": self.ws_param.BusinessArgs,
                            "data": {
                                "status": 0,
                                "format": "audio/L16;rate=16000",
                                "audio": base64.b64encode(buf).decode("utf-8"),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))
                        status = STATUS_CONTINUE_FRAME
                    else:
                        d = {
                            "data": {
                                "status": 1,
                                "format": "audio/L16;rate=16000",
                                "audio": base64.b64encode(buf).decode("utf-8"),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))

                    time.sleep(0.04)

            except KeyboardInterrupt:
                print("🛑 手动终止，结束发送")
                d = {
                    "data": {
                        "status": 2,
                        "format": "audio/L16;rate=16000",
                        "audio": "",
                        "encoding": "raw"
                    }
                }
                ws.send(json.dumps(d))
                time.sleep(1)
                ws.close()
                stream.stop_stream()
                stream.close()
                pa.terminate()

        threading.Thread(target=run).start()

    def start(self):
        ws_url = self.ws_param.create_url()
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def get_result(self):
        return self.final_result

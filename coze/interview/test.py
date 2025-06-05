from recorder.xfyun_asr import ASRClient

asr = ASRClient(app_id="49fade5c", api_key="03887408f57f7f23fa36fd17371cb3ff", api_secret="YmM1MTFlZjMwYmRmMDQ5MGM0ZmE4Yzcy")
asr.start()

# 如果你想获取识别后的文本（可在主线程等待一段时间后再调用）
print(asr.get_result())

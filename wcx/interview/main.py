# main.py
import time
from recorder.xfyun_asr import ASRClient
from llm.spark_agent import SparkAgent
from tts.xfyun_tts import synthesize_text
from playback.player import play_pcm

# 配置参数
APP_ID = "49fade5c"
API_KEY = "03887408f57f7f23fa36fd17371cb3ff"
API_SECRET = "YmM1MTFlZjMwYmRmMDQ5MGM0ZmE4Yzcy"
SPARK_DOMAIN = "4.0Ultra"
SYSTEM_PROMPT = """
你是一位 Java 技术面试官。
请按照以下格式进行五轮技术面试：
- 每一轮你主动提出一个与 Java 岗位相关的问题。
- 等待候选人回答后，请简洁、正式地进行点评。
每次提问时，不要解释问题，不要一次提多个问题。
"""

PCM_PATH = "./pcm_output/output.pcm"
LOG_PATH = "./history_log.txt"

# 初始化 Spark 面试官
agent = SparkAgent(APP_ID, API_KEY, API_SECRET, SPARK_DOMAIN, SYSTEM_PROMPT)

# 播放文本转语音
def play_text(text):
    synthesize_text(text, APP_ID, API_KEY, API_SECRET, output_path=PCM_PATH)
    time.sleep(2)
    play_pcm(PCM_PATH)

# 录音并识别语音
def record_and_transcribe():
    asr = ASRClient(APP_ID, API_KEY, API_SECRET)
    asr.start()
    print("🎙️ 请开始回答...")
    time.sleep(10)  # 候选人作答时间
    return asr.get_result().strip()

# 保存每轮记录
def save_history(q, a, c, i):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n【第{i}轮】\n问题：{q}\n回答：{a}\n点评：{c}\n")

# 主流程
def main():
    print("🤖 正式开始 Java 面试，总共五轮。\n")
    round_num = 0
    history = []  # 用于保存问题回答对 [(q, a), ...]

    while round_num < 5:
        round_num += 1
        print(f"\n🎯 第 {round_num} 轮面试")

        # Step 1：组织历史上下文用于提问引导
        if not history:
            prompt = "请以 Java 技术面试官的身份，提出第一轮面试问题。"
        else:
            context = "\n".join([f"第{i+1}轮：我问：{q}\n候选人答：{a}" for i, (q, a) in enumerate(history)])
            prompt = f"""以下是我之前对候选人的提问和他的回答：
{context}
        请基于以上内容提出第 {round_num} 个新的 Java 技术面试问题，不要重复提问，不要解释问题。"""

        question = agent.ask(prompt)


        print("🗨️ 面试官提问：", question)

        # Step 2：播报问题语音
        play_text(question)

        # Step 3：倒计时 + 开始作答提示
        play_text("你有十秒时间思考，请准备作答。")
        time.sleep(10)
        play_text("请开始作答。")

        # Step 4：接收回答
        answer = record_and_transcribe()
        print("📝 候选人回答文本：", answer)

        # Step 5：大模型点评
        comment_prompt = f"以下是我提出的问题：{question}\n这是候选人的回答：{answer}\n请你做出正式、简要的点评。"
        agent.ask(comment_prompt)
        comment = agent.chat_history[-1].content.strip()
        print("📋 面试官点评：", comment)
        play_text(comment)

        # Step 6：保存到历史和日志
        history.append((question, answer))
        save_history(question, answer, comment, round_num)

    print("\n✅ 五轮面试完成，记录保存在 history_log.txt")



if __name__ == "__main__":
    main()

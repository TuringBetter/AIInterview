from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

class SparkAgent:
    def __init__(self, app_id, api_key, api_secret, domain, system_prompt):
        self.chat_history = [ChatMessage(role="system", content=system_prompt)]
        self.handler = ChunkPrintHandler()

        self.spark = ChatSparkLLM(
            spark_api_url='wss://spark-api.xf-yun.com/v4.0/chat',
            spark_app_id=app_id,
            spark_api_key=api_key,
            spark_api_secret=api_secret,
            spark_llm_domain=domain,
            streaming=False  # 如果需要流式输出可设为 True
        )

    def ask(self, user_input):
        self.chat_history.append(ChatMessage(role="user", content=user_input))
        print(f"🧠 面试官：", end="", flush=True)
        result = self.spark.generate([self.chat_history], callbacks=[self.handler])
        response_text = result.generations[0][0].text.strip()
        print()  # 输出换行
        self.chat_history.append(ChatMessage(role="assistant", content=response_text))
        return response_text



    def reset(self):
        self.chat_history = [msg for msg in self.chat_history if msg.role == "system"]

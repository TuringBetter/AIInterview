# 可以正常运行的
import json
from cozepy import (
    COZE_CN_BASE_URL,
    Coze,
    TokenAuth,
    Stream,
    WorkflowEvent,
    WorkflowEventType,
)

# === 🧩 配置 ===
API_TOKEN = "pat_DdnmJr9l18O74w9Y1i7LsxPx16Dua715FITUjZO6rrMGkhSfdFvhYHFXq1pNWeNo"         # 替换为你的 Token
WORKFLOW_ID = "7509447097432227880"     # 替换为你的 Workflow ID
PROMPT_TEXT = "你好，青岛的天气怎么样"  # 👈 自定义提示词

# === 🚀 初始化客户端 ===
coze = Coze(auth=TokenAuth(token=API_TOKEN), base_url=COZE_CN_BASE_URL)

# === 📦 输入参数（仅含 prompt）===
parameters = {
    "input": PROMPT_TEXT
}

# === 🔁 流式处理函数 ===
def handle_workflow_iterator(stream: Stream[WorkflowEvent]):
    for event in stream:
        if event.event == WorkflowEventType.MESSAGE:
            print("📩 got message:", event.message.content)
        elif event.event == WorkflowEventType.ERROR:
            print("❌ got error:")
            print("  code:", getattr(event.error, "code", "N/A"))
            print("  detail:", getattr(event.error, "detail", str(event.error)))
        elif event.event == WorkflowEventType.INTERRUPT:
            print("⏸ got interrupt:", event.interrupt.interrupt_data)
            handle_workflow_iterator(
                coze.workflows.runs.resume(
                    workflow_id=WORKFLOW_ID,
                    event_id=event.interrupt.interrupt_data.event_id,
                    resume_data="继续",
                    interrupt_type=event.interrupt.interrupt_data.type,
                )
            )

# === 🔄 执行对话 ===
handle_workflow_iterator(
    coze.workflows.runs.stream(
        workflow_id=WORKFLOW_ID,
        parameters=parameters,
    )
)

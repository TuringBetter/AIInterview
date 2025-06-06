import json
import time
from pathlib import Path
from PyPDF2 import PdfReader
from cozepy import (
    COZE_CN_BASE_URL,
    ChatStatus,
    Coze,
    DeviceOAuthApp,
    TokenAuth,
    Stream,
    WorkflowEvent,
    WorkflowEventType,
)

# ==== 🔧 配置信息 ====
API_TOKEN = "pat_DdnmJr9l18O74w9Y1i7LsxPx16Dua715FITUjZO6rrMGkhSfdFvhYHFXq1pNWeNo"
WORKFLOW_ID = "7511327674183319587"
pdf_path = "./coze/profile.pdf"
prompt_text = "我想面试java"

# ==== 🚀 初始化 Coze 客户端 ====
coze = Coze(auth=TokenAuth(token=API_TOKEN), base_url=COZE_CN_BASE_URL)

# ==== 📤 读取 PDF 文件内容 ====
print(f"📄 正在读取 PDF 文件: {pdf_path}")
pdf_reader = PdfReader(pdf_path)
pdf_text = ""
for page in pdf_reader.pages:
    pdf_text += page.extract_text()
print(f"✅ PDF内容读取成功")

# ==== ⚙️ 构造参数 ====
parameters = {
    "gangwei": prompt_text,
    "jianli": json.dumps({"file": pdf_text})
}

# ==== 🎧 处理流式响应（增加等待提示） ====
def handle_workflow_iterator(stream: Stream[WorkflowEvent]):
    thinking_shown = False  # 是否已显示过"正在思考..."提示
    for event in stream:
        if not thinking_shown:
            print("⏳ 模型正在思考，请稍候...\n")
            thinking_shown = True

        if event.event == WorkflowEventType.MESSAGE:
            print("🗨️  AI:", event.message.content)
        elif event.event == WorkflowEventType.ERROR:
            print("❌ 错误:", event.error)
        elif event.event == WorkflowEventType.INTERRUPT:
            print("⏸️ 中断，正在恢复...\n")
            handle_workflow_iterator(
                coze.workflows.runs.resume(
                    workflow_id=WORKFLOW_ID,
                    event_id=event.interrupt.interrupt_data.event_id,
                    resume_data="resume",
                    interrupt_type=event.interrupt.interrupt_data.type,
                )
            )

# ==== 🧠 启动工作流 ====
handle_workflow_iterator(
    coze.workflows.runs.stream(
        workflow_id=WORKFLOW_ID,
        parameters=parameters,
    ))
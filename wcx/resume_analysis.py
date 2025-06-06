# # 可以正常运行的
# import json
# from cozepy import (
#     COZE_CN_BASE_URL,
#     Coze,
#     TokenAuth,
#     Stream,
#     WorkflowEvent,
#     WorkflowEventType,
# )

<<<<<<< HEAD
# # === 🧩 配置 ===
# API_TOKEN = "pat_DdnmJr9l18O74w9Y1i7LsxPx16Dua715FITUjZO6rrMGkhSfdFvhYHFXq1pNWeNo"         # 替换为你的 Token
# WORKFLOW_ID = "7509447097432227880"     # 替换为你的 Workflow ID
# PROMPT_TEXT = "你好，青岛的天气怎么样"  # 👈 自定义提示词
=======
# # ==== 🔧 配置信息 ====
# API_TOKEN = "pat_DdnmJr9l18O74w9Y1i7LsxPx16Dua715FITUjZO6rrMGkhSfdFvhYHFXq1pNWeNo"
# WORKFLOW_ID = "7511327674183319587"
# pdf_path = "./个人简历.pdf"
# prompt_text = "我想面试java"
>>>>>>> 0259b8769fea2677dd99e87a2c4978fb6a5d2eca

# # === 🚀 初始化客户端 ===
# coze = Coze(auth=TokenAuth(token=API_TOKEN), base_url=COZE_CN_BASE_URL)

# # === 📦 输入参数（仅含 prompt）===
# parameters = {
#     "input": PROMPT_TEXT
# }

# # === 🔁 流式处理函数 ===
# def handle_workflow_iterator(stream: Stream[WorkflowEvent]):
#     for event in stream:
#         if event.event == WorkflowEventType.MESSAGE:
#             print("📩 got message:", event.message.content)
#         elif event.event == WorkflowEventType.ERROR:
#             print("❌ got error:")
#             print("  code:", getattr(event.error, "code", "N/A"))
#             print("  detail:", getattr(event.error, "detail", str(event.error)))
#         elif event.event == WorkflowEventType.INTERRUPT:
#             print("⏸ got interrupt:", event.interrupt.interrupt_data)
#             handle_workflow_iterator(
#                 coze.workflows.runs.resume(
#                     workflow_id=WORKFLOW_ID,
#                     event_id=event.interrupt.interrupt_data.event_id,
#                     resume_data="继续",
#                     interrupt_type=event.interrupt.interrupt_data.type,
#                 )
#             )

# # === 🔄 执行对话 ===
# handle_workflow_iterator(
#     coze.workflows.runs.stream(
#         workflow_id=WORKFLOW_ID,
#         parameters=parameters,
#     )
# )

# 报错的 上传pdf
import json
import time
from pathlib import Path
import fitz

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


def extract_pdf_text(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# ==== 🔧 配置信息 ====
API_TOKEN = "pat_DdnmJr9l18O74w9Y1i7LsxPx16Dua715FITUjZO6rrMGkhSfdFvhYHFXq1pNWeNo"
WORKFLOW_ID = "7511327674183319587"
pdf_path = "./个人简历.pdf"
prompt_text = "java开发岗位"
jianliContent = extract_pdf_text(pdf_path)

# ==== 🚀 初始化 Coze 客户端 ====
coze = Coze(auth=TokenAuth(token=API_TOKEN), base_url=COZE_CN_BASE_URL)

# ==== 📤 上传 PDF 文件 ====



# ==== ⚙️ 构造参数 ====
parameters = {
    "gangwei": prompt_text,
    "jianli": jianliContent
}

# ==== 🎧 处理流式响应（增加等待提示） ====
def handle_workflow_iterator(stream: Stream[WorkflowEvent]):
    thinking_shown = False  # 是否已显示过“正在思考...”提示
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





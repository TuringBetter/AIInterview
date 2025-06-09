import json
import asyncio
import io
import tempfile # 导入 tempfile
import os # 导入 os
from typing import AsyncGenerator
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  # 解决跨域问题
from PyPDF2 import PdfReader
from cozepy import (
    COZE_CN_BASE_URL,
    Coze,
    TokenAuth,
    WorkflowEvent,
    WorkflowEventType,
)

# ==== 🔧 配置信息 ====
# 建议从环境变量读取，而不是硬编码
API_TOKEN = "pat_DdnmJr9l18O74w9Y1i7LsxPx16Dua715FITUjZO6rrMGkhSfdFvhYHFXq1pNWeNo"
WORKFLOW_ID = "7511327674183319587"

# ==== 🚀 初始化 FastAPI 应用和 Coze 客户端 ====
app = FastAPI()
coze = Coze(auth=TokenAuth(token=API_TOKEN), base_url=COZE_CN_BASE_URL)

# 配置 CORS 中间件，允许所有来源的请求（在开发环境中很方便）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== 🧠 定义流式处理生成器 ====
async def stream_coze_workflow(pdf_file: UploadFile, gangwei: str) -> AsyncGenerator[str, None]:
    """
    处理 Coze 工作流并以 Server-Sent Events (SSE) 格式流式返回结果
    """
    temp_file_path = None # 初始化临时文件路径
    try:
        # 1. 异步读取上传的 PDF 文件内容到内存
        pdf_content = await pdf_file.read()
        
        # 2. 将内容保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_content)
            temp_file_path = temp_file.name # 保存临时文件路径
        
        # 3. 使用 PyPDF2 从临时文件读取内容
        pdf_text = ""
        with open(temp_file_path, "rb") as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() or ""

        # 4. 构造参数
        parameters = {
            "gangwei": gangwei,
            "jianli": json.dumps({"file": pdf_text})
        }

        # 5. 显示思考提示
        yield f"data: {json.dumps({'event': 'thinking', 'data': '模型正在思考，请稍候...'})}\n\n"

        # 6. 调用 Coze 工作流并处理流式响应
        stream = coze.workflows.runs.stream(
            workflow_id=WORKFLOW_ID,
            parameters=parameters,
        )

        for event in stream:
            if event.event == WorkflowEventType.MESSAGE:
                response_data = {'event': 'message', 'data': event.message.content}
                yield f"data: {json.dumps(response_data)}\n\n"
            elif event.event == WorkflowEventType.ERROR:
                response_data = {'event': 'error', 'data': event.error}
                yield f"data: {json.dumps(response_data)}\n\n"
            # 注意：中断和恢复逻辑在无状态的API中处理会更复杂，这里简化为仅通知
            elif event.event == WorkflowEventType.INTERRUPT:
                response_data = {'event': 'interrupt', 'data': '任务已中断'}
                yield f"data: {json.dumps(response_data)}\n\n"
        
        # 7. 发送流结束信号
        yield f"data: {json.dumps({'event': 'done', 'data': '分析完成'})}\n\n"

    except Exception as e:
        error_data = {'event': 'error', 'data': f"发生内部错误: {str(e)}"}
        yield f"data: {json.dumps(error_data)}\n\n"
    finally:
        # 确保临时文件被删除
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# ==== 🔗 定义 API 端点 ====
@app.post("/interview")
async def run_interview_analysis(
    pdf_file: UploadFile = File(..., description="用户上传的简历PDF文件"),
    gangwei: str = Form(..., description="希望面试的岗位"),
):
    """
    接收简历和岗位，流式返回面试分析结果。
    """
    if pdf_file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="文件格式错误，请上传PDF文件。")
    
    return StreamingResponse(
        stream_coze_workflow(pdf_file, gangwei),
        media_type="text/event-stream" # 指定为 Server-Sent Events 类型
    )

# ==== (可选) 用于本地测试的启动命令 ====
if __name__ == "__main__":
    import uvicorn
    # 运行服务器: uvicorn main:app --reload
    uvicorn.run(app, host="127.0.0.1", port=18000)
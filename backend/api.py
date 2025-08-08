import getpass
import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from adaptive_rag import create_graph

def _set_env(var: str):
    """安全地设置环境变量。"""
    if not os.environ.get(var):
        # 在非交互式服务器环境中，我们不能使用 getpass
        # 这里假设您已经通过其他方式（如 .env 文件或系统环境变量）设置了它们
        # 如果没有设置，服务启动时会因缺少密钥而失败
        api_key = os.environ.get(var)
        if not api_key:
            raise ValueError(f"环境变量 {var} 未设置。请在启动服务器前设置它。")

# --- 1. 设置 API 密钥 ---
# 在生产环境中，强烈建议使用 .env 文件或其他安全方式管理密钥
# 例如，使用 python-dotenv 库
# from dotenv import load_dotenv
# load_dotenv()
_set_env("OPENAI_API_KEY")
_set_env("TAVILY_API_KEY")

# --- 2. 创建 FastAPI 应用和 RAG 图 ---
app = FastAPI(
    title="Adaptive RAG API",
    description="一个通过 FastAPI 暴露的 Adaptive RAG 应用",
    version="1.0.0",
)

# 在应用启动时创建并加载 RAG 图
# rag_app = create_graph() #todo: 临时

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    接收一个问题，通过 Adaptive RAG 流程处理，并返回最终答案。
    """
    rag_app = create_graph() #todo: 临时
    inputs = {"question": request.question}
    final_generation = rag_app.invoke(inputs).get("generation", "未能生成答案。")
    return {"answer": final_generation}

@app.post("/ask_test", response_model=AnswerResponse)
async def ask_question_test(request: QuestionRequest):
    """
    用于 API 测试的端点，接收一个问题，返回一个固定的答案。
    """
    print(f"收到测试问题: {request.question}")
    fixed_answer = f"这是一个针对问题 '{request.question}' 的固定测试回答。"
    return {"answer": fixed_answer}

@app.get("/")
async def root():
    return {"message": "欢迎使用 Adaptive RAG API。请访问 /docs 查看 API 文档。"}

if __name__ == "__main__":
    # 使用 uvicorn 启动服务器
    # 在生产环境中，建议使用 Gunicorn + Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
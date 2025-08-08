# LangGraph Adaptive RAG Project

这是一个演示项目，展示了如何使用 LangGraph 构建一个自适应 RAG (Retrieval-Augmented Generation) 系统。项目包含一个 React 前端和一个 Python (FastAPI) 后端。

## 项目结构
.
├── backend/      # Python FastAPI 后端
│   ├── adaptive_rag.py
│   ├── api.py
│   ├── main.py
│   ├── README.md   # 后端专属说明
│   └── ...
├── frontend/     # React 前端 (待开发)
└── README.md     # 本文档


## 后端 (Backend)

后端使用 Python、FastAPI 和 LangGraph 实现 Adaptive RAG 流程。

详细的设置和运行说明，请参考 [backend/README.md](./backend/README.md)。

### 快速启动

1.  **进入后端目录**
    ```bash
    cd backend
    ```

2.  **设置环境并安装依赖**
    ```bash
    # 创建并激活虚拟环境
    python3 -m venv rag
    source rag/bin/activate

    # 安装依赖
    pip install -r requirements.txt
    ```

3.  **设置 API 密钥**
    ```bash
    export OPENAI_API_KEY="您的_OPENAI_API_密钥"
    export TAVILY_API_KEY="您的_TAVILY_API_密钥"
    ```

4.  **启动 API 服务器**
    ```bash
    python api.py
    ```

5.  **测试 API**
    服务器运行后，可以在 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看 API 文档，或使用以下命令测试：
    ```bash
    curl -X POST "http://127.0.0.1:8000/ask_test" -H "Content-Type: application/json" -d '{"question": "test"}'
    ```

## 前端 (Frontend)

前端部分计划使用 React 实现，用于提供一个用户友好的界面来与后端的 RAG 系统进行交互。

**(这部分尚未开发)**

### 计划功能

*   一个输入框，用于用户提问。
*   一个显示区域，用于展示 RAG 系统返回的答案。
*   调用后端的 `/ask` 或 `/ask_test` API 端点。

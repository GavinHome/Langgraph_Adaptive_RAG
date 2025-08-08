# LangGraph Adaptive RAG

这是一个演示项目，展示了如何使用 LangGraph 构建一个自适应 RAG (Retrieval-Augmented Generation) 系统。项目包含一个 React 前端和一个 Python (FastAPI) 后端。

## 项目结构

```text
.
├── LICENSE
├── README.md
├── README.zh.md
├── backend/
│   ├── README.md
│   ├── adaptive_rag.py
│   ├── api.py
│   └── requirements.txt
└── frontend/
    ├── README.md
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        └── index.js
```

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

## 前端 (Frontend)

前端使用 React 实现，提供一个用户友好的界面来与后端的 RAG 系统进行交互。

### 快速启动

1.  **进入前端目录**
    ```bash
    cd frontend
    ```

2.  **安装依赖**
    ```bash
    npm install
    ```

3.  **启动开发服务器**
    ```bash
    npm start
    ```
    应用将在 [http://localhost:3000](http://localhost:3000) 上运行。

4.  **环境变量配置**
    前端应用可以通过 `.env` 文件配置环境变量。例如，当后端服务部署在不同地址时，可以设置 `REACT_APP_API_BASE_URL`。开发环境留空后会代理到8000端口，可以在 `package.json` 中配置。

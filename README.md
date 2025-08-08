# LangGraph Adaptive RAG Project

This is a demo project that demonstrates how to build an Adaptive RAG (Retrieval-Augmented Generation) system using LangGraph. The project includes a React frontend and a Python (FastAPI) backend.

## Project Structure

```text
.
├── LICENSE
├── README.md
├── backend/
│   ├── .gitignore
│   ├── adaptive_rag.py
│   ├── api.py
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── .gitignore
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        └── index.js
```

## Backend

The backend is implemented using Python, FastAPI, and LangGraph to create the Adaptive RAG flow.

For detailed setup and running instructions, please refer to [backend/README.md](./backend/README.md).

### Quick Start

1.  **Navigate to the backend directory**
    ```bash
    cd backend
    ```

2.  **Set up the environment and install dependencies**
    ```bash
    # Create and activate a virtual environment
    python3 -m venv rag
    source rag/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Set API Keys**
    ```bash
    export OPENAI_API_KEY="your_openai_api_key"
    export TAVILY_API_KEY="your_tavily_api_key"
    ```

4.  **Start the API Server**
    ```bash
    python api.py
    ```

## Frontend

The frontend is built with React to provide a user-friendly interface for interacting with the backend RAG system.

### Quick Start

1.  **Navigate to the frontend directory**
    ```bash
    cd frontend
    ```

2.  **Install dependencies**
    ```bash
    npm install
    ```

3.  **Start the development server**
    ```bash
    npm start
    ```
    The application will run at [http://localhost:3000](http://localhost:3000).

4.  **Environment Variables**
    The frontend application can be configured with environment variables via `.env` files. For example, `REACT_APP_API_BASE_URL` can be set when the backend service is deployed at a different address. If left blank in the development environment, it will be proxied to port 8000, which can be configured in `package.json`.
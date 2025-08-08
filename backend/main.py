import getpass
import os
from adaptive_rag import create_graph

def _set_env(var: str):
    """安全地设置环境变量。"""
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"请输入您的 {var}: ")

def main():
    """主运行函数"""
    # --- 1. 设置 API 密钥 ---
    _set_env("OPENAI_API_KEY")
    _set_env("TAVILY_API_KEY")
    print("API 密钥设置完毕。")

    # --- 2. 创建 Adaptive RAG 应用 ---
    print("\n--- 正在创建 Adaptive RAG 应用 ---")
    app = create_graph()
    print("应用创建成功！")

    # --- 3. 运行测试用例 ---
    print("\n--- 测试用例 1: 应路由到 vectorstore ---")
    inputs1 = {"question": "What are the types of agent memory?"}
    for output in app.stream(inputs1):
        for key, value in output.items():
            print(f"节点 '{key}' 已执行。")
    final_generation1 = app.invoke(inputs1)["generation"]
    print(f"\n>>> 最终答案 1:\n{final_generation1}")

    print("\n--- 测试用例 2: 应路由到 web_search ---")
    inputs2 = {"question": "What player at the Bears expected to draft first in the 2024 NFL draft?"}
    for output in app.stream(inputs2):
        for key, value in output.items():
            print(f"节点 '{key}' 已执行。")
    final_generation2 = app.invoke(inputs2)["generation"]
    print(f"\n>>> 最终答案 2:\n{final_generation2}")

if __name__ == "__main__":
    main()
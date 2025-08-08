import os
from typing import List, Literal, TypedDict

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

# 1. 定义图的状态 (Define Graph State)
# 这是整个流程中传递的数据结构。
class GraphState(TypedDict):
    """图的状态

    Attributes:
        question: 用户问题
        generation: LLM 生成的答案
        documents: 检索到的文档列表
    """
    question: str
    generation: str
    documents: List[str]


def create_graph():
    """创建并编译一个完整的 Adaptive RAG 图。"""

    # --- 辅助组件初始化 (LLMs, Retriever, Prompts) ---
    # 这些是构成图节点和边的基础工具

    # LLMs
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Retriever
    embd = OpenAIEmbeddings()
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)
    vectorstore = Chroma.from_documents(
        documents=doc_splits, collection_name="rag-chroma", embedding=embd
    )
    retriever = vectorstore.as_retriever()

    # Router
    class RouteQuery(BaseModel):
        datasource: Literal["vectorstore", "web_search"] = Field(..., description="路由决策")
    structured_llm_router = llm.with_structured_output(RouteQuery)
    route_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个路由专家... (省略详细提示)"),
        ("human", "{question}"),
    ])
    question_router = route_prompt | structured_llm_router

    # Grader
    class GradeDocuments(BaseModel):
        binary_score: str = Field(description="相关性评分 'yes' 或 'no'")
    structured_llm_grader = llm.with_structured_output(GradeDocuments)
    grade_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个评估者... (省略详细提示)"),
        ("human", "文档: {document}\n问题: {question}"),
    ])
    retrieval_grader = grade_prompt | structured_llm_grader

    # Generator
    class Generate(BaseModel):
        generation: str = Field(description="生成的答案")
    structured_llm_generator = llm.with_structured_output(Generate)
    generate_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个问答助手... (省略详细提示)"),
        ("human", "问题: {question}\n上下文: {context}"),
    ])
    generator = generate_prompt | structured_llm_generator

    # 2. 定义图的流程 (Define Graph Flow)
    # 包括所有节点 (Nodes) 和边 (Edges)

    # 节点函数
    def retrieve(state):
        print("-> 节点: retrieve")
        state["documents"] = retriever.invoke(state["question"])
        return state

    def grade_documents(state):
        print("-> 节点: grade_documents")
        if state["documents"]:
            score = retrieval_grader.invoke({"question": state["question"], "document": state["documents"][0].page_content})
            if score.binary_score == "no":
                state["documents"] = [] # 评分不通过，清空文档
        return state

    def generate(state):
        print("-> 节点: generate")
        context = "\n\n".join([doc.page_content for doc in state["documents"]])
        generation = generator.invoke({"context": context, "question": state["question"]})
        state["generation"] = generation.generation
        return state

    def web_search(state):
        print("-> 节点: web_search")
        state["generation"] = "此问题需要网络搜索，目前实现为占位符。"
        state["documents"] = []
        return state

    # 条件边函数
    def route_question(state):
        source = question_router.invoke({"question": state["question"]})
        return "web_search" if source.datasource == 'web_search' else "vectorstore"

    def decide_to_generate(state):
        return "generate" if state["documents"] else "web_search"

    # 3. 编译图 (Compile Graph)
    workflow = StateGraph(GraphState)

    # 添加节点
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("web_search", web_search)

    # 设置入口和边
    workflow.set_conditional_entry_point(route_question, {"vectorstore": "retrieve", "web_search": "web_search"})
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges("grade_documents", decide_to_generate, {"generate": "generate", "web_search": "web_search"})
    workflow.add_edge("web_search", END)
    workflow.add_edge("generate", END)

    # 编译并返回
    return workflow.compile()
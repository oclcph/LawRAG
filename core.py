from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings  # 使用新版
from langchain_chroma import Chroma
import os
from chromadb import PersistentClient

# 法律专用提示模板
LAW_PROMPT = ChatPromptTemplate.from_template("""
你是一名专业法律助手，请严格根据以下条款回答：
----------------------------------------
{context}
----------------------------------------
问题：{question}

回答要求：
1. 引用具体条款（格式：根据《XX法》第X条）
2. 解释条款含义
3. 列出例外情况（如有）
""")

# 构建RAG链
embedding = HuggingFaceEmbeddings(
    model_name="models/text2vec-large-chinese",  # 本地路径
    model_kwargs={'device': 'cpu'}
)

import os
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('ALL_PROXY', None)
os.environ.pop('socks_proxy', None)


llm = ChatOpenAI(
    model="deepseek-r1",
    openai_api_key="sk-442b4075f26549a58c3c755b0c7a7685",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

client = PersistentClient(path="./law_db")
print("集合列表:", client.list_collections())
try:
    collection = client.get_collection("documents")
    print("集合存在，文档数:", collection.count())
except:
    print("集合不存在，可能未正确保存")
vectorstore = Chroma(
    persist_directory="./law_db",  # 与保存时的路径一致
    embedding_function=embedding,
    collection_name="documents"
)

if vectorstore._collection.count() == 0:  # 直接访问底层集合
    print("向量库为空")
else:
    print(f"向量库中有 {vectorstore._collection.count()} 个文档")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": LAW_PROMPT},
    return_source_documents=True,
    input_key="question"
)

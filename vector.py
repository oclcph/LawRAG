from chromadb import PersistentClient
from langchain_huggingface import HuggingFaceEmbeddings  # 使用新版
from langchain_community.vectorstores import Chroma
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from loader import chunks
import os

embedding = HuggingFaceEmbeddings(
    model_name="models/text2vec-large-chinese",  # 本地路径
    model_kwargs={'device': 'cpu'}
)

# 创建带元数据的向量库
# 1. 预计算带进度条的 embeddings
embeddings_list = []
for chunk in tqdm(chunks, desc="生成嵌入"):
    embeddings_list.append(embedding.embed_query(chunk.page_content))  # 假设 embedding 是 HuggingFaceEmbeddings

# 2. 创建 Chroma（跳过自动嵌入计算）
client = PersistentClient(path="./law_db")
try:
    client.delete_collection("documents")
except Exception as e:
    print(f"集合不存在或无权限删除: {e}")
collection = client.create_collection("documents")

print(f"准备添加 {len(chunks)} 条文档")
print(f"生成的embeddings数量: {len(embeddings_list)}")

# 4. 添加数据
collection.add(
    ids=[f"doc_{i}" for i in range(len(chunks))],
    documents=[doc.page_content for doc in chunks],
    embeddings=embeddings_list,
    metadatas=[doc.metadata for doc in chunks]
)

from chromadb import PersistentClient
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # 使用新版

client = PersistentClient(path="./law_db")
print("集合列表:", client.list_collections())
try:
    collection = client.get_collection("documents")
    print("集合存在，文档数:", collection.count())
except:
    print("集合不存在，可能未正确保存")

embedding = HuggingFaceEmbeddings(
    model_name="models/text2vec-large-chinese",  # 本地路径
    model_kwargs={'device': 'cpu'}
)
vectorstore = Chroma(
    persist_directory="./law_db",  # 与保存时的路径一致
    embedding_function=embedding,
    collection_name="documents"
)
# 4. 测试检索
if vectorstore._collection.count() > 0:
    print("检索测试:", vectorstore.similarity_search("法律", k=1))
else:
    print("向量库为空，需要重新保存数据")
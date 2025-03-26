from core import qa_chain

if __name__ == "__main__":
    question = "重伤是什么？"
    result = qa_chain.invoke(question)
    retrieved_docs = qa_chain.retriever.invoke(question)
    print(f"检索到的文档数: {len(retrieved_docs)}")

    print("【问题】", question)
    print("【回答】", result["result"])
    print("【参考条款】")
    for doc in result["source_documents"]:
        print(f"- {doc.metadata.get('法律名称', '')} 第{doc.metadata.get('条', 'N/A')}条")
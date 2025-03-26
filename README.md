# RAG应用后端
本RAG应用使用FastAPI架构。

`books`文件夹下为相关的法律条例，`models`文件夹下为将文档转换为向量所需要的大模型，转换后的向量保存在`law_db`下。

1. `api.py`封装后端主要逻辑
2. `core.py`封装RAG应用主要逻辑（加载向量库，提供prompt，构建基于Langchain的RAG链）
3. `loader.py`加载法律法规
4. `vector.py`依据文档构建向量库并做持久化
5. `main.py`为RAG逻辑脚本
6. `test.py`用于调试
7. `downloads.py`用于下载Huggingface的预训练模型（如果本地无代理可以直接从Huggingface下载）

常用命令：
``` python
# 测试RAG
python main.py

# 构建向量库
python vector.py
```

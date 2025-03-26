from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


class LawLoader(DirectoryLoader):
    def __init__(self, path, **kwargs):
        super().__init__(
            path,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"autodetect_encoding": True},
            **kwargs
        )

path = "./books/其他"
loader = LawLoader(path=path, show_progress=True)
docs = loader.load()
raw_texts = [doc.page_content for doc in docs]  # 仅提取文本内容
headers_to_split_on = [
    ("#", "法律名称"),
    ("##", "编/章"),
    ("###", "节"),
    ("####", "条")
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 4. 处理多个文档
header_docs = []
for text in raw_texts:
    header_docs.extend(splitter.split_text(text))  # 逐个处理文本

# 用 RecursiveCharacterTextSplitter 拆分长段落
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = []
for doc in header_docs:
    # 使用原文档的 metadata（如果存在），否则设置默认值
    metadata = doc.metadata if hasattr(doc, "metadata") and doc.metadata else {"source": "default"}
    # 分块并保留 metadata
    split_chunks = text_splitter.split_text(doc.page_content)
    chunks.extend([Document(page_content=chunk, metadata=metadata) for chunk in split_chunks])

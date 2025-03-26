FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# 下载预训练模型（建议提前放入镜像或使用Volume）
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
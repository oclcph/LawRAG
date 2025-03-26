FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# 下载预训练模型（建议提前放入镜像或使用Volume）
RUN python downloads.py
RUN python vector.py

CMD ["uvicorn", "api:app", "--host", "0.0.0.0"]
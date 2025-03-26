from fastapi import FastAPI
from pydantic import BaseModel
from core import qa_chain  # 复用现有核心逻辑

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/query")
async def query(input: Question):
    return {"answer": qa_chain.invoke(input.question)}
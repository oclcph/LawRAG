from sentence_transformers import SentenceTransformer

model = SentenceTransformer("GanymedeNil/text2vec-large-chinese", device='cpu')
model.save("./models/text2vec-large-chinese")  # 保存到指定目录
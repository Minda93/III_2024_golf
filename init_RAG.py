import os

import pandas as pd
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def create_documents(file_path):
    # 讀取回饋規則轉換成條列式的document
    data = pd.read_excel(file_path)
    documents = [
        Document(
            page_content=" | ".join(map(str, row.values)),
            metadata={"row_index": index}
        )
        for index, row in data.iterrows()
    ]
    print(f"生成了 {len(documents)} 個文檔")
    return documents


def vectorize_docunments(documents):
    # 使用 OpenAI Embeddings 進行向量化
    openai_api_key = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # 創建向量數據庫
    vectorstore = Chroma.from_documents(documents, embeddings)
    return vectorstore
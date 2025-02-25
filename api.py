import os

from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate


'''
setting
'''
# 載入環境變數
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 讀取 回饋規則 檔案
file_path = "data/回饋規則.xlsx"
data = pd.read_excel(file_path)

# 讀取初始提示
init_prompt =  open('data/rag_init_prompt.txt').read()

# 將數據轉換為文字格式（或提取特定欄位）
text_representation = data.to_string()


'''
setting
'''


def call_openai_api(image, text,vectorstore):
    # 初始化生成模型
    client = ChatOpenAI(api_key=openai_api_key, model="chatgpt-4o-latest", temperature=0.2)

    # 構建 RetrievalQA 鏈
    retriever = vectorstore.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        ('system', init_prompt + '{context}'),
        ('user', [
            {"type": "text", "text": "{input}"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/jpeg;base64,'{image}'",
                    "detail": "high",
                },
            },
        ],
         ),
    ])

    document_chain = create_stuff_documents_chain(client, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({
        'context': retriever,
        'image': image,
        'input': text,
    })
    return response['answer']

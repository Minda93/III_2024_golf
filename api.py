from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv

'''
setting
'''
# 載入環境變數
load_dotenv()

# 讀取 回饋規則 檔案
file_path = "data/回饋規則.xlsx"
data = pd.read_excel(file_path)

# 讀取初始提示
init_prompt =  open('data/init_prompt.txt').read()

# 將數據轉換為文字格式（或提取特定欄位）
text_representation = data.to_string()

# 定義提示字串
prompt = f"""
{init_prompt}
以下是一些來自回饋規則檔案的數據：
{text_representation}"""

'''
setting
'''


def call_openai_api(image, text):
    # 呼叫 OpenAI API
    client = OpenAI()

    completion = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}",
                            "detail": "high",
                        }
                    },
                ],
            }
        ]
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

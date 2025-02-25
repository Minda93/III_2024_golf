import base64
import eel
from PIL import Image
from io import BytesIO
import api
import init_RAG


#eel自動inject這個函數到js裡面
@eel.expose
def handle_text_and_image(image_data, text):
    print("Received image")
    image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))
    image.save("temp.jpg")
    with open("temp.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    response = api.call_openai_api(encoded_image, text,vectorstore)
    print(f"Received text: {text}")
    return response

documents = init_RAG.create_documents("data/回饋規則.xlsx")
vectorstore=init_RAG.vectorize_docunments(documents)

eel.init('web')
eel.start('index.html', size=(1920, 1080), mode="browser", port=8080)

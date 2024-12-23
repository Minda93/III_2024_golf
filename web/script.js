async function submitData() {
    document.getElementById("output").innerText = "Processing...";
    const imageInput = document.getElementById("imageInput");
    const textInput = document.getElementById("textInput").value;

    if (imageInput.files.length === 0) {
        alert("Please upload an image.");
        return;
    }

    const reader = new FileReader();
    reader.onload = async function () {
        const imageData = reader.result;
        // 调用 Python 後端api
        await eel.handle_text_and_image(imageData, textInput)(function (response) {
            document.getElementById("output").innerText = response;
        });
    };
    reader.readAsDataURL(imageInput.files[0]);
}

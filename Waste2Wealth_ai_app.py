import streamlit as st
from PIL import Image
import requests
import io

st.set_page_config(page_title="Waste2Wealth AI Lite", layout="centered")

st.title("♻️ Waste2Wealth AI Lite")
st.subheader("Extract Waste Type and Text from Uploaded Image")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

def extract_text_from_image(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={"filename": img_bytes},
        data={
            "apikey": "helloworld",  # Replace with your API key for production
            "language": "eng",
        },
    )

    result = response.json()
    if result.get("IsErroredOnProcessing"):
        return "OCR failed: " + result.get("ErrorMessage", ["Unknown error"])[0]
    return result["ParsedResults"][0]["ParsedText"]

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.markdown("### 🧠 Predicted Class: Plastic Bottle")
    st.markdown("### 💰 Estimated Value: ₦15.00")

    st.markdown("### 🔍 Extracted Text (OCR)")
    text = extract_text_from_image(image)
    st.text(text if text.strip() else "No text found.")

st.markdown("---")
st.caption("Powered by OCR.Space API + Streamlit")

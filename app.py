import streamlit as st
import easyocr
from PIL import Image
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.set_page_config(page_title="OCR App", layout="centered")

st.title("📝 Handwriting OCR App")
st.write("Upload an image and extract handwritten text instantly")

# Cache model (VERY IMPORTANT for speed)
@st.cache_resource
def load_model():
    return easyocr.Reader(['en'])

reader = load_model()

# Upload
uploaded_file = st.file_uploader("📤 Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Image", use_column_width=True)

    if st.button("🚀 Extract Text"):
        with st.spinner("Reading text..."):
            result = reader.readtext(np.array(image), detail=0)
            text = " ".join(result)

            st.success("✅ Text Extracted")

            # Show output
            st.subheader("📄 Output")
            st.write(text)

            # ---------------- DOWNLOAD TXT ----------------
            st.download_button(
                label="⬇️ Download as TXT",
                data=text,
                file_name="output.txt",
                mime="text/plain"
            )

            # ---------------- DOWNLOAD PDF ----------------
            def create_pdf(text):
                file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                doc = SimpleDocTemplate(file.name)
                styles = getSampleStyleSheet()
                story = [Paragraph(text, styles["Normal"])]
                doc.build(story)
                return file.name

            pdf_path = create_pdf(text)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download as PDF",
                    data=f,
                    file_name="output.pdf",
                    mime="application/pdf"
                )
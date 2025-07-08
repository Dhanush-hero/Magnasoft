# app.py
import streamlit as st
from utils.converter import convert_annotations
from utils.visualizer import draw_annotations
from utils.helpers import get_image_size, read_annotation_file
from PIL import Image

st.set_page_config(page_title="🧊 Annotation Format Converter", layout="wide")
st.title("🚀 Modular Annotation Format Tool")

with st.sidebar:
    st.header("📂 Upload Files")
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    annotation_file = st.file_uploader("Upload Annotation File", type=["json", "txt"])
    conversion_type = st.selectbox("Convert Format", [
        "GeoJSON → COCO", "COCO → YOLO", "YOLO → COCO"
    ])

if image_file and annotation_file:
    image = Image.open(image_file)
    width, height = get_image_size(image)
    annotation_text = annotation_file.read().decode("utf-8")

    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.markdown("---")

    try:
        converted, draw_boxes, ext = convert_annotations(
            conversion_type, annotation_text, width, height
        )
        st.subheader("📤 Converted Output")
        if ext == "json":
            st.json(converted)
            download_data = str(converted).encode()
        else:
            st.code(converted)
            download_data = converted.encode()

        st.download_button("⬇️ Download", data=download_data, file_name=f"converted.{ext}")
        st.subheader("🔍 Preview")
        fig = draw_annotations(image, draw_boxes)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("📎 Upload both image and annotation to start.")

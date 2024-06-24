import streamlit as st
from PIL import Image
import io
import zipfile

def resize_image(image, width, height):
    return image.resize((width, height))

def main():
    st.title("Batch Image Resizer")
    st.text("Especially for David")

    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        width = st.number_input("Width", value=100)
        height = st.number_input("Height", value=100)

        if st.button("Resize All"):
            resized_images = []
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                resized_image = resize_image(image, width, height)
                resized_images.append((uploaded_file.name, resized_image))
                st.image(resized_image, caption=f"Resized Image: {uploaded_file.name}", use_column_width=True)

            with io.BytesIO() as buffer:
                with zipfile.ZipFile(buffer, "w") as zip_file:
                    for file_name, resized_image in resized_images:
                        img_byte_arr = io.BytesIO()
                        resized_image.save(img_byte_arr, format='PNG')
                        zip_file.writestr(file_name, img_byte_arr.getvalue())
                buffer.seek(0)
                st.download_button("Download All Resized Images", data=buffer, file_name="resized_images.zip", mime="application/zip")

if __name__ == "__main__":
    main()

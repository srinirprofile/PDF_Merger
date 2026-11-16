
import streamlit as st
import re
from io import BytesIO
from PIL import Image
from pypdf import PdfWriter

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="PDF Merger",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF & Image Merger")
st.write("Upload multiple PDF and image files to combine them into one PDF.")

# --------------------------------
# NATURAL SORTING
# --------------------------------

def natural_sort_key(text):
    return [
        int(c) if c.isdigit() else c.lower()
        for c in re.split(r"(\d+)", text)
    ]

# --------------------------------
# FILE UPLOADER
# --------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF or Image Files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# --------------------------------
# DISPLAY UPLOADED FILES
# --------------------------------

if uploaded_files:

    # Sort files naturally
    uploaded_files = sorted(
        uploaded_files,
        key=lambda file: natural_sort_key(file.name)
    )

    st.subheader("Uploaded Files")

    for index, file in enumerate(uploaded_files, start=1):
        st.write(f"{index}. {file.name}")

    st.write(f"Total files: {len(uploaded_files)}")

    # --------------------------------
    # MERGE BUTTON
    # --------------------------------

    if st.button("Merge PDF", type="primary"):

        writer = PdfWriter()
        output_buffer = BytesIO()

        try:

            for file in uploaded_files:

                st.write(f"Processing: {file.name}")

                file_bytes = file.getvalue()

                # Existing PDF
                if file.name.lower().endswith(".pdf"):

                    writer.append(BytesIO(file_bytes))

                # Image files
                else:

                    img = Image.open(BytesIO(file_bytes))

                    if img.mode != "RGB":
                        img = img.convert("RGB")

                    # Convert image into PDF in memory
                    image_pdf = BytesIO()

                    img.save(image_pdf, format="PDF")
                    image_pdf.seek(0)

                    # Append image PDF
                    writer.append(image_pdf)

            # Save merged PDF in memory
            writer.write(output_buffer)
            output_buffer.seek(0)

            st.success("PDF created successfully!")

            # --------------------------------
            # DOWNLOAD BUTTON
            # --------------------------------

            st.download_button(
                label="⬇️ Download Merged PDF",
                data=output_buffer.getvalue(),
                file_name="Merged_All.pdf",
                mime="application/pdf"
            )

        except Exception as e:

            st.error(f"Error while merging files: {e}")

        finally:

            writer.close()

else:

    st.info("Please upload at least one PDF or image file.")


import streamlit as st
import re
from io import BytesIO
from PIL import Image
from pypdf import PdfWriter


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="PDF Merger",
    page_icon="📄",
    layout="centered"
)


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================

if "merged_pdf" not in st.session_state:
    st.session_state.merged_pdf = None


# ==========================================
# 3. APPLICATION TITLE
# ==========================================

st.title("📄 PDF & Image Merger")

st.write(
    "Upload multiple PDF and image files "
    "to combine them into a single PDF."
)


# ==========================================
# 4. NATURAL SORTING FUNCTION
# ==========================================

def natural_sort_key(text):

    return [
        int(c) if c.isdigit() else c.lower()
        for c in re.split(r"(\d+)", text)
    ]


# ==========================================
# 5. FILE UPLOADER
# ==========================================

uploaded_files = st.file_uploader(
    "Upload PDF or Image Files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)


# ==========================================
# 6. DISPLAY UPLOADED FILES
# ==========================================

if uploaded_files:

    # Sort files naturally
    uploaded_files = sorted(
        uploaded_files,
        key=lambda file: natural_sort_key(file.name)
    )

    st.subheader("Uploaded Files")

    for index, file in enumerate(uploaded_files, start=1):

        st.write(f"{index}. {file.name}")

    st.info(f"Total files uploaded: {len(uploaded_files)}")


    # ==========================================
    # 7. MERGE PDF BUTTON
    # ==========================================

    if st.button("Merge PDF", type="primary"):

        writer = PdfWriter()

        output_buffer = BytesIO()

        # Clear previous output
        st.session_state.merged_pdf = None

        try:

            progress = st.progress(0)

            for index, file in enumerate(uploaded_files):

                st.write(f"Processing: {file.name}")

                file_bytes = file.getvalue()

                # ----------------------------------
                # EXISTING PDF FILE
                # ----------------------------------

                if file.name.lower().endswith(".pdf"):

                    writer.append(BytesIO(file_bytes))

                # ----------------------------------
                # IMAGE FILE
                # ----------------------------------

                else:

                    img = Image.open(BytesIO(file_bytes))

                    try:

                        if img.mode != "RGB":

                            img = img.convert("RGB")

                        # Convert image into PDF in memory
                        image_pdf = BytesIO()

                        img.save(
                            image_pdf,
                            format="PDF"
                        )

                        image_pdf.seek(0)

                        # Append image PDF
                        writer.append(image_pdf)

                        image_pdf.close()

                    finally:

                        img.close()

                progress.progress(
                    (index + 1) / len(uploaded_files)
                )

            # ----------------------------------
            # GENERATE FINAL MERGED PDF
            # ----------------------------------

            writer.write(output_buffer)

            output_buffer.seek(0)

            # Store generated PDF in session state
            st.session_state.merged_pdf = (
                output_buffer.getvalue()
            )

            st.success("PDF created successfully!")

        except Exception as e:

            st.error(f"Error while merging files: {e}")

        finally:

            writer.close()
            output_buffer.close()


    # ==========================================
    # 8. DOWNLOAD MERGED PDF
    # ==========================================

    if st.session_state.merged_pdf:

        st.download_button(
            label="⬇️ Download Merged PDF",

            data=st.session_state.merged_pdf,

            file_name="Merged_All.pdf",

            mime="application/pdf",

            type="primary"
        )

else:

    st.session_state.merged_pdf = None

    st.info("Please upload at least one PDF or image file.")


# Initialize session state
if "merged_pdf" not in st.session_state:
    st.session_state.merged_pdf = None

# Merge button
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

                image_pdf = BytesIO()

                img.save(image_pdf, format="PDF")
                image_pdf.seek(0)

                writer.append(image_pdf)

                img.close()

        # Generate final PDF
        writer.write(output_buffer)

        # Store PDF in session state
        st.session_state.merged_pdf = output_buffer.getvalue()

        st.success("PDF created successfully!")

    except Exception as e:

        st.error(f"Error while merging files: {e}")

    finally:

        writer.close()
        output_buffer.close()


# Download button outside merge condition
if st.session_state.merged_pdf:

    st.download_button(
        label="⬇️ Download Merged PDF",
        data=st.session_state.merged_pdf,
        file_name="Merged_All.pdf",
        mime="application/pdf"
    )

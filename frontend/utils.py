import os
import streamlit as st
import base64
import fitz
from io import BytesIO

def save_uploaded_file(uploaded_file, directory):
    if uploaded_file is not None:
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Convert uploaded file buffer to a BytesIO object
        file_stream = BytesIO(uploaded_file.getbuffer())
        
        # Load the PDF from the BytesIO object
        doc = fitz.open(stream=file_stream, filetype="pdf")

        # Iterate through each page in the PDF
        for i, page in enumerate(doc):
            # Render the page to an image (pixmap)
            pix = page.get_pixmap()

            # Construct the image path
            image_path = os.path.join(directory, f"{uploaded_file.name}_page_{i+1}.png")

            # Save the image
            pix.save(image_path)
        
        # Close the document
        doc.close()
        
    return None

def save_pdf_as_image(pdf_path):
    # Open the PDF document
    doc = fitz.open(pdf_path)
    
    # Ensure the document is not empty
    if len(doc) > 0:
        # Get the first page
        page = doc[0]
        
        # Render the page to an image (pixmap)
        pix = page.get_pixmap()
        
        # Determine the image path based on the PDF path
        image_path = pdf_path.rsplit('.', 1)[0] + '.png'
        
        # Save the pixmap (image) to a file
        pix.save(image_path)
        
        # Close the document
        doc.close()
        
        return image_path
    else:
        # Close the document and return None if it's empty
        doc.close()
        return None



def displayImage(image_path):
    # Check if the image exists
    if not os.path.exists(image_path):
        print(image_path)
        st.info("Give us your info so we can display it here.")
        return

    # Display the image
    st.image(image_path, width=700)
    
def display_images_from_folder(folder_path):
    images = os.listdir(folder_path)
    for image_name in images:
        image_path = os.path.join(folder_path, image_name)
        st.image(image_path, caption=image_name, use_column_width=True)


def displayPDF(uploaded_file):
    # Read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="300" type="application/pdf"></iframe>'
    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)
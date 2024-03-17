import streamlit as st
import PyPDF2

import joblib
from save_to import text_to_pdf

medic = joblib.load('falcon_medic.joblib')


dialogue_model=joblib.load('tk5_dialogue.joblib')

def extract_text_from_pdf(uploaded_file,selected_pages=None):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    num_pages = len(pdf_reader.pages)

    if selected_pages is None:
        selected_pages = range(1, num_pages + 1)  # PyPDF2 pages are 0-indexed
    for page_num in selected_pages:
        # Adjust for 0-indexing of PyPDF2
        page_index = page_num - 1
        if 0 <= page_index < num_pages:
            page = pdf_reader.pages[page_index]
            text += page.extract_text() + "\n"
        else:
            print(f"Page {page_num} is out of range. Skipping.")

    return text

# Function for dialogue summarization
def summarize_dialogue(dialogue_text):
    # Add your dialogue summarization logic here
    return "Summarized Dialogue: " + dialogue_model(dialogue_text)[0]['summary_text']  # Placeholder logic

# Streamlit app
def main():
    st.title("Summarization App")

    # Sidebar with buttons
    st.sidebar.title("Summarization Options")
    summarization_option = st.sidebar.radio("Choose Summarization Type", ("Dialogue", "Health Report"))

    if summarization_option == "Dialogue":
        st.header("Dialogue Summarization")
        dialogue_text = st.text_area("Enter the dialogue:")
        if st.button("Summarize"):
            if dialogue_text:
                summarized_dialogue = summarize_dialogue(dialogue_text)
                st.write(summarized_dialogue)
            else:
                st.warning("Please enter some text to summarize.")

    elif summarization_option == "Health Report":
        st.header("Health Report Summarization")
        all_pages = st.checkbox("Summarize all pages")
        if not all_pages:
            st.write("Enter the page numbers to summarize (comma-separated):")
            page_input = st.text_input("Page numbers")
            selected_pages = [int(page.strip()) for page in page_input.split(',') if page.strip().isdigit()]
        else:
            selected_pages = None  # Summarize all pages

        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file is not None:
            # Extract text from uploaded PDF
            text = extract_text_from_pdf(uploaded_file,selected_pages)
            st.header("Original Text:")
            st.text(text)
            if st.button("Summarize"):
                if text:
                    summarized_dialogue = medic(text)[0]["summary_text"]
                    st.write(summarized_dialogue)
                    pdf_filename = text_to_pdf(summarized_dialogue)

# Provide download button for the PDF
                    with open(pdf_filename, "rb") as f:
                        st.download_button(
                        label="Download Summary as PDF",
                        data=f,
                        file_name="summary.pdf",
                        mime="application/pdf"
                        )
                else:
                    st.warning("Please enter some text to summarize.")
                
            # Add your health report summarization code here


if __name__ == "__main__":
    main()

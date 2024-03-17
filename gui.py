import streamlit as st
import os


def execute_script(script_path):
    os.system(f"streamlit run {script_path}")


def main():
    st.title("Linguistic Odyssey")

    
    if st.button("Text Summarization"):
        execute_script("summarisation.py")

  
    if st.button("Customer Sentiment Analysis"):
        execute_script("sentiment.py")
    
  
    if st.button("Admin Login"):
        execute_script("admin.py")
    
if __name__ == "__main__":
    main()

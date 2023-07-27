import os
import tempfile
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from src.utils import setup_dbqa
from db_build import run_db_build
from langchain.callbacks import StreamlitCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.callbacks.base import CallbackManager


    
	    

def generate_response(uploaded_file, query_text):
    print("uploaded file is",uploaded_file)
    temp_file_path = os.getcwd()
    if uploaded_file is not None:
        
        # Save the uploaded file to a temporary location
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)
        print(temp_file_path)
        with open(temp_file_path, "wb") as temp_file:             
            temp_file.write(uploaded_file.read())
        
        # loaded_text=pdf_to_pages(uploaded_file) 
        run_db_build(temp_file_path)
        dbqa = setup_dbqa()
        return dbqa.run(query_text)

# Customize the layout
st.set_page_config(page_title="PnC Claims", page_icon="🤖", layout="wide", )     
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1509537257950-20f875b03669?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1469&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)
st.title("📄 Analyse Claim 🤖")


# File upload
uploaded_file = st.file_uploader('Upload an article', type='pdf')


# Query text
query_text = st.text_input('Enter your question:', placeholder = 'Please provide a short summary.', disabled=not uploaded_file)


# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    # openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_file and query_text))
    submitted = st.form_submit_button('Submit', disabled=not(uploaded_file and query_text))
    if submitted :
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file,  query_text)
            result.append(response)
            

if len(result):
    st.info(response)

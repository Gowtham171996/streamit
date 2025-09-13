#https://github.com/riteshhere/creativeWriter-llama


import streamlit as st
import os,torch
from headerfooter import footer,Disclaimer,JobSearch
from llama_cpp import Llama
LANGCHAIN_TRACING_V2=False


## Function to get response from LLAMA 2 Model
def getLlamaResponse(input_text, no_words, category):
    
    MODEL_PATH = "gemma-3-4b-it-q4_0.gguf"

    # Load the GGUF model using llama-cpp-python
    print("Loading the Gemma GGUF model...")
    try:
        llm = Llama(
            model_path=MODEL_PATH,
            chat_format="llama-2", # Gemma-3 models can use llama-2 or other chat formats
            n_ctx=4096, # Adjust the context size as needed
            n_gpu_layers=-1 if torch.cuda.is_available() else 0,
            n_threads=os.cpu_count()
        )
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        llm = None

    # Construct the prompt as a list of message dictionaries
    messages = [
        {"role": "system", "content": f"You are a {category} writing assistant."},
        {"role": "user", "content": f"Write a {category} on {input_text} in less than {no_words} words."}
    ]

    with st.spinner("Running the model... just a few seconds more..."):
        try:
            # Use the correct method for chat-formatted models
            response = llm.create_chat_completion(
                messages=messages,
                stop=["</s>"], # Stop generation when the end-of-turn token is encountered
                stream=False
            )
            
            # The actual generated text is nested within the response dictionary
            generated_text = response['choices'][0]['message']['content']
            return generated_text
        except Exception as e:
            st.error(f"Error generating response: {e}")
            return f"An error occurred: {e}"



st.set_page_config(page_title = "Essay Writer",
                    layout='centered',
                    initial_sidebar_state = "auto")


col1, col2 = st.columns([60,40],gap="medium",vertical_alignment="bottom")
with st.container(border=True):
    with col1:
        st.header("Essay Writer")
    with col2:    
        if st.button("Home",use_container_width=True):
            st.switch_page("Home.py")

st.write("---")

with st.container(border=True):
    input_text = st.text_input("Enter the topic you want to write about:","Australia")

    col1,col2 = st.columns([5,5])

    with col1:
        no_words = st.text_input('No of words',"200")
    with col2:
        category = st.selectbox("category",
                                ('Story', 'Poem', 'Blog'),
                                index=0)
        
    submit = st.button("Generate")

    if submit:
        st.write(getLlamaResponse(input_text, no_words, category))



Disclaimer()
st.markdown(footer,unsafe_allow_html=True)
#Getlogo()
JobSearch()
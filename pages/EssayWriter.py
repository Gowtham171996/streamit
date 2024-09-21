#https://github.com/riteshhere/creativeWriter-llama


from pathlib import Path
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from accelerate import Accelerator
import streamlit as st
from urllib.request import urlopen
from shutil import copyfileobj

#accelerator = Accelerator()
URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q3_K_S.gguf"
MODELPATH = "models/llama-2-7b-chat.Q3_K_S.gguf"

def load_model():

    save_dest = Path('models')
    save_dest.mkdir(exist_ok=True)
    
    f_checkpoint = Path(MODELPATH)

    if not f_checkpoint.exists():
        with st.spinner("Downloading model... this may take awhile! \n Don't stop it!"):
            with urlopen(URL) as in_stream, open(MODELPATH, 'wb') as out_file:
                copyfileobj(in_stream, out_file)
        print("Finished Downloading model")
    else:
        print("Model already exists.")


## Function to get response from LLAMA 2 Model
def getLlamaResponse(input_text, no_words, category):
    load_model()
     
    llm = CTransformers(model = MODELPATH,
                        model_type = 'llama',
                        config={'max_new_tokens': 256,
                                'temperature': 0.01,
                                #'gpu_layers':50
                                })
    
    #llm = accelerator.prepare(llm)
    
    ## PromptTemplate
    template = """Write a  {category} on {input_text} in less than {no_words} words"""

    prompt = PromptTemplate(input_variables = ["input_text", "no_words", "category"],
                            template = template)
    
    with st.spinner("Running the model... just few seconds more...."):
        ## Generate the reponse from the LLama 2 Model
        respone = llm.invoke(prompt.format(category=category,input_text=input_text,no_words=no_words))
        print(respone)
    return respone



st.set_page_config(page_title = "Essay Writer",
                    layout='centered',
                    initial_sidebar_state = "expanded")


col1, col2 = st.columns(2)
with st.container(border=True):
    with col1:
        st.header("Essay Writer")
    with col2:    
        if st.button("Home",use_container_width=True):
            st.switch_page("Home.py")

with st.container(border=True):
    input_text = st.text_input("Enter the topic you want to write about")

    col1,col2 = st.columns([5,5])

    with col1:
        no_words = st.text_input('No of words')
    with col2:
        category = st.selectbox("category",
                                ('Essays', 'Poem', 'Blog'),
                                index=0)
        
    submit = st.button("Generate")

    if submit:
        st.write(getLlamaResponse(input_text, no_words, category))
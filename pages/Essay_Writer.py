#https://github.com/riteshhere/creativeWriter-llama


import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from accelerate import Accelerator
import streamlit as st

accelerator = Accelerator()
## Function to get response from LLAMA 2 Model
def getLlamaResponse(input_text, no_words, category):
    llm = CTransformers(model = 'models\llama-2-7b-chat.Q3_K_S.gguf',
                        model_type = 'llama',
                        config={'max_new_tokens': 256,
                                'temperature': 0.01,
                                'gpu_layers':50
                                })
    
    llm = accelerator.prepare(llm)
    
    ## PromptTemplate
    template = """Write a  {category} on {input_text} in less than {no_words} words"""

    prompt = PromptTemplate(input_variables = ["input_text", "no_words", "category"],
                            template = template)
    
    ## Generate the reponse from the LLama 2 Model
    respone = llm(prompt.format(category=category,input_text=input_text,no_words=no_words))
    print(respone)
    return respone



st.set_page_config(page_title = "Essay Writer",
                    layout='centered',
                    initial_sidebar_state = "collapsed")

st.header("Essay Writer")
if st.button("Home"):
    st.switch_page("Home.py")

with st.container(border=True):
    input_text = st.text_input("Enter the topic you want to write about")

    col1,col2 = st.columns([5,5])

    with col1:
        no_words = st.text_input('No of words')
    with col2:
        category = st.selectbox("category",
                                ('Essays', 'Poem', 'Joke', 'Blog'),
                                index=0)
        
    submit = st.button("Generate")

    if submit:
        st.write(getLlamaResponse(input_text, no_words, category))
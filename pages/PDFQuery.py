from pypdf import PdfReader
import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
from headerfooter import footer,Disclaimer

def ReadPDF(file_path):
    #file_path = "models/sanjith-authorizationletter.pdf"
    reader  = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    return text

def FindAnswer(context,question):
    qa_pipeline = pipeline(
        "question-answering",
        "distilbert-base-cased-distilled-squad",
        #"timpal0l/mdeberta-v3-base-squad2",
        #model="mrm8488/bert-small-finetuned-squadv2",
        #tokenizer="mrm8488/bert-small-finetuned-squadv2",
        framework="pt"
    )

    answer = qa_pipeline({
        'context': context,
        'question': question
    })

    # Print the answer
    print("Answer:", answer)
    return answer



st.set_page_config(page_title = "PDF Query",
                    layout='centered',
                    initial_sidebar_state = "auto")

col1, col2 = st.columns(2)
with st.container(border=True):
    with col1:
        st.header("PDF Question and Answering")
    with col2:    
        if st.button("Home",use_container_width=True):
            st.switch_page("Home.py")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


with st.container(border=True):
    
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    
    #question = st.text_input("Enter the Question:",'Where is the office ?')

    #messages = st.container(height=300)
    if uploaded_file is not None:
        context = ReadPDF(uploaded_file) 

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        ######################################################################################
        
        if question := st.chat_input(placeholder="Enter the Question:"):
            st.session_state.messages.append({"role": "user", "content": question})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(question)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                answer = FindAnswer(context,question)["answer"]
                response = st.write(answer)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})


        ###########################################################################################

    else:
        st.markdown(''':red[Please upload the PDF file.]''')


Disclaimer()
st.markdown(footer,unsafe_allow_html=True)

                #context = "remember the number 123456, I'll ask you later."
            #print(context)
            #question = "Where is the office ?"

        #question = st.chat_input("Say something")
        #if question:
        #    messages.chat_message("user").write(question)
        #    answer = FindAnswer(context,question)
        #    #st.write(answer)
        #    messages.chat_message("assistant").write(f"Echo: {answer}")
        
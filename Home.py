#https://github.com/riteshhere/creativeWriter-llama


import streamlit as st
from headerfooter import footer,Disclaimer 
st.set_page_config(page_title = "Gowtham B C Portfolio",layout='centered',initial_sidebar_state = "expanded")

#st.markdown(header,unsafe_allow_html=True)

st.title("Gowtham B C Portfolio")
st.header("✍️ LLM Tools Demo", divider=True)

with st.container(border=True):
    col1, col2 = st.columns([30,70],gap="medium")
    with col1:
        if st.button("Summarizer"):
            st.switch_page("pages/Summarizer.py")
    with col2:
        st.markdown("This is a simple text summarizer which will take an lenghty essay input and try to summarize it. ")


with st.container(border=True):
    col1, col2 = st.columns([30,70],gap="medium")
    with col1:
        if st.button("Essay Writer"):
            st.switch_page("pages/EssayWriter.py")
    with col2:
        st.markdown("This is a simple essay writer which will write a breif essay on the topic provided. ")


with st.container(border=True):
    col1, col2 = st.columns([30,70],gap="medium")
    with col1:
        if st.button("PDF Question & Answer"):
            st.switch_page("pages/PDFQuery.py")
    with col2:
        st.markdown("A Q&A tool which accepts PDF in text format and answers question based on the PDF text.  \n"  
                    ":red[Note:] Future support: OCR and from url")


with st.container(border=True):
    col1, col2 = st.columns([30,70],gap="medium")
    with col1:
        if st.button("Web Scrapper"):
            st.switch_page("pages/WebScraper.py")
    with col2:
        st.markdown("A webscraper which will take a URL as input and try to organise text information to dataframes. ")    

Disclaimer("These models are very small in neurons (computation capabilities) hence they cant perform like state of the art solutions. These models are here to demonstrate the ability that these systems can be built by the Gowtham B C. Provided enough time and resources.")
#st.markdown("Email Id: bcgowtham17@gmail.com")
st.markdown(footer,unsafe_allow_html=True)



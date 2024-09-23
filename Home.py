#https://github.com/riteshhere/creativeWriter-llama


import streamlit as st
st.set_page_config(page_title = "Gowtham B C Portfolio",layout='centered',initial_sidebar_state = "expanded")

st.title("Gowtham B C Portfolio")
st.header("✍️ LLM Tools Demo", divider=True)

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Web Scrapper"):
            st.switch_page("pages/WebScraper.py")
    with col2:
        st.markdown("A webscraper which will take a URL as input and try to organise text information to dataframes. ")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Summarizer"):
            st.switch_page("pages/Summarizer.py")
    with col2:
        st.markdown("This is a simple text summarizer which will take an lenghty essay input and try to summarize it. ")


with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Essay Writer"):
            st.switch_page("pages/EssayWriter.py")
    with col2:
        st.markdown("This is a simple essay writer which will write a breif essay on the topic provided. ")


st.markdown("Note: These models are very small in neurons (computation capabilities) hence they cant perform like state of the art solutions. These models are here to demonstrate the ability that these systems can be built by the Gowtham B C. Provided enough time and resources.")
st.markdown("Email Id: bcgowtham17@gmail.com")    




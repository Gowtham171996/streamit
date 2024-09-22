import streamlit as st
import requests
from bs4 import BeautifulSoup



def WebParser(url):
    webresponse = requests.get(url)

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(webresponse.content, 'html.parser')
    print(soup)

    # Step 3: Find all relevant sections (articles)
    paragraphs = soup.find_all('p')
    
    text = ""
    # Extract and print the content of each paragraph
    for p in paragraphs:
        text += p.get_text() + "\n" 
        print(p.get_text())
        print()  # Print a blank line between paragraphs
    
    print("Finished")
    return text



st.set_page_config(page_title = "Web Scrapper",
                    layout='centered',
                    initial_sidebar_state = "expanded")

col1, col2 = st.columns(2)
with st.container(border=True):
    with col1:
        st.header("Web Scrapper")
    with col2:    
        if st.button("Home",use_container_width=True):
            st.switch_page("Home.py")

with st.container(border=True):
    input_URL = st.text_input("Enter the URL to parse:",'https://www.gesetze-im-internet.de/englisch_gg/englisch_gg.html')

    #col1,col2 = st.columns(2)

    #with col1:
    #    no_words = st.text_input('No of words')
    #with col2:
    #    category = st.selectbox("category",
    #                            ('Story', 'Poem', 'Blog'),
    #                            index=0)
        
    submit = st.button("Generate")

    if submit:
        st.write("Parsed:", WebParser(input_URL))
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from headerfooter import footer,Disclaimer,JobSearch



def WebParser(url,table):
    webresponse = requests.get(url)

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(webresponse.content, 'html.parser')
    print(soup)

    # Step 3: Find all relevant sections (articles)
    paragraphs = soup.find_all('p')
    
    text = ""
    # Extract and print the content of each paragraph
    i = 0
    for p in paragraphs:
        table.loc[i] = [p.get_text()]
        i += 1
        #table.add_rows(st.text(p.get_text()))
        #text += p.get_text() + "\n" 
        print(p.get_text())
        print()  # Print a blank line between paragraphs
    
    print("Finished")
    return table



st.set_page_config(page_title = "Web Scrapper",
                    layout='centered',
                    initial_sidebar_state = "expanded")

col1, col2 = st.columns([60,40],gap="medium",vertical_alignment="bottom")
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
        df = pd.DataFrame({"paragraph": []})
        
        df = WebParser(input_URL,df)
        df = df.drop_duplicates()
        table = st.dataframe(df,use_container_width=True)

Disclaimer("Since every site has there own html tags and styles, currently it is optimised for default site url. Which can be extended as in required.")

st.markdown(footer,unsafe_allow_html=True)
JobSearch()
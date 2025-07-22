#  Emoji https://emojidb.org/ai-emojis?utm_source=user_search

import streamlit as st
from pathlib import Path
from PIL import Image
import base64,os

def Getlogo():
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    logopath = current_dir / "pages" / "assets" / "logo2.png"
    logo = st.logo(
        image=Image.open(logopath)
    )
    return logo

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_img_with_href(local_img_path, target_url):
    #img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    img_format = "svg+xml"
    bin_str = get_base64_of_bin_file(local_img_path)

    html_code = f''' 
        <a href="{target_url}">
            <img  class = 'fullHeight' src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code

def sidebar():
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    css_file = current_dir / "pages/assets" / "main.css"
    with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


def Disclaimer(text=""):
    disclaimerbox = st.container(border=True)
    with disclaimerbox:
        if(text == ""):
            st.markdown('''
                :red[NOTE:] 
                    Since the Freemium server computation capability is restricted to 2.3GB RAM. 
                Considerably very small LLM's are used. This can be easily scaled as in when hardware resources are available which gives better performance.  ''')
        else:
            st.markdown( ":red[NOTE:] " + text)

    return disclaimerbox



def JobSearch():
    jobsearchbanner = st.sidebar
    SHOWBANNER:bool = st.secrets["SHOWBANNER"]
    if SHOWBANNER:
        with jobsearchbanner:
            if st.button("Hi, I am Gowtham BC looking for Job opportunities within Germany.",help="Digital CV link",use_container_width=True):
                    st.switch_page("pages/Resume.py")
            st.html('''<p style='color:black;'> Location: Berlin, Germany, 🇩🇪 </br>
                    <b> Data Science & AI Team Lead </b> with 6.5+ years work experience in AI, Software engineer & Consulting</br>
                    <b>Relocation</b>: Throughout Germany </br>
                    <b>Joining</b>: 2 Weeks notice </br>
                    <b>Visa</b>: Permanent Residense
                    </p>''')

    return jobsearchbanner



footer="""<style>
a:link , a:visited > span{
    background-color: transparent;
    color: black ;
}

a:link  > span{
    background-color: transparent;
    color: black ;
}

a:hover,  a:active {
    background-color: transparent;
    color:red;
}

hr {
    border-bottom:4px solid rgba(245, 222, 179, 0.2);
}

/* Change the sidebar color*/
[data-testid=stSidebar] {
  background-image: linear-gradient(#ffffff, #e3daab);
}

section[data-testid="stSidebar"] {
    width: 25% !important; 
}

 [data-testid="stSidebarHeader"]::before {
                content: "Gowtham Portfolio";
                margin-left: 10px;
                margin-top: 20px;
                font-size: inherit;
                font-weight: bold;
                top: 100px;
                color:black;
            }

[data-testid=stSidebarCollapseButton], [data-testid=stSidebarNavViewButton],[data-testid=stSidebarNavItems] > header  {
  color:black !important;
}



.footercustom {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgb(38 39 48);
    color: black;
    text-align: center;
}

</style>
<div class="footercustom">
    <p style="color:white;">
        Developed with ❤ by
        <a style='text-align:center;text-decoration: auto; color: wheat ;' href="https://www.linkedin.com/in/gowtham-buvalli-chikkathammaiah-788b62a9/" target="_blank">
            Gowtham B C 
        </a>
    </p>
</div>
"""


#.stLogo {
#    height: 10vh;
#    width: calc(100vw - 150px);
#}







































###################################################################################################################################
header="""<style>

.headercustom {
    position: fixed;
    left: 0px;
    Top: 100px;
    width:100%;
    background-color: rgb(38 39 48);
    color: black;
    text-align: center;
    z-index:100;
}

</style>
<div class="headercustom">
    <p>
        <a style='text-decoration: auto; color: wheat ;' href="https://www.linkedin.com/in/gowtham-buvalli-chikkathammaiah-788b62a9/" target="_blank">
            Hi, I am Gowtham BC looking for Job oppurtunities in Germany. 
            reach me at bcgowtham17@gmail.com
        </a>
    </p>
</div>
"""

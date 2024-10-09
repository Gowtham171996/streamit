import streamlit as st
from pathlib import Path

import base64,os


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

header="""<style>

.header {
    position: fixed;
    left: 0;
    bottom: 1;
    width: 100%;
    background-color: rgb(38 39 48); 
    color: black;
    text-align: center;
}

</style>
<div class="header">
        <h3 style="color:wheat;">
            Gowtham B C Portfolio
        </h3>
</div>
"""


footer="""<style>
a:link , a:visited{
    background-color: transparent;
    color: wheat;
}

a:hover,  a:active {
    background-color: transparent;
    color:red;
}

/* Change the sidebar color*/
[data-testid=stSidebar] {
  background-image: linear-gradient(#000395,#EC058E);
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgb(38 39 48);
    color: black;
    text-align: center;
}

</style>
<div class="footer">
    <p style="color:white;">
        Developed with ❤ by
        <a style='text-align:center;text-decoration: auto;' href="https://www.linkedin.com/in/gowtham-buvalli-chikkathammaiah-788b62a9/" target="_blank">
            Gowtham B C 
        </a>
    </p>
</div>
"""


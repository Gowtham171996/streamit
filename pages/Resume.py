#https://github.com/Sven-Bo/digital-resume-template-streamlit/blob/master/app.py

from pathlib import Path
import streamlit as st
from PIL import Image
from headerfooter import get_img_with_href,footer,JobSearch,Getlogo


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "assets" / "main.css"
resume_file = current_dir / "assets" / "gowtham-AI-resume.pdf" 
profile_pic = current_dir / "assets" / "Gowtham.PNG"
githublogo = current_dir / "assets" / "github.svg"
linkedinlogo = current_dir / "assets" / "linkedin2.svg"


# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Gowtham B C"
PAGE_ICON = ":wave:"
NAME = "Gowtham B C"
DESCRIPTION = """
Data science and Artificial Intelligence Team Lead, assisting enterprises in application of AI solutions.
"""
EMAIL = "bcgowtham17@gmail.com"


PROJECTS = {
    "🏆 ISO 42001:2023 certified AI/ML auditor from TUV SÜD": "https://www.linkedin.com/in/gowtham-buvalli-chikkathammaiah-788b62a9/overlay/1751030806395/single-media-viewer/?profileId=ACoAABchS9gBQL62xfkrVDNWGwMY-NT9qyUHXew",
    "🏆 Best Master thesis award 2021 from city Hof, Bavaria": "https://www.tvo.de/hochschule-hof-700-absolventinnen-und-absolventen-verabschiedet-581078/",
    "🏆 Many AI/ML research paper Publications": "https://www.ijsrp.org/research-paper-0619.php?rp=P908743",

}


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


github_html = get_img_with_href(githublogo, 'https://github.com/Gowtham171996')
linkedin_html = get_img_with_href(linkedinlogo, 'https://www.linkedin.com/in/gowtham-buvalli-chikkathammaiah-788b62a9/')


with st.container(border=True):
    # --- LOAD CSS, PDF & PROFIL PIC ---
    with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
    with open(resume_file, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    profile_pic = Image.open(profile_pic)


    # --- HERO SECTION ---
    col1, col2 = st.columns([0.4,0.6], gap="medium")
    with col1:
        #st.image(profile_pic, width=220)
        st.image(profile_pic)

    with col2:
        st.title(NAME)
        st.write(DESCRIPTION)
        
        
        #st.write(EMAIL)
    
        with st.container(border=False):
            cola, colb,colc = st.columns([55,20,25],vertical_alignment="center")
            with colc:
                st.markdown(linkedin_html, unsafe_allow_html=True)
            with cola:
                st.download_button(
                    label=" 📄 Download Resume",
                    data=PDFbyte,
                    file_name=resume_file.name,
                    mime="application/octet-stream",
                )
            with colb:
                st.markdown(github_html, unsafe_allow_html=True)
            st.write('\n')

# --- SOCIAL LINKS ---
st.write("---")
st.write('\n')

# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("Experience & Qualifications")
st.write(
    """
- ✔️ 🧑‍💻 6.5+ Years experience of Artificial Instelligence, Software Engineer and Consulting.
- ✔️ Strong hands on experience and knowledge in Full stack software development.
- ✔️ Good understanding of statistical principles and their respective applications
- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
"""
)


# --- SKILLS ---
st.write('\n')
st.write('\n')
st.write("---")
st.subheader("Hard Skills")
st.write(
    """
- ► Programming Languages: Python, Bash, MongoDB, SQL, C++
- ► Front End: HTML, Javascript, Node.js, ReactJS, ExpressJS Rest API’s, FastAPI
- ► Deployment: Docker, Kubernetes CI/CD pipelines: AWS, GCP, Azure DevOps, Jenkins, Terraform,
- ► AI Frameworks: Tensorflow, Pytorch, Keras, Huggingface, Numpy, Pandas, YOLO, OpenAI
- ► LLM’s: Transformers, LLaMa 3, BERT, GPT 3, GPT4, Mistral, Langchain
- ► Collaboration Tools: Scrum, Agile workflow, Firebase, MLOps, Version Control: Jira, Git, Github,
- ► Development: Parallel Threads, CUDA, Distributed Training, Design principles, Agile Development

"""
)


# --- WORK HISTORY ---
#st.write('\n')
st.write("---")
st.subheader("Work History")
#st.write("---")

# --- JOB 1
st.write("🚧", "**Senior Artificial Consultant | IISYS, Bavaria**")
st.write("10/2021 - Present")
st.write(
    """
- ► Generative AI: Collaborated with a German Management to develop a real-time mobile application that identifies eCommerce products and customer problems in text using Generative AI classification models for quality assurance. Web scraping of Product Images, EIN (European Identification Number), User sentiments, product review and text summarisation in dashboard.
- ► Industry 4.0: German automotive manufacturers use our deployed custom-built novel LSTM and GenAImodels, Transformers and analytics for preventive maintenance of tool wearing using MLOps.
"""
)

# --- JOB 2
st.write('\n')
st.write("🚧", "**Computer Vision and Machine Learning engineer | Livello, Dusseldorf & IISYS - Hof, Germany**")
st.write("08/2020 - 09/2021")
st.write(
    """
- ►  Object Detection: For smart fridges: Creation of Data, Training model with TensorFlow, Deployment on Azure framework, Admin Dashboard using MERNstack, communication and coordinate demo for clients such as Aldi. 
"""
)

# --- JOB 3
st.write('\n')
st.write("🚧", "**Senior software engineer | CGI & Mindtree, Bangalore, India**")
st.write("06/2017 - 02/2020")
st.write(
    """
- ► Developed web applications dashboard for simplified User Interface and User Experience (UI and UX), site monitoring tool solutions using Sharepoint Elastic search and custom crawlers scripts which index 10000+ sites on half weekly basis and collect gigabytes of text information to our database.
- ► Worked on dashboard as Full stack developer including Azure cloud infrastructure setup, cloud monitoring and custom sharepoint .Net scripts development.Devised KPIs using SQL across company website in collaboration with cross-functional teams to achieve a 120% jump in organic traﬃc
"""
)

# --- SKILLS ---
st.write('\n')
st.write('\n')
st.write("---")
st.subheader("Languages")
st.write(
    """
- ► 🇩🇪 German: B2
- ► 🇺🇸 English: C1
"""
)


# --- Certificates & Accomplishments ---
st.write('\n')
st.write("---")
st.subheader("Certificates & Accomplishments")

for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")


st.markdown(footer,unsafe_allow_html=True)
JobSearch()
#Getlogo()

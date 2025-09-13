import streamlit as st
import requests
import json

# Set Streamlit page configuration for a wider layout and centered content
st.set_page_config(
    page_title="Gemma 3n Demo Lab",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend API endpoint URL from the React app
API_URL = 'http://localhost:8000/generate'

# --- State Management Initialization ---
# Initialize session state variables if they don't exist
if 'loading' not in st.session_state:
    st.session_state.loading = False
if 'error' not in st.session_state:
    st.session_state.error = None
if 'qa_output' not in st.session_state:
    st.session_state.qa_output = ''
if 'summary_output' not in st.session_state:
    st.session_state.summary_output = ''
if 'essay_output' not in st.session_state:
    st.session_state.essay_output = ''
if 'rag_output' not in st.session_state:
    st.session_state.rag_output = ''
if 'ds_output' not in st.session_state:
    st.session_state.ds_output = ''

# --- UI Components ---
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 9999px;
            padding: 0.5rem 1rem;
        }
        .stTabs [aria-selected="true"] {
            background-color: #3b82f6;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Gemma 3n Demo Lab")
st.write("A playground to test the power of the latest large language models.")
st.markdown("---")

# --- API Call Function ---
def handle_api_call(prompt, task_type, output_key):
    """Handles the API call to the backend and updates session state."""
    st.session_state.loading = True
    st.session_state.error = None
    st.session_state[output_key] = ''
    st.session_state.qa_input_disabled = True

    try:
        response = requests.post(
            API_URL,
            json={'prompt': prompt, 'task_type': task_type},
            timeout=120  # Set a timeout for the request
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        result = response.json()
        text = result.get('response', 'No response from model.')
        st.session_state[output_key] = text
        
    except requests.exceptions.RequestException as e:
        st.session_state.error = f"An error occurred: {e}. Please ensure your backend is running."
    finally:
        st.session_state.loading = False
        st.session_state.qa_input_disabled = False

# --- Tab-based UI for different tasks ---
tabs = st.tabs(["💬 Q&A", "📝 Summary", "🖋️ Essay", "🗂️ RAG", "📊 DS Explainer"])

# --- Q&A Tab ---
with tabs[0]:
    st.header("Question and Answering")
    qa_input = st.text_input("Ask a question...", key="qa_input", disabled=st.session_state.loading)
    
    if st.button("Ask", disabled=st.session_state.loading, use_container_width=True):
        if not qa_input.strip():
            st.session_state.error = "Please enter a question."
        else:
            handle_api_call(qa_input, 'qa', 'qa_output')

    st.markdown("### Answer")
    if st.session_state.loading:
        st.info("Loading...")
    else:
        st.markdown(
            st.session_state.qa_output or "Your answer will appear here.",
            unsafe_allow_html=True
        )

# --- Summary Tab ---
with tabs[1]:
    st.header("Summary")
    summary_text = st.text_area("Paste text to summarize...", height=200, key="summary_input", disabled=st.session_state.loading)
    
    if st.button("Summarize", disabled=st.session_state.loading, use_container_width=True):
        if not summary_text.strip():
            st.session_state.error = "Please paste text to summarize."
        else:
            handle_api_call(summary_text, 'summary', 'summary_output')

    st.markdown("### Summary")
    if st.session_state.loading:
        st.info("Loading...")
    else:
        st.markdown(
            st.session_state.summary_output or "Your summary will appear here.",
            unsafe_allow_html=True
        )

# --- Essay Tab ---
with tabs[2]:
    st.header("Write an Essay")
    essay_topic = st.text_input("Essay topic...", key="essay_topic_input", disabled=st.session_state.loading)
    essay_words = st.number_input("Approximate word count...", min_value=1, key="essay_words_input", disabled=st.session_state.loading)
    
    if st.button("Generate Essay", disabled=st.session_state.loading, use_container_width=True):
        if not essay_topic.strip() or not essay_words:
            st.session_state.error = "Please enter a topic and word count."
        else:
            prompt = f"Topic: '{essay_topic}', Word count: {essay_words}"
            handle_api_call(prompt, 'essay', 'essay_output')

    st.markdown("### Essay")
    if st.session_state.loading:
        st.info("Loading...")
    else:
        st.markdown(
            st.session_state.essay_output or "Your essay will appear here.",
            unsafe_allow_html=True
        )

# --- RAG Tab ---
with tabs[3]:
    st.header("RAG (PDF Content)")
    st.write("Since we can't upload files directly, paste the text from your PDF below.")
    pdf_text = st.text_area("Paste PDF text here...", height=200, key="pdf_input", disabled=st.session_state.loading)
    rag_question = st.text_input("Ask a question about the text...", key="rag_question_input", disabled=st.session_state.loading)
    
    if st.button("Get Answer from Text", disabled=st.session_state.loading, use_container_width=True):
        if not pdf_text.strip() or not rag_question.strip():
            st.session_state.error = "Please provide text from the PDF and a question."
        else:
            prompt = f"Document Text:\n{pdf_text}\n\nQuestion: '{rag_question}'"
            handle_api_call(prompt, 'rag', 'rag_output')

    st.markdown("### Answer")
    if st.session_state.loading:
        st.info("Loading...")
    else:
        st.markdown(
            st.session_state.rag_output or "Your answer based on the text will appear here.",
            unsafe_allow_html=True
        )

# --- Data Science Explainer Tab ---
with tabs[4]:
    st.header("Data Science Explainer")
    ds_concept = st.text_input("Enter a data science concept...", key="ds_concept_input", disabled=st.session_state.loading)
    
    if st.button("Explain", disabled=st.session_state.loading, use_container_width=True):
        if not ds_concept.strip():
            st.session_state.error = "Please enter a data science concept to explain."
        else:
            handle_api_call(ds_concept, 'ds-explainer', 'ds_output')

    st.markdown("### Explanation")
    if st.session_state.loading:
        st.info("Loading...")
    else:
        st.markdown(
            st.session_state.ds_output or "The explanation will appear here.",
            unsafe_allow_html=True
        )

# --- Global Error Display ---
if st.session_state.error:
    st.error(st.session_state.error)

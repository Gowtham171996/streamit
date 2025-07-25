import streamlit as st
import os # Import os for path handling
import sqlite3
from sqlalchemy import create_engine, text, inspect
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
import torch
import traceback
import json
from datetime import datetime, timezone
import random
import pandas as pd 

from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.prompts import PromptTemplate
from headerfooter import footer,Disclaimer,JobSearch,Getlogo,current_dir

# --- Database Setup ---
DATABASE_FILE_NAME = "ecotraders.db"
# Use an absolute path relative to the current script's directory
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_FILE_NAME)

def setup_file_database(force_recreate=False):
    """
    Sets up a file-based SQLite database and populates it if it doesn't exist,
    or if force_recreate is True.
    Returns the SQLAlchemy engine connected to this database.
    """
    db_exists = os.path.exists(DATABASE_PATH) # Check existence using absolute path

    if force_recreate and db_exists:
        os.remove(DATABASE_PATH) # Delete using absolute path
        db_exists = False
        st.warning(f"Existing database '{DATABASE_FILE_NAME}' deleted. Recreating...")

    if not db_exists:
        st.info(f"Creating and populating new database: {DATABASE_FILE_NAME} at {DATABASE_PATH} with 100 sample entries per table.")
        # Use sqlite3 directly for initial creation and population with absolute path
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY,
                name TEXT,
                owner TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                operation_id INTEGER PRIMARY KEY,
                company_id INTEGER,
                name TEXT,
                description TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(company_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farms (
                farm_id INTEGER PRIMARY KEY,
                operation_id INTEGER,
                location TEXT,
                crop TEXT,
                area_sq_m REAL,
                FOREIGN KEY (operation_id) REFERENCES operations (operation_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                car_id INTEGER PRIMARY KEY,
                operation_id INTEGER,
                model TEXT,
                lease_status TEXT,
                daily_rate REAL,
                FOREIGN KEY (operation_id) REFERENCES operations(operation_id)
            )
        """)

        # --- Insert 100 Sample Data Entries ---
        company_names = ["Global Corp", "Tech Solutions", "Innovate Inc.", "Future Systems", "Alpha Omega"]
        owner_names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Williams"]
        operation_types = ["Sales", "Marketing", "HR", "R&D", "Logistics", "Finance", "Production"]
        farm_locations = ["Mysore", "Bangalore", "Chennai", "Delhi", "Mumbai"]
        crops = ["Coffee", "Pepper", "Rice", "Wheat", "Corn", "Sugarcane"]
        car_models = ["Tesla Model 3", "Mercedes-Benz C-Class", "BMW 3 Series", "Audi A4", "Toyota Camry", "Honda Civic"]
        lease_statuses = ["Available", "Leased", "Maintenance"]

        # Companies
        for i in range(1, 101):
            cursor.execute("INSERT INTO companies (company_id, name, owner) VALUES (?, ?, ?)",
                           (i, f"{random.choice(company_names)} {i}", random.choice(owner_names)))

        # Operations (link to existing companies)
        for i in range(101, 201):
            company_id = random.randint(1, 100)
            cursor.execute("INSERT INTO operations (operation_id, company_id, name, description) VALUES (?, ?, ?, ?)",
                           (i, company_id, f"{random.choice(operation_types)} Op {i}", f"Description for {random.choice(operation_types)} Operation {i}"))

        # Farms (link to existing operations)
        for i in range(1, 101):
            operation_id = random.randint(101, 200)
            cursor.execute("INSERT INTO farms (farm_id, operation_id, location, crop, area_sq_m) VALUES (?, ?, ?, ?, ?)",
                           (i, operation_id, random.choice(farm_locations), random.choice(crops), round(random.uniform(10000, 100000), 2)))

        # Cars (link to existing operations)
        for i in range(1, 101):
            operation_id = random.randint(101, 200)
            cursor.execute("INSERT INTO cars (car_id, operation_id, model, lease_status, daily_rate) VALUES (?, ?, ?, ?, ?)",
                           (i, operation_id, random.choice(car_models), random.choice(lease_statuses), round(random.uniform(50, 200), 2)))

        conn.commit()
        conn.close()
        st.success(f"Database '{DATABASE_FILE_NAME}' created and populated with 100 sample entries per table!")

        # VERIFICATION STEP: Read data back to confirm
        temp_conn = sqlite3.connect(DATABASE_PATH) # Use absolute path for verification
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("SELECT COUNT(*) FROM companies")
        st.info(f"Verification: Companies count: {temp_cursor.fetchone()[0]}")
        temp_cursor.execute("SELECT COUNT(*) FROM operations")
        st.info(f"Verification: Operations count: {temp_cursor.fetchone()[0]}")
        temp_cursor.execute("SELECT COUNT(*) FROM farms")
        st.info(f"Verification: Farms count: {temp_cursor.fetchone()[0]}")
        temp_cursor.execute("SELECT COUNT(*) FROM cars")
        st.info(f"Verification: Cars count: {temp_cursor.fetchone()[0]}")
        temp_conn.close()

    else:
        st.info(f"Using existing database: {DATABASE_FILE_NAME} at {DATABASE_PATH}")

    # Now, create and return the SQLAlchemy Engine connected to the file using absolute path
    engine = create_engine(f"sqlite:///{DATABASE_PATH}")
    return engine

# --- LLM and QA Setup ---
device = 0 if torch.cuda.is_available() else -1

gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)

# --- Helper function to format response as JSON ---
def format_response_as_json(original_question: str, answer_content: str, source_type: str):
    """
    Formats the given answer content into a JSON structure.
    """
    json_data = {
        "question": original_question,
        "answer": answer_content,
        "source": source_type,
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
    }
    return json_data

# --- Main Answer Function with RAG Logic ---
def answer_question(question: str, sql_agent_executor=None):
    """
    Determines the best way to answer a question: from DB, or general knowledge.
    """
    final_answer_content = "I could not find an answer."
    source_used = "None"

    db_keywords = ["how many", "list all", "total", "what is the", "show me", "companies", "operations", "farms", "cars", "owner", "crop", "model", "ecofinance", "aurum trade", "eco finance", "eco cars", "eco agri", "mysore", "coffee", "pepper", "tesla", "mercedes", "count", "average", "sum"]
    is_db_question = any(keyword in question.lower() for keyword in db_keywords)

    # 1. Try to answer from Database if SQL agent is available and question seems database-related
    if sql_agent_executor and is_db_question:
        try:
            st.session_state.messages.append({"role": "assistant", "content": "Attempting to query the database..."})
            db_response = sql_agent_executor.invoke({"input": question})
            
            if db_response and db_response.get("output"):
                raw_output = db_response['output']
                if "Final Answer:" in raw_output:
                    final_answer_content = raw_output.split("Final Answer:", 1)[1].strip()
                else:
                    final_answer_content = raw_output.strip()
                
                source_used = "Database"
                st.session_state.messages.append({"role": "assistant", "content": f"**From Database:** {final_answer_content}"})
                return format_response_as_json(question, final_answer_content, source_used)
        except Exception as e:
            st.error(f"Error querying database: {e}. See terminal for full traceback.")
            traceback.print_exc()
            st.session_state.messages.append({"role": "assistant", "content": f"Could not answer from database due to an internal error. Please check the terminal for details. Trying general knowledge."})

    # 2. Fallback to General Knowledge LLM
    try:
        st.session_state.messages.append({"role": "assistant", "content": "Answering using general knowledge..."})
        general_answer = gemini_llm.invoke(question).content
        final_answer_content = general_answer
        source_used = "General Knowledge"
        st.session_state.messages.append({"role": "assistant", "content": f"**General Answer:** {final_answer_content}"})
        return format_response_as_json(question, final_answer_content, source_used)
    except Exception as e:
        st.error(f"Failed to get a general answer: {e}")
        st.session_state.messages.append({"role": "assistant", "content": f"I apologize, I could not find an answer to your question. Error: {e}"})
        return format_response_as_json(question, "I apologize, I could not find an answer to your question.", "Failed")

def SQLAgentInitate():
    st.session_state.sql_agent_executor = initialize_agent(
        tools=tools,
        llm=gemini_llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "prefix": SQL_AGENT_PROMPT_PREFIX.format(
                tools="\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
                tool_names=", ".join([tool.name for tool in tools]),
                table_info=st.session_state.langchain_db.get_table_info()
            ),
            "suffix": SQL_AGENT_PROMPT_SUFFIX
        }
    )
    st.success("Database connected and SQL agent initialized!")


# --- Streamlit UI Layout ---
st.set_page_config(page_title="Intelligent Query Buddy", layout='centered', initial_sidebar_state="auto")

col1, col2 = st.columns([65, 35], gap="small", vertical_alignment="bottom")
with st.container(border=True):
    with col1:
        st.header("Intelligent Query Buddy")
    with col2:
        if st.button("Home", use_container_width=True):
            st.switch_page("Home.py")

st.write("---")

# Initialize session state variables for database and agent
if "messages" not in st.session_state:
    st.session_state.messages = []
if "langchain_db" not in st.session_state:
    st.session_state.langchain_db = None
if "sql_agent_executor" not in st.session_state:
    st.session_state.sql_agent_executor = None

# Database Initialization (run once per session, or forced reset)
if st.button("Reset Database (Deletes ecotraders.db)", type="secondary"):
    if os.path.exists(DATABASE_PATH): # Use absolute path here
        os.remove(DATABASE_PATH)
        st.session_state.langchain_db = None
        st.session_state.sql_agent_executor = None
        st.rerun()

if st.session_state.langchain_db is None:
    st.session_state.db_engine = setup_file_database()
    st.session_state.langchain_db = SQLDatabase(st.session_state.db_engine)
    st.session_state.sql_toolkit = SQLDatabaseToolkit(db=st.session_state.langchain_db, llm=gemini_llm)
    
    tools = st.session_state.sql_toolkit.get_tools()

    # --- REFINED PROMPT STRUCTURE ---
    SQL_AGENT_PROMPT_PREFIX = """You are an AI assistant that can answer questions about the database.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Database Schema:
{table_info}

"""
    SQL_AGENT_PROMPT_SUFFIX = """Question: {input}
Thought:{agent_scratchpad}"""


    SQLAgentInitate()

    # --- Display Database Schema and Sample Data ---
    st.markdown("### Database Schema and Sample Data")
    
    # Display Schema
    #st.markdown(f"**Schema:**")
    #st.code(st.session_state.langchain_db.get_table_info(), language='sql')

    # Display Top 10 rows for each table
    st.markdown(f"**Top 5 Rows from Each Table:**")
    db_tables = ["companies", "operations", "farms", "cars"]
    for table_name in db_tables:
        try:
            # Use SQLAlchemy engine to fetch data
            with st.session_state.db_engine.connect() as connection:
                query = f"SELECT * FROM {table_name} LIMIT 5"
                result = connection.execute(text(query)).fetchall()
                
                # Get column names using inspector
                inspector = inspect(st.session_state.db_engine)
                column_names = [col["name"] for col in inspector.get_columns(table_name)]

                st.markdown(f"**Table: `{table_name}`**")
                if result:
                    # Convert to pandas DataFrame for st.dataframe
                    df = pd.DataFrame(result, columns=column_names) # NEW: Use pd.DataFrame
                    st.dataframe(df, hide_index=True) # Pass DataFrame directly
                else:
                    st.info(f"No data found in `{table_name}`.")
        except Exception as e:
            st.error(f"Error fetching data for table `{table_name}`: {e}")
            traceback.print_exc()


with st.container(border=True):
    st.markdown("---")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if question := st.chat_input(placeholder="Ask a question about the database or general knowledge..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            answer_placeholder = st.empty()
            full_answer_json = answer_question(
                question=question,
                sql_agent_executor=st.session_state.sql_agent_executor
            )
            answer_placeholder.json(full_answer_json)
            
            st.session_state.messages.append({"role": "assistant", "content": f"```json\n{json.dumps(full_answer_json, indent=2)}\n```"})

Disclaimer()
st.markdown(footer,unsafe_allow_html=True)
JobSearch()
#Getlogo()
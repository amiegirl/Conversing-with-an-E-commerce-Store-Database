import streamlit as st
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.prompts import PromptTemplate

# Read the API key
#f = open("keys/gemini_api_key.txt")
#key = f.read()

#  Setup chat model
chat_model = ChatGoogleGenerativeAI(google_api_key=key, model="gemini-1.5-pro-latest")

# connect to our database
db = SQLDatabase.from_uri("sqlite:///laptops.db")


# set up chat template
# set up chat template
prompt = PromptTemplate.from_template(
    """You are a helpful AI assistant expert in querying SQL Database,
        The Database has the name laptops
        and has the following columns - brand, description, model, price, RAM(GB), storage,
        capacity(GB), processor, warranty(years) and display(inch). The price is in Naira.
        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        if a question does not seem related to the database, the response should be,
        "I may not be able to provide information about this topic"
        Given the following user question, generate corresponding SQL query, and SQL result, 
        and answer the user question. 
        Question: {question}
        Answer: 
        """
)

# set up sql chain
sql_toolkit = SQLDatabaseToolkit(db=db, llm=chat_model)
sql_toolkit.get_tools()

sqldb_agent = create_sql_agent(
    llm=chat_model,
    toolkit=sql_toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Streamlit UI
with st.sidebar:
    st.title(":blue[This Chatbot is designed to enable users interact with businesses by querying e-commerce database using simple everyday language.]")
    st.markdown('''
    ## About
    Our database contain information about laptop brand, model, description, price, RAM(GB), storage,
        capacity(GB), processor, warranty(years) and display(inch) 
    ''')
    st.write('Made by Aminat Owodunni')
st.title(":blue[Conversing with an E-commerce Laptop Store Database]")
question = st.text_area("Enter your query:", placeholder="Enter your query here...", height=100)

if st.button("Submit Your Query"):
    if question:
        response = sqldb_agent.run(prompt.format(
        question=question
        ))
        st.write(response)
    else:
        st.warning("Please enter a question.")
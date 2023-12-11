
import os
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = "ADD YOUR KEY HERE"


# Connection details for the first database
dbname = 'new_database_name'
user = 'new_username'
password = 'new_password'
host = 'localhost'
port = '5432'
connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Initialize database
db = SQLDatabase.from_uri(connection_string)

# Initialize LangChain
llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

def query_and_synthesize(query):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

    try:
        # Get results from the database
        result = agent_executor.run(query)

        return result
    except Exception as e:
        return f"Error: {e}"

while True:
    user_query = input("Enter your query (or type 'exit' to quit): ")
    if user_query.lower() == 'exit':
        print('Exiting...')
        break
    result = query_and_synthesize(user_query)
    print("Result:", result)
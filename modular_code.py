import streamlit as st
import os
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)


class DatabaseConnector:
    def __init__(self, db_uri: str):
        self.db = SQLDatabase.from_uri(db_uri)
    
    def get_db(self):
        return self.db

class LLMConnector:
    def __init__(self, model_name: str, api_key: str, verbose: bool = False):
        self.llm = ChatGroq(model=model_name, api_key=api_key, verbose=verbose)
    
    def get_llm(self):
        return self.llm

class SQLAgentFramework:
    def __init__(self, db_connector: DatabaseConnector, llm_connector: LLMConnector):
        self.db = db_connector.get_db()
        self.llm = llm_connector.get_llm()
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
        assert len(self.prompt_template.messages) == 1
        self.system_message = self.prompt_template.format(dialect="SQLite", top_k=5)
        self.agent_executor = create_react_agent(self.llm, self.toolkit.get_tools(), state_modifier=self.system_message)

    def execute_query(self, user_input: str):
        result_final = []
        events = self.agent_executor.stream({"messages": [("user", user_input)]}, stream_mode="values")
        for event in events:
            result = event["messages"][-1].content
            result_final.append(result)
        return result_final[-1] if result_final else "No response generated."

class StreamlitInterface:
    def __init__(self, title: str, header: str):
        st.set_page_config(page_title=title)
        st.header(header)

    def run(self, agent_framework: SQLAgentFramework):
        user_input = st.text_input("Enter your question:")
        submit = st.button("Ask the question")
        if submit:
            if user_input:
                st.subheader("The Response is")
                response = agent_framework.execute_query(user_input)
                st.write(response)
            else:
                st.write("Enter your question before click on submit")


def main():
    # Set up environment variables if needed
    db_uri = "sqlite:///travel.sqlite"
    model_name = "llama-3.1-70b-versatile"
    api_key = os.getenv("GROQ_API_KEY", "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")

    # Initialize connectors
    db_connector = DatabaseConnector(db_uri=db_uri)
    llm_connector = LLMConnector(model_name=model_name, api_key=api_key, verbose=False)

    # Initialize agent framework
    agent_framework = SQLAgentFramework(db_connector=db_connector, llm_connector=llm_connector)

    # Start Streamlit interface
    interface = StreamlitInterface(title="Q&A Demo", header="NSQLG")
    interface.run(agent_framework)

if __name__ == "__main__":
    main()


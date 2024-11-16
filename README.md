#                                            _intelligent-db-query-agent-
An AI-driven SQL query assistant that helps interact with databases and generate real-time query results.

# database:https://www.kaggle.com/datasets/saadharoon27/airlines-dataset

# Tools and Libraries Used
**Streamlit**: Provides an interactive web interface for users to input questions and receive answers.

**LangChain**: Facilitates agent-based applications by integrating SQL databases and large language models (LLMs).

**ChatGroq**: An LLM used to process and generate responses to user queries.

**SQLDatabaseToolkit**: Helps the LLM interact with SQL databases, enabling dynamic query generation and execution.

**SQL Agent**: The central agent that pulls everything together – it connects the LLM and database tools to handle user queries effectively.

# Main Classes
**DatabaseConnector**: Manages the connection to the SQL database (e.g., SQLite).

**LLMConnector**: Connects to the ChatGroq LLM using an API key for query processing.

**SQLAgentFramework**: Combines database and LLM connectors to create a SQL agent capable of handling and processing queries.

**StreamlitInterface**: Manages the user-facing web interface where questions are entered and responses displayed.

# Workflow of the Agent
**User Input**: The user enters a question or SQL query through the Streamlit interface.

**SQLAgent Framework**: The framework sends the input to the LLM (ChatGroq) for processing.

# Key Tools in SQLDatabseToolKit: 
Converts natural language inputs into SQL queries and executes them on the database.

**InfoSQLDatabaseTool**: Retrieves database metadata.

**ListSQLDatabaseTool**: Lists tables or data in the database.

**QuerySQLCheckerTool**: Validates SQL query syntax.

**QuerySQLDataBaseTool**: Executes SQL queries and retrieves results.

# How SQL Queries are Validated
The QuerySQLCheckerTool checks if the generated SQL query is valid and free from errors before running it.

# Query Execution and Display
Once validated, QuerySQLDataBaseTool executes the query.
Results are returned by the LLM and displayed on the Streamlit interface.

# Prompt System
A pre-defined prompt template from LangChain's hub, customized with SQL dialect and parameters (like top K results), guides the LLM in accurately generating SQL queries.

# Step-by-Step Process
1. The user inputs a question on the Streamlit interface.
2. The question is processed by the SQLAgentFramework.
3. The LLM (via ChatGroq) generates an SQL query.
4. QuerySQLCheckerTool in SQLDatabaseToolkit validates the query.
5. QuerySQLDataBaseTool executes the validated query on the database.
6. The agent formats the results and sends them back to the Streamlit interface.
7. The results are displayed to the user.

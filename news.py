import os
import logging
import streamlit as st
from langchain_community.tools.polygon import PolygonAPIWrapper
from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain_core.pydantic_v1 import BaseModel
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API keys securely
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
CHATGROQ_API_KEY = os.getenv('CHATGROQ_API_KEY')
ASTRA_DB_CLIENT_ID = os.getenv('ASTRA_DB_CLIENT_ID')
ASTRA_DB_CLIENT_SECRET = os.getenv('ASTRA_DB_CLIENT_SECRET')
ASTRA_DB_KEYSPACE = os.getenv('ASTRA_DB_KEYSPACE')

if not POLYGON_API_KEY:
    logger.error("Polygon API key not found. Please set the POLYGON_API_KEY environment variable.")
if not CHATGROQ_API_KEY:
    logger.error("ChatGroq API key not found. Please set the CHATGROQ_API_KEY environment variable.")
if not ASTRA_DB_CLIENT_ID or not ASTRA_DB_CLIENT_SECRET:
    logger.error("Astra DB credentials not found. Please set the ASTRA_DB_CLIENT_ID and ASTRA_DB_CLIENT_SECRET environment variables.")

# Initialize APIs
polygon_wrapper = PolygonAPIWrapper(api_key=POLYGON_API_KEY)
chat_client = ChatGroq(api_key=CHATGROQ_API_KEY)

# Initialize Astra DB connection
auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
cluster = Cluster(cloud={'secure_connect_bundle': os.getenv('ASTRA_DB_SECURE_CONNECT_BUNDLE')}, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace(ASTRA_DB_KEYSPACE)

# Define a data model for queries
class QueryData(BaseModel):
    question: str

# Node functions
def retrieve_stock_data(question: str, ticker: str):
    """Retrieve stock performance or news based on the question."""
    try:
        if "performance" in question.lower():
            stock_data = polygon_wrapper.get_previous_close(ticker)
            if stock_data:
                return f"Performance for {ticker}: Close price ${stock_data['close']}, High ${stock_data['high']}, Low ${stock_data['low']}"
            else:
                return "No performance data available for the given ticker."
        elif "news" in question.lower():
            news_articles = polygon_wrapper.get_news(ticker)
            if news_articles:
                news_summary = "\n".join(
                    [f"- [{article['title']}]({article['url']}) on {article['published_utc']}" for article in news_articles]
                )
                return f"News for {ticker}: {news_summary}"
            else:
                return "No news articles found for the given ticker."
        else:
            return "Please ask about stock performance or news."
    except Exception as e:
        logger.error(f"Error retrieving stock data: {e}")
        return f"An error occurred: {e}"

def retrieve_from_astra(query: str):
    """Retrieve documents related to the query from AstraDB."""
    try:
        rows = session.execute("SELECT url FROM documents WHERE topic=%s", (query,))
        urls = [row.url for row in rows]
        if urls:
            return f"Retrieved URLs related to '{query}':\n" + "\n".join(urls)
        else:
            return f"No documents found in AstraDB for the topic '{query}'."
    except Exception as e:
        logger.error(f"Error retrieving data from AstraDB: {e}")
        return f"An error occurred while retrieving documents: {e}"

def generate_summary(question: str):
    """Generate insights using Llama model."""
    try:
        response = chat_client.chat(question, model="llama-3.1-70b-versatile")
        return response['text'].strip()
    except Exception as e:
        logger.error(f"Error generating summary with Llama model: {e}")
        return f"An error occurred: {e}"

# Workflow setup
def route_question(question: str):
    """Route the question to the appropriate node."""
    if "news" in question.lower() or "performance" in question.lower():
        return "retrieve_stock_data"
    elif "inflation" in question.lower() or "interest rate" in question.lower():
        return "retrieve_from_astra"
    else:
        return "generate_summary"

# Main agent function
def agent(question: str, ticker: str = None):
    """Multi-agent RAG system orchestrator."""
    logger.info(f"Routing question: {question}")
    route = route_question(question)

    if route == "retrieve_stock_data" and ticker:
        return retrieve_stock_data(question, ticker)
    elif route == "retrieve_from_astra":
        return retrieve_from_astra(question)
    elif route == "generate_summary":
        return generate_summary(question)
    else:
        return "Invalid question or missing ticker for stock data retrieval."

# Streamlit UI
def main():
    st.title("Multi-Agent System: Stock Data, Insights & Summaries")

    # Input for question
    question = st.text_input("Enter your question:")

    # Input for ticker (if applicable)
    ticker = None
    if "stock" in question.lower():
        ticker = st.text_input("Enter stock ticker (if applicable):")
    
    # Submit button
    if st.button("Submit"):
        if question:
            response = agent(question, ticker)
            st.write("Response:")
            st.write(response)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()

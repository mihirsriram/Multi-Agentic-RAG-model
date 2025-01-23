# Multi-Agent RAG System

This repository contains a multi-agent Retrieval-Augmented Generation (RAG) system designed to process and respond to user queries. The system integrates:

- **Polygon API**: To retrieve stock market performance and news.
- **ChatGroq (Llama model)**: For generating summaries and insights based on user queries.
- **AstraDB**: To store and retrieve documents (e.g., URLs, PDFs) related to specific topics such as inflation and interest rates.

---

## Features

### 1. Stock Market Data Retrieval
- Fetch stock performance data (close price, high, low) for a given ticker.
- Retrieve and summarize recent news articles for a specific stock.

### 2. Document Retrieval from AstraDB
- Query AstraDB to fetch URLs or documents related to topics such as inflation or interest rates.

### 3. Insight Generation with Llama Model
- Generate detailed summaries or responses using the Llama model by ChatGroq.

### 4. Multi-Agent Orchestration
- Route user queries to the appropriate module based on context (stock data, document retrieval, or insight generation).

---

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- AstraDB account and secure connect bundle
- API keys for Polygon and ChatGroq

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/multi-agent-rag-system.git
   cd multi-agent-rag-system
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `POLYGON_API_KEY`: Your Polygon API key.
   - `CHATGROQ_API_KEY`: Your ChatGroq API key.
   - `ASTRA_DB_CLIENT_ID`: Client ID for AstraDB.
   - `ASTRA_DB_CLIENT_SECRET`: Client secret for AstraDB.
   - `ASTRA_DB_SECURE_CONNECT_BUNDLE`: Path to the secure connect bundle.
   - `ASTRA_DB_KEYSPACE`: Your AstraDB keyspace.

   Example:
   ```bash
   export POLYGON_API_KEY="your_polygon_api_key"
   export CHATGROQ_API_KEY="your_chatgroq_api_key"
   export ASTRA_DB_CLIENT_ID="your_astra_db_client_id"
   export ASTRA_DB_CLIENT_SECRET="your_astra_db_client_secret"
   export ASTRA_DB_SECURE_CONNECT_BUNDLE="path_to_secure_connect_bundle.zip"
   export ASTRA_DB_KEYSPACE="your_keyspace"
   ```

---

## Usage

### Running the System
Execute the following command:
```bash
python main.py
```
You will be prompted to enter:
1. A question (e.g., "What is the latest performance for AAPL?" or "What documents are available on inflation?").
2. A stock ticker (if applicable).

### Example Queries
#### Stock Performance Query:
```
Enter your question: What is the latest performance for AAPL?
Enter stock ticker (if applicable): AAPL
```
#### Inflation Documents Query:
```
Enter your question: What documents are available on inflation?
Enter stock ticker (if applicable):
```

---

## Code Structure

- **`main.py`**: The main script orchestrating the multi-agent system.
- **`news.py`**: Contains the implementation of stock data retrieval, document fetching from AstraDB, and insight generation using Llama.
- **`requirements.txt`**: Specifies required Python packages.

---

## Technologies Used
- **Python**: Core programming language.
- **Streamlit**: (Optional) For creating a UI if desired.
- **LangChain**: For integrating AI-driven workflows.
- **AstraDB**: For document storage and retrieval.
- **Polygon API**: For stock market data.
- **ChatGroq**: For advanced Llama-based summarization.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request with a clear description of your changes.



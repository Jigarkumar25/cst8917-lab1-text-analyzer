# CST8917 – Azure Functions Text Analyzer (Lab 01)

## Overview
This project implements a **serverless Text Analyzer application** using **Azure Functions (Python)** and **Azure Cosmos DB (NoSQL)**.

The application analyzes input text, stores the analysis results in a database, and allows retrieval of previously analyzed text records. The solution is developed locally and deployed to **Azure Functions** in the **West US 2** region.

---

## Application Features

### 1. TextAnalyzer API
The TextAnalyzer function accepts text input and performs the following analysis:

- Word count  
- Character count (with and without spaces)  
- Sentence count  
- Paragraph count  
- Average word length  
- Longest word  
- Estimated reading time  
- Metadata (timestamp and text preview)  

Each request generates a unique identifier, and the analysis result is **stored in Azure Cosmos DB**.

**Supported input methods:**
- Query string  
- JSON request body  

---

### 2. GetAnalysisHistory API
The GetAnalysisHistory function retrieves previously analyzed text records from Azure Cosmos DB.

**Features:**
- Returns recent analysis results  
- Supports a `limit` query parameter  
- Results are ordered by analysis timestamp  

---

## API Endpoints

### TextAnalyzer
- GET /api/TextAnalyzer
- POST /api/TextAnalyzer


**Example:**
- /api/TextAnalyzer?text=hello world hello

---

### GetAnalysisHistory
- GET /api/GetAnalysisHistory

**Example:**
- /api/GetAnalysisHistory?limit=5

---

## Technology Stack
- Azure Functions (Python)
- Azure Cosmos DB (NoSQL, Serverless)
- Python 3.11 / 3.12
- Azure Functions Core Tools
- Azure Cosmos DB Python SDK

---

## Running the Application Locally

### Prerequisites
- Python 3.11 or 3.12
- Azure Functions Core Tools
- Azure Cosmos DB account

---

### Local Setup Steps

1. Create and activate a Python virtual environment:
- python -m venv .venv
- source .venv/bin/activate

2. Install dependencies:
- pip install -r requirements.txt

3. Configure environment variables in `local.settings.json`:
- COSMOS_ENDPOINT
- COSMOS_KEY
- COSMOS_DATABASE
- COSMOS_CONTAINER

4. Start the Azure Functions host:
- func start

5. Test the APIs locally:
- http://localhost:7071/api/TextAnalyzer?text=hello
- http://localhost:7071/api/GetAnalysisHistory?limit=5

---

## Azure Deployment

- Platform: Azure Functions
- Region: West US 2
- Hosting Plan: Consumption
- Database: Azure Cosmos DB (NoSQL, Serverless)

All required environment variables (`COSMOS_*`) are configured in the Azure Function App settings.

---

## Database Usage

Azure Cosmos DB (NoSQL) is used to store text analysis results.  
Each record is stored as a JSON document containing:

- Unique identifier  
- Analysis data  
- Metadata  
- Original input text  

The database selection and justification are explained in a separate document.

---

## Demo Video
A short demonstration video (under 5 minutes) shows:

- Local execution of the application  
- Azure-hosted execution  
- Data persistence in Cosmos DB  

The video link is provided in **DEMO.md**.

---

## Database Selection
The database choice and justification are documented in:

- `DATABASE_CHOICE.md`

---


---

## Notes
- Sensitive configuration files are excluded from version control  
- All secrets are stored using environment variables  
- Cosmos DB is configured in serverless mode to minimize cost  

---

## Author
**Jigar**  


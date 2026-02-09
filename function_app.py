import azure.functions as func
import logging
import json
import re
import os
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def get_cosmos_container():
    endpoint = os.environ.get("COSMOS_ENDPOINT")
    key = os.environ.get("COSMOS_KEY")
    db_name = os.environ.get("COSMOS_DATABASE")
    container_name = os.environ.get("COSMOS_CONTAINER")

    if not endpoint or not key or not db_name or not container_name:
        raise ValueError("Cosmos settings missing. Check local.settings.json / Azure env vars.")

    client = CosmosClient(endpoint, credential=key)
    database = client.get_database_client(db_name)
    container = database.get_container_client(container_name)
    return container

@app.route(route="TextAnalyzer", methods=["GET", "POST"])
def TextAnalyzer(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("TextAnalyzer called")

    text = req.params.get("text")
    if not text:
        try:
            body = req.get_json()
            text = body.get("text")
        except ValueError:
            text = None

    if not text:
        return func.HttpResponse(
            json.dumps(
                {
                    "error": "No text provided",
                    "how_to_use": {
                        "GET": "/api/TextAnalyzer?text=Hello world",
                        "POST": {"text": "Hello world"}
                    }
                },
                indent=2
            ),
            status_code=400,
            mimetype="application/json"
        )

    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    sentence_count = len(re.findall(r"[.!?]+", text)) or 1
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()]) or 1
    reading_time_minutes = round(word_count / 200, 1)
    avg_word_length = round((char_count_no_spaces / word_count), 1) if word_count > 0 else 0.0
    longest_word = max(words, key=len) if words else ""

    analysis = {
        "wordCount": word_count,
        "characterCount": char_count,
        "characterCountNoSpaces": char_count_no_spaces,
        "sentenceCount": sentence_count,
        "paragraphCount": paragraph_count,
        "averageWordLength": avg_word_length,
        "longestWord": longest_word,
        "readingTimeMinutes": reading_time_minutes
    }

    metadata = {
        "analyzedAt": datetime.utcnow().isoformat(),
        "textPreview": text[:100] + "..." if len(text) > 100 else text
    }

    record_id = str(uuid.uuid4())
    record = {
        "id": record_id,
        "analysis": analysis,
        "metadata": metadata,
        "originalText": text
    }

    try:
        container = get_cosmos_container()
        container.upsert_item(record)
    except Exception as e:
        logging.exception("Cosmos write failed")
        return func.HttpResponse(
            json.dumps({"error": "Failed to store result in Cosmos DB", "details": str(e)}, indent=2),
            status_code=500,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps({"id": record_id, "analysis": analysis, "metadata": metadata}, indent=2),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="GetAnalysisHistory", methods=["GET"])
def GetAnalysisHistory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("GetAnalysisHistory called")

    limit_str = req.params.get("limit", "10")
    try:
        limit = int(limit_str)
    except ValueError:
        limit = 10

    if limit < 1:
        limit = 1
    if limit > 50:
        limit = 50

    try:
        container = get_cosmos_container()
        query = f"SELECT TOP {limit} c.id, c.analysis, c.metadata FROM c ORDER BY c.metadata.analyzedAt DESC"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return func.HttpResponse(
            json.dumps({"count": len(items), "results": items}, indent=2),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("Cosmos read failed")
        return func.HttpResponse(
            json.dumps({"error": "Failed to retrieve history", "details": str(e)}, indent=2),
            status_code=500,
            mimetype="application/json"
        )

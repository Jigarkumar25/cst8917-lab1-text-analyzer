# Database Choice – Azure Cosmos DB (NoSQL)

## Selected Database
Azure Cosmos DB using the NoSQL API was selected as the database for this project.

---

## Reason for Selection
Azure Cosmos DB is well suited for this serverless application for the following reasons:

- **Serverless compatibility:** Cosmos DB integrates seamlessly with Azure Functions and supports event-driven, serverless workloads.
- **Flexible schema:** The text analysis results are stored as JSON documents, allowing the data structure to evolve without schema migrations.
- **Scalability:** Cosmos DB automatically scales to handle varying workloads, which is ideal for APIs with unpredictable traffic.
- **Low latency:** Provides fast read and write operations, improving API responsiveness.
- **Azure-native integration:** The database can be securely accessed using environment variables and the official `azure-cosmos` Python SDK.

---

## Cost Considerations
Cosmos DB is configured in **serverless mode**, which minimizes cost by charging only for requests that are executed. This makes it suitable for student labs and small workloads.

---

## Alternatives Considered
The following alternatives were considered before selecting Cosmos DB:

- **Azure Table Storage:** Offers lower cost and simplicity, but has limited querying and filtering capabilities.
- **SQLite:** Suitable for local testing, but not recommended for cloud or serverless environments due to its file-based nature and lack of scalability.

Cosmos DB was selected because it provides the best balance of scalability, flexibility, and cloud-native features.

---

## Conclusion
Azure Cosmos DB (NoSQL) is an appropriate choice for this project as it supports serverless architecture, efficiently stores JSON data, and integrates cleanly with Azure Functions while keeping operational overhead and cost low.

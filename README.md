# LLM-Powered-Knowledge-Graph-Construction

Project Overview
This project develops an end-to-end LLM-powered Knowledge Graph Construction and Question Answering system.
The system takes unstructured text, extracts entities and relationships using a local Large Language Model (LLM), normalizes the extracted information, stores the resulting knowledge graph in Neo4j, and allows users to ask questions in natural language.

The natural-language question is converted into Cypher by an LLM, validated using a safety layer, executed against Neo4j, and converted into a concise natural-language answer.

Core pipeline
Unstructured Text
       |
       v
LLM-based Knowledge Extraction
       |
       v
Entities + Relationships
       |
       v
Entity Linking / Normalization
       |
       v
Relationship Normalization
       |
       v
Neo4j Knowledge Graph
       |
       +-------------------------------+
       |                               |
       v                               |
Natural Language Question              |
       |                               |
       v                               |
LLM: Question -> Cypher                |
       |                               |
       v                               |
Cypher Validation / Safety             |
       |                               |
       v                               |
Neo4j Query                            |
       |                               |
       v                               |
Database Result                        |
       |                               |
       v                               |
Natural Language Answer <--------------+
1. Problem Statement
Large amounts of useful information exist in unstructured text such as documents, reports, articles, and notes. Traditional keyword search can retrieve relevant text but does not naturally represent the relationships between people, organizations, locations, products, and events.
This project addresses that problem by combining:

Natural Language Processing
Large Language Models
Prompt Engineering
Entity Linking
Relationship Normalization
Knowledge Graphs
Neo4j
Cypher
Natural Language Question Answering
The objective is to convert unstructured information into a structured graph that can subsequently be queried using natural language.
2. Objectives
Primary Objective
To design and implement an LLM-powered pipeline that automatically converts unstructured text into a structured Knowledge Graph and supports natural-language querying over that graph.
Specific Objectives
Extract named entities from unstructured text.
Classify entities into predefined types.
Extract relationships between entities.
Use prompt engineering to improve extraction quality.
Normalize entity names and relationship directions.
Store the resulting graph in Neo4j.
Query the graph using Cypher.
Convert natural-language questions into Cypher queries.
Validate generated Cypher before execution.
Convert database results into natural-language answers.
Compare a baseline extraction prompt with an engineered prompt.
Evaluate entity and relationship extraction using precision, recall, and F1-score.
Perform error analysis to identify and correct extraction failures.
3. Technologies Used
Technology	Purpose
Python	Main programming language
Ollama	Local LLM execution
Llama 3.2	Local LLM used for extraction and querying
Pydantic	Structured output validation
Neo4j	Knowledge Graph database
Cypher	Graph query language
python-dotenv	Environment variable management
JSON	Structured data storage
Git / GitHub	Version control and project sharing
4. System Architecture
4.1 Knowledge Extraction Pipeline
Raw Text
   |
   v
LLM Extractor
   |
   +--> Entities
   |
   +--> Relationships
   |
   v
Pydantic Validation
   |
   v
Entity Linking
   |
   v
Relationship Normalization
   |
   v
JSON Output
   |
   v
Neo4j Graph
4.2 Question Answering Pipeline
User Question
      |
      v
LLM Cypher Generator
      |
      v
Generated Cypher
      |
      v
Cypher Validator
      |
      +---- Invalid --> Reject
      |
      v
Neo4j
      |
      v
Query Results
      |
      v
Answer Generator
      |
      v
Natural Language Answer
5. Project Structure
PythonProject4/
│
├── data/
│   ├── raw/
│   │   └── sample.txt
│   │
│   └── evaluation/
│       ├── documents/
│       │   ├── doc1.txt
│       │   ├── doc2.txt
│       │   ├── doc3.txt
│       │   ├── doc4.txt
│       │   └── doc5.txt
│       │
│       └── ground_truth/
│           ├── doc1.json
│           ├── doc2.json
│           ├── doc3.json
│           ├── doc4.json
│           └── doc5.json
│
├── output/
│   ├── knowledge.json
│   ├── baseline_results.json
│   ├── engineered_results.json
│   └── batch_evaluation_results.json
│
├── src/
│   ├── main.py
│   ├── text_loader.py
│   ├── llm_extractor.py
│   ├── entity_linker.py
│   ├── relationship_normalizer.py
│   ├── schemas.py
│   ├── neo4j_manager.py
│   ├── graph_builder.py
│   ├── output_manager.py
│   ├── evaluator.py
│   ├── evaluation_runner.py
│   ├── batch_evaluation.py
│   ├── batch_error_analysis.py
│   ├── baseline_extractor.py
│   ├── prompt_comparison.py
│   ├── graph_queries.py
│   ├── query_test.py
│   ├── nl_query.py
│   ├── nl_query_test.py
│   ├── answer_generator.py
│   ├── cypher_validator.py
│   └── config.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
.env contains local credentials and must never be committed to GitHub.
6. Entity Types
The extraction pipeline uses a controlled vocabulary of entity types.
PERSON
COMPANY
LOCATION
PRODUCT
DATE
Examples:
Entity	Type
Satya Nadella	PERSON
Microsoft	COMPANY
San Francisco	LOCATION
Azure	PRODUCT
2018	DATE
7. Relationship Types
The system uses predefined relationship types:
CEO_OF
ACQUIRED
HEADQUARTERED_IN
DEVELOPED
FOUNDED_BY
WORKS_AT
LOCATED_IN
CREATED
Examples:
Satya Nadella --CEO_OF--> Microsoft

Microsoft --ACQUIRED--> GitHub

GitHub --HEADQUARTERED_IN--> San Francisco

Microsoft --DEVELOPED--> Azure

Meta --FOUNDED_BY--> Mark Zuckerberg
8. LLM Knowledge Extraction
The project uses Llama 3.2 through Ollama.
The extraction prompt was engineered to reduce hallucination and improve consistency.

Important prompt rules include:

Extract every explicitly mentioned named entity.
Extract explicit dates and years.
Do not add information from background knowledge.
Preserve entity names as written.
Do not invent company suffixes.
Every entity must occur explicitly in the input text.
Use only predefined relationship types.
Relationship endpoints must exist in the entity list.
Explicitly define relationship direction.
Validate extracted output using a structured Pydantic schema.
9. Structured Output
The project uses Pydantic models to enforce the expected structure.
class Entity(BaseModel):
    name: str
    type: str


class Relationship(BaseModel):
    source: str
    relation: str
    target: str


class KnowledgeGraph(BaseModel):
    entities: list[Entity]
    relationships: list[Relationship]
This prevents the downstream pipeline from relying on arbitrary unstructured LLM output.
10. Entity Linking and Normalization
LLMs may produce variations such as:
Microsoft
Microsoft Corporation
Microsoft Corp
Microsoft Inc.
The deterministic entity linker normalizes known company suffixes.
For example:

Microsoft Corporation -> Microsoft
Microsoft Corp -> Microsoft
This improves consistency before graph construction.
The normalization is deliberately deterministic rather than asking another LLM to make the decision.

11. Relationship Normalization
Relationship direction is important in a Knowledge Graph.
For example:

Mark Zuckerberg founded Meta.
The desired graph representation is:
Meta --FOUNDED_BY--> Mark Zuckerberg
The relationship normalizer checks the entity types and corrects the direction when necessary.
It also removes duplicate relationships.

12. Neo4j Knowledge Graph
Neo4j stores the extracted information as a graph.
Example:

(Satya Nadella)
       |
    CEO_OF
       |
       v
   (Microsoft)
       |
   DEVELOPED
       |
       v
     (Azure)
Nodes use:
Entity
and store properties such as:
name
type
Relationships represent semantic connections between entities.
13. Example Cypher Queries
Find CEOs
MATCH (person)-[:CEO_OF]->(company)
RETURN person.name AS CEO,
       company.name AS Company;
Find products developed by Microsoft
MATCH (company)-[:DEVELOPED]->(product)
WHERE company.name = "Microsoft"
RETURN product.name AS Product;
Find the company that developed Azure
MATCH (company)-[:DEVELOPED]->(product)
WHERE product.name = "Azure"
RETURN company.name AS Company;
Find a company's connected entities
MATCH (company:Entity {name: "Microsoft"})-[r]-(connected)
RETURN type(r) AS Relationship,
       connected.name AS ConnectedEntity;
14. Natural Language Querying
The system allows users to ask questions without writing Cypher.
Example:

User:
Which company developed Azure?
The LLM generates:
MATCH (company)-[:DEVELOPED]->(product)
WHERE product.name = "Azure"
RETURN company.name AS Answer
Neo4j returns:
Microsoft
The answer generator converts this into:
Microsoft developed Azure.
15. Cypher Safety Validation
Generated Cypher should not be executed blindly.
The project therefore implements a validation layer.

The validator:

Allows read-only MATCH queries.
Blocks CREATE.
Blocks MERGE.
Blocks DELETE.
Blocks DETACH.
Blocks SET.
Blocks REMOVE.
Blocks DROP.
Blocks other destructive operations.
Checks relationship types against the approved relationship vocabulary.
Example:
Natural Language
       |
       v
Generated Cypher
       |
       v
Cypher Validator
       |
   +---+---+
   |       |
Valid    Invalid
   |       |
   v       v
Neo4j    Reject
This provides an additional safety layer between the LLM and the database.
16. Evaluation Methodology
The project includes a controlled evaluation dataset containing five documents.
Each document has:

Input text
Ground-truth entities
Ground-truth relationships
The system is evaluated using:
True Positives
False Positives
False Negatives
Precision
Recall
F1-score
The evaluation uses exact matching of entity and relationship tuples.
Metrics
Precision
Precision = TP / (TP + FP)
Precision measures how many predicted items are correct.
Recall
Recall = TP / (TP + FN)
Recall measures how many expected items were successfully extracted.
F1-score
F1 = 2 × Precision × Recall / (Precision + Recall)
F1 combines precision and recall.
17. Baseline vs Engineered Prompt
The project compares two approaches using the same five-document controlled evaluation set.
Baseline
The baseline prompt provides only basic instructions to extract entities and relationships.
Engineered
The engineered pipeline adds:
Controlled entity types
Controlled relationship types
Explicit extraction rules
Anti-hallucination instructions
Exact entity preservation
Explicit relationship direction
Structured output validation
Deterministic entity normalization
Deterministic relationship normalization
18. Evaluation Results
Results on the controlled five-document evaluation set:
Pipeline	Entity F1	Relationship F1
Baseline	0.927	0.375
Engineered	1.000	1.000
The engineered pipeline therefore performed better on this controlled evaluation set, particularly for relationship extraction.
These results should be interpreted as a controlled experiment rather than a claim of universal model accuracy.

19. Error Analysis
The project also performs document-level error analysis.
Before normalization and prompt improvements, observed errors included:

Entity errors
Examples included:
apple
being incorrectly returned as:
apple inc.
and dates being hallucinated even when they were not present in the source text.
Relationship errors
For:
Mark Zuckerberg founded Meta.
the LLM initially produced:
Mark Zuckerberg --FOUNDED_BY--> Meta
while the required representation was:
Meta --FOUNDED_BY--> Mark Zuckerberg
Fixes
These errors motivated:
Explicit anti-hallucination prompt rules.
Exact entity-name preservation.
Deterministic company suffix normalization.
Explicit relationship-direction instructions.
Deterministic relationship normalization.
The final controlled evaluation showed no remaining errors across the five evaluation documents.
20. How to Run the Project
Prerequisites
Install:
Python 3.10+
Neo4j
Ollama
Llama 3.2
Pull the local model:
ollama pull llama3.2
Start Neo4j.
Create Virtual Environment
python3 -m venv .venv
Activate:
macOS / Linux
source .venv/bin/activate
Install dependencies:
pip install -r requirements.txt
21. Environment Configuration
Create .env:
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=YOUR_PASSWORD
Never commit .env.
The repository includes .gitignore rules to prevent the file from being uploaded.

22. Run the Main Knowledge Graph Pipeline
python src/main.py
This performs:
Load text
   ↓
Extract knowledge
   ↓
Normalize entities
   ↓
Normalize relationships
   ↓
Save JSON
   ↓
Build Neo4j graph
23. Test Direct Graph Queries
python src/query_test.py
Example output:
CEOs
----
Satya Nadella -> Microsoft

Microsoft Products
------------------
Visual Studio Code
Azure

Company That Developed Azure
----------------------------
Microsoft
24. Test Natural Language QA
python src/nl_query_test.py
Example:
Ask a question about the knowledge graph:
Which company developed Azure?
Expected flow:
Generating Cypher...
Cypher query is valid.
Executing query...
Microsoft developed Azure.
25. Run Evaluation
Prompt comparison:
python src/prompt_comparison.py
Batch evaluation:
python src/batch_evaluation.py
Error analysis:
python src/batch_error_analysis.py
26. Output Files
The output/ directory contains generated artifacts such as:
knowledge.json
baseline_results.json
engineered_results.json
batch_evaluation_results.json
These contain extracted knowledge and evaluation results.
27. Key Research Contribution
The project is not limited to simply calling an LLM for extraction.
The main contribution is the combination of:

LLM
+
Prompt Engineering
+
Structured Output
+
Deterministic Normalization
+
Knowledge Graph
+
Cypher
+
Natural Language Querying
+
Cypher Validation
+
Quantitative Evaluation
This hybrid approach separates tasks that are better handled by an LLM from tasks that benefit from deterministic rules.
28. Limitations
The evaluation dataset contains only five controlled documents.
The reported F1 results should not be interpreted as general benchmark performance.
The relationship and entity vocabularies are predefined.
Complex linguistic constructions may require additional extraction rules.
Ambiguous entities may require more sophisticated entity resolution.
Natural-language-to-Cypher generation can fail for questions outside the supported schema.
The current system uses a local LLM and therefore depends on local model availability and performance.
The graph currently focuses on a relatively small controlled schema.
29. Future Scope
Possible future improvements include:
Larger real-world evaluation datasets.
More entity and relationship types.
Advanced entity disambiguation.
Confidence scores for extracted facts.
Graph embeddings.
Hybrid vector + graph retrieval.
RAG integration.
Multi-hop reasoning.
Graph-based question answering.
Web-based user interface.
Streamlit or FastAPI deployment.
Authentication and access control.
Query logging and monitoring.
Automated evaluation on larger datasets.
Support for multiple documents and document provenance.
Source citations for individual graph facts.
30. Example End-to-End Demonstration
Input
Satya Nadella is the CEO of Microsoft.
Microsoft acquired GitHub in 2018.
GitHub is headquartered in San Francisco.
Microsoft developed Azure.
Extracted entities
Satya Nadella → PERSON
Microsoft → COMPANY
GitHub → COMPANY
2018 → DATE
San Francisco → LOCATION
Azure → PRODUCT
Extracted relationships
Satya Nadella --CEO_OF--> Microsoft

Microsoft --ACQUIRED--> GitHub

GitHub --HEADQUARTERED_IN--> San Francisco

Microsoft --DEVELOPED--> Azure
Graph
Satya Nadella
      |
    CEO_OF
      |
      v
  Microsoft
    |     \
    |      \
ACQUIRED  DEVELOPED
    |         |
    v         v
 GitHub     Azure
    |
HEADQUARTERED_IN
    |
    v
San Francisco
User question
Which company developed Azure?
Generated Cypher
MATCH (company)-[:DEVELOPED]->(product)
WHERE product.name = "Azure"
RETURN company.name AS Answer
Final answer
Microsoft developed Azure.

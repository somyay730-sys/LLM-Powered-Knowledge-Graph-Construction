from ollama import chat


def generate_cypher(question):

    prompt = f"""
You are a Neo4j Cypher query generator.

The knowledge graph contains nodes with the label:

Entity

Each Entity node has these properties:

name
type

Possible entity types are:

PERSON
COMPANY
LOCATION
PRODUCT
DATE

The graph contains relationships such as:

CEO_OF
ACQUIRED
HEADQUARTERED_IN
DEVELOPED
FOUNDED_BY
WORKS_AT
LOCATED_IN
CREATED

Examples:

Question:
Who is the CEO of Microsoft?

Cypher:
MATCH (person)-[:CEO_OF]->(company)
WHERE company.name = "Microsoft"
RETURN person.name AS Answer

Question:
Which company developed Azure?

Cypher:
MATCH (company)-[:DEVELOPED]->(product)
WHERE product.name = "Azure"
RETURN company.name AS Answer

Question:
Where is Microsoft headquartered?

Cypher:
MATCH (company)-[:HEADQUARTERED_IN]->(location)
WHERE company.name = "Microsoft"
RETURN location.name AS Answer

Question:
Which products did Microsoft develop?

Cypher:
MATCH (company)-[:DEVELOPED]->(product)
WHERE company.name = "Microsoft"
RETURN product.name AS Answer

Rules:

1. Return ONLY the Cypher query.
2. Do not use markdown.
3. Do not explain the query.
4. Use only the Entity label.
5. Use only the relationship types listed above.
6. Do not invent entities or relationships.
7. Return the answer using the alias:

AS Answer

USER QUESTION:

{question}
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response.message.content.strip()
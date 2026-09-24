from ollama import chat

from schemas import KnowledgeGraph


def extract_baseline_knowledge(text):
    prompt = f"""
Extract entities and relationships from the following text.

Entity types:
PERSON
COMPANY
LOCATION
PRODUCT
DATE

Return entities and relationships as structured data.

TEXT:

{text}
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=KnowledgeGraph.model_json_schema(),
        options={
            "temperature": 0
        }
    )

    knowledge = KnowledgeGraph.model_validate_json(
        response.message.content
    )

    return knowledge.model_dump()
from ollama import chat


def generate_answer(question, results):

    prompt = f"""
You are a question-answering assistant.

Answer the user's question using ONLY the information
provided in the database results.

USER QUESTION:
{question}

DATABASE RESULTS:
{results}

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the database results are empty, say:
   "I could not find this information in the knowledge graph."
4. Give a short, direct answer.
5. Do not mention Cypher, Neo4j, or the database.
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
from neo4j_manager import Neo4jManager
from nl_query import generate_cypher
from answer_generator import generate_answer
from cypher_validator import validate_cypher

from config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD
)

def execute_query(db, cypher):

    with db.driver.session() as session:

        result = session.run(cypher)

        return [
            record.data()
            for record in result
        ]


def main():
    db = Neo4jManager(
        NEO4J_URI,
        NEO4J_USERNAME,
        NEO4J_PASSWORD
    )

    question = input(
        "\nAsk a question about the knowledge graph: "
    )

    print("\nGenerating Cypher...")
    print("--------------------")

    cypher = generate_cypher(question)

    print(cypher)

    print("\nValidating Cypher...")
    print("--------------------")

    is_valid, message = validate_cypher(cypher)

    print(message)

    if not is_valid:
        print("\nQuery rejected for safety.")
        db.close()
        return

    print("\nExecuting query...")
    print("------------------")

    results = execute_query(
        db,
        cypher
    )

    print("\nDATABASE RESULT")
    print("---------------")

    for result in results:
        print(result)

    answer = generate_answer(
        question,
        results
    )

    print("\nANSWER")
    print("------")

    print(answer)

    db.close()


if __name__ == "__main__":
    main()
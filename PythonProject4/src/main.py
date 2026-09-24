import json
from pathlib import Path

from text_loader import load_text
from llm_extractor import extract_knowledge
from entity_linker import link_entities
from neo4j_manager import Neo4jManager
from graph_builder import build_graph
from output_maager import save_knowledge


def main():
    # Find project root folder
    project_root = Path(__file__).resolve().parent.parent

    # Input text file path
    file_path = (
        project_root
        / "data"
        / "raw"
        / "sample.txt"
    )

    # Load unstructured text
    text = load_text(file_path)

    print("\nDOCUMENT CONTENT")
    print("----------------")
    print(text)

    # Extract entities and relationships using LLM
    print("\nEXTRACTING KNOWLEDGE...")
    print("-----------------------")

    knowledge = extract_knowledge(text)

    print("\nEXTRACTED KNOWLEDGE")
    print("-------------------")

    print(
        json.dumps(
            knowledge,
            indent=4
        )
    )

    # Entity linking and normalization
    print("\nLINKING AND NORMALIZING ENTITIES...")
    print("-----------------------------------")

    linked_knowledge = link_entities(
        knowledge
    )

    print("\nNORMALIZED KNOWLEDGE")
    print("--------------------")

    print(
        json.dumps(
            linked_knowledge,
            indent=4
        )
    )

    # Save extracted knowledge
    output_path = (
        project_root
        / "output"
        / "knowledge.json"
    )

    save_knowledge(
        linked_knowledge,
        output_path
    )

    # Neo4j connection details
    from config import (
        NEO4J_URI,
        NEO4J_USERNAME,
        NEO4J_PASSWORD
    )

    # Connect to Neo4j
    db = Neo4jManager(
        NEO4J_URI,
        NEO4J_USERNAME,
        NEO4J_PASSWORD
    )

    # Build Knowledge Graph
    build_graph(
        linked_knowledge,
        db
    )

    # Close Neo4j connection
    db.close()

    print(
        "\nKNOWLEDGE GRAPH CREATED SUCCESSFULLY!"
    )


if __name__ == "__main__":
    main()
from neo4j_manager import Neo4jManager
from graph_queries import GraphQueries


from config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD
)


def main():
    db = Neo4jManager(
        NEO4J_URI,
        NEO4J_USERNAME,
        NEO4J_PASSWORD
    )

    queries = GraphQueries(db)

    print("\nCEOs")
    print("----")

    ceos = queries.get_ceos()

    for result in ceos:
        print(
            f"{result['CEO']} "
            f"-> {result['Company']}"
        )

    print("\nMicrosoft Products")
    print("------------------")

    products = (
        queries.get_products_by_company(
            "Microsoft"
        )
    )

    for result in products:
        print(result["Product"])

    print("\nCompany That Developed Azure")
    print("----------------------------")

    companies = (
        queries.get_company_for_product(
            "Azure"
        )
    )

    for result in companies:
        print(result["Company"])

    db.close()


if __name__ == "__main__":
    main()
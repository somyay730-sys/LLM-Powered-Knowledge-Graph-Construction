import re


ALLOWED_RELATIONSHIPS = {
    "CEO_OF",
    "ACQUIRED",
    "HEADQUARTERED_IN",
    "DEVELOPED",
    "FOUNDED_BY",
    "WORKS_AT",
    "LOCATED_IN",
    "CREATED"
}


FORBIDDEN_KEYWORDS = [
    "CREATE",
    "MERGE",
    "DELETE",
    "DETACH",
    "SET",
    "REMOVE",
    "DROP",
    "LOAD CSV",
    "ALTER",
    "RENAME"
]


def validate_cypher(query):

    query_upper = query.upper().strip()

    # Only allow read-only MATCH queries
    if not (
        query_upper.startswith("MATCH")
        or query_upper.startswith("OPTIONAL MATCH")
    ):
        return False, "Only MATCH queries are allowed."

    # Block write/destructive operations
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, query_upper):
            return False, (
                f"Forbidden Cypher operation detected: {keyword}"
            )

    # Check relationship types
    relationship_pattern = r":([A-Z_]+)"

    relationships = re.findall(
        relationship_pattern,
        query_upper
    )

    for relationship in relationships:

        if relationship not in ALLOWED_RELATIONSHIPS:

            return False, (
                f"Unknown relationship type: "
                f"{relationship}"
            )

    return True, "Cypher query is valid."
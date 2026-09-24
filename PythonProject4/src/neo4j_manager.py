from neo4j import GraphDatabase


class Neo4jManager:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

        self.driver.verify_connectivity()

        print("Neo4j connected successfully.")

    def close(self):
        self.driver.close()

    def create_entity(self, name, entity_type):
        query = """
        MERGE (e:Entity {name: $name})
        SET e.type = $entity_type
        """

        with self.driver.session() as session:
            session.run(
                query,
                name=name,
                entity_type=entity_type
            )

        print(f"Entity created: {name} ({entity_type})")

    def create_relationship(self, source, relation, target):
        allowed_relations = {
            "CEO_OF",
            "ACQUIRED",
            "HEADQUARTERED_IN",
            "DEVELOPED",
            "FOUNDED_BY",
            "WORKS_AT",
            "LOCATED_IN",
            "CREATED"
        }

        relation = relation.upper().replace(" ", "_")

        if relation not in allowed_relations:
            relation = "RELATED_TO"

        query = f"""
        MATCH (source:Entity {{name: $source}})
        MATCH (target:Entity {{name: $target}})

        MERGE (source)-[:{relation}]->(target)
        """

        with self.driver.session() as session:
            session.run(
                query,
                source=source,
                target=target
            )

        print(
            f"Relationship created: "
            f"{source} --{relation}--> {target}"
        )
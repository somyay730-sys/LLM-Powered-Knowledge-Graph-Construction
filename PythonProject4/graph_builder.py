def build_graph(knowledge, db):

    entities = knowledge.get("entities", [])
    relationships = knowledge.get("relationships", [])

    print("\nCREATING ENTITIES")
    print("-----------------")

    for entity in entities:

        name = entity["name"]
        entity_type = entity["type"]

        db.create_entity(
            name,
            entity_type
        )

    print("\nCREATING RELATIONSHIPS")
    print("----------------------")

    for relationship in relationships:

        source = relationship["source"]
        relation = relationship["relation"]
        target = relationship["target"]

        db.create_relationship(
            source,
            relation,
            target
        )
def normalize_relationships(knowledge):
    entity_types = {
        entity["name"]: entity["type"].upper()
        for entity in knowledge["entities"]
    }

    normalized_relationships = []
    seen_relationships = set()

    for relationship in knowledge["relationships"]:
        source = relationship["source"]
        relation = relationship["relation"].upper()
        target = relationship["target"]

        source_type = entity_types.get(source)
        target_type = entity_types.get(target)

        if (
            relation == "FOUNDED_BY"
            and source_type == "PERSON"
            and target_type == "COMPANY"
        ):
            source, target = target, source

        relationship_key = (
            source.lower(),
            relation,
            target.lower()
        )

        if relationship_key not in seen_relationships:
            normalized_relationships.append(
                {
                    "source": source,
                    "relation": relation,
                    "target": target
                }
            )

            seen_relationships.add(
                relationship_key
            )

    return {
        "entities": knowledge["entities"],
        "relationships": normalized_relationships
    }
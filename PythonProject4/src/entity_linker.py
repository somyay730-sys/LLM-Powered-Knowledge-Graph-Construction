COMPANY_SUFFIXES = [
    " corporation",
    " corp.",
    " corp",
    " inc.",
    " inc",
    " limited",
    " ltd.",
    " ltd"
]


def normalize_entity_name(name):
    normalized_name = name.strip()

    lower_name = normalized_name.lower()

    for suffix in COMPANY_SUFFIXES:
        if lower_name.endswith(suffix):
            normalized_name = normalized_name[
                :len(normalized_name) - len(suffix)
            ].strip()

            break

    return normalized_name


def link_entities(knowledge):
    normalized_entities = []
    entity_mapping = {}
    seen_entities = set()

    for entity in knowledge["entities"]:
        original_name = entity["name"]
        entity_type = entity["type"]

        normalized_name = normalize_entity_name(
            original_name
        )

        entity_mapping[original_name] = (
            normalized_name
        )

        entity_key = (
            normalized_name.lower(),
            entity_type.upper()
        )

        if entity_key not in seen_entities:
            normalized_entities.append(
                {
                    "name": normalized_name,
                    "type": entity_type
                }
            )

            seen_entities.add(entity_key)

    normalized_relationships = []

    for relationship in knowledge[
        "relationships"
    ]:
        source = entity_mapping.get(
            relationship["source"],
            relationship["source"]
        )

        target = entity_mapping.get(
            relationship["target"],
            relationship["target"]
        )

        normalized_relationships.append(
            {
                "source": source,
                "relation": relationship[
                    "relation"
                ],
                "target": target
            }
        )

    return {
        "entities": normalized_entities,
        "relationships": (
            normalized_relationships
        )
    }
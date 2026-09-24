import json


def load_ground_truth(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def calculate_metrics(
    predicted_items,
    actual_items
):
    predicted_set = set(predicted_items)
    actual_set = set(actual_items)

    true_positive_items = (
        predicted_set & actual_set
    )

    false_positive_items = (
        predicted_set - actual_set
    )

    false_negative_items = (
        actual_set - predicted_set
    )

    true_positives = len(
        true_positive_items
    )

    false_positives = len(
        false_positive_items
    )

    false_negatives = len(
        false_negative_items
    )

    precision = (
        true_positives
        / (
            true_positives
            + false_positives
        )
        if (
            true_positives
            + false_positives
        ) > 0
        else 0
    )

    recall = (
        true_positives
        / (
            true_positives
            + false_negatives
        )
        if (
            true_positives
            + false_negatives
        ) > 0
        else 0
    )

    f1_score = (
        2 * precision * recall
        / (precision + recall)
        if precision + recall > 0
        else 0
    )

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,

        "correct_items": list(
            true_positive_items
        ),

        "wrong_predictions": list(
            false_positive_items
        ),

        "missed_items": list(
            false_negative_items
        )
    }


def evaluate_entities(
    predicted,
    actual
):
    predicted_entities = [
        (
            entity["name"].lower(),
            entity["type"].upper()
        )
        for entity in predicted["entities"]
    ]

    actual_entities = [
        (
            entity["name"].lower(),
            entity["type"].upper()
        )
        for entity in actual["entities"]
    ]

    return calculate_metrics(
        predicted_entities,
        actual_entities
    )


def evaluate_relationships(
    predicted,
    actual
):
    predicted_relationships = [
        (
            relationship["source"].lower(),
            relationship["relation"].upper(),
            relationship["target"].lower()
        )
        for relationship
        in predicted["relationships"]
    ]

    actual_relationships = [
        (
            relationship["source"].lower(),
            relationship["relation"].upper(),
            relationship["target"].lower()
        )
        for relationship
        in actual["relationships"]
    ]

    return calculate_metrics(
        predicted_relationships,
        actual_relationships
    )


def evaluate_knowledge(
    predicted,
    actual
):
    entity_metrics = evaluate_entities(
        predicted,
        actual
    )

    relationship_metrics = (
        evaluate_relationships(
            predicted,
            actual
        )
    )

    return {
        "entity_metrics": entity_metrics,
        "relationship_metrics": (
            relationship_metrics
        )
    }
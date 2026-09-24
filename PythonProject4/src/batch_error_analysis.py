import json
from pathlib import Path


def load_json(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def print_items(title, items):
    print(f"\n{title}")

    if not items:
        print("None")
        return

    for item in items:
        print(item)


def main():
    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    results_path = (
        project_root
        / "output"
        / "batch_evaluation_results.json"
    )

    results = load_json(results_path)

    print("\nBATCH ERROR ANALYSIS")
    print("====================")

    for document in results["document_results"]:
        entity_metrics = document["entity_metrics"]

        relationship_metrics = document[
            "relationship_metrics"
        ]

        entity_f1 = entity_metrics["f1_score"]

        relationship_f1 = relationship_metrics[
            "f1_score"
        ]

        if (
            entity_f1 < 1.0
            or relationship_f1 < 1.0
        ):
            print("\n")
            print("=" * 50)

            print(
                f"DOCUMENT: "
                f"{document['document']}"
            )

            print("=" * 50)

            print(
                f"\nEntity F1: "
                f"{entity_f1:.3f}"
            )

            print_items(
                "Wrong Entity Predictions:",
                entity_metrics[
                    "wrong_predictions"
                ]
            )

            print_items(
                "Missed Entities:",
                entity_metrics[
                    "missed_items"
                ]
            )

            print(
                f"\nRelationship F1: "
                f"{relationship_f1:.3f}"
            )

            print_items(
                "Wrong Relationship Predictions:",
                relationship_metrics[
                    "wrong_predictions"
                ]
            )

            print_items(
                "Missed Relationships:",
                relationship_metrics[
                    "missed_items"
                ]
            )


if __name__ == "__main__":
    main()
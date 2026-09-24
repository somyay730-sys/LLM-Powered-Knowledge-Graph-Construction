import json
from pathlib import Path

from evaluator import (
    load_ground_truth,
    evaluate_knowledge
)


def main():
    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    prediction_path = (
        project_root
        / "output"
        / "knowledge.json"
    )

    ground_truth_path = (
        project_root
        / "data"
        / "evaluation"
        / "ground_truth.json"
    )

    with open(
        prediction_path,
        "r",
        encoding="utf-8"
    ) as file:
        predicted = json.load(file)

    actual = load_ground_truth(
        ground_truth_path
    )

    results = evaluate_knowledge(
        predicted,
        actual
    )

    print("\nEVALUATION RESULTS")
    print("==================")

    # ENTITY EVALUATION

    print("\nENTITY EXTRACTION")
    print("-----------------")

    entity_metrics = results["entity_metrics"]

    print(
        f"True Positives: "
        f"{entity_metrics['true_positives']}"
    )

    print(
        f"False Positives: "
        f"{entity_metrics['false_positives']}"
    )

    print(
        f"False Negatives: "
        f"{entity_metrics['false_negatives']}"
    )

    print(
        f"Precision: "
        f"{entity_metrics['precision']:.3f}"
    )

    print(
        f"Recall: "
        f"{entity_metrics['recall']:.3f}"
    )

    print(
        f"F1 Score: "
        f"{entity_metrics['f1_score']:.3f}"
    )

    print("\nCorrect Entity Predictions:")

    for item in entity_metrics["correct_items"]:
        print(item)

    print("\nWrong Entity Predictions:")

    for item in entity_metrics["wrong_predictions"]:
        print(item)

    print("\nMissed Entities:")

    for item in entity_metrics["missed_items"]:
        print(item)

    # RELATIONSHIP EVALUATION

    print("\nRELATIONSHIP EXTRACTION")
    print("-----------------------")

    relationship_metrics = results[
        "relationship_metrics"
    ]

    print(
        f"True Positives: "
        f"{relationship_metrics['true_positives']}"
    )

    print(
        f"False Positives: "
        f"{relationship_metrics['false_positives']}"
    )

    print(
        f"False Negatives: "
        f"{relationship_metrics['false_negatives']}"
    )

    print(
        f"Precision: "
        f"{relationship_metrics['precision']:.3f}"
    )

    print(
        f"Recall: "
        f"{relationship_metrics['recall']:.3f}"
    )

    print(
        f"F1 Score: "
        f"{relationship_metrics['f1_score']:.3f}"
    )

    print("\nCorrect Relationship Predictions:")

    for item in relationship_metrics["correct_items"]:
        print(item)

    print("\nWrong Relationship Predictions:")

    for item in relationship_metrics[
        "wrong_predictions"
    ]:
        print(item)

    print("\nMissed Relationships:")

    for item in relationship_metrics["missed_items"]:
        print(item)

def save_evaluation_results(results, output_path):
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            results,
            file,
            indent=4
        )

    print(
        f"\nEvaluation results saved to: "
        f"{output_path}"
    )

if __name__ == "__main__":
    main(results = evaluate_knowledge(
    predicted,
    actual
))
import json
from pathlib import Path

from text_loader import load_text
from baseline_extractor import extract_baseline_knowledge
from llm_extractor import extract_knowledge
from entity_linker import link_entities
from relationship_normalizer import normalize_relationships
from evaluator import evaluate_knowledge


def load_json(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def calculate_overall(counts):
    precision = (
        counts["tp"] / (counts["tp"] + counts["fp"])
        if counts["tp"] + counts["fp"] > 0
        else 0
    )

    recall = (
        counts["tp"] / (counts["tp"] + counts["fn"])
        if counts["tp"] + counts["fn"] > 0
        else 0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


def main():
    project_root = Path(__file__).resolve().parent.parent

    documents_folder = (
        project_root
        / "data"
        / "evaluation"
        / "documents"
    )

    ground_truth_folder = (
        project_root
        / "data"
        / "evaluation"
        / "ground_truth"
    )

    methods = {
        "baseline": {
            "entity": {"tp": 0, "fp": 0, "fn": 0},
            "relationship": {"tp": 0, "fp": 0, "fn": 0}
        },
        "engineered": {
            "entity": {"tp": 0, "fp": 0, "fn": 0},
            "relationship": {"tp": 0, "fp": 0, "fn": 0}
        }
    }

    document_files = sorted(
        documents_folder.glob("*.txt")
    )

    print("\nPROMPT COMPARISON")
    print("=================")

    for document_path in document_files:
        document_name = document_path.stem

        print(f"\nProcessing: {document_name}")

        text = load_text(document_path)

        actual = load_json(
            ground_truth_folder
            / f"{document_name}.json"
        )

        baseline = extract_baseline_knowledge(text)

        engineered = extract_knowledge(text)
        engineered = link_entities(engineered)
        engineered = normalize_relationships(engineered)

        predictions = {
            "baseline": baseline,
            "engineered": engineered
        }

        for method_name, prediction in predictions.items():
            results = evaluate_knowledge(
                prediction,
                actual
            )

            entity_metrics = results["entity_metrics"]

            relationship_metrics = results[
                "relationship_metrics"
            ]

            methods[method_name]["entity"]["tp"] += (
                entity_metrics["true_positives"]
            )

            methods[method_name]["entity"]["fp"] += (
                entity_metrics["false_positives"]
            )

            methods[method_name]["entity"]["fn"] += (
                entity_metrics["false_negatives"]
            )

            methods[method_name]["relationship"]["tp"] += (
                relationship_metrics["true_positives"]
            )

            methods[method_name]["relationship"]["fp"] += (
                relationship_metrics["false_positives"]
            )

            methods[method_name]["relationship"]["fn"] += (
                relationship_metrics["false_negatives"]
            )

    comparison_results = {}

    print("\nOVERALL COMPARISON")
    print("==================")

    for method_name, counts in methods.items():
        entity_metrics = calculate_overall(
            counts["entity"]
        )

        relationship_metrics = calculate_overall(
            counts["relationship"]
        )

        comparison_results[method_name] = {
            "entity_metrics": entity_metrics,
            "relationship_metrics": relationship_metrics
        }

        print(f"\n{method_name.upper()}")

        print(
            f"Entity F1: "
            f"{entity_metrics['f1_score']:.3f}"
        )

        print(
            f"Relationship F1: "
            f"{relationship_metrics['f1_score']:.3f}"
        )

    output_path = (
        project_root
        / "output"
        / "prompt_comparison_results.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            comparison_results,
            file,
            indent=4
        )

    print(
        f"\nComparison saved to: {output_path}"
    )


if __name__ == "__main__":
    main()
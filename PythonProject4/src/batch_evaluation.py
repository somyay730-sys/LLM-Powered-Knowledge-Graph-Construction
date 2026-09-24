import json
from pathlib import Path
from relationship_normalizer import normalize_relationships
from text_loader import load_text
from llm_extractor import extract_knowledge
from entity_linker import link_entities
from evaluator import evaluate_knowledge


def load_json(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def main():
    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

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

    document_files = sorted(
        documents_folder.glob("*.txt")
    )

    entity_tp = 0
    entity_fp = 0
    entity_fn = 0

    relation_tp = 0
    relation_fp = 0
    relation_fn = 0

    document_results = []

    print("\nBATCH EVALUATION")
    print("================")

    for document_path in document_files:
        document_name = document_path.stem

        print(
            f"\nProcessing: {document_name}"
        )

        text = load_text(document_path)

        knowledge = extract_knowledge(text)

        linked_knowledge = link_entities(
            knowledge
        )
        normalized_knowledge = normalize_relationships(
            linked_knowledge
        )
        ground_truth_path = (
            ground_truth_folder
            / f"{document_name}.json"
        )

        actual = load_json(
            ground_truth_path
        )

        results = evaluate_knowledge(
            normalized_knowledge,
            actual
        )
        entity_metrics = results[
            "entity_metrics"
        ]

        relationship_metrics = results[
            "relationship_metrics"
        ]

        entity_tp += entity_metrics[
            "true_positives"
        ]

        entity_fp += entity_metrics[
            "false_positives"
        ]

        entity_fn += entity_metrics[
            "false_negatives"
        ]

        relation_tp += relationship_metrics[
            "true_positives"
        ]

        relation_fp += relationship_metrics[
            "false_positives"
        ]

        relation_fn += relationship_metrics[
            "false_negatives"
        ]

        document_results.append(
            {
                "document": document_name,
                "entity_metrics": entity_metrics,
                "relationship_metrics": (
                    relationship_metrics
                )
            }
        )

        print(
            f"Entity F1: "
            f"{entity_metrics['f1_score']:.3f}"
        )

        print(
            f"Relationship F1: "
            f"{relationship_metrics['f1_score']:.3f}"
        )

    entity_precision = (
        entity_tp / (entity_tp + entity_fp)
        if entity_tp + entity_fp > 0
        else 0
    )

    entity_recall = (
        entity_tp / (entity_tp + entity_fn)
        if entity_tp + entity_fn > 0
        else 0
    )

    entity_f1 = (
        2 * entity_precision * entity_recall
        / (entity_precision + entity_recall)
        if entity_precision + entity_recall > 0
        else 0
    )

    relation_precision = (
        relation_tp
        / (relation_tp + relation_fp)
        if relation_tp + relation_fp > 0
        else 0
    )

    relation_recall = (
        relation_tp
        / (relation_tp + relation_fn)
        if relation_tp + relation_fn > 0
        else 0
    )

    relation_f1 = (
        2 * relation_precision * relation_recall
        / (
            relation_precision
            + relation_recall
        )
        if (
            relation_precision
            + relation_recall
        ) > 0
        else 0
    )

    overall_results = {
        "documents_evaluated": len(
            document_files
        ),
        "entity_metrics": {
            "true_positives": entity_tp,
            "false_positives": entity_fp,
            "false_negatives": entity_fn,
            "precision": entity_precision,
            "recall": entity_recall,
            "f1_score": entity_f1
        },
        "relationship_metrics": {
            "true_positives": relation_tp,
            "false_positives": relation_fp,
            "false_negatives": relation_fn,
            "precision": relation_precision,
            "recall": relation_recall,
            "f1_score": relation_f1
        },
        "document_results": document_results
    }

    print("\nOVERALL RESULTS")
    print("===============")

    print(
        f"\nDocuments evaluated: "
        f"{len(document_files)}"
    )

    print("\nENTITY EXTRACTION")
    print("-----------------")

    print(
        f"Precision: {entity_precision:.3f}"
    )

    print(
        f"Recall: {entity_recall:.3f}"
    )

    print(
        f"F1 Score: {entity_f1:.3f}"
    )

    print("\nRELATIONSHIP EXTRACTION")
    print("-----------------------")

    print(
        f"Precision: {relation_precision:.3f}"
    )

    print(
        f"Recall: {relation_recall:.3f}"
    )

    print(
        f"F1 Score: {relation_f1:.3f}"
    )

    output_path = (
        project_root
        / "output"
        / "batch_evaluation_results.json"
    )

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
            overall_results,
            file,
            indent=4
        )

    print(
        f"\nResults saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()
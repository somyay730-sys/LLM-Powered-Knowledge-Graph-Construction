import json
from pathlib import Path


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

    baseline_path = (
        project_root
        / "output"
        / "baseline_results.json"
    )

    engineered_path = (
        project_root
        / "output"
        / "engineered_results.json"
    )

    baseline = load_json(baseline_path)
    engineered = load_json(engineered_path)

    baseline_entity_f1 = (
        baseline["entity_metrics"]["f1_score"]
    )

    baseline_relation_f1 = (
        baseline["relationship_metrics"]["f1_score"]
    )

    engineered_entity_f1 = (
        engineered["entity_metrics"]["f1_score"]
    )

    engineered_relation_f1 = (
        engineered["relationship_metrics"]["f1_score"]
    )

    print("\nPROMPT ENGINEERING COMPARISON")
    print("=============================")

    print(
        f"\n{'Method':<25}"
        f"{'Entity F1':<15}"
        f"{'Relationship F1':<20}"
    )

    print("-" * 60)

    print(
        f"{'Baseline Prompt':<25}"
        f"{baseline_entity_f1:<15.3f}"
        f"{baseline_relation_f1:<20.3f}"
    )

    print(
        f"{'Engineered Prompt':<25}"
        f"{engineered_entity_f1:<15.3f}"
        f"{engineered_relation_f1:<20.3f}"
    )

    entity_improvement = (
        engineered_entity_f1
        - baseline_entity_f1
    )

    relation_improvement = (
        engineered_relation_f1
        - baseline_relation_f1
    )

    print("\nF1 SCORE CHANGE")
    print("---------------")

    print(
        f"Entity F1 change: "
        f"{entity_improvement:+.3f}"
    )

    print(
        f"Relationship F1 change: "
        f"{relation_improvement:+.3f}"
    )


if __name__ == "__main__":
    main()
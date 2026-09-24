import json
from pathlib import Path


def save_knowledge(knowledge, output_path):
    output_path = Path(output_path)

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
            knowledge,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Knowledge saved to: {output_path}"
    )
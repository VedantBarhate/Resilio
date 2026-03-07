import json
from pathlib import Path

# -------- CONFIG --------
PROJECT_NAME = "Resolio"
CREATED_BY = "@vedant_barhate powered by OpenAI"

PROMPT_FILES = {
    "reasoning": "prompts/reasoning.txt",
    "logical": "prompts/logical.txt",
    "classification": "prompts/classification.txt",
    "qna": "prompts/qna.txt"
}

OUTPUT_FILE = "ideal_prompts.json"
# ------------------------


def load_prompts(file_path, category):
    prompts = []
    with open(file_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            prompt = line.strip()
            if prompt:
                prompts.append({
                    "id": f"{category}_{idx}",
                    "category": category,
                    "prompt": prompt
                })
    return prompts


def main():
    all_prompts = []

    for category, path in PROMPT_FILES.items():
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")
        all_prompts.extend(load_prompts(file_path, category))

    data = {
        "metadata": {
            "project": PROJECT_NAME,
            "total_prompts": len(all_prompts),
            "categories": list(PROMPT_FILES.keys()),
            "created_by": CREATED_BY
        },
        "prompts": all_prompts
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"JSON file created successfully: {OUTPUT_FILE}")
    print(f"Total prompts: {len(all_prompts)}")


if __name__ == "__main__":
    main()

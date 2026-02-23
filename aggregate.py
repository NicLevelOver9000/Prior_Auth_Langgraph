import json
import os
from schemas.prior_auth_master_schema import PriorAuthMasterSchema
from llm.llm_client import LLMClient


# ----------------------------
# Deep Merge Utility
# ----------------------------
def deep_merge(master: dict, new_data: dict) -> dict:
    for key, value in new_data.items():

        # Skip null values
        if value is None:
            continue

        if isinstance(value, dict) and isinstance(master.get(key), dict):
            master[key] = deep_merge(master[key], value)
        else:
            master[key] = value

    return master


# ----------------------------
# LLM Lab Summary Generator
# ----------------------------
def generate_lab_summary(lab_results: dict) -> dict:
    if not lab_results:
        return {}

    llm = LLMClient()

    prompt = f"""
Interpret the following lab results and summarize key abnormalities.

Return ONLY valid JSON in this format:

{{
  "clinical_information": {{
    "lab_summary": "<summary>"
  }}
}}

Lab Results:
{json.dumps(lab_results)}
"""

    response = llm.chat([
        {"role": "system", "content": "You summarize medical lab findings."},
        {"role": "user", "content": prompt}
    ])

    return json.loads(response)


# ----------------------------
# Main Aggregation Logic
# ----------------------------
if __name__ == "__main__":

    print("Starting aggregation process...")

    master_dict = PriorAuthMasterSchema().model_dump()

    partial_files = [
        "output/form.json",
        "output/labs.json",
        "output/imaging.json",
        "output/notes.json",
    ]

    for file_path in partial_files:
        if os.path.exists(file_path):
            print(f"Merging: {file_path}")
            with open(file_path, "r") as f:
                partial_data = json.load(f)
                master_dict = deep_merge(master_dict, partial_data)
        else:
            print(f"Skipped (not found): {file_path}")

    # ----------------------------
    # Generate Lab Summary + Remove Raw Labs
    # ----------------------------
    lab_results = master_dict["clinical_information"].get("lab_results")

    if lab_results:
        print("Generating lab summary via LLM...")
        summary_json = generate_lab_summary(lab_results)
        master_dict = deep_merge(master_dict, summary_json)

        # Remove detailed structured labs from final output
        master_dict["clinical_information"].pop("lab_results", None)

    # ----------------------------
    # Validate Final Schema
    # ----------------------------
    final_object = PriorAuthMasterSchema(**master_dict)

    os.makedirs("output", exist_ok=True)

    with open("output/final_prior_auth.json", "w") as f:
        json.dump(final_object.model_dump(), f, indent=4)

    print("Final Prior Auth JSON created successfully.")

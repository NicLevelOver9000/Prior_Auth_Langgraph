import json
import os

from schemas.prior_auth_master_schema import PriorAuthMasterSchema
from llm.llm_client import LLMClient


# ----------------------------
# Deep Merge Utility
# ----------------------------
def deep_merge(master: dict, new_data: dict) -> dict:

    for key, value in new_data.items():

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
# Orchestrator Node
# ----------------------------
def orchestrator_node(state):

    print("\nStarting aggregation process...")
    print("STATE RECEIVED BY ORCHESTRATOR:")
    print(state)

    master_dict = PriorAuthMasterSchema().model_dump()

    partial_results = [
        state.get("form_data"),
        state.get("labs_data"),
        state.get("imaging_data"),
        state.get("notes_data")
    ]

    for partial in partial_results:

        if partial:
            print("Merging partial result...")
            master_dict = deep_merge(master_dict, partial)

    # ----------------------------
    # Generate Lab Summary
    # ----------------------------
    lab_results = master_dict["clinical_information"].get("lab_results")

    if lab_results:

        print("Generating lab summary via LLM...")

        summary_json = generate_lab_summary(lab_results)

        master_dict = deep_merge(master_dict, summary_json)

        master_dict["clinical_information"].pop("lab_results", None)

    # ----------------------------
    # Validate Schema
    # ----------------------------
    final_object = PriorAuthMasterSchema(**master_dict)

    os.makedirs("output", exist_ok=True)

    with open("output/final_prior_auth.json", "w") as f:
        json.dump(final_object.model_dump(), f, indent=4)

    print("Final Prior Auth JSON created successfully.")
    print("Final Prior Auth JSON: ", final_object.model_dump())

    return {"final_prior_auth": final_object.model_dump()}

import json
import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from datetime import datetime


from openai import AzureOpenAI
from llm.llm_client import LLMClient

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = "policies-index"

EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-01"
)


# ----------------------------
# EMBEDDING
# ----------------------------
def get_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model=EMBEDDING_DEPLOYMENT
    )
    return response.data[0].embedding


# ----------------------------
# HYBRID RETRIEVAL
# ----------------------------
def retrieve_policies(query):

    client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(SEARCH_KEY)
    )

    vector = get_embedding(query)

    results = client.search(
        search_text=query,  # keyword search
        vector_queries=[
            {
                "kind": "vector",
                "vector": vector,
                "k": 5,
                "fields": "content_vector"
            }
        ],
        top=5
    )

    policies = []

    for r in results:
        policies.append({
            "content": r["content"],
            "source": r["source"]
        })

    return policies


# ----------------------------
# BETTER QUERY BUILDER
# ----------------------------
def build_query(final_json):

    clinical = final_json.get("clinical_information", {})
    treatment = clinical.get("treatment_request", {})

    query = f"""
    Diagnosis: {clinical.get('diagnosis', '')}
    ICD: {clinical.get('icd_10_code', '')}
    Medication: {treatment.get('name_of_medication_or_procedure', '')}
    Symptoms: {clinical.get('symptom_severity_and_impact', '')}
    Prior Treatment: {clinical.get('prior_treatments_and_results', '')}
    """

    return query.strip()


# ----------------------------
# LLM EVALUATION (IMPROVED)
# ----------------------------
def evaluate_policy(final_json, policies):

    llm = LLMClient()

    prompt = f"""
You are a medical prior authorization decision engine.

STRICT RULES:
- Use ONLY the provided policy chunks
- Do NOT assume missing data
- If insufficient info → NEED_MORE_INFO

Return ONLY JSON:

{{
  "decision": "APPROVED / DENIED / NEED_MORE_INFO",
  "confidence": 0.0-1.0,
  "reason": "<clear explanation>",
  "policy_references": ["policy file names used"],
  "matched_policy_text": "<exact relevant snippet>"
}}

Patient Case:
{json.dumps(final_json)}

Policy Chunks:
{json.dumps(policies)}
"""

    response = llm.chat([
        {"role": "system", "content": "You are a strict healthcare policy evaluator."},
        {"role": "user", "content": prompt}
    ])

    return json.loads(response)


# ----------------------------
# RUN POLICY ENGINE
# ----------------------------
def run_policy_engine():

    with open("output/final_prior_auth_reject.json", "r") as f:
        final_json = json.load(f)

    # 🔥 Better query
    query = build_query(final_json)

    print("\nSEARCH QUERY:\n", query)

    policies = retrieve_policies(query)

    print(f"\nRetrieved {len(policies)} policy chunks\n")

    # 🔍 DEBUG: show retrieved chunks
    for i, p in enumerate(policies):
        print(f"\n--- POLICY {i+1} ({p['source']}) ---")
        print(p["content"][:200])

    decision = evaluate_policy(final_json, policies)

    print("\nFINAL DECISION:\n")
    print(json.dumps(decision, indent=2, ensure_ascii=False))
    filename = f"output/policy_decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    final_output = {
        "input": final_json,
        "retrieved_policies": policies,
        "decision": decision
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    return decision


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    run_policy_engine()

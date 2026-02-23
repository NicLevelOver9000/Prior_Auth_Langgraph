import json
from llm.llm_client import LLMClient


class NotesExtractor:

    def __init__(self):
        self.llm = LLMClient()

    def extract(self, text: str) -> dict:

        prompt = f"""
You are extracting clinical narrative information from a physician's notes
for a prior authorization case.

Extract the following fields if present:

- diagnosis
- icd_10_code
- prior_treatments_and_results
- symptom_severity_and_impact
- prognosis_and_risk_if_not_approved
- clinical_rationale_for_urgency

Return STRICT JSON in this format:

{{
  "clinical_information": {{
    "diagnosis": "...",
    "icd_10_code": "...",
    "prior_treatments_and_results": "...",
    "symptom_severity_and_impact": "...",
    "prognosis_and_risk_if_not_approved": "...",
    "clinical_rationale_for_urgency": "..."
  }}
}}

If a field is not present, return null for that field.

Document:
{text}
"""

        response = self.llm.chat([
            {"role": "system", "content": "You extract structured physician note data."},
            {"role": "user", "content": prompt}
        ])

        return json.loads(response)

import json
from llm.llm_client import LLMClient


class FormExtractor:

    def __init__(self):
        self.llm = LLMClient()

    def extract(self, text: str) -> dict:

        prompt = """
You are extracting structured demographic and provider information
from a prior authorization form.

Extract the following fields if present:

PATIENT INFORMATION:
- patient_name
- patient_date_of_birth
- patient_id
- patient_address
- patient_phone_number

PHYSICIAN INFORMATION:
- physician_name
- specialty
- physician_contact:
    - office_phone
    - fax
    - office_address

TREATMENT REQUEST (if present):
- name_of_medication_or_procedure
- code_of_medication_or_procedure
- dosage
- duration
- rationale
- presumed_eligibility

Return STRICT JSON in this exact structure:

{
  "patient_information": {
    "patient_name": "...",
    "patient_date_of_birth": "...",
    "patient_id": "...",
    "patient_address": "...",
    "patient_phone_number": "..."
  },
  "physician_information": {
    "physician_name": "...",
    "specialty": "...",
    "physician_contact": {
        "office_phone": "...",
        "fax": "...",
        "office_address": "..."
    }
  },
  "clinical_information": {
    "treatment_request": {
        "name_of_medication_or_procedure": "...",
        "code_of_medication_or_procedure": "...",
        "dosage": "...",
        "duration": "...",
        "rationale": "...",
        "presumed_eligibility": "..."
    }
  }
}

If any field is missing, return null for that field.
Do not return explanations.
Return only valid JSON.
"""

        full_prompt = prompt + "\n\nDocument:\n" + text

        response = self.llm.chat([
            {"role": "system",
                "content": "You extract structured prior authorization form data."},
            {"role": "user", "content": full_prompt}
        ])

        return json.loads(response)

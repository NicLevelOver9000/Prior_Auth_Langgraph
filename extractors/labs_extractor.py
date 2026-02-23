import json
from llm.llm_client import LLMClient


class LabsExtractor:

    def __init__(self):
        self.llm = LLMClient()

    def extract(self, text: str) -> dict:

        base_prompt = """
You are extracting structured laboratory results from a medical document.

Extract:
- CBC values
- CMP values
- ESR
- CRP
- Fecal markers
- Any abnormal lab values

Mark each result as:
- HIGH
- LOW
- NORMAL
- ABNORMAL

Return STRICT JSON in this format:

{
  "clinical_information": {
    "lab_results": {
      "CBC": {},
      "CMP": {},
      "ESR": {},
      "CRP": {},
      "Fecal_markers": {}
    }
  }
}

If no laboratory data is found, return:

{
  "clinical_information": {
    "lab_results": null
  }
}

Return only valid JSON.
"""

        full_prompt = base_prompt + "\n\nDocument:\n" + text

        response = self.llm.chat([
            {"role": "system", "content": "You extract structured laboratory findings."},
            {"role": "user", "content": full_prompt}
        ])

        return json.loads(response)

import json
from llm.llm_client import LLMClient


class ImagingExtractor:

    def __init__(self):
        self.llm = LLMClient()

    def extract(self, text: str) -> dict:

        base_prompt = """
You are extracting imaging and procedure findings from a medical document.

Imaging includes:
- CT scans
- MRI
- Ultrasound
- X-ray
- EGD
- Colonoscopy
- Endoscopy
- Radiology interpretations

Extract ONLY imaging/procedure findings.

Return STRICT JSON in this format:

{
  "clinical_information": {
    "imaging_results": "Clear structured summary of imaging findings"
  }
}

If no imaging findings are present, return:

{
  "clinical_information": {
    "imaging_results": null
  }
}

Return only valid JSON.
"""

        full_prompt = base_prompt + "\n\nDocument:\n" + text

        response = self.llm.chat([
            {"role": "system", "content": "You extract structured imaging findings."},
            {"role": "user", "content": full_prompt}
        ])

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "clinical_information": {
                    "imaging_results": None
                }
            }

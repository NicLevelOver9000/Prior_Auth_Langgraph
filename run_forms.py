import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.form_extractor import FormExtractor

if __name__ == "__main__":

    print("Running Patient Form Extractor...")

    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/form.pdf")

    extractor = FormExtractor()
    form_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/form.json", "w") as f:
        json.dump(form_data, f, indent=4)

    print("Form JSON saved.")

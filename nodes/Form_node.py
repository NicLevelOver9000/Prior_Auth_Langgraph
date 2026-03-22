
import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.form_extractor import FormExtractor


def form_node(state):
    print("Inside Form Node")
    print("Current State in Form Node: ", state)

    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/form.pdf")

    extractor = FormExtractor()
    form_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/form.json", "w") as f:
        json.dump(form_data, f, indent=4)

    print("Form node Output: ", form_data)

    return {"form_data": form_data}

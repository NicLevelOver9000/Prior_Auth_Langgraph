import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.labs_extractor import LabsExtractor


def labs_node(state):
    print("Inside Labs Node")
    print("Current State in Labs Node: ", state)

    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/labs.pdf")

    extractor = LabsExtractor()
    labs_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/labs.json", "w") as f:
        json.dump(labs_data, f, indent=4)

    print("Labs node Output: ", labs_data)

    return {"labs_data": labs_data}

import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.labs_extractor import LabsExtractor

if __name__ == "__main__":

    print("Running Labs Extractor...")

    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/labs.pdf")

    extractor = LabsExtractor()
    labs_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/labs.json", "w") as f:
        json.dump(labs_data, f, indent=4)

    print("Labs JSON saved.")

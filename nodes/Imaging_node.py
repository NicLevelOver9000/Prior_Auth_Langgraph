import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.imaging_extractor import ImagingExtractor


def imaging_node(state):
    print("Inside Imaging Node")
    print("Current State in Imaging Node: ", state)
    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/imaging.pdf")

    extractor = ImagingExtractor()
    imaging_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/imaging.json", "w") as f:
        json.dump(imaging_data, f, indent=4)

    print("Imaging node Output: ", imaging_data)

    return {"imaging_data": imaging_data}

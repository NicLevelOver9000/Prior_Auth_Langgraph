import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.labs_extractor import LabsExtractor


def labs_node(state):
    print("Inside Labs Node")
    print("Current State in Labs Node: ", state)

    file_path = "input_pdfs/labs.pdf"

    # ✅ Check if file exists
    if not os.path.exists(file_path):
        print("No labs.pdf found, skipping Labs Node...")

        return {"labs_data": None}

    try:
        ocr = AzureDocumentOCR()
        text = ocr.extract_text(file_path)

        extractor = LabsExtractor()
        labs_data = extractor.extract(text)

        os.makedirs("output", exist_ok=True)

        with open("output/labs.json", "w") as f:
            json.dump(labs_data, f, indent=4)

        print("Labs node Output: ", labs_data)

        return {"labs_data": labs_data}

    except Exception as e:
        print(f"Error in Labs Node: {e}")

        # ✅ Fail gracefully
        return {"labs_data": None}

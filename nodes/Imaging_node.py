import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.imaging_extractor import ImagingExtractor


def imaging_node(state):
    print("Inside Imaging Node")
    print("Current State in Imaging Node: ", state)

    file_path = "input_pdfs/imaging.pdf"

    # ✅ Check if file exists
    if not os.path.exists(file_path):
        print("No imaging.pdf found, skipping Imaging Node...")

        # Return empty structure (important for downstream consistency)
        return {"imaging_data": None}

    try:
        ocr = AzureDocumentOCR()
        text = ocr.extract_text(file_path)

        extractor = ImagingExtractor()
        imaging_data = extractor.extract(text)

        os.makedirs("output", exist_ok=True)

        with open("output/imaging.json", "w") as f:
            json.dump(imaging_data, f, indent=4)

        print("Imaging node Output: ", imaging_data)

        return {"imaging_data": imaging_data}

    except Exception as e:
        print(f"Error in Imaging Node: {e}")

        # Fail gracefully
        return {"imaging_data": None}

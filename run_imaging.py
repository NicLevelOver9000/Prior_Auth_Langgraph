import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.imaging_extractor import ImagingExtractor

if __name__ == "__main__":

    print("Running Imaging Extractor...")

    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/imaging.pdf")

    extractor = ImagingExtractor()
    imaging_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/imaging.json", "w") as f:
        json.dump(imaging_data, f, indent=4)

    print("Imaging JSON saved.")

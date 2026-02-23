import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.notes_extractor import NotesExtractor

if __name__ == "__main__":

    print("Running Doctor Notes Extractor...")

    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/doctor_notes.pdf")

    extractor = NotesExtractor()
    notes_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/notes.json", "w") as f:
        json.dump(notes_data, f, indent=4)

    print("Doctor Notes JSON saved.")

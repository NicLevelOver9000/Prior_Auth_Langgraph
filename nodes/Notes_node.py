import json
import os
from ocr.azure_document_ocr import AzureDocumentOCR
from extractors.notes_extractor import NotesExtractor


def notes_node(state):

    print("Inside Notes Node")
    print("Current State in Notes Node: ", state)

    ocr = AzureDocumentOCR()
    text = ocr.extract_text("input_pdfs/notes.pdf")

    extractor = NotesExtractor()
    notes_data = extractor.extract(text)

    os.makedirs("output", exist_ok=True)

    with open("output/notes.json", "w") as f:
        json.dump(notes_data, f, indent=4)

    print("Notes node Output: ", notes_data)

    return {"notes_data": notes_data}

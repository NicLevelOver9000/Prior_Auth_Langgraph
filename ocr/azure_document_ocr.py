import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()


class AzureDocumentOCR:

    def __init__(self):
        self.endpoint = os.getenv("AZURE_DOCINTEL_ENDPOINT")
        self.key = os.getenv("AZURE_DOCINTEL_KEY")

        self.client = DocumentAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

    def extract_text(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            poller = self.client.begin_analyze_document(
                "prebuilt-layout",
                f
            )
            result = poller.result()

        lines = []
        for page in result.pages:
            for line in page.lines:
                lines.append(line.content)

        return "\n".join(lines)

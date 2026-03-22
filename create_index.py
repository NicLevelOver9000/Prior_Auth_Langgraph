import os
import re
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

from openai import AzureOpenAI

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = "policies-index"

EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-01"
)


# ----------------------------
# PDF TEXT EXTRACTION
# ----------------------------
def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# ----------------------------
# CHUNKING
# ----------------------------
def chunk_text(text, chunk_size=1200, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

# ----------------------------
# EMBEDDING GENERATION
# ----------------------------


def get_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model=EMBEDDING_DEPLOYMENT
    )
    return response.data[0].embedding


# ----------------------------
# CREATE INDEX (ONLY IF NEEDED)
# ----------------------------
def create_index():

    index_client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT,
        credential=AzureKeyCredential(SEARCH_KEY)
    )

    existing_indexes = [idx.name for idx in index_client.list_indexes()]

    if INDEX_NAME in existing_indexes:
        print("Index already exists. Skipping creation.")
        return

    print("Creating new index...")

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),

        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchableField(name="source", type=SearchFieldDataType.String),

        SimpleField(name="chunk_id", type=SearchFieldDataType.String),

        # 🔥 VECTOR FIELD
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="vector-profile"
        )
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="hnsw-config")
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config"
            )
        ]
    )

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
        vector_search=vector_search
    )

    index_client.create_index(index)

    print("Index created successfully.")


# ----------------------------
# UPLOAD DOCUMENTS (UPSERT)
# ----------------------------
def upload_documents():

    client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(SEARCH_KEY)
    )

    docs = []

    for file in os.listdir("policies"):

        if file.endswith(".pdf"):

            print(f"Processing {file}...")

            file_path = os.path.join("policies", file)

            text = extract_pdf_text(file_path)
            chunks = chunk_text(text)

            safe_file = file.replace(".pdf", "")

            for i, chunk in enumerate(chunks):

                embedding = get_embedding(chunk)

                docs.append({
                    "id": f"{safe_file}_{i}",
                    "content": chunk,
                    "source": file,
                    "chunk_id": f"{safe_file}_{i}",
                    "content_vector": embedding
                })

    if docs:
        client.upload_documents(docs)
        print(f"Uploaded/Updated {len(docs)} chunks.")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    create_index()
    upload_documents()

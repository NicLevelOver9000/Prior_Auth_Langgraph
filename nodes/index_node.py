from create_index import create_index, upload_documents


def index_node(state):

    print("\nCreating index...")

    create_index()
    upload_documents()

    return {"index_ready": True}

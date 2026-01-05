import sys
import os
from qdrant_client.http import models

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qdrant_helper import QdrantHelper

def run_test():
    helper = QdrantHelper()
    
    # Using a specialized config for sparse indexing or reusing ingestion_config
    collection_name = "test_collection"
    data_path = os.path.join("data", "sparse_sample_data.json")

    if not helper.collection_exists(collection_name):
        print(f"Error: Collection '{collection_name}' does not exist.")
        return

    print(f"Loading sparse data from {data_path}...")
    data = helper.load_json_data(data_path)
    
    points = []
    for item in data:
        points.append(models.PointStruct(
            id=item["id"],
            vector={
                "sparse-text": models.SparseVector(
                    indices=item["sparse_vector"]["indices"],
                    values=item["sparse_vector"]["values"]
                )
            },
            payload=item["payload"]
        ))

    print(f"Indexing {len(points)} sparse points into '{collection_name}'...")
    helper.client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("Sparse indexing complete.")

if __name__ == "__main__":
    run_test()

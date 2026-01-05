import sys
import os
import json
from qdrant_client.http import models

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qdrant_helper import QdrantHelper

def index_benchmark_data():
    helper = QdrantHelper()
    collection_name = "test_collection"
    data_path = "data/benchmark_data.json"

    if not os.path.exists(data_path):
        print("Benchmark data not found. Run generate_data.py first.")
        return

    with open(data_path, 'r') as f:
        data = json.load(f)

    points = []
    for item in data:
        points.append(models.PointStruct(
            id=item["id"],
            vector={
                "": item["vector"],  # Default dense vector
                "sparse-text": models.SparseVector(
                    indices=item["sparse_vector"]["indices"],
                    values=item["sparse_vector"]["values"]
                )
            },
            payload=item["payload"]
        ))

    print(f"Indexing {len(points)} benchmark records...")
    helper.client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("Benchmark data indexed.")

if __name__ == "__main__":
    index_benchmark_data()

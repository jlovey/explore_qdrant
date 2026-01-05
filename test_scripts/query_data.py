import sys
import os
from qdrant_client.http import models

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qdrant_helper import QdrantHelper

def run_test():
    helper = QdrantHelper()
    config_path = os.path.join("configs", "query_config.json")
    
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    config = helper.load_config(config_path)
    collection_name = config.get("collection_name")
    queries = config.get("queries", [])

    if not helper.collection_exists(collection_name):
        print(f"Error: Collection '{collection_name}' does not exist.")
        return

    for q in queries:
        print(f"\n--- Running query: {q['name']} ---")
        
        if "sparse_vector" in q:
            response = helper.client.query_points(
                collection_name=collection_name,
                query=models.SparseVector(
                    indices=q["sparse_vector"]["vector"]["indices"],
                    values=q["sparse_vector"]["vector"]["values"]
                ),
                using=q["sparse_vector"]["name"],
                limit=q.get("limit", 5),
                query_filter=models.Filter(**q["filter"]) if "filter" in q else None
            )
        else:
            response = helper.client.query_points(
                collection_name=collection_name,
                query=q["vector"],
                limit=q.get("limit", 5),
                query_filter=models.Filter(**q["filter"]) if "filter" in q else None
            )
        
        for hit in response.points:
            print(f"ID: {hit.id}, Score: {hit.score}, Payload: {hit.payload}")

if __name__ == "__main__":
    run_test()

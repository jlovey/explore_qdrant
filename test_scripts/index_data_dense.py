import sys
import os
from qdrant_client.http import models

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qdrant_helper import QdrantHelper

def run_test():
    helper = QdrantHelper()
    config_path = os.path.join("configs", "ingestion_config.json")
    
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    config = helper.load_config(config_path)
    collection_name = config.get("collection_name")
    data_path = config.get("data_path")

    if not helper.collection_exists(collection_name):
        print(f"Error: Collection '{collection_name}' does not exist. Please create it first.")
        return

    print(f"Loading data from {data_path}...")
    data = helper.load_json_data(data_path)
    
    points = []
    for item in data:
        points.append(models.PointStruct(
            id=item["id"],
            vector=item["vector"],
            payload=item["payload"]
        ))

    print(f"Indexing {len(points)} points into '{collection_name}'...")
    helper.client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("Indexing complete.")

if __name__ == "__main__":
    run_test()

import sys
import os

# Add the project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qdrant_helper import QdrantHelper

def run_test():
    helper = QdrantHelper()
    config_path = os.path.join("configs", "collection_config.json")
    
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    config = helper.load_config(config_path)
    collection_name = config.get("collection_name")
    vector_config = config.get("vector_config")
    sparse_config = config.get("sparse_config")

    print(f"Attempting to create collection: {collection_name}...")
    result = helper.create_collection(collection_name, vector_config, sparse_config)
    print(result)

if __name__ == "__main__":
    run_test()

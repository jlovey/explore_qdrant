import sys
import os
import json
import numpy as np

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qdrant_helper import QdrantHelper
from utils.metrics_helper import calculate_precision_at_k, calculate_recall_at_k, calculate_ndcg_at_k
from qdrant_client.http import models

def run_accuracy_test():
    helper = QdrantHelper()
    collection_name = "test_collection"
    
    if not helper.collection_exists(collection_name):
        print(f"Collection {collection_name} does not exist.")
        return

    # In a real scenario, ground truth comes from manual labeling or exhaustive linear search
    # For this test, we'll assume the 'top results' from a very high-limit dense search are our "relevant" items
    # to compare how sparse or hybrid search performs against it.
    
    test_vector = [0.1, 0.2, 0.3, 0.4]
    k = 5
    
    print(f"Running Accuracy Evaluation (K={k})...")

    # 1. Get "Ground Truth" (using standard dense search with higher limit)
    # We'll assume the top 10 from dense search are the absolute "relevant" ones for this query
    gt_response = helper.client.query_points(
        collection_name=collection_name,
        query=test_vector,
        limit=10
    )
    ground_truth_ids = [hit.id for hit in gt_response.points]
    
    # 2. Test Sparse Search (Representing BM25-like behavior)
    sparse_query = {"indices": [1, 10], "values": [0.5, 0.5]}
    sparse_response = helper.client.query_points(
        collection_name=collection_name,
        query=models.SparseVector(**sparse_query),
        using="sparse-text",
        limit=k
    )
    sparse_ids = [hit.id for hit in sparse_response.points]
    
    # 3. Test Dense Search
    dense_response = helper.client.query_points(
        collection_name=collection_name,
        query=test_vector,
        limit=k
    )
    dense_ids = [hit.id for hit in dense_response.points]

    # Metrics Calculation
    results = {
        "Dense": {
            "Precision@K": calculate_precision_at_k(dense_ids, ground_truth_ids, k),
            "Recall@K": calculate_recall_at_k(dense_ids, ground_truth_ids, k),
            "NDCG@K": calculate_ndcg_at_k(dense_ids, ground_truth_ids, k)
        },
        "Sparse (BM25-like)": {
            "Precision@K": calculate_precision_at_k(sparse_ids, ground_truth_ids, k),
            "Recall@K": calculate_recall_at_k(sparse_ids, ground_truth_ids, k),
            "NDCG@K": calculate_ndcg_at_k(sparse_ids, ground_truth_ids, k)
        }
    }

    print("\n--- Algorithm Accuracy Comparison ---")
    for method, metrics in results.items():
        print(f"\nMethod: {method}")
        for metric_name, value in metrics.items():
            print(f"  {metric_name}: {value:.4f}")

if __name__ == "__main__":
    run_accuracy_test()

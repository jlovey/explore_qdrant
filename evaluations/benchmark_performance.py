import sys
import os
import time
import json
import numpy as np

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qdrant_helper import QdrantHelper

def run_performance_test():
    helper = QdrantHelper()
    collection_name = "test_collection"
    
    if not helper.collection_exists(collection_name):
        print(f"Collection {collection_name} does not exist.")
        return

    # Prepare random queries
    num_queries = 50
    vector_size = 4
    queries = [np.random.rand(vector_size).tolist() for _ in range(num_queries)]
    
    print(f"Starting latency benchmark with {num_queries} queries...")
    
    latencies = []
    for q_vec in queries:
        start_time = time.perf_counter()
        helper.client.query_points(
            collection_name=collection_name,
            query=q_vec,
            limit=10
        )
        end_time = time.perf_counter()
        latencies.append((end_time - start_time) * 1000)  # ms

    avg_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)
    p99_latency = np.percentile(latencies, 99)
    throughput = num_queries / (sum(latencies) / 1000)

    print("\n--- Performance Results ---")
    print(f"Average Latency: {avg_latency:.2f} ms")
    print(f"P95 Latency:     {p95_latency:.2f} ms")
    print(f"P99 Latency:     {p99_latency:.2f} ms")
    print(f"Throughput:      {throughput:.2f} queries/sec")

if __name__ == "__main__":
    run_performance_test()

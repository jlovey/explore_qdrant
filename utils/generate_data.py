import json
import random
import numpy as np

def generate_synthetic_data(num_records=100, vector_size=4):
    data = []
    for i in range(num_records):
        vector = [round(random.uniform(0, 1), 4) for _ in range(vector_size)]
        sparse_indices = random.sample(range(100), 10)
        sparse_values = [round(random.uniform(0, 1), 4) for _ in range(10)]
        
        record = {
            "id": i + 1000,
            "vector": vector,
            "sparse_vector": {"indices": sparse_indices, "values": sparse_values},
            "payload": {
                "city": random.choice(["Berlin", "London", "Moscow", "New York", "Tokyo"]),
                "category": random.choice(["electronics", "books", "fashion"]),
                "price": random.randint(10, 2000),
                "rank": random.randint(1, 100)
            }
        }
        data.append(record)
    
    with open("data/benchmark_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print(f"Generated {num_records} synthetic records in data/benchmark_data.json")

if __name__ == "__main__":
    generate_synthetic_data(200)

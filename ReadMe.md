# Explore Qdrant

This project provides a structured way to interact with Qdrant Vector DB locally using Docker.

## Setup

1. **Start Qdrant**:
   ```bash
   docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `configs/`: Contains JSON configuration files for collection creation, indexing, and querying.
- `utils/`: Helper scripts for Qdrant client initialization and data processing.
- `test_scripts/`: Python scripts to perform various operations like creation, ingestion, and search.
- `data/`: Sample JSON data files for indexing.

## Usage

### 1. Create Collection
Creates a collection named `test_collection` with both dense and sparse vector support.
```bash
python3 test_scripts/create_collection.py
```

### 2. Index Dense Data
Indexes sample records with 4-dimensional dense vectors.
```bash
python3 test_scripts/index_data_dense.py
```

### 3. Index Sparse Data
Indexes sample records using named sparse vectors (`sparse-text`).
```bash
python3 test_scripts/index_data_sparse.py
```

### 4. Query Data
Performs multiple searches including:
- **Basic Dense Search**: Simple vector similarity.
- **Filter Search**: Matches specific categories.
- **Range Filter Search**: Filters by numerical ranges.
- **Sparse Search**: Search using named sparse indices.
```bash
source .venv/bin/activate
python3 test_scripts/query_data.py
```

## Evaluations & Benchmarking

The `evaluations/` folder contains scripts to measure performance and accuracy.

### 1. Generate & Index Benchmark Data
Creates 200 synthetic records with dense and sparse vectors and indexes them.
```bash
source .venv/bin/activate
python3 utils/generate_data.py
python3 evaluations/index_benchmark_data.py
```

### 2. Performance Benchmark
Measures Average Latency, P95/P99, and Throughput.
```bash
python3 evaluations/benchmark_performance.py
```

### 3. Accuracy Benchmark
Calculates metrics against a dense-search ground truth:
- **Precision@K**
- **Recall@K**
- **NDCG@K**
- **BM25 Comparison**: Sparse vectors are used to simulate BM25 retrieval behavior.
```bash
python3 evaluations/benchmark_accuracy.py
```

## Setup (Venv)
This project uses a dedicated virtual environment.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# MetricSQL

A prototype SQL-like retrieval engine exploring **metric-space indexing** vs **embedding-based retrieval** using **Generalized Hyperplane Trees (GHTs)**.

The project combines:

- Context-free grammar based query parsing
- Abstract Syntax Tree (AST) generation
- Semantic similarity search
- Metric-space Approximate Nearest Neighbor (ANN) indexing
- C++ acceleration using PyBind11

---

# Features

- SQL-like custom query language
- CFG parser using Lark
- AST-based query execution
- Semantic search using sentence embeddings
- Custom Generalized Hyperplane Tree implementation in C++
- Metric-space retrieval using edit distance
- DNA sequence similarity experiments
- Embedding vs metric retrieval benchmarking

---

# Project Structure

```text
metricSQL/
│
├── engine/
├── parser/
├── storage/
├── similarity/
│   ├── cpp/
│   │   ├── ght.cpp
│   │   ├── metric_ght.cpp
│   │   ├── bindings.cpp
│   │   ├── metric_bindings.cpp
│   │   └── setup.py
│   │
│   ├── embeddings.py
│   └── semantic_search.py
│
├── experiments/
│   ├── dna_dataset.py
│   ├── benchmark_dna.py
│   └── test_metric_ght.py
│
├── main.py
└── requirements.txt
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/saranshikens/metricSQL.git

cd metricSQL
```

---

## 2. Create Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

.\venv\Scripts\Activate.ps1
```

### Linux / WSL

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Building the C++ Extensions

The project uses:
- C++
- PyBind11
- Python extension modules

Go to:

```bash
cd similarity/cpp
```

Build extensions:

```bash
python setup.py build_ext --inplace
```

If successful, you should see:

### Windows

```text
ght_cpp.cp310-win_amd64.pyd
metric_ght_cpp.cp310-win_amd64.pyd
```

### Linux

```text
ght_cpp.so
metric_ght_cpp.so
```

---

# Running the Main SQL Prototype

From project root:

```bash
python main.py
```

---

# Example Custom Query

Example SQL-like query:

```sql
SELECT title
FROM papers
WHERE year = "2024"
SIMILAR TO "graph neural networks"
TOP 5
```

The parser:
1. Parses the query using a CFG
2. Builds an AST
3. Executes semantic retrieval

---

# How the Parser Works

The query system is implemented using:

- Context-Free Grammar (CFG)
- Abstract Syntax Trees (ASTs)

Grammar rules are defined in:

```text
parser/grammar.lark
```

The parser converts queries into AST nodes which are later executed by the engine.

---

# Testing the Metric GHT

## Run Simple GHT Test

From project root:

```bash
python experiments/test_metric_ght.py
```

This:
- builds the metric-space GHT,
- indexes DNA sequences,
- performs nearest-neighbor retrieval using edit distance.

---

# Running the Benchmark

Run:

```bash
python experiments/benchmark_dna.py
```

This compares:

1. Embedding-based retrieval
2. Exact metric retrieval
3. GHT-based ANN retrieval

using DNA sequences.

---

# Benchmark Results

## Query Sequence

```text
AACGGGTGCAAAACCTATAACAGTACACCCCATGGCGGTAGACACCCATAAAACCCCGTC
```

---

## Embedding Baseline

### Search Time

```text
8.144623s
```

### Recall@5

```text
0.20
```

---

## Exact Metric Search

### Search Time

```text
0.004007s
```

### Recall@5

```text
1.00
```

(ground truth)

---

## GHT Metric Search

### Build Time

```text
0.830492s
```

### Search Time

```text
0.000000s
```

### Recall@5

```text
0.20
```

---

# Discussion

## 1. Embedding-Based Retrieval Performs Poorly

The embedding model was trained for natural language semantics, not biological sequence similarity.

As a result:
- semantically meaningless embeddings are produced,
- structural similarity is not preserved well,
- retrieval quality is poor.

This is reflected in:

```text
Recall@5 = 0.20
```

---

## 2. Exact Metric Retrieval Is Strong

Using edit distance directly preserves the intrinsic geometry of DNA sequences.

This gives:
- exact nearest neighbors,
- highly meaningful structural retrieval,
- very fast search for small datasets.

This acts as the ground-truth baseline.

---

## 3. GHT Enables Metric-Space ANN Retrieval

The Generalized Hyperplane Tree indexes the data directly in metric space.

Unlike embedding approaches:
- no vector embedding is required,
- no Euclidean projection is needed,
- retrieval works directly on edit distance.

This demonstrates:
- metric-space indexing,
- ANN retrieval over non-Euclidean data,
- direct retrieval using intrinsic metrics.

---

## 4. Current GHT Limitations

The current implementation is intentionally simple.

Limitations:
- naive pivot selection,
- weak pruning,
- small dataset size,
- low Recall@5.

Future improvements could include:
- triangle-inequality pruning,
- better pivot selection,
- larger datasets,
- comparison with VP-Trees / BK-Trees.

---

# Technologies Used

- Python
- C++
- PyBind11
- Lark
- SentenceTransformers
- scikit-learn
- NumPy

---

# Research Motivation

Traditional semantic retrieval pipelines typically:
1. convert data into vector embeddings,
2. perform retrieval in Euclidean or cosine spaces.

However, many real-world domains are naturally:
- non-Euclidean,
- non-vectorial,
- intrinsically metric-space structured.

Examples:
- DNA sequences
- trajectories
- edit-distance retrieval
- graph similarity
- tree similarity

This project explores whether:
- direct metric-space indexing
can preserve structure better than:
- embedding-based approximations.

---

# Future Work

- Better GHT pruning
- Generic metric interfaces
- Larger-scale datasets
- Distance computation counting
- Dynamic Time Warping experiments
- VP-Trees / BK-Trees comparison
- Hybrid embedding + metric retrieval

# Resource-Efficient Hierarchical Multi-Agent Workflows

![Status](https://img.shields.io/badge/Status-Research_Prototype-blue)
![Hardware](https://img.shields.io/badge/Hardware-RTX_3060_(6GB)-green)
![Models](https://img.shields.io/badge/Models-Llama_3.2-orange)

> **Research implementation for the paper: "Resource-Efficient Hierarchical Multi-Agent Workflows via Graph-Based State Management on Consumer Hardware"**

## 📄 Abstract
This repository contains the experimental code and data for optimizing **Hierarchical Multi-Agent Systems (MAS)** on resource-constrained edge devices.

Inspired by the **AGENTiGraph framework (Zhao et al., 2025)** and **Zero-Shot Reasoners (Kojima et al., 2022)**, this project implements a "Manager-Worker" architecture that decouples agent memory from linear conversation history. By using a **Graph-Based State Management (GBSM)** system, we significantly reduce VRAM usage and token processing load, enabling complex agentic workflows on consumer hardware (NVIDIA RTX 3060).

**[📄 Read the Full Research Paper (PDF)](./Research_Paper.pdf)**

---

## 🚀 Key Results
We compared a standard **Linear History** workflow against our **Graph-Based (Context Pruned)** workflow on a local NVIDIA RTX 3060.

| Metric | Linear Baseline | Graph-Based (Ours) | Improvement |
| :--- | :--- | :--- | :--- |
| **Latency** | 150.08s | **88.38s** | **+41.1% Speedup** |
| **Total Tokens** | 3,669 | **2,422** | **33.9% Reduction** |
| **Worker Context** | 1,494 tokens | 676 tokens | **Reduced VRAM Footprint** |

*Data verified on: NVIDIA RTX 3060 (6GB VRAM), Intel i5-11400H, Ollama v0.5.4*

---

## 🛠️ System Architecture
The system consists of two quantized agents running locally via Ollama:
1.  **Manager Agent (`llama3.2:3b`)**: Performs high-level reasoning and decomposes tasks into a graph structure.
2.  **Worker Agent (`llama3.2:1b`)**: Queries specific nodes of the graph to execute sub-tasks without loading the full conversation history.

---

## 💻 Installation & Usage

### Prerequisites
1.  **Ollama**: Ensure Ollama is installed and running (`ollama serve`).
2.  **Python 3.8+**

### Setup
# Clone the repository
git clone [https://github.com/YourUsername/Hierarchical-Agent-Graph-3060.git](https://github.com/YourUsername/Hierarchical-Agent-Graph-3060.git)
cd Hierarchical-Agent-Graph-3060

# Install dependencies
pip install requests

# Pull the required quantized models
ollama pull llama3.2
ollama pull llama3.2:1b
Running the Experiment
To reproduce the results from the paper, run the comparison script:

Bash

python experiment.py
This will run both the Baseline and Proposed workflows and output a comparison table to the console.

📚 References
This work builds upon the following foundational research:

AGENTiGraph: Zhao, X. et al. (2025). AGENTiGraph: A Multi-Agent Knowledge Graph Framework for Interactive, Domain-Specific LLM Chatbots. CIKM 2025.

Zero-Shot Reasoners: Kojima, T. et al. (2022). Large Language Models are Zero-Shot Reasoners. NeurIPS 2022.

👤 Author
Soham Shelke
soham3105@gmail.com
Department of Computer Engineering, Savitribai Phule Pune University (SPPU)

Contact: soham3105@gmail.com

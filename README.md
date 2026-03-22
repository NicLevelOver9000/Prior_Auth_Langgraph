# Prior Authorization Pipeline

AI-powered prior authorization document extraction and decisioning system built using a modular LangGraph workflow.

---

## 🚀 Features

- LangGraph-based orchestration pipeline  
- Modular nodes for Forms, Labs, Imaging, and Clinical Notes  
- Azure Document Intelligence OCR integration  
- LLM-powered clinical summarization  
- Policy engine for prior authorization decisioning  
- Deep merge aggregation of extracted data  
- Pydantic schema validation for structured outputs  
- Standardized final decision output (Approved / Rejected)  

---

## 🏗️ Architecture Overview

- **Node-based design**: Each document type is processed independently via dedicated nodes  
- **Orchestrator node**: Manages execution flow across all nodes using LangGraph  
- **Extractor layer**: Updated to align with node-based processing  
- **Aggregation layer**: Combines outputs into a unified structure  
- **Policy engine**: Evaluates aggregated data against defined policies  
- **Final output**: Generates structured prior authorization decision  

---

## ⚙️ Setup

1. Create a virtual environment  
2. Install dependencies  
3. Configure Azure credentials in `.env`  
4. Create policy index:
   ```bash
   python create_index.py
5. Run the pipeline:
   ```bash
   python main.py
6. Generate final decision: 
   ```bash
   python policy_engine.py

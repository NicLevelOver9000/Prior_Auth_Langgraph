Prior Authorization Pipeline

AI-powered prior authorization document extraction and decisioning system built using a modular LangGraph workflow.

🚀 Features
LangGraph-based orchestration pipeline
Modular nodes for Forms, Labs, Imaging, and Clinical Notes
Azure Document Intelligence OCR integration
LLM-powered clinical summarization
Policy engine for prior authorization decisioning
Deep merge aggregation of extracted data
Pydantic schema validation for structured outputs
Standardized final decision output (Approved / Rejected)

🏗️ Architecture Overview
Node-based design: Each document type is processed independently via dedicated nodes
Orchestrator node: Manages execution flow across all nodes using LangGraph
Extractor layer: Updated to align with node-based processing
Aggregation layer: Combines outputs into a unified structure
Policy engine: Evaluates aggregated data against defined policies
Final output: Generates structured prior authorization decision

⚙️ Setup
Create a virtual environment
Install dependencies
Configure Azure credentials in .env
Create an index of your policies via create_index.py
Run the pipeline via orchestrator
Run policy_engine.py to generate final output in /output

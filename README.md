<!--
README.md - SYNTHETIC ITSM INCIDENT DATA ENGINE v2.0 (Updated May 30, 2025)
-->
# Synthetic ITSM Incident Data Engine v2.0

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/License-Capgemini_Internal-red)](https://capgemini.com)

A production-grade synthetic ServiceNow incident data generator powered by Azure OpenAI, designed for enterprise-scale LLM training, ServiceNow integration testing, and ITSM analytics.

> **v2.0 Production Release (May 2025):**
>
> - `golden_incident_generator_v2.py` is the primary generator for all ad-hoc and batch use cases.
> - `production_batch_generator.py` is the robust, checkpointed, monitored batch orchestrator for large-scale production runs.
> - All configuration is centralized in `enhanced_incident_config.json` and `.env` (Azure OpenAI credentials).

---

## 🎯 Project Purpose

- Generate high-quality, realistic ServiceNow/ITSM incident data for:
  - **LLM fine-tuning** (Azure OpenAI, GADM Work Assistant, etc.)
  - **AI/ML model training**
  - **ServiceNow integration and workflow testing**
  - **ITSM staff training and scenario simulation**

## 🚀 Key Features

- **Azure OpenAI integration** (managed identity, robust error handling)
- **Advanced prompt engineering** (business context, trending issues, personas)
- **Config-driven, extensible architecture**
- **Production-grade logging, monitoring, and checkpointing**
- **Batch processing with progress tracking and recovery**
- **Multi-format export** (CSV, JSON, Excel)
- **Comprehensive metadata and analytics**

## 📁 Project Structure

```text
synthetic_data_engine_2.0/
├── README.md
├── requirements.txt
├── .env / .example.env
├── golden_incident_generator_v2.py         # Main generator (ad-hoc & batch)
├── production_batch_generator.py           # Production batch orchestrator
├── enhanced_incident_prompt_template.py    # Prompt engineering
├── enhanced_incident_config.json           # Central config
├── docs/
│   ├── COMPREHENSIVE_USER_GUIDE.md        # User guide (detailed)
│   └── ENGINEERING_GUIDE.md               # Engineering/architecture guide
├── tests/
│   ├── test_golden_generator_v2.py        # Modern test suite
│   └── test_generator.py                  # Legacy tests (deprecated)
├── logs/                                  # Log files
└── synthetic_data_output/                  # Output files (CSV, JSON, Excel)
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Azure OpenAI service access
- Valid Azure subscription

### 1. Environment Setup

```powershell
cd synthetic_data_engine_2.0
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .example.env .env
```

### 2. Configure Azure OpenAI

Edit `.env` with your Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

### 3. Verify Installation

```powershell
python test_golden_generator_v2.py
```

---

## 🎮 Quick Start

### Python API (ad-hoc or batch)

```python
from golden_incident_generator_v2 import GoldenIncidentGeneratorV2

generator = GoldenIncidentGeneratorV2()
incidents = generator.generate_batch(count=10)
generator.export_to_csv("incidents.csv")
generator.export_to_json("incidents.json")
generator.export_to_excel("incidents.xlsx")
generator.print_generation_summary()
```

### CLI (ad-hoc)

```powershell
python golden_incident_generator_v2.py --count 25 --export all
```

### Production Batch (robust, checkpointed)

```powershell
python production_batch_generator.py --target 1000 --batch-size 10 --max-memory 16000
```

---

## ⚙️ Configuration

- All settings are in `enhanced_incident_config.json` (categories, domains, personas, priorities, etc.)
- LLM and Azure credentials are in `.env`
- See `docs/COMPREHENSIVE_USER_GUIDE.md` for full config schema and examples

---

## 📊 Output Formats

- **CSV**: Excel/Power BI ready, with/without metadata
- **JSON**: API-ready, includes metadata and metrics
- **Excel**: Multi-sheet (incidents, metrics, analytics)
- All exports go to `synthetic_data_output/`

---

## 🏭 Production Batch vs. Ad-hoc Generation

| Use Case                | Script                          | Features                                                      |
|------------------------|----------------------------------|---------------------------------------------------------------|
| Ad-hoc/small batch     | golden_incident_generator_v2.py  | Fast, interactive, flexible, all export formats               |
| Production/large batch | production_batch_generator.py    | Checkpointing, monitoring, resource mgmt, recovery, analytics |

---

## 🧪 Testing & Validation

```powershell
python test_golden_generator_v2.py
```

- See `tests/` for test coverage and examples
- Manual review: generate a small batch, check output, scale up

---

## 🔧 Troubleshooting

- **Import errors**: `pip install -r requirements.txt`
- **Azure OpenAI errors**: Check `.env` and deployment names
- **Memory issues**: Use smaller batch size or increase `--max-memory`
- **Config errors**: Validate `enhanced_incident_config.json` (see user guide)
- **Export errors**: Ensure `synthetic_data_output/` exists and is writable

---

## 📈 Scaling & Performance

- Use `production_batch_generator.py` for 1000+ incidents
- Monitor logs in `logs/` for progress and errors
- Tune batch size and memory for your environment
- All exports are chunked for large runs

---

## 🤝 Contributing

- Extend categories, prompts, or personas in config/template files
- Add new tests in `tests/`
- See `docs/ENGINEERING_GUIDE.md` for architecture and API details

---

## 📋 Roadmap

- v2.1: Multi-language, ServiceNow API validation, analytics
- v3.0: Real-time streaming, ML-based quality, multi-tenant support

---

## 🆘 Support

- See `docs/COMPREHENSIVE_USER_GUIDE.md` for full user guide
- Contact: Hans Havlik (Capgemini)
- Azure OpenAI docs: <https://docs.microsoft.com/azure/cognitive-services/openai/>

---

*Generated with 💙 by Synthetic ITSM Data Engine v2.0*
*Powered by Azure OpenAI and advanced prompt engineering*

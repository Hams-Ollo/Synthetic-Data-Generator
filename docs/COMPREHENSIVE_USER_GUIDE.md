<!--
COMPREHENSIVE_USER_GUIDE.md - SYNTHETIC ITSM INCIDENT DATA ENGINE v2.0 (Updated May 30, 2025)
-->
# 🚀 Synthetic ITSM Incident Data Engine v2.0 - Comprehensive User Guide

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green)](https://python.langchain.com/)

**Author:** Hans Havlik  
**Organization:** Capgemini  
**Version:** 2.0.0  
**Date:** May 30, 2025  
**Application:** GADM Work Assistant v1.1.4

---

## 📋 Table of Contents

1. [Overview & Purpose](#overview--purpose)
2. [Architecture Overview](#architecture-overview)
3. [Quick Start Guide](#quick-start-guide)
4. [Configuration Management](#configuration-management)
5. [Data Generation Workflows](#data-generation-workflows)
6. [Customization Guide](#customization-guide)
7. [Export Formats & Output](#export-formats--output)
8. [Monitoring & Analytics](#monitoring--analytics)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)
11. [Support & Resources](#support--resources)

---

## 🎯 Overview & Purpose

The Synthetic ITSM Incident Data Engine v2.0 is a production-ready tool for generating high-quality, realistic ServiceNow incident data for:

- LLM fine-tuning (Azure OpenAI, GADM Work Assistant, etc.)
- AI/ML model training
- ServiceNow integration and workflow testing
- ITSM staff training and scenario simulation

**Key Features:**

- Azure OpenAI integration (managed identity, robust error handling)
- Advanced prompt engineering (business context, trending issues, personas)
- Config-driven, extensible architecture
- Production-grade logging, monitoring, and checkpointing
- Batch processing with progress tracking and recovery
- Multi-format export (CSV, JSON, Excel)
- Comprehensive metadata and analytics

---

## 🏗️ Architecture Overview

### System Architecture Diagram

```curl
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SYNTHETIC ITSM DATA ENGINE v2.0                        │
│                            Architecture Overview                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │  Configuration  │    │ Azure OpenAI    │
│                 │    │                 │    │                 │
│ • CLI Commands  │    │ • JSON Config   │    │ • GPT-4o-mini   │
│ • Python API    │    │ • Environment   │    │ • Temperature   │
│ • Batch Scripts │    │ • Domains       │    │ • Max Tokens    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │          GOLDEN INCIDENT GENERATOR v2.0                 │
        │                                                         │
        │  ┌─────────────────┐  ┌─────────────────┐               │
        │  │ Incident Context│  │ Prompt Engine   │               │
        │  │ Generator       │  │                 │               │
        │  │                 │  │ • System Prompt │               │
        │  │ • Category      │  │ • User Prompt   │               │
        │  │ • Priority      │  │ • Category Rules│               │
        │  │ • Department    │  │ • Domain Context│               │
        │  │ • User Persona  │  └─────────────────┘               │
        │  └─────────────────┘                                    │
        │                                                         │
        │  ┌─────────────────┐  ┌─────────────────┐               │
        │  │ LLM Response    │  │ Data Processing │               │
        │  │ Parser          │  │                 │               │
        │  │                 │  │ • Validation    │               │
        │  │ • JSON Extract  │  │ • Enhancement   │               │
        │  │ • Validation    │  │ • Timestamps    │               │
        │  │ • Error Handle  │  │ • Formatting    │               │
        │  └─────────────────┘  └─────────────────┘               │
        └─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │              INCIDENT RECORD CREATION                   │
        │                                                         │
        │  ┌─────────────────┐  ┌─────────────────┐               │
        │  │ ServiceNow      │  │ Enhanced        │               │
        │  │ Fields          │  │ Metadata        │               │
        │  │                 │  │                 │               │
        │  │ • Number        │  │ • AI Confidence │               │
        │  │ • Description   │  │ • Complexity    │               │
        │  │ • Work Notes    │  │ • Keywords      │               │
        │  │ • Priority      │  │ • Business Impact│              │
        │  │ • Category      │  │ • User Persona  │               │
        │  └─────────────────┘  └─────────────────┘               │
        └─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │                   OUTPUT GENERATION                     │
        │                                                         │
        │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
        │  │    CSV      │ │    JSON     │ │   Excel     │       │
        │  │             │ │             │ │             │       │
        │  │ • Standard  │ │ • Metadata  │ │ • Multiple  │       │
        │  │ • Formatted │ │ • Complete  │ │   Sheets    │       │
        │  │ • Headers   │ │ • Metrics   │ │ • Analytics │       │
        │  └─────────────┘ └─────────────┘ └─────────────┘       │
        └─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │              ANALYTICS & MONITORING                     │
        │                                                         │
        │ • Generation Success Rate    • Token Usage              │
        │ • Category Distribution      • Cost Estimation          │
        │ • Priority Distribution      • Performance Metrics      │
        │ • Department Distribution    • Error Tracking           │
        └─────────────────────────────────────────────────────────┘
```

### Core Components

1. **🎯 GoldenIncidentGeneratorV2**: Main orchestrator class
2. **⚙️ Configuration Manager**: Handles settings and business domains
3. **🤖 Azure OpenAI Client**: Manages LLM interactions
4. **📝 Prompt Engineering**: Advanced template system
5. **💾 Export Engine**: Multi-format output generation
6. **📊 Metrics Collector**: Performance and analytics tracking

---

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8+
- Azure OpenAI service access
- Valid Azure subscription

### 1. Environment Setup

```powershell
# Navigate to project directory
cd synthetic_data_engine_2.0

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .example.env .env
```

### 2. Configure Azure OpenAI

Edit your `.env` file:

```env
# Azure OpenAI Configuration (Required)
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

# Optional: LangSmith Tracing
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=GADM Work Assistant v1.1.4
```

### 3. Basic Usage Examples

#### Python API Method

```python
from golden_incident_generator_v2 import GoldenIncidentGeneratorV2

# Initialize generator
generator = GoldenIncidentGeneratorV2()

# Generate 10 incidents
incidents = generator.generate_batch(count=10)

# Export to different formats
csv_file = generator.export_to_csv("my_incidents.csv")
json_file = generator.export_to_json("my_incidents.json")
excel_file = generator.export_to_excel("my_incidents.xlsx")

print(f"Generated {len(incidents)} incidents")
generator.print_generation_summary()
```

#### Command Line Interface

```powershell
# Generate 25 incidents and export to CSV
python golden_incident_generator_v2.py --count 25 --output incidents.csv

# Advanced usage with custom configuration
python golden_incident_generator_v2.py `
  --count 100 `
  --config enhanced_incident_config.json `
  --batch-size 20 `
  --output large_batch.json `
  --verbose
```

### 4. Test Installation

```powershell
# Run comprehensive tests
python test_golden_generator_v2.py

# Run legacy tests
python test_generator.py
```

---

## ⚙️ Configuration Management

### Configuration File Structure

The engine uses `enhanced_incident_config.json` for comprehensive configuration:

```json
{
  "company_name": "Your Company Name",
  "business_domain": "Technology",
  "technical_environment": "Azure cloud environment with hybrid connectivity",
  
  "generation_settings": {
    "default_batch_size": 10,
    "max_retries": 3,
    "retry_delay": 1.0,
    "temperature": 0.7,
    "max_tokens": 2000
  },
  
  "priority_distribution": {
    "1 - Critical": 10,
    "2 - High": 25,
    "3 - Moderate": 50,
    "4 - Low": 15
  },
  
  "business_domains": {
    "Technology": {
      "departments": ["Engineering", "DevOps", "Product"],
      "common_technologies": ["Azure", "Kubernetes", "Docker"]
    }
  }
}
```

### Key Configuration Sections

#### 1. Company & Environment Settings

```json
{
  "company_name": "Abstergo Industries",
  "business_domain": "Technology",
  "technical_environment": "Azure cloud environment with hybrid connectivity, Microsoft 365"
}
```

#### 2. Generation Settings

```json
{
  "generation_settings": {
    "default_batch_size": 10,        // Default incidents per batch
    "max_retries": 3,                // Retry attempts for failed generations
    "retry_delay": 1.0,              // Seconds between retries
    "temperature": 0.7,              // LLM creativity (0.0-1.0)
    "max_tokens": 2000,              // Maximum tokens per generation
    "enable_progress_tracking": true,
    "enable_detailed_logging": true
  }
}
```

#### 3. Priority Distribution

Controls the probability distribution of incident priorities:

```json
{
  "priority_distribution": {
    "1 - Critical": 10,    // 10% of incidents
    "2 - High": 25,        // 25% of incidents
    "3 - Moderate": 50,    // 50% of incidents
    "4 - Low": 15          // 15% of incidents
  }
}
```

#### 4. State Distribution

Controls incident state probabilities:

```json
{
  "state_distribution": {
    "New": 5,
    "In Progress": 20,
    "Pending": 10,
    "Resolved": 35,
    "Closed": 30
  }
}
```

#### 5. Business Domains

Define industry-specific contexts:

```json
{
  "business_domains": {
    "Technology": {
      "departments": ["Engineering", "DevOps", "Product", "QA"],
      "common_technologies": ["Azure", "Kubernetes", "Docker", "CI/CD"],
      "compliance_requirements": ["SOC2", "GDPR", "HIPAA"]
    },
    "Healthcare": {
      "departments": ["Clinical", "Administration", "IT", "Compliance"],
      "common_technologies": ["EMR", "PACS", "Laboratory Systems"],
      "compliance_requirements": ["HIPAA", "HITECH", "FDA"]
    }
  }
}
```

#### 6. Incident Categories

Hierarchical category structure:

```json
{
  "incident_categories": {
    "Hardware": {
      "Desktop Workstation": [
        "Boot Issues", "Power Supply", "Memory", "Hard Drive"
      ],
      "Server": [
        "Hardware Failure", "Performance", "Storage", "Network Card"
      ]
    },
    "Software": {
      "Operating System": [
        "Windows Update", "Boot Issues", "Performance", "Blue Screen"
      ]
    }
  }
}
```

#### 7. Technician Specializations

Assign specialized technicians by category:

```json
{
  "technician_specializations": {
    "Hardware": ["Alex Chen", "Sarah Johnson", "Mike Rodriguez"],
    "Software": ["Emily Davis", "James Wilson", "Lisa Park"],
    "Network": ["David Kim", "Anna Schmidt", "Carlos Lopez"],
    "Security": ["Rachel Green", "Tom Anderson", "Maya Patel"]
  }
}
```

---

## 🔄 Data Generation Workflows

### Single Incident Generation

```python
# Generate single incident with context
generator = GoldenIncidentGeneratorV2()

# Create incident context
context = generator.generate_incident_context()
print(f"Context: {context['category']} - {context['priority']}")

# Generate incident
incident = generator.generate_single_incident(context)
if incident:
    print(f"Generated: {incident.number} - {incident.short_description}")
```

### Batch Generation Workflow

```python
# Configure for large batch
generator = GoldenIncidentGeneratorV2(
    max_retries=5,
    batch_size=25,
    retry_delay=1.5
)

# Define progress callback
def progress_callback(current, total):
    percentage = (current / total) * 100
    print(f"Progress: {current}/{total} ({percentage:.1f}%)")

# Generate with progress tracking
incidents = generator.generate_batch(
    count=100,
    progress_callback=progress_callback
)

print(f"Successfully generated {len(incidents)} incidents")
```

### Production Batch Processing

For large-scale generation (1000+ incidents):

```python
from production_batch_generator import ProductionBatchGenerator

# Initialize production generator
batch_gen = ProductionBatchGenerator(
    target_incidents=1000,
    batch_size=50,
    max_concurrent_batches=3
)

# Generate with checkpointing and recovery
batch_gen.run_production_batch()
```

---

## 🎨 Customization Guide

### Custom Business Domains

Add your own business domain:

```json
{
  "business_domains": {
    "YourDomain": {
      "departments": [
        "Department1", 
        "Department2", 
        "Department3"
      ],
      "common_technologies": [
        "Technology1", 
        "Technology2", 
        "Technology3"
      ],
      "compliance_requirements": [
        "Regulation1", 
        "Regulation2"
      ]
    }
  }
}
```

### Custom Incident Categories

Define domain-specific incident types:

```json
{
  "incident_categories": {
    "YourCategory": {
      "Subcategory1": [
        "Issue Type 1",
        "Issue Type 2",
        "Issue Type 3"
      ],
      "Subcategory2": [
        "Issue Type A",
        "Issue Type B"
      ]
    }
  }
}
```

### Custom User Personas

Add role-specific personas:

```json
{
  "user_personas": {
    "YourPersonaCategory": [
      "Role 1",
      "Role 2",
      "Role 3"
    ]
  }
}
```

### Adjusting Data Quality

#### Temperature Settings

Control creativity vs. consistency:

```json
{
  "generation_settings": {
    "temperature": 0.3   // Conservative (0.0-0.3)
    "temperature": 0.7   // Balanced (0.4-0.8)
    "temperature": 0.9   // Creative (0.8-1.0)
  }
}
```

#### Retry Logic

Configure error handling:

```json
{
  "generation_settings": {
    "max_retries": 3,      // Number of retry attempts
    "retry_delay": 1.0,    // Base delay between retries
    "enable_exponential_backoff": true
  }
}
```

### Priority Distribution Tuning

#### Scenario: High-Priority Focus

```json
{
  "priority_distribution": {
    "1 - Critical": 25,    // Increased critical incidents
    "2 - High": 35,        // More high-priority issues
    "3 - Moderate": 30,    // Reduced moderate
    "4 - Low": 10          // Minimal low-priority
  }
}
```

#### Scenario: Training Dataset Balance

```json
{
  "priority_distribution": {
    "1 - Critical": 15,    // Sufficient critical examples
    "2 - High": 25,        // Good high-priority coverage
    "3 - Moderate": 35,    // Majority moderate (realistic)
    "4 - Low": 25          // Adequate low-priority examples
  }
}
```

---

## 💾 Export Formats & Output

### CSV Export

**Features:**

- Standard CSV format with headers
- Configurable metadata inclusion
- UTF-8 encoding support
- Excel-compatible

**Usage:**

```python
# Basic CSV export
csv_file = generator.export_to_csv("incidents.csv")

# CSV without metadata
csv_file = generator.export_to_csv(
    filename="clean_incidents.csv",
    include_metadata=False
)
```

**Sample CSV Structure:**

```csv
number,short_description,category,priority,state,created,description,work_notes
INC0012345,"Azure VM - Performance Issue - CPU Spike",Hardware,2 - High,Resolved,2025-05-30T10:00:00,"Detailed description...","Work note 1..."
```

### JSON Export

**Features:**

- Comprehensive metadata
- Generation metrics
- Hierarchical structure
- API-friendly format

**Usage:**

```python
# Full JSON export with metadata
json_file = generator.export_to_json("incidents.json")

# Clean JSON without metadata
json_file = generator.export_to_json(
    filename="clean_incidents.json",
    include_metadata=False
)
```

**Sample JSON Structure:**

```json
{
  "metadata": {
    "generation_timestamp": "2025-05-30T15:30:00",
    "total_incidents": 10,
    "generator_version": "2.0.0",
    "model_version": "gpt-4o-mini",
    "config": {
      "company_name": "Abstergo Industries",
      "business_domain": "Technology"
    },
    "metrics": {
      "success_rate": 95.0,
      "total_tokens_used": 15000,
      "avg_generation_time": 2.5
    }
  },
  "incidents": [
    {
      "number": "INC0012345",
      "short_description": "Azure VM - Performance Issue",
      "description": "Detailed incident description...",
      "work_notes": "Formatted work notes...",
      "priority": "2 - High",
      "category": "Hardware",
      "business_impact_level": "Medium",
      "technical_keywords": "Azure, VM, Performance, CPU"
    }
  ]
}
```

### Excel Export

**Features:**

- Multiple worksheets
- Analytics sheets
- Formatted tables
- Charts and visualizations

**Usage:**

```python
# Full Excel export with analytics
excel_file = generator.export_to_excel("incidents.xlsx")

# Excel without analytics sheets
excel_file = generator.export_to_excel(
    filename="simple_incidents.xlsx",
    include_analytics=False
)
```

**Excel Worksheets:**

1. **Incidents**: Main incident data
2. **Metrics**: Generation performance metrics
3. **Category_Distribution**: Category breakdown
4. **Priority_Distribution**: Priority analysis
5. **Department_Distribution**: Department statistics

### Output Directory Structure

```curl
synthetic_data_output/
├── golden_incidents_20250530_153000.csv
├── golden_incidents_20250530_153000.json
├── golden_incidents_20250530_153000.xlsx
└── analytics/
    ├── generation_metrics.json
    └── performance_report.html
```

---

## 📊 Monitoring & Analytics

### Built-in Metrics

The engine automatically tracks comprehensive metrics:

```python
# Access metrics after generation
print(f"Success Rate: {generator.metrics.success_rate:.1f}%")
print(f"Total Tokens: {generator.metrics.total_tokens_used:,}")
print(f"Estimated Cost: ${generator.metrics.cost_estimate:.4f}")
print(f"Avg Generation Time: {generator.metrics.avg_generation_time:.2f}s")
```

### Generation Summary

```python
# Print comprehensive summary
generator.print_generation_summary()
```

**Sample Output:**

```curl
================================================================================
GOLDEN INCIDENT GENERATOR v2.0 - GENERATION SUMMARY
================================================================================

GENERATION STATISTICS:
  Total Requested: 100
  Successfully Generated: 95
  Failed: 5
  Success Rate: 95.0%
  Average Generation Time: 2.35s per incident

AZURE OPENAI USAGE:
  Total Tokens Used: 142,500
  Estimated Cost: $0.2138

CATEGORY DISTRIBUTION:
  Hardware: 25 (26.3%)
  Software: 30 (31.6%)
  Network: 20 (21.1%)
  Security: 12 (12.6%)
  Database: 8 (8.4%)

PRIORITY DISTRIBUTION:
  1 - Critical: 9 (9.5%)
  2 - High: 24 (25.3%)
  3 - Moderate: 48 (50.5%)
  4 - Low: 14 (14.7%)

DEPARTMENT DISTRIBUTION:
  Engineering: 35 (36.8%)
  DevOps: 18 (18.9%)
  Product: 15 (15.8%)
  QA: 12 (12.6%)
  Architecture: 15 (15.8%)
```

### Performance Monitoring

Monitor resource usage during generation:

```python
import psutil

# Check system resources
def monitor_resources():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    print(f"CPU: {cpu_percent}% | Memory: {memory.percent}%")

# Monitor during generation
incidents = generator.generate_batch(count=100)
monitor_resources()
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. Azure OpenAI Connection Issues

**Problem:** `Failed to initialize Azure OpenAI`

**Solution:**

```powershell
# Verify environment variables
echo $env:AZURE_OPENAI_ENDPOINT
echo $env:AZURE_OPENAI_API_KEY

# Test connection
python -c "
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
client = AzureOpenAI(
    azure_endpoint='YOUR_ENDPOINT',
    api_key='YOUR_KEY',
    api_version='2024-02-15-preview'
)
print('Connection successful')
"
```

#### 2. Import Errors

**Problem:** `ModuleNotFoundError: No module named 'golden_incident_generator_v2'`

**Solution:**

```powershell
# Install dependencies
pip install -r requirements.txt

# Verify Python path
python -c "import sys; print('\n'.join(sys.path))"

# Add current directory to path
$env:PYTHONPATH += ";$(Get-Location)"
```

#### 3. Configuration File Issues

**Problem:** `Failed to load config from enhanced_incident_config.json`

**Solution:**

```python
# Validate JSON syntax
import json
with open('enhanced_incident_config.json', 'r') as f:
    config = json.load(f)
print("Configuration valid")

# Reset to defaults
generator = GoldenIncidentGeneratorV2()
# This will create a new default config
```

#### 4. Low Success Rate

**Problem:** Success rate below 80%

**Diagnosis & Solution:**

```python
# Check error patterns
generator = GoldenIncidentGeneratorV2()
incidents = generator.generate_batch(count=10)

# Review logs
import logging
logging.basicConfig(level=logging.DEBUG)

# Adjust retry settings
generator = GoldenIncidentGeneratorV2(
    max_retries=5,
    retry_delay=2.0
)
```

#### 5. Memory Issues with Large Batches

**Problem:** `MemoryError` during large batch generation

**Solution:**

```python
# Use smaller batch sizes
generator = GoldenIncidentGeneratorV2(batch_size=10)

# Process in chunks
def generate_large_batch(total_count, chunk_size=50):
    all_incidents = []
    for i in range(0, total_count, chunk_size):
        chunk_count = min(chunk_size, total_count - i)
        chunk_incidents = generator.generate_batch(chunk_count)
        all_incidents.extend(chunk_incidents)
        print(f"Generated {len(all_incidents)}/{total_count}")
    return all_incidents
```

### Debugging Tips

#### Enable Verbose Logging

```python
# Initialize with debug logging
generator = GoldenIncidentGeneratorV2(
    log_level="DEBUG",
    console_output=True
)
```

#### Monitor Token Usage

```python
# Track token consumption
initial_tokens = generator.metrics.total_tokens_used
incidents = generator.generate_batch(count=10)
tokens_used = generator.metrics.total_tokens_used - initial_tokens
print(f"Tokens used for 10 incidents: {tokens_used}")
```

#### Validate Generated Data

```python
# Check data quality
for incident in incidents[:5]:  # Sample first 5
    print(f"Number: {incident.number}")
    print(f"Category: {incident.category}")
    print(f"Priority: {incident.priority}")
    print(f"Description length: {len(incident.description)}")
    print("---")
```

---

## 🏆 Best Practices

### 1. Configuration Management

#### ✅ DO

- Use version control for configuration files
- Create environment-specific configs
- Document configuration changes
- Validate JSON syntax before deployment

#### ❌ DON'T

- Hardcode credentials in configuration
- Use production configs in development
- Ignore configuration validation errors

### 2. Generation Quality

#### ✅ DO

- Monitor success rates (target: >90%)
- Validate generated data samples
- Use appropriate temperature settings
- Implement retry logic for failures

#### ❌ DON'T

- Accept low success rates without investigation
- Use extreme temperature values (0.0 or 1.0)
- Ignore error patterns in logs

### 3. Performance Optimization

#### ✅ DO

- Use appropriate batch sizes (10-50 incidents)
- Monitor resource usage during generation
- Implement progress tracking for long runs
- Cache configuration and prompt components

#### ❌ DON'T

- Generate thousands of incidents in single batch
- Ignore memory constraints
- Run without progress monitoring

### 4. Data Export

#### ✅ DO

- Include metadata in training datasets
- Use compression for large exports
- Validate export file integrity
- Document export parameters

#### ❌ DON'T

- Export without error checking
- Ignore file size limitations
- Mix training and testing data

### 5. Production Deployment

#### ✅ DO

- Use environment variables for secrets
- Implement comprehensive logging
- Set up monitoring and alerting
- Create backup and recovery procedures

#### ❌ DON'T

- Deploy without testing
- Skip security reviews
- Ignore resource limits
- Run without monitoring

### 6. Cost Management

#### ✅ DO

- Monitor Azure OpenAI token usage
- Set budget alerts and limits
- Optimize prompt efficiency
- Track cost per incident generated

#### ❌ DON'T

- Generate without cost awareness
- Use inefficient prompts
- Ignore token consumption patterns

---

## 📞 Support & Resources

- See this guide and `README.md` for usage and troubleshooting
- Contact: Hans Havlik (Capgemini)
- Azure OpenAI docs: <https://docs.microsoft.com/azure/cognitive-services/openai/>

---

**Last Updated:** May 30, 2025  
**Version:** 2.0.0  
**Next Review:** September 2025

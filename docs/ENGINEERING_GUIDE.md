<!--
ENGINEERING_GUIDE.md - SYNTHETIC ITSM INCIDENT DATA ENGINE v2.0 (Updated May 30, 2025)
-->
# Synthetic Data Engine v2.0 - Engineering Guide

## Table of Contents

1. Technical Architecture
2. Code Structure Analysis
3. Core Components Deep Dive
4. API Documentation
5. Development Guidelines
6. Performance Optimization
7. Security Implementation
8. Testing Strategy
9. Deployment Architecture
10. Monitoring and Observability
11. Conclusion

---

## Technical Architecture

### System Overview

The Synthetic Data Engine v2.0 is built on a modern, cloud-native architecture leveraging Azure OpenAI services for intelligent data generation. The system follows enterprise-grade patterns for scalability, reliability, and maintainability.

```curl
┌───────────────────────────────────────────────────────────────────┐
│                    AZURE CLOUD ENVIRONMENT                        │
├───────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐│
│  │   Azure OpenAI  │    │  Azure Monitor  │    │ Azure Key Vault ││
│  │   GPT-4o-mini   │    │   & Logging     │    │   Credentials   ││
│  │   Deployment    │    │                 │    │   Management    ││
│  └─────────────────┘    └─────────────────┘    └─────────────────┘│
└───────────────────────────────────────────────────────────────────┘
           │                        │                        │
           │ HTTPS/API              │ Telemetry              │ Auth
           │                        │                        │
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              GoldenIncidentGeneratorV2                      ││
│  │                   (Core Engine)                             ││
│  └─────────────────────────────────────────────────────────────┘│
│           │                 │                 │                 │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐       │
│  │ Configuration  │ │ Prompt Engine  │ │ Export Manager │       │
│  │   Management   │ │   & Templates  │ │  (CSV/JSON/XL) │       │
│  └────────────────┘ └────────────────┘ └────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
           │                 │                 │
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐          │
│  │ Configuration │ │   Generated   │ │    Metrics    │          │
│  │    Files      │ │   Incidents   │ │  & Analytics  │          │
│  │   (JSON)      │ │ (DataClasses) │ │   (Tracking)  │          │
│  └───────────────┘ └───────────────┘ └───────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

#### Core Technologies

- **Python 3.8+**: Runtime environment with async/await support
- **LangChain Framework**: LLM orchestration and prompt management
- **Azure OpenAI**: GPT-4o-mini model for text generation
- **Pandas**: Data manipulation and analysis
- **Pydantic**: Data validation and settings management

#### Development & Operations

- **Logging**: Structured logging with rotation and levels
- **Configuration**: JSON-based with environment variable overrides
- **Testing**: Pytest with async support and mocking
- **Export**: Multiple formats (CSV, JSON, Excel) with metadata

---

## Code Structure Analysis

### Project Architecture Pattern

The codebase follows a **Domain-Driven Design (DDD)** approach with clear separation of concerns:

```curl
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  • test_golden_generator_v2.py    (Testing Interface)           │
│  • production_batch_generator.py  (Batch Processing CLI)        │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  • GoldenIncidentGeneratorV2     (Main Application Service)     │
│  • EnhancedIncidentPromptTemplate (Prompt Engineering)          │
│  • ProductionBatchGenerator      (Batch Processing Logic)       │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                       DOMAIN LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  • GoldenIncident               (Core Domain Model)             │
│  • GenerationMetrics           (Metrics Aggregation)            │
│  • IncidentValidator           (Business Rules)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  • Azure OpenAI Client         (External API Integration)       │
│  • Configuration Loader        (Settings Management)            │
│  • File System Operations      (Export/Import)                  │
│  • Logging Infrastructure      (Observability)                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Patterns

#### 1. Factory Pattern

```python
class GoldenIncidentGeneratorV2:
    def __init__(self, config_path: str = None):
        self.llm = self._create_llm_client()  # Factory method
        self.prompt_template = self._create_prompt_template()
```

#### 2. Builder Pattern

```python
class IncidentBuilder:
    def with_category(self, category: str) -> 'IncidentBuilder':
        self.category = category
        return self
    
    def with_priority(self, priority: str) -> 'IncidentBuilder':
        self.priority = priority
        return self
```

#### 3. Strategy Pattern

```python
class ExportStrategy:
    def export(self, incidents: List[GoldenIncident]) -> str:
        pass

class CSVExportStrategy(ExportStrategy):
    def export(self, incidents: List[GoldenIncident]) -> str:
        # CSV-specific export logic
```

---

## Core Components Deep Dive

### 1. GoldenIncidentGeneratorV2 Class

#### Class Hierarchy

```python
GoldenIncidentGeneratorV2
├── Configuration Management
│   ├── _load_configuration()
│   ├── _validate_config()
│   └── _setup_environment()
├── LLM Integration
│   ├── _create_llm_client()
│   ├── _setup_retry_logic()
│   └── _handle_api_errors()
├── Incident Generation
│   ├── generate_single_incident()
│   ├── generate_batch()
│   └── _apply_business_rules()
├── Data Processing
│   ├── _validate_incident()
│   ├── _enrich_metadata()
│   └── _calculate_metrics()
└── Export Operations
    ├── export_to_csv()
    ├── export_to_json()
    └── export_to_excel()
```

#### Key Methods Analysis

**`generate_single_incident()`**

```python
def generate_single_incident(self, business_domain: str = None, 
                           category: str = None) -> GoldenIncident:
    """
    Generates a single synthetic incident with full lifecycle simulation.
    
    Technical Flow:
    1. Domain Selection & Validation
    2. Prompt Construction with Context
    3. LLM API Call with Retry Logic
    4. Response Parsing & Validation
    5. Metadata Enrichment
    6. Business Rule Application
    7. Quality Assurance Checks
    """
```

**`_setup_azure_openai_client()`**

```python
def _setup_azure_openai_client(self) -> AzureChatOpenAI:
    """
    Initializes Azure OpenAI client with enterprise configuration.
    
    Features:
    • Managed Identity Support
    • Connection Pooling
    • Retry Mechanisms
    • Request Throttling
    • Error Handling
    """
```

### 2. Data Models

#### GoldenIncident DataClass

```python
@dataclass
class GoldenIncident:
    # Core ServiceNow Fields
    incident_id: str
    short_description: str
    description: str
    category: str
    subcategory: str
    priority: str
    urgency: str
    impact: str
    state: str
    
    # Assignment & Ownership
    assigned_to: str
    assignment_group: str
    caller_id: str
    
    # Temporal Fields
    opened_at: datetime
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    
    # Technical Details
    configuration_item: str
    business_service: str
    work_notes: str
    resolution_notes: str
    
    # Metadata & Quality
    ai_confidence_score: float
    generation_timestamp: datetime
    model_version: str
    business_domain: str
```

#### GenerationMetrics DataClass

```python
@dataclass
class GenerationMetrics:
    total_generated: int = 0
    successful_generations: int = 0
    failed_generations: int = 0
    average_confidence: float = 0.0
    generation_time_seconds: float = 0.0
    api_calls_made: int = 0
    tokens_consumed: int = 0
    category_distribution: Dict[str, int] = field(default_factory=dict)
    priority_distribution: Dict[str, int] = field(default_factory=dict)
```

### 3. Configuration Management

#### Configuration Schema

```json
{
    "company_name": "string",
    "business_domain": "string",
    "incident_categories": {
        "category_name": {
            "subcategories": ["list"],
            "weight": "float",
            "typical_priority": "string",
            "resolution_time_range": ["int", "int"]
        }
    },
    "user_personas": {
        "persona_name": {
            "departments": ["list"],
            "common_issues": ["list"],
            "technical_level": "string"
        }
    },
    "technician_groups": {
        "group_name": {
            "specialties": ["list"],
            "escalation_level": "int"
        }
    }
}
```

#### Environment Configuration

```python
# Required Environment Variables
AZURE_OPENAI_ENDPOINT: str
AZURE_OPENAI_API_KEY: str
AZURE_OPENAI_API_VERSION: str
AZURE_OPENAI_DEPLOYMENT_NAME: str

# Optional Configuration
LANGCHAIN_TRACING_V2: bool = False
LANGCHAIN_PROJECT: str = "Synthetic Data Engine"
LOG_LEVEL: str = "INFO"
OUTPUT_DIRECTORY: str = "synthetic_data_output"
```

---

## API Documentation

### Core API Methods

#### Generator Initialization

```python
def __init__(self, config_path: Optional[str] = None, 
             log_level: str = "INFO") -> None:
    """
    Initialize the Golden Incident Generator V2.
    
    Parameters:
    -----------
    config_path : Optional[str]
        Path to configuration JSON file. Defaults to 'enhanced_incident_config.json'
    log_level : str
        Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        
    Raises:
    -------
    FileNotFoundError: If configuration file not found
    ValueError: If configuration validation fails
    ConfigurationError: If Azure OpenAI setup fails
    """
```

#### Batch Generation

```python
def generate_batch(self, count: int, business_domain: Optional[str] = None,
                  progress_callback: Optional[Callable] = None) -> List[GoldenIncident]:
    """
    Generate a batch of synthetic incidents with progress tracking.
    
    Parameters:
    -----------
    count : int
        Number of incidents to generate (1-10000)
    business_domain : Optional[str]
        Specific business domain context
    progress_callback : Optional[Callable]
        Callback function for progress updates
        
    Returns:
    --------
    List[GoldenIncident]: Generated incidents with metadata
    
    Raises:
    -------
    ValueError: If count is invalid
    APIError: If Azure OpenAI service fails
    ValidationError: If generated data fails validation
    """
```

#### Export Operations

```python
def export_to_csv(self, filename: Optional[str] = None, 
                 include_metadata: bool = True) -> str:
    """
    Export incidents to CSV format with optional metadata.
    
    Parameters:
    -----------
    filename : Optional[str]
        Output filename. Auto-generated if None
    include_metadata : bool
        Include AI generation metadata in export
        
    Returns:
    --------
    str: Path to exported file
        
    Technical Details:
    ------------------
    • UTF-8 encoding with BOM for Excel compatibility
    • Configurable column ordering
    • Metadata filtering options
    • Automatic timestamp generation
    """
```

### Error Handling

#### Exception Hierarchy

```python
class SyntheticDataEngineError(Exception):
    """Base exception for all engine errors"""
    pass

class ConfigurationError(SyntheticDataEngineError):
    """Configuration loading or validation errors"""
    pass

class APIError(SyntheticDataEngineError):
    """Azure OpenAI API communication errors"""
    pass

class ValidationError(SyntheticDataEngineError):
    """Data validation and quality errors"""
    pass

class ExportError(SyntheticDataEngineError):
    """File export operation errors"""
    pass
```

#### Retry Mechanisms

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((APIError, ConnectionError))
)
def _call_azure_openai(self, prompt: str) -> str:
    """Azure OpenAI API call with exponential backoff retry"""
```

---

## Development Guidelines

### Code Style Standards

#### Python Code Standards

- **PEP 8**: Python code style guide compliance
- **Type Hints**: Full type annotation coverage
- **Docstrings**: Google-style docstring format
- **Import Organization**: Standard library, third-party, local imports

#### Example Code Style

```python
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import logging

class ExampleClass:
    """
    Example class demonstrating code style standards.
    
    This class serves as a template for consistent code style
    across the synthetic data engine codebase.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the example class.
        
        Args:
            config: Configuration dictionary containing setup parameters
            
        Raises:
            ValueError: If configuration is invalid
        """
        self._config = self._validate_config(config)
        self._logger = logging.getLogger(__name__)
        
    def process_data(self, 
                    input_data: List[str], 
                    options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process input data with optional configuration.
        
        Args:
            input_data: List of strings to process
            options: Optional processing configuration
            
        Returns:
            Dict containing processed results and metadata
            
        Raises:
            ProcessingError: If data processing fails
        """
        # Implementation here
        pass
```

### Testing Guidelines

#### Test Structure

```python
# test_golden_generator_v2.py structure
import pytest
from unittest.mock import Mock, patch
import asyncio

class TestGoldenIncidentGeneratorV2:
    """Comprehensive test suite for GoldenIncidentGeneratorV2"""
    
    @pytest.fixture
    def generator(self):
        """Fixture providing initialized generator instance"""
        return GoldenIncidentGeneratorV2()
    
    @pytest.fixture
    def mock_azure_client(self):
        """Fixture providing mocked Azure OpenAI client"""
        return Mock()
    
    def test_single_incident_generation(self, generator):
        """Test single incident generation with default parameters"""
        # Test implementation
        pass
    
    @pytest.mark.asyncio
    async def test_batch_generation_async(self, generator):
        """Test asynchronous batch generation"""
        # Async test implementation
        pass
    
    @pytest.mark.parametrize("count,expected", [
        (1, 1),
        (10, 10),
        (100, 100)
    ])
    def test_batch_count_validation(self, generator, count, expected):
        """Test batch generation with various counts"""
        # Parameterized test implementation
        pass
```

#### Test Coverage Requirements

- **Unit Tests**: 90%+ code coverage
- **Integration Tests**: Azure OpenAI service integration
- **Performance Tests**: Batch generation benchmarks
- **Error Handling Tests**: Exception scenario coverage

### Performance Guidelines

#### Memory Management

```python
# Efficient batch processing with generators
def generate_incidents_stream(self, count: int) -> Iterator[GoldenIncident]:
    """
    Generate incidents as a stream to minimize memory usage.
    
    Yields incidents one at a time instead of loading all into memory.
    Suitable for large batch operations (10,000+ incidents).
    """
    for i in range(count):
        yield self.generate_single_incident()
```

#### Async Programming

```python
import asyncio
from typing import List

async def generate_batch_async(self, count: int) -> List[GoldenIncident]:
    """
    Asynchronous batch generation for improved performance.
    
    Uses asyncio to parallelize API calls while respecting
    rate limits and connection pooling.
    """
    semaphore = asyncio.Semaphore(10)  # Limit concurrent requests
    
    async def generate_single() -> GoldenIncident:
        async with semaphore:
            return await self._generate_single_async()
    
    tasks = [generate_single() for _ in range(count)]
    return await asyncio.gather(*tasks)
```

---

## Performance Optimization

### Caching Strategies

#### Configuration Caching

```python
from functools import lru_cache

class GoldenIncidentGeneratorV2:
    @lru_cache(maxsize=1)
    def _load_configuration(self, config_path: str) -> Dict[str, Any]:
        """Cache configuration to avoid repeated file I/O"""
        return self._parse_config_file(config_path)
    
    @lru_cache(maxsize=128)
    def _get_domain_context(self, business_domain: str) -> str:
        """Cache domain context strings for reuse"""
        return self._build_domain_context(business_domain)
```

#### Response Caching

```python
from typing import Dict
import hashlib

class ResponseCache:
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
    
    def get_cache_key(self, prompt: str, parameters: Dict) -> str:
        """Generate cache key from prompt and parameters"""
        content = f"{prompt}:{sorted(parameters.items())}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve cached response"""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Store response in cache with LRU eviction"""
        if len(self._cache) >= self._max_size:
            # Remove oldest entry
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = value
```

### Batch Processing Optimization

#### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class BatchProcessor:
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self._thread_local = threading.local()
    
    def process_batch_parallel(self, count: int) -> List[GoldenIncident]:
        """
        Process batch with parallel workers while maintaining thread safety.
        
        Each worker gets its own generator instance to avoid shared state issues.
        """
        chunk_size = max(1, count // self.max_workers)
        chunks = [chunk_size] * (self.max_workers - 1)
        chunks.append(count - sum(chunks))
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self._process_chunk, chunk)
                for chunk in chunks if chunk > 0
            ]
            
            results = []
            for future in as_completed(futures):
                results.extend(future.result())
                
        return results
```

### Memory Optimization

#### Streaming Exports

```python
import csv
from contextlib import contextmanager

@contextmanager
def streaming_csv_writer(filename: str):
    """Context manager for streaming CSV writing without memory buildup"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=GoldenIncident.__annotations__.keys())
        writer.writeheader()
        yield writer

def export_to_csv_streaming(self, filename: str, batch_size: int = 1000):
    """
    Export incidents to CSV using streaming to handle large datasets.
    
    Processes incidents in batches to maintain constant memory usage
    regardless of total incident count.
    """
    with streaming_csv_writer(filename) as writer:
        for i in range(0, len(self.generated_incidents), batch_size):
            batch = self.generated_incidents[i:i + batch_size]
            for incident in batch:
                writer.writerow(asdict(incident))
```

---

## Security Implementation

### Authentication & Authorization

#### Azure Managed Identity

```python
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

class SecureAzureClient:
    def __init__(self):
        # Prefer Managed Identity in Azure environments
        try:
            self.credential = ManagedIdentityCredential()
        except Exception:
            # Fallback to default credential chain
            self.credential = DefaultAzureCredential()
    
    def get_token(self) -> str:
        """Retrieve secure token for Azure OpenAI access"""
        token = self.credential.get_token("https://cognitiveservices.azure.com/.default")
        return token.token
```

#### API Key Management

```python
import os
from cryptography.fernet import Fernet

class SecureConfigManager:
    def __init__(self):
        self.fernet = Fernet(self._get_encryption_key())
    
    def _get_encryption_key(self) -> bytes:
        """Retrieve encryption key from secure storage"""
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            raise SecurityError("Encryption key not found in environment")
        return key.encode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key from secure storage"""
        return self.fernet.decrypt(encrypted_key.encode()).decode()
```

### Data Protection

#### PII Sanitization

```python
import re
from typing import Pattern

class DataSanitizer:
    """Sanitize generated data to prevent PII leakage"""
    
    # Regex patterns for PII detection
    EMAIL_PATTERN: Pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN: Pattern = re.compile(r'\b\d{3}-\d{3}-\d{4}\b')
    SSN_PATTERN: Pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    
    def sanitize_incident(self, incident: GoldenIncident) -> GoldenIncident:
        """Remove or mask potential PII from incident data"""
        sanitized = deepcopy(incident)
        
        # Sanitize text fields
        sanitized.description = self._sanitize_text(sanitized.description)
        sanitized.work_notes = self._sanitize_text(sanitized.work_notes)
        sanitized.resolution_notes = self._sanitize_text(sanitized.resolution_notes)
        
        return sanitized
    
    def _sanitize_text(self, text: str) -> str:
        """Apply sanitization patterns to text"""
        text = self.EMAIL_PATTERN.sub('[EMAIL_REDACTED]', text)
        text = self.PHONE_PATTERN.sub('[PHONE_REDACTED]', text)
        text = self.SSN_PATTERN.sub('[SSN_REDACTED]', text)
        return text
```

### Audit Logging

#### Security Event Logging

```python
import structlog
from datetime import datetime

class SecurityLogger:
    def __init__(self):
        self.logger = structlog.get_logger("security")
    
    def log_api_access(self, endpoint: str, status: str, user_context: Dict):
        """Log API access attempts for security monitoring"""
        self.logger.info(
            "api_access",
            timestamp=datetime.utcnow().isoformat(),
            endpoint=endpoint,
            status=status,
            user_context=user_context,
            event_type="api_access"
        )
    
    def log_data_export(self, export_type: str, record_count: int, user_context: Dict):
        """Log data export operations for compliance"""
        self.logger.info(
            "data_export",
            timestamp=datetime.utcnow().isoformat(),
            export_type=export_type,
            record_count=record_count,
            user_context=user_context,
            event_type="data_export"
        )
```

---

## Testing Strategy

### Test Pyramid Implementation

#### Unit Tests (Base Layer)

```python
# Fast, isolated tests for individual components
class TestIncidentValidator:
    def test_validate_priority_valid(self):
        """Test priority validation with valid values"""
        validator = IncidentValidator()
        assert validator.validate_priority("High") == True
        assert validator.validate_priority("Medium") == True
        assert validator.validate_priority("Low") == True
    
    def test_validate_priority_invalid(self):
        """Test priority validation with invalid values"""
        validator = IncidentValidator()
        with pytest.raises(ValidationError):
            validator.validate_priority("Invalid")
```

#### Integration Tests (Middle Layer)

```python
# Test component interactions and external dependencies
class TestAzureOpenAIIntegration:
    @pytest.mark.integration
    def test_azure_client_connectivity(self):
        """Test actual Azure OpenAI service connectivity"""
        generator = GoldenIncidentGeneratorV2()
        response = generator._test_azure_connection()
        assert response.status_code == 200
    
    @pytest.mark.integration
    def test_end_to_end_generation(self):
        """Test complete incident generation workflow"""
        generator = GoldenIncidentGeneratorV2()
        incident = generator.generate_single_incident()
        assert isinstance(incident, GoldenIncident)
        assert incident.incident_id is not None
```

#### End-to-End Tests (Top Layer)

```python
# Test complete user workflows
class TestCompleteWorkflows:
    @pytest.mark.e2e
    def test_batch_generation_and_export_workflow(self):
        """Test complete batch generation and export process"""
        generator = GoldenIncidentGeneratorV2()
        
        # Generate batch
        incidents = generator.generate_batch(count=10)
        assert len(incidents) == 10
        
        # Export to all formats
        csv_path = generator.export_to_csv()
        json_path = generator.export_to_json()
        excel_path = generator.export_to_excel()
        
        # Verify exports exist and contain data
        assert Path(csv_path).exists()
        assert Path(json_path).exists()
        assert Path(excel_path).exists()
```

### Test Data Management

#### Fixtures and Mock Data

```python
@pytest.fixture
def sample_incident():
    """Provide sample incident for testing"""
    return GoldenIncident(
        incident_id="INC0000001",
        short_description="Test incident",
        description="Detailed test description",
        category="Software",
        subcategory="Application",
        priority="Medium",
        urgency="Medium",
        impact="Medium",
        state="New",
        assigned_to="John Doe",
        assignment_group="IT Support",
        caller_id="jane.smith@company.com",
        opened_at=datetime.now(),
        resolved_at=None,
        closed_at=None,
        configuration_item="SAP Production",
        business_service="Finance Applications",
        work_notes="Initial investigation in progress",
        resolution_notes="",
        ai_confidence_score=0.95,
        generation_timestamp=datetime.now(),
        model_version="gpt-4o-mini",
        business_domain="Technology"
    )

@pytest.fixture
def mock_azure_response():
    """Provide mock Azure OpenAI response"""
    return {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "short_description": "Email system outage",
                    "description": "Users unable to access email...",
                    "category": "Infrastructure",
                    "priority": "High"
                })
            }
        }],
        "usage": {
            "total_tokens": 150
        }
    }
```

### Performance Testing

#### Load Testing

```python
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

class PerformanceTest:
    def test_generation_performance(self):
        """Test incident generation performance metrics"""
        generator = GoldenIncidentGeneratorV2()
        
        # Measure single incident generation time
        start_time = time.time()
        generator.generate_single_incident()
        single_time = time.time() - start_time
        
        assert single_time < 5.0  # Should complete within 5 seconds
    
    def test_batch_generation_scalability(self):
        """Test batch generation scalability"""
        generator = GoldenIncidentGeneratorV2()
        batch_sizes = [10, 50, 100, 500]
        
        for batch_size in batch_sizes:
            start_time = time.time()
            incidents = generator.generate_batch(count=batch_size)
            generation_time = time.time() - start_time
            
            # Performance assertions
            assert len(incidents) == batch_size
            assert generation_time / batch_size < 2.0  # Max 2 seconds per incident
    
    def test_memory_usage_during_batch(self):
        """Test memory usage during large batch generation"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        generator = GoldenIncidentGeneratorV2()
        generator.generate_batch(count=1000)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory should not increase by more than 100MB for 1000 incidents
        assert memory_increase < 100 * 1024 * 1024
```

---

## Deployment Architecture

### Production Deployment Patterns

#### Container Deployment

```dockerfile
# Dockerfile for production deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from golden_incident_generator_v2 import GoldenIncidentGeneratorV2; GoldenIncidentGeneratorV2()"

# Expose port (if running as web service)
EXPOSE 8000

# Default command
CMD ["python", "-m", "production_batch_generator"]
```

#### Kubernetes Deployment

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: synthetic-data-engine
  namespace: data-generation
spec:
  replicas: 3
  selector:
    matchLabels:
      app: synthetic-data-engine
  template:
    metadata:
      labels:
        app: synthetic-data-engine
    spec:
      serviceAccountName: synthetic-data-engine-sa
      containers:
      - name: generator
        image: your-registry/synthetic-data-engine:v2.0
        env:
        - name: AZURE_OPENAI_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: azure-openai-config
              key: endpoint
        - name: AZURE_OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: azure-openai-config
              key: api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: output-volume
          mountPath: /app/synthetic_data_output
      volumes:
      - name: config-volume
        configMap:
          name: generator-config
      - name: output-volume
        persistentVolumeClaim:
          claimName: output-pvc
```

#### Azure Container Apps Deployment

```yaml
# azure-container-apps.yaml
apiVersion: apps/v1alpha1
kind: ContainerApp
metadata:
  name: synthetic-data-engine
spec:
  environmentId: /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Web/managedEnvironments/{env}
  configuration:
    secrets:
    - name: azure-openai-key
      value: "{key-value}"
    ingress:
      external: false
      targetPort: 8000
  template:
    containers:
    - image: your-registry/synthetic-data-engine:v2.0
      name: generator
      env:
      - name: AZURE_OPENAI_ENDPOINT
        value: "https://your-openai.openai.azure.com/"
      - name: AZURE_OPENAI_API_KEY
        secretRef: azure-openai-key
      resources:
        cpu: 0.5
        memory: 1Gi
    scale:
      minReplicas: 1
      maxReplicas: 10
      rules:
      - name: queue-scaling
        custom:
          type: azure-servicebus
          metadata:
            queueName: generation-requests
            messageCount: "5"
```

### Infrastructure as Code

#### Terraform Configuration

```hcl
# terraform/main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

resource "azurerm_resource_group" "synthetic_data" {
  name     = "rg-synthetic-data-engine"
  location = var.location
}

resource "azurerm_cognitive_account" "openai" {
  name                = "openai-synthetic-data"
  location            = azurerm_resource_group.synthetic_data.location
  resource_group_name = azurerm_resource_group.synthetic_data.name
  kind                = "OpenAI"
  sku_name           = "S0"

  tags = {
    Environment = var.environment
    Project     = "Synthetic Data Engine"
  }
}

resource "azurerm_cognitive_deployment" "gpt4o_mini" {
  name                 = "gpt-4o-mini"
  cognitive_account_id = azurerm_cognitive_account.openai.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o-mini"
    version = "2024-07-18"
  }
  scale {
    type = "Standard"
  }
}

resource "azurerm_container_app_environment" "synthetic_data" {
  name                = "cae-synthetic-data"
  location            = azurerm_resource_group.synthetic_data.location
  resource_group_name = azurerm_resource_group.synthetic_data.name
}
```

---

## Monitoring and Observability

### Logging Architecture

#### Structured Logging Implementation

```python
import structlog
import logging.config

def setup_logging(log_level: str = "INFO", 
                 output_file: Optional[str] = None) -> None:
    """
    Configure structured logging for the application.
    
    Features:
    • JSON formatting for machine readability
    • Contextual field injection
    • Log level filtering
    • File rotation support
    • Performance metrics logging
    """
    
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.JSONRenderer()
    ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

class ContextualLogger:
    def __init__(self, name: str):
        self.logger = structlog.get_logger(name)
    
    def log_generation_attempt(self, business_domain: str, attempt: int):
        """Log incident generation attempt with context"""
        self.logger.info(
            "incident_generation_attempt",
            business_domain=business_domain,
            attempt_number=attempt,
            operation="generate_incident"
        )
    
    def log_api_call(self, endpoint: str, duration: float, token_usage: int):
        """Log Azure OpenAI API call metrics"""
        self.logger.info(
            "azure_openai_api_call",
            endpoint=endpoint,
            duration_seconds=duration,
            tokens_used=token_usage,
            operation="llm_api_call"
        )
```

### Metrics Collection

#### Application Metrics

```python
from dataclasses import dataclass
from typing import Dict, List
import time

@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics tracking"""
    
    # Generation Metrics
    total_incidents_generated: int = 0
    successful_generations: int = 0
    failed_generations: int = 0
    average_generation_time: float = 0.0
    
    # API Metrics
    api_calls_made: int = 0
    total_tokens_consumed: int = 0
    api_error_count: int = 0
    average_api_response_time: float = 0.0
    
    # Quality Metrics
    average_confidence_score: float = 0.0
    validation_failures: int = 0
    
    # Resource Metrics
    peak_memory_usage_mb: float = 0.0
    cpu_time_seconds: float = 0.0

class MetricsCollector:
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self._generation_times: List[float] = []
        self._api_times: List[float] = []
        self._confidence_scores: List[float] = []
    
    def record_generation_time(self, duration: float):
        """Record incident generation duration"""
        self._generation_times.append(duration)
        self.metrics.average_generation_time = sum(self._generation_times) / len(self._generation_times)
    
    def record_api_call(self, duration: float, tokens: int, success: bool):
        """Record API call metrics"""
        self.metrics.api_calls_made += 1
        self.metrics.total_tokens_consumed += tokens
        
        if success:
            self._api_times.append(duration)
            self.metrics.average_api_response_time = sum(self._api_times) / len(self._api_times)
        else:
            self.metrics.api_error_count += 1
    
    def record_confidence_score(self, score: float):
        """Record AI confidence score"""
        self._confidence_scores.append(score)
        self.metrics.average_confidence_score = sum(self._confidence_scores) / len(self._confidence_scores)
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export metrics for monitoring systems"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": asdict(self.metrics),
            "distributions": {
                "generation_times": self._generation_times[-100:],  # Last 100 samples
                "api_response_times": self._api_times[-100:],
                "confidence_scores": self._confidence_scores[-100:]
            }
        }
```

### Health Checks

#### Application Health Monitoring

```python
from enum import Enum
from typing import Dict, Any

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class HealthChecker:
    def __init__(self, generator: GoldenIncidentGeneratorV2):
        self.generator = generator
        self.logger = structlog.get_logger("health_check")
    
    async def check_overall_health(self) -> Dict[str, Any]:
        """Comprehensive health check of all system components"""
        checks = {
            "azure_openai": await self._check_azure_openai(),
            "configuration": self._check_configuration(),
            "memory": self._check_memory_usage(),
            "disk_space": self._check_disk_space()
        }
        
        # Determine overall status
        if all(check["status"] == HealthStatus.HEALTHY.value for check in checks.values()):
            overall_status = HealthStatus.HEALTHY
        elif any(check["status"] == HealthStatus.UNHEALTHY.value for check in checks.values()):
            overall_status = HealthStatus.UNHEALTHY
        else:
            overall_status = HealthStatus.DEGRADED
        
        return {
            "overall_status": overall_status.value,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks
        }
    
    async def _check_azure_openai(self) -> Dict[str, Any]:
        """Check Azure OpenAI service connectivity"""
        try:
            start_time = time.time()
            # Perform lightweight test call
            response = await self.generator._test_azure_connection()
            response_time = time.time() - start_time
            
            if response_time > 5.0:  # Slow response
                return {
                    "status": HealthStatus.DEGRADED.value,
                    "response_time": response_time,
                    "message": "Azure OpenAI responding slowly"
                }
            
            return {
                "status": HealthStatus.HEALTHY.value,
                "response_time": response_time,
                "message": "Azure OpenAI service operational"
            }
            
        except Exception as e:
            self.logger.error("azure_openai_health_check_failed", error=str(e))
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "error": str(e),
                "message": "Azure OpenAI service unavailable"
            }
```

### Alerting and Monitoring

#### Prometheus Metrics Export

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest

class PrometheusMetrics:
    def __init__(self):
        # Counters
        self.incidents_generated = Counter(
            'incidents_generated_total',
            'Total number of incidents generated',
            ['business_domain', 'category']
        )
        
        self.api_calls = Counter(
            'azure_openai_api_calls_total',
            'Total Azure OpenAI API calls',
            ['status']
        )
        
        # Histograms
        self.generation_duration = Histogram(
            'incident_generation_duration_seconds',
            'Time spent generating incidents',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        self.api_response_time = Histogram(
            'azure_openai_response_time_seconds',
            'Azure OpenAI API response time',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        # Gauges
        self.active_generations = Gauge(
            'active_generations',
            'Number of currently active generation processes'
        )
        
        self.confidence_score = Gauge(
            'average_confidence_score',
            'Average AI confidence score'
        )
    
    def record_incident_generated(self, business_domain: str, category: str):
        """Record incident generation event"""
        self.incidents_generated.labels(
            business_domain=business_domain,
            category=category
        ).inc()
    
    def record_generation_time(self, duration: float):
        """Record generation duration"""
        self.generation_duration.observe(duration)
    
    def export_metrics(self) -> str:
        """Export metrics in Prometheus format"""
        return generate_latest()
```

---

## Conclusion

This engineering guide provides comprehensive technical documentation for the Synthetic Data Engine v2.0, covering architecture patterns, implementation details, and operational considerations. The system is designed for enterprise-scale deployment with emphasis on:

- **Scalability**: Handles batch generation from single incidents to tens of thousands
- **Reliability**: Comprehensive error handling, retry mechanisms, and health monitoring
- **Security**: Azure Managed Identity, PII sanitization, and audit logging
- **Observability**: Structured logging, metrics collection, and health checks
- **Maintainability**: Clean architecture, comprehensive testing, and documentation

For implementation questions or architectural decisions, refer to the specific sections above or consult the User Guide for operational procedures.

---

**Document Version**: 1.0  
**Last Updated**: May 30, 2025  
**Maintained By**: Engineering Team  
**Next Review**: June 30, 2025

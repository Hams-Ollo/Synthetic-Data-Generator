#!/usr/bin/env python3
"""
Golden Incident Generator v2.0
===============================

Production-ready synthetic ServiceNow incident data generator using Azure OpenAI
and advanced prompt engineering templates. This version integrates all enhanced
features for generating high-quality training data for custom LLM models.

Features:
- Azure OpenAI integration with managed identity support
- Advanced prompt engineering with contextual enhancement
- Business domain-specific incident generation
- Comprehensive error handling and retry logic
- Production-grade logging and monitoring
- Batch processing with progress tracking
- Multiple export formats (CSV, JSON, Excel)
- Performance optimization and caching

Author: Hans Havlik
Date: May 30, 2025
Version: 2.0.0
Application: GADM Work Assistant Training Data Generation
"""

import json
import csv
import os
import sys
import logging
import argparse
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import random
import traceback
import uuid
from pathlib import Path
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import traceback
import re

# Environment variables management
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Config'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Main'))

# Azure OpenAI and LangChain imports
try:
    from langchain_openai import AzureChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.prompts import PromptTemplate
    from langchain_community.callbacks import get_openai_callback
except ImportError as e:
    logging.error(f"LangChain imports failed: {e}")
    sys.exit(1)

# LLM configuration is now sourced exclusively from environment variables (.env file)
try:
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    # Validate required environment variables
    if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME]):
        missing_vars = []
        if not AZURE_OPENAI_ENDPOINT: missing_vars.append('AZURE_OPENAI_ENDPOINT')
        if not AZURE_OPENAI_KEY: missing_vars.append('AZURE_OPENAI_API_KEY')
        if not AZURE_OPENAI_API_VERSION: missing_vars.append('AZURE_OPENAI_API_VERSION')
        if not AZURE_OPENAI_DEPLOYMENT_NAME: missing_vars.append('AZURE_OPENAI_DEPLOYMENT_NAME')
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    from enhanced_incident_prompt_template import (
        ENHANCED_INCIDENT_SYSTEM_PROMPT,
        get_enhanced_prompt
    )
except ImportError as e:
    logging.error(f"Configuration imports failed: {e}")
    print("Please ensure all configuration files are properly set up.")
    sys.exit(1)
except EnvironmentError as e:
    logging.error(f"Environment configuration error: {e}")
    print("Please ensure all required environment variables are set in your .env file.")
    sys.exit(1)


@dataclass
class IncidentMetrics:
    """Metrics for tracking generation performance"""
    total_requested: int = 0
    total_generated: int = 0
    total_failed: int = 0
    success_rate: float = 0.0
    avg_generation_time: float = 0.0
    total_tokens_used: int = 0.0
    cost_estimate: float = 0.0
    category_distribution: Dict[str, int] = None
    priority_distribution: Dict[str, int] = None
    department_distribution: Dict[str, int] = None
    
    def __post_init__(self):
        if self.category_distribution is None:
            self.category_distribution = {}
        if self.priority_distribution is None:
            self.priority_distribution = {}
        if self.department_distribution is None:
            self.department_distribution = {}


@dataclass
class EnhancedIncidentRecord:
    """Enhanced incident record with comprehensive metadata"""
    # Core ServiceNow fields
    number: str
    short_description: str
    description: str
    assignment_group: str
    assigned_to: str
    state: str
    parent: str
    configuration_item: str
    impact: str
    urgency: str
    priority: str
    category: str
    subcategory: str
    close_notes: str
    resolved_by: str
    work_notes: str
    comments_and_work_notes: str
    opened_by: str
    created: str
    resolve_time: str
    closed: str
    caller: str
    requestor_email: str
    close_code: str
    
    # Enhanced metadata fields
    business_impact_level: str = ""
    resolution_category: str = ""
    technical_keywords: str = ""
    user_department: str = ""
    user_role: str = ""
    business_domain: str = ""
    incident_complexity: str = ""
    escalation_level: str = ""
    user_persona: str = ""
    ai_confidence_score: float = 0.0
    generation_timestamp: str = ""
    model_version: str = ""


class GoldenIncidentGeneratorV2:
    """Production-ready golden incident generator with Azure OpenAI integration"""
    
    def __init__(self, config_path: Optional[str] = None, **kwargs):
        """
        Initialize the golden incident generator
        
        Args:
            config_path: Path to configuration file
            **kwargs: Additional configuration options
        """
        self.setup_logging(**kwargs)
        self.config = self.load_configuration(config_path)
        self.llm = self.initialize_azure_openai()
        self.metrics = IncidentMetrics()
        self.generated_incidents: List[EnhancedIncidentRecord] = []
        self.cache = {}
        
        # Production settings
        self.max_retries = kwargs.get('max_retries', 3)
        self.retry_delay = kwargs.get('retry_delay', 1.0)
        self.batch_size = kwargs.get('batch_size', 10)
        self.enable_caching = kwargs.get('enable_caching', True)
        
        self.logger.info("Golden Incident Generator v2.0 initialized successfully")
        
    def setup_logging(self, log_level: str = "INFO", **kwargs):
        """Configure production-grade logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"golden_incident_generator_{timestamp}.log"
        
        # Configure logging format
        log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
        
        # Setup handlers
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Always log DEBUG to file
        handlers = [file_handler]

        if kwargs.get('console_output', True):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_level.upper()))
            handlers.append(console_handler)

        logging.basicConfig(
            level=logging.DEBUG,  # Set root logger to DEBUG
            format=log_format,
            handlers=handlers,
            force=True
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Logging initialized - Log file: {log_file}")
        
    def load_configuration(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration with fallback to defaults"""
        if config_path is None:
            config_path = Path(__file__).parent / "enhanced_incident_config.json"
        else:
            config_path = Path(config_path)
            
        # Try to load existing config
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Configuration loaded from {config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")
                
        # Create default configuration
        self.logger.info("Creating default configuration...")
        default_config = self.create_default_configuration()
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Default configuration saved to {config_path}")
        except Exception as e:
            self.logger.warning(f"Failed to save default config: {e}")
            
        return default_config
        
    def create_default_configuration(self) -> Dict[str, Any]:
        """Create comprehensive default configuration (aligned with enhanced_incident_config.json)"""
        return {
            "__doc__": "Central configuration for synthetic ServiceNow incident generation. Edit pools and settings below to control the realism and variability of generated incidents. See docs/CONFIG_GUIDE.md for field explanations.",
            "config_version": "2.1.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "company_name": "Abstergo Industries",
            "business_domain": "Technology",
            "technical_environment": "Azure cloud environment with hybrid connectivity, Microsoft 365, Azure Active Directory, IKON Knowledge Base, and ServiceNow ITSM",
            "generation_settings": {
                "default_batch_size": 50,
                "max_retries": 3,
                "retry_delay": 1.0,
                "enable_progress_tracking": True,
                "enable_detailed_logging": True,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "default_settings": {
                "assignment_groups": ["Golden_Incident_Management", "IT Support", "Network Operations", "Service Desk"],
                "assigned_to_pool": ["Alex Chen", "Sarah Johnson", "Mike Rodriguez", "David Park", "Emily Davis", "James Wilson", "Lisa Park", "Kevin Zhang"],
                "caller_pool": ["Jane Doe", "John Smith", "Emily Davis", "Michael Brown", "Hans Havlik"],
                "requestor_email_domain": "abstergo.com",
                "configuration_items": ["AMO", "CRM", "Email Gateway", "VPN Appliance", "Database Cluster"],
                "close_code_options": ["Closed/Resolved", "Closed/Cancelled", "Closed/No Fault Found"],
                "default_state": "Closed"
            },
            "work_notes_templates": [
                "User reported issue resolved after cache clear.",
                "Rebooted affected server and confirmed service restoration.",
                "Coordinated with network team for firewall rule update.",
                "Provided user with workaround pending permanent fix.",
                "Escalated to vendor for further analysis.",
                "User confirmed resolution and no further issues."
            ],
            "close_notes_templates": [
                "Incident resolved by applying latest security patch.",
                "Root cause identified as misconfigured DNS entry.",
                "User training provided to prevent recurrence.",
                "Hardware component replaced and system tested successfully.",
                "No fault found after extensive diagnostics; monitoring ongoing."
            ],
            "trending_issues": [
                "VPN connectivity failures",
                "Phishing email reports",
                "Outlook synchronization delays",
                "Database performance degradation"
            ],
            "custom_fields": {
                "location": ["New York", "London", "Berlin", "Bangalore", "Remote"],
                "region": ["Americas", "EMEA", "APAC"]
            },
            "technician_specializations": {
                "Hardware": ["Alex Chen", "Sarah Johnson", "Mike Rodriguez", "David Park"],
                "Software": ["Emily Davis", "James Wilson", "Lisa Park", "Kevin Zhang"],
                "Network": ["David Kim", "Anna Schmidt", "Carlos Lopez", "Rachel Turner"],
                "Security": ["Rachel Green", "Tom Anderson", "Maya Patel", "Ahmed Ali"],
                "Database": ["Kevin Liu", "Sophie Brown", "Ahmed Hassan", "Maria Garcia"],
                "Email": ["Jennifer Smith", "Mark Taylor", "Priya Sharma", "Chris Johnson"]
            },
            "business_domains": {
                "Technology": {
                    "departments": ["Engineering", "DevOps", "Product", "QA", "Architecture", "Data Science"],
                    "common_technologies": ["Azure", "Kubernetes", "Docker", "CI/CD", "Microservices", "React", "Node.js"],
                    "compliance_requirements": ["SOC2", "GDPR", "HIPAA", "ISO 27001"]
                },
                "Financial Services": {
                    "departments": ["Trading", "Risk Management", "Compliance", "Operations", "IT", "Quantitative Analysis"],
                    "common_technologies": ["Trading Platforms", "Risk Systems", "Core Banking", "Payment Processing", "Bloomberg Terminal"],
                    "compliance_requirements": ["SOX", "PCI-DSS", "Basel III", "MiFID II", "GDPR"]
                },
                "Healthcare": {
                    "departments": ["Clinical", "Administration", "IT", "Compliance", "Research", "Patient Services"],
                    "common_technologies": ["EMR", "PACS", "Laboratory Systems", "Telehealth", "Medical Devices"],
                    "compliance_requirements": ["HIPAA", "HITECH", "FDA", "GDPR", "ISO 13485"]
                },
                "Manufacturing": {
                    "departments": ["Production", "Quality", "Logistics", "Maintenance", "IT", "Supply Chain"],
                    "common_technologies": ["ERP", "MES", "SCADA", "PLM", "IoT Sensors", "Robotics"],
                    "compliance_requirements": ["ISO 9001", "ISO 14001", "OSHA", "FDA", "CE Marking"]
                },
                "Retail": {
                    "departments": ["Sales", "Marketing", "Inventory", "Customer Service", "IT", "E-commerce"],
                    "common_technologies": ["POS Systems", "E-commerce", "Inventory Management", "CRM", "Analytics"],
                    "compliance_requirements": ["PCI-DSS", "GDPR", "CCPA", "SOX", "FTC Guidelines"]
                }
            },
            "incident_categories": {
                "Hardware": {
                    "Desktop Workstation": [
                        "Boot Issues", "Power Supply", "Memory", "Hard Drive", "Graphics Card", "Motherboard", "CPU", "Optical Drive", "USB Ports", "Cooling Fan"
                    ],
                    "Laptop": [
                        "Battery", "Screen", "Keyboard", "Performance", "Overheating", "Trackpad", "Webcam", "Audio", "WiFi Card", "Docking Station"
                    ],
                    "Server": [
                        "Hardware Failure", "Performance", "Storage", "Network Card", "Memory", "Power Supply", "RAID Controller", "Cooling", "Motherboard", "CPU"
                    ],
                    "Network Equipment": [
                        "Switch", "Router", "Firewall", "Wireless Access Point", "Cable", "Load Balancer", "Modem", "Hub", "Patch Panel", "UPS"
                    ],
                    "Printer": [
                        "Paper Jam", "Toner", "Connectivity", "Print Quality", "Driver Issues", "Network Setup", "Hardware Failure", "Configuration", "Maintenance", "Scanner Issues"
                    ]
                },
                "Software": {
                    "Operating System": ["Windows Update", "Boot Issues", "Performance", "Blue Screen", "Drivers", "Registry", "File System", "Services"],
                    "Applications": ["Office Suite", "Database", "Email Client", "Web Browser", "Custom Software", "ERP System", "CRM", "CAD Software"],
                    "Security Software": ["Antivirus", "Firewall", "VPN", "Encryption", "Authentication", "Endpoint Protection", "Backup Software", "Monitoring Tools"]
                },
                "Network": {
                    "Connectivity": ["Internet Access", "Local Network", "VPN", "WiFi", "Ethernet", "DNS Resolution", "DHCP", "Gateway"],
                    "Performance": ["Slow Connection", "Bandwidth", "Latency", "Packet Loss", "DNS", "Throughput", "Jitter", "Congestion"],
                    "Remote Access": ["VPN Issues", "RDP", "SSH", "Authentication", "Permissions", "Terminal Services", "Citrix", "VNC"]
                },
                "Security": {
                    "Access Control": ["Password Reset", "Account Lockout", "Permissions", "Multi-factor Auth", "Single Sign-On", "Role Assignment", "Group Membership", "Privileged Access"],
                    "Incidents": ["Malware", "Phishing", "Data Breach", "Unauthorized Access", "Security Alert", "Virus Detection", "Suspicious Activity", "Policy Violation"],
                    "Compliance": ["Audit", "Policy Violation", "Data Classification", "Encryption", "Backup", "Retention", "Access Review", "Certification"]
                },
                "Database": {
                    "Performance": ["Slow Queries", "Deadlocks", "Connection Issues", "Timeout", "Memory Usage", "CPU Usage", "Index Issues", "Blocking"],
                    "Availability": ["Database Down", "Connection Failed", "Service Restart", "Failover", "Backup Issues", "Recovery", "Replication", "Clustering"],
                    "Data": ["Corruption", "Missing Data", "Incorrect Data", "Import Issues", "Export Issues", "Synchronization", "Migration", "Transformation"]
                },
                "Email": {
                    "Delivery": ["Cannot Send", "Cannot Receive", "Delayed Delivery", "Bounced Messages", "Spam Issues", "Attachment Issues", "Size Limits", "Queue Issues"],
                    "Client Issues": ["Outlook Crashes", "Configuration", "Profile Corruption", "OST Issues", "Synchronization", "Add-ins", "Performance", "Search Issues"],
                    "Server Issues": ["Exchange Down", "Mailbox Issues", "Storage Limits", "Transport Issues", "Certificate Issues", "Authentication", "Database Issues", "Backup Issues"]
                }
            },
            "priority_distribution": {
                "1 - Critical": 8,
                "2 - High": 22,
                "3 - Moderate": 55,
                "4 - Low": 15
            },
            "state_distribution": {
                "Closed": 100
            },
            "impact_urgency_matrix": {
                "1 - Critical": {"impact": "1 - High", "urgency": "1 - High"},
                "2 - High": {"impact": "2 - Medium", "urgency": "2 - Medium"},
                "3 - Moderate": {"impact": "2 - Medium", "urgency": "3 - Low"},
                "4 - Low": {"impact": "3 - Low", "urgency": "3 - Low"}
            },
            "resolution_categories": [
                "Configuration", "Software Update", "Hardware Replacement", "User Training", "Process Improvement", "Security Patch", "Network Reconfiguration", "Database Optimization", "Application Restart", "Cache Clearing", "Permission Update", "System Reboot", "Driver Update", "Firewall Rule", "DNS Configuration"
            ],
            "business_impact_levels": ["Low", "Medium", "High", "Critical"],
            "escalation_triggers": {
                "priority_1_time_limit": 60,
                "priority_2_time_limit": 240,
                "priority_3_time_limit": 1440,
                "priority_4_time_limit": 4320,
                "customer_escalation_keywords": [
                    "escalate", "manager", "urgent", "critical", "emergency", "outage"
                ]
            },
            "quality_metrics": {
                "min_description_length": 200,
                "max_description_length": 1000,
                "min_work_notes": 3,
                "max_work_notes": 7,
                "min_close_notes_length": 100,
                "max_close_notes_length": 500,
                "required_technical_keywords": 3
            },
            "user_personas": {
                "Executive": [
                    "CEO", "CTO", "CFO", "VP Engineering", "Director of Operations", "VP Sales", "Chief Data Officer", "VP Product"
                ],
                "Manager": [
                    "Department Head", "Team Lead", "Project Manager", "Product Manager", "Engineering Manager", "Sales Manager", "Operations Manager", "Quality Manager"
                ],
                "Technical": [
                    "Software Engineer", "DevOps Engineer", "Data Scientist", "System Administrator", "Database Administrator", "Security Engineer", "Network Engineer", "Cloud Architect"
                ],
                "Business": [
                    "Business Analyst", "Sales Representative", "Marketing Specialist", "Customer Success", "Product Owner", "Account Manager", "Financial Analyst", "Operations Specialist"
                ],
                "Support": [
                    "Help Desk Technician", "Customer Support", "Technical Writer", "QA Engineer", "IT Support", "Field Service", "Training Coordinator", "Documentation Specialist"
                ],
                "Administrative": [
                    "HR Specialist", "Finance Analyst", "Administrative Assistant", "Facilities Coordinator", "Procurement Specialist", "Legal Assistant", "Executive Assistant", "Office Manager"
                ]
            }
        }
        
    def initialize_azure_openai(self) -> AzureChatOpenAI:
        """Initialize Azure OpenAI client with environment variables"""
        try:
            # Get Azure OpenAI configuration from environment variables
            azure_config = {
                'azure_endpoint': AZURE_OPENAI_ENDPOINT,
                'api_key': AZURE_OPENAI_KEY,
                'api_version': AZURE_OPENAI_API_VERSION,
                'model': AZURE_OPENAI_DEPLOYMENT_NAME,
                'temperature': self.config.get('generation_settings', {}).get('temperature', 0.7),
                'max_tokens': self.config.get('generation_settings', {}).get('max_tokens', 2000)
            }
            
            # Initialize Azure Chat OpenAI
            llm = AzureChatOpenAI(
                azure_endpoint=azure_config['azure_endpoint'],
                api_key=azure_config['api_key'],
                api_version=azure_config['api_version'],
                model=azure_config['model'],
                temperature=azure_config['temperature'],
                max_tokens=azure_config['max_tokens']
            )
            
            self.logger.info(f"Azure OpenAI initialized - Model: {azure_config['model']}")
            return llm
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure OpenAI: {e}")
            raise
            
    def generate_incident_context(self) -> Dict[str, Any]:
        """Generate random incident context with enhanced business alignment and global variables"""
        config = self.config
        default_settings = config.get('default_settings', {})
        # Select category and subcategory
        category = random.choice(list(config['incident_categories'].keys()))
        subcategory_dict = config['incident_categories'][category]
        subcategory = random.choice(list(subcategory_dict.keys()))
        triage_tag = random.choice(subcategory_dict[subcategory])
        # Select priority based on distribution
        priority_choices = list(config['priority_distribution'].keys())
        priority_weights = list(config['priority_distribution'].values())
        priority = random.choices(priority_choices, weights=priority_weights)[0]
        # Always set state to default_state
        state = default_settings.get('default_state', 'Closed')
        # Select business domain and department
        business_domain = random.choice(list(config['business_domains'].keys()))
        departments = config['business_domains'][business_domain]['departments']
        department = random.choice(departments)
        # Select user persona
        persona_categories = list(config['user_personas'].keys())
        persona_category = random.choice(persona_categories)
        user_roles = config['user_personas'][persona_category]
        user_role = random.choice(user_roles)
        # Select assignment group, assigned_to, caller, configuration item, close code
        assignment_group = random.choice(default_settings.get('assignment_groups', ['Golden_Incident_Management']))
        assigned_to = random.choice(default_settings.get('assigned_to_pool', ['Hans Havlik']))
        caller = random.choice(default_settings.get('caller_pool', ['Hans Havlik']))
        configuration_item = random.choice(default_settings.get('configuration_items', ['AMO']))
        close_code = random.choice(default_settings.get('close_code_options', ['Closed/Resolved']))
        # Generate requestor email from caller and domain
        email_domain = default_settings.get('requestor_email_domain', 'abstergo.com')
        requestor_email = f"{caller.lower().replace(' ', '.')}@{email_domain}"
        # Add custom fields
        custom_fields = {}
        for field, values in config.get('custom_fields', {}).items():
            custom_fields[field] = random.choice(values)
        # Trending issue injection (10% chance)
        trending_issue = None
        if 'trending_issues' in config and random.random() < 0.1:
            trending_issue = random.choice(config['trending_issues'])
        return {
            'company_name': config['company_name'],
            'business_domain': business_domain,
            'category': category,
            'subcategory': subcategory,
            'triage_tag': triage_tag,
            'priority': priority,
            'state': state,
            'department': department,
            'user_role': user_role,
            'user_name': caller,
            'persona_category': persona_category,
            'technical_environment': config.get('technical_environment', 'Standard enterprise environment'),
            'assignment_group': assignment_group,
            'assigned_to': assigned_to,
            'configuration_item': configuration_item,
            'caller': caller,
            'requestor_email': requestor_email,
            'close_code': close_code,
            'custom_fields': custom_fields,
            'trending_issue': trending_issue
        }

    def generate_single_incident(self, context: Dict[str, Any], retries: int = 0) -> Optional[EnhancedIncidentRecord]:
        """Generate a single incident with retry logic and error handling"""
        start_time = time.time()
        try:
            # Generate robust, field-driven prompt
            prompt = get_enhanced_prompt(context)
            messages = [HumanMessage(content=prompt)]
            # Generate incident with token tracking
            with get_openai_callback() as cb:
                response = self.llm(messages)
                self.metrics.total_tokens_used += cb.total_tokens
                self.metrics.cost_estimate += cb.total_cost if hasattr(cb, 'total_cost') else 0
            # Parse response
            incident_data = self.parse_llm_response(response.content, context)
            if incident_data:
                # Use work_notes_templates and close_notes_templates
                config = self.config
                qmetrics = config.get('quality_metrics', {})
                # Work notes
                min_notes = qmetrics.get('min_work_notes', 3)
                max_notes = qmetrics.get('max_work_notes', 7)
                num_notes = random.randint(min_notes, max_notes)
                work_notes_templates = config.get('work_notes_templates', [])
                if work_notes_templates:
                    incident_data['work_notes'] = [random.choice(work_notes_templates) for _ in range(num_notes)]
                # Close notes
                min_close = qmetrics.get('min_close_notes_length', 100)
                max_close = qmetrics.get('max_close_notes_length', 500)
                close_notes_templates = config.get('close_notes_templates', [])
                if close_notes_templates:
                    close_note = random.choice(close_notes_templates)
                    # Pad/trim to length
                    if len(close_note) < min_close:
                        close_note = close_note + ' ' + ('.' * (min_close - len(close_note)))
                    incident_data['close_notes'] = close_note[:max_close]
                # Trending issue injection
                if context.get('trending_issue'):
                    if 'short_description' in incident_data:
                        incident_data['short_description'] = f"{context['trending_issue']} - {incident_data['short_description']}"
                    if 'description' in incident_data:
                        incident_data['description'] = f"{context['trending_issue']}: {incident_data['description']}"
                # Add custom fields
                if 'custom_fields' in context:
                    for k, v in context['custom_fields'].items():
                        incident_data[k] = v
                incident_record = self.create_incident_record(incident_data, context)
                generation_time = time.time() - start_time
                self.logger.debug(f"Generated incident in {generation_time:.2f}s - Category: {context['category']}")
                return incident_record
            else:
                raise ValueError("Failed to parse LLM response")
        except Exception as e:
            self.logger.warning(f"Generation attempt {retries + 1} failed: {e}")
            if retries < self.max_retries:
                time.sleep(self.retry_delay * (retries + 1))  # Exponential backoff
                return self.generate_single_incident(context, retries + 1)
            else:
                self.logger.error(f"Failed to generate incident after {self.max_retries} retries")
                self.metrics.total_failed += 1
                return None
                
    def fix_llm_json_artifacts(self, text: str) -> str:
        """Fix unescaped double quotes inside string values and common LLM artifacts in JSON text."""
        import re
        # Replace user"s with user's (common LLM artifact)
        text = re.sub(r'user"s', "user's", text)
        text = re.sub(r'([A-Za-z])"([A-Za-z])', r"\1'\2", text)  # e.g., team"s -> team's

        # Regex to find string values in JSON and escape unescaped double quotes inside them
        def escape_quotes_in_string(match):
            s = match.group(0)
            # Remove the surrounding quotes
            inner = s[1:-1]
            # Escape only double quotes that are not already escaped
            # (negative lookbehind for backslash)
            inner = re.sub(r'(?<!\\)"', r'\\"', inner)
            return '"' + inner + '"'

        # This regex matches JSON string values (handles escaped quotes inside)
        string_regex = r'"((?:[^"\\]|\\.)*)"'
        text = re.sub(string_regex, escape_quotes_in_string, text)
        return text

    def parse_llm_response(self, response_text: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse LLM response with robust tolerant JSON parsing and error handling"""
        import re
        try:
            response_text = response_text.strip()
            self.logger.debug(f"Raw LLM response: {response_text[:1000]}")

            # Remove markdown code block markers
            response_text = re.sub(r"^```(json)?", "", response_text, flags=re.IGNORECASE).strip()
            response_text = re.sub(r"```$", "", response_text).strip()
            # Extract the largest {...} block
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if match:
                response_text = match.group(0)
            # Replace smart quotes
            response_text = response_text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
            # Remove trailing commas
            response_text = re.sub(r",\s*([}}\]])", r"\1", response_text)

            # Try tolerant parsing with demjson3 if available
            try:
                import demjson3
                incident_data = demjson3.decode(response_text)
            except Exception:
                # Fallback: fix artifacts and use standard json
                response_text = self.fix_llm_json_artifacts(response_text)
                incident_data = json.loads(response_text)

            # Validate required fields
            required_fields = ['short_description', 'description', 'work_notes', 'close_notes']
            for field in required_fields:
                if field not in incident_data or not incident_data[field]:
                    self.logger.warning(f"LLM response missing required field: {field}. Full response: {incident_data}")
                    raise ValueError(f"Missing required field: {field}")

            return incident_data

        except Exception as e:
            self.logger.error(f"LLM JSON parsing error: {e}")
            self.logger.error(f"Failed to parse response: {response_text}")
            self.logger.debug(traceback.format_exc())
            return None
            
    def create_incident_record(self, incident_data: Dict[str, Any], context: Dict[str, Any]) -> EnhancedIncidentRecord:
        """Create enhanced incident record with comprehensive metadata"""
        import re
        # Clean up close_notes: remove trailing repeated periods (3 or more) and whitespace
        close_notes_raw = incident_data.get('close_notes', '')
        close_notes_clean = re.sub(r'[.\s]{3,}$', '', close_notes_raw).rstrip()
        # Generate incident number
        incident_number = f"INC{random.randint(1000000, 9999999):07d}"
        # Get assigned technician based on category specialization
        assigned_to = self.get_specialized_technician(context['category'])
        # Generate timestamps
        timestamps = self.generate_realistic_timestamps(context['priority'], context['state'])
        # Format work notes
        work_notes_formatted = self.format_work_notes(
            incident_data.get('work_notes', []), 
            timestamps, 
            assigned_to
        )
        # Extract technical keywords
        technical_keywords = self.extract_technical_keywords(incident_data)
        # Determine complexity and escalation level
        complexity = self.determine_incident_complexity(context, incident_data)
        escalation_level = self.determine_escalation_level(context, complexity)
        return EnhancedIncidentRecord(
            # Core ServiceNow fields
            number=incident_number,
            short_description=incident_data.get('short_description', ''),
            description=incident_data.get('description', ''),
            assignment_group=context['assignment_group'],
            assigned_to=assigned_to,
            state=context['state'],
            parent="",
            configuration_item=context['configuration_item'],
            impact=self.get_impact_from_priority(context['priority']),
            urgency=self.get_urgency_from_priority(context['priority']),
            priority=context['priority'],
            category=context['category'],
            subcategory=context['subcategory'],
            close_notes=close_notes_clean,
            resolved_by=assigned_to if context['state'] in ['Resolved', 'Closed'] else "",
            work_notes=work_notes_formatted,
            comments_and_work_notes=work_notes_formatted,
            opened_by=context['user_name'],
            created=timestamps['created'],
            resolve_time=timestamps.get('resolved', ''),
            closed=timestamps.get('closed', ''),
            caller=context['user_name'],
            requestor_email=f"{context['user_name'].lower().replace(' ', '.')}@{self.config['company_name'].lower().replace(' ', '')}.com",
            close_code=context['close_code'],
            # Enhanced metadata fields
            business_impact_level=incident_data.get('business_impact_level', 'Medium'),
            resolution_category=incident_data.get('resolution_category', 'Configuration'),
            technical_keywords=technical_keywords,
            user_department=context['department'],
            user_role=context['user_role'],
            business_domain=context['business_domain'],
            incident_complexity=complexity,
            escalation_level=escalation_level,
            user_persona=context['persona_category'],
            ai_confidence_score=random.uniform(0.85, 0.98),  # Simulated confidence
            generation_timestamp=datetime.now().isoformat(),
            model_version=AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
    def get_specialized_technician(self, category: str) -> str:
        """Get specialized technician based on incident category"""
        specializations = self.config.get('technician_specializations', {})
        
        if category in specializations:
            return random.choice(specializations[category])
        else:
            return self.config['default_settings']['assigned_to']
            
    def generate_realistic_timestamps(self, priority: str, state: str) -> Dict[str, str]:
        """Generate realistic timestamps based on priority and state"""
        base_time = datetime.now() - timedelta(days=random.randint(1, 30))
        
        # Priority-based resolution times (in hours)
        resolution_times = {
            "1 - Critical": random.uniform(0.5, 4),
            "2 - High": random.uniform(2, 24),
            "3 - Moderate": random.uniform(4, 72),
            "4 - Low": random.uniform(8, 168)
        }
        
        timestamps = {
            'created': base_time.isoformat()
        }
        
        if state in ['In Progress', 'Pending', 'Resolved', 'Closed']:
            resolution_hours = resolution_times.get(priority, 24)
            resolved_time = base_time + timedelta(hours=resolution_hours)
            timestamps['resolved'] = resolved_time.isoformat()
            
        if state == 'Closed':
            # Closed 30 minutes to 2 hours after resolution
            close_delay = timedelta(minutes=random.randint(30, 120))
            closed_time = datetime.fromisoformat(timestamps['resolved']) + close_delay
            timestamps['closed'] = closed_time.isoformat()
            
        return timestamps
        
    def format_work_notes(self, work_notes: List[str], timestamps: Dict[str, str], assigned_to: str) -> str:
        """Format work notes with timestamps and technician information"""
        if not work_notes:
            return ""
            
        formatted_notes = []
        base_time = datetime.fromisoformat(timestamps['created'])
        
        for i, note in enumerate(work_notes):
            # Calculate realistic timestamp for each note
            if i == 0:
                note_time = base_time + timedelta(minutes=random.randint(2, 10))
            else:
                note_time = base_time + timedelta(minutes=random.randint(15, 180) * (i + 1))
                
            timestamp_str = note_time.strftime('%Y-%m-%d %H:%M:%S')
            formatted_note = f"[{timestamp_str}] {assigned_to}: {note}"
            formatted_notes.append(formatted_note)
            
        return "\n\n".join(formatted_notes)
        
    def extract_technical_keywords(self, incident_data: Dict[str, Any]) -> str:
        """Extract and format technical keywords from incident data"""
        keywords = incident_data.get('technical_keywords', [])
        if isinstance(keywords, list):
            return ", ".join(keywords)
        return str(keywords)
        
    def determine_incident_complexity(self, context: Dict[str, Any], incident_data: Dict[str, Any]) -> str:
        """Determine incident complexity based on context and content"""
        complexity_factors = 0
        
        # Priority factor
        if context['priority'] == "1 - Critical":
            complexity_factors += 3
        elif context['priority'] == "2 - High":
            complexity_factors += 2
        elif context['priority'] == "3 - Moderate":
            complexity_factors += 1
            
        # Category factor
        complex_categories = ['Database', 'Security', 'Network']
        if context['category'] in complex_categories:
            complexity_factors += 2
            
        # Description length factor
        description_length = len(incident_data.get('description', ''))
        if description_length > 1000:
            complexity_factors += 2
        elif description_length > 500:
            complexity_factors += 1
            
        # Work notes count factor
        work_notes_count = len(incident_data.get('work_notes', []))
        if work_notes_count > 5:
            complexity_factors += 2
        elif work_notes_count > 3:
            complexity_factors += 1
            
        # Determine complexity level
        if complexity_factors >= 6:
            return "High"
        elif complexity_factors >= 3:
            return "Medium"
        else:
            return "Low"
            
    def determine_escalation_level(self, context: Dict[str, Any], complexity: str) -> str:
        """Determine escalation level based on context and complexity"""
        if context['priority'] == "1 - Critical" and complexity == "High":
            return "Level 3"
        elif context['priority'] in ["1 - Critical", "2 - High"] or complexity == "High":
            return "Level 2"
        else:
            return "Level 1"
            
    def get_impact_from_priority(self, priority: str) -> str:
        """Map priority to impact level"""
        mapping = {
            "1 - Critical": "1 - High",
            "2 - High": "2 - Medium",
            "3 - Moderate": "3 - Low",
            "4 - Low": "3 - Low"
        }
        return mapping.get(priority, "3 - Low")
        
    def get_urgency_from_priority(self, priority: str) -> str:
        """Map priority to urgency level"""
        mapping = {
            "1 - Critical": "1 - High",
            "2 - High": "2 - Medium",
            "3 - Moderate": "2 - Medium",
            "4 - Low": "3 - Low"
        }
        return mapping.get(priority, "3 - Low")
        
    def generate_batch(self, count: int, progress_callback: Optional[callable] = None) -> List[EnhancedIncidentRecord]:
        """Generate a batch of incidents with progress tracking"""
        self.logger.info(f"Starting batch generation of {count} incidents...")
        
        batch_start_time = time.time()
        incidents = []
        
        # Update metrics
        self.metrics.total_requested += count
        
        for i in range(count):
            try:
                # Generate incident context
                context = self.generate_incident_context()
                
                # Generate incident
                incident = self.generate_single_incident(context)
                
                if incident:
                    incidents.append(incident)
                    self.generated_incidents.append(incident)
                    self.metrics.total_generated += 1
                    
                    # Update distribution metrics
                    self.update_distribution_metrics(context)
                    
                    self.logger.debug(f"Generated incident {i + 1}/{count}: {incident.number}")
                else:
                    self.logger.warning(f"Failed to generate incident {i + 1}/{count}")
                    
                # Progress callback
                if progress_callback:
                    progress_callback(i + 1, count)
                    
            except Exception as e:
                self.logger.error(f"Unexpected error generating incident {i + 1}: {e}")
                self.metrics.total_failed += 1
                
        # Update final metrics
        batch_time = time.time() - batch_start_time
        self.metrics.success_rate = (self.metrics.total_generated / self.metrics.total_requested) * 100
        self.metrics.avg_generation_time = batch_time / count if count > 0 else 0
        
        self.logger.info(f"Batch generation completed: {len(incidents)} incidents generated in {batch_time:.2f}s")
        
        return incidents
        
    def update_distribution_metrics(self, context: Dict[str, Any]):
        """Update distribution metrics for analytics"""        # Category distribution
        category = context['category']
        self.metrics.category_distribution[category] = self.metrics.category_distribution.get(category, 0) + 1
        
        # Priority distribution
        priority = context['priority']
        self.metrics.priority_distribution[priority] = self.metrics.priority_distribution.get(priority, 0) + 1
        
        # Department distribution
        department = context['department']
        self.metrics.department_distribution[department] = self.metrics.department_distribution.get(department, 0) + 1
        
    def export_to_csv(self, filename: Optional[str] = None, include_metadata: bool = True) -> str:
        """Export incidents to CSV format"""
        if not self.generated_incidents:
            raise ValueError("No incidents to export")
            
        # Ensure output directory exists
        output_dir = Path("synthetic_data_output")
        output_dir.mkdir(exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"golden_incidents_{timestamp}.csv"
            
        # Ensure filename includes the output directory
        if not str(filename).startswith("synthetic_data_output"):
            filename = output_dir / filename
            
        # Convert incidents to dictionaries
        incidents_data = []
        for incident in self.generated_incidents:
            incident_dict = asdict(incident)
            
            # Optionally exclude metadata fields
            if not include_metadata:
                metadata_fields = [
                    'business_impact_level', 'resolution_category', 'technical_keywords',
                    'user_department', 'user_role', 'business_domain', 'incident_complexity',
                    'escalation_level', 'user_persona', 'ai_confidence_score',
                    'generation_timestamp', 'model_version'
                ]
                for field in metadata_fields:
                    incident_dict.pop(field, None)
                    
            incidents_data.append(incident_dict)
              # Write to CSV
        output_path = Path(filename)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            if incidents_data:
                fieldnames = incidents_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(incidents_data)
                
        self.logger.info(f"Exported {len(self.generated_incidents)} incidents to {output_path}")
        return str(output_path)
        
    def export_to_json(self, filename: Optional[str] = None, include_metadata: bool = True) -> str:
        """Export incidents to JSON format with metadata"""
        if not self.generated_incidents:
            raise ValueError("No incidents to export")
            
        # Ensure output directory exists
        output_dir = Path("synthetic_data_output")
        output_dir.mkdir(exist_ok=True)
            
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"golden_incidents_{timestamp}.json"
        
        # Ensure filename includes the output directory
        if not str(filename).startswith("synthetic_data_output"):
            filename = output_dir / filename
            
        # Prepare export data
        export_data = {
            "metadata": {
                "generation_timestamp": datetime.now().isoformat(),
                "total_incidents": len(self.generated_incidents),
                "generator_version": "2.0.0",
                "model_version": AZURE_OPENAI_DEPLOYMENT_NAME,
                "config": {
                    "company_name": self.config['company_name'],
                    "business_domain": self.config['business_domain']
                },
                "metrics": asdict(self.metrics)
            },
            "incidents": []
        }
        
        # Convert incidents to dictionaries
        for incident in self.generated_incidents:
            incident_dict = asdict(incident)
            
            # Optionally exclude metadata fields
            if not include_metadata:
                metadata_fields = [
                    'ai_confidence_score', 'generation_timestamp', 'model_version'
                ]
                for field in metadata_fields:
                    incident_dict.pop(field, None)
                    
            export_data["incidents"].append(incident_dict)
              # Write to JSON
        output_path = Path(filename)
        with open(output_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False, default=str)
            
        self.logger.info(f"Exported {len(self.generated_incidents)} incidents to {output_path}")
        return str(output_path)
        
    def export_to_excel(self, filename: Optional[str] = None, include_analytics: bool = True) -> str:
        """Export incidents to Excel format with multiple sheets"""
        if not self.generated_incidents:
            raise ValueError("No incidents to export")
            
        # Ensure output directory exists
        output_dir = Path("synthetic_data_output")
        output_dir.mkdir(exist_ok=True)
            
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"golden_incidents_{timestamp}.xlsx"
        
        # Ensure filename includes the output directory
        if not str(filename).startswith("synthetic_data_output"):
            filename = output_dir / filename
            
        # Convert incidents to DataFrame
        incidents_data = [asdict(incident) for incident in self.generated_incidents]
        df_incidents = pd.DataFrame(incidents_data)
        
        # Create Excel writer
        output_path = Path(filename)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Main incidents sheet
            df_incidents.to_excel(writer, sheet_name='Incidents', index=False)
            
            if include_analytics:
                # Metrics sheet
                metrics_data = asdict(self.metrics)
                df_metrics = pd.DataFrame([metrics_data])
                df_metrics.to_excel(writer, sheet_name='Metrics', index=False)
                
                # Category distribution
                if self.metrics.category_distribution:
                    df_categories = pd.DataFrame(
                        list(self.metrics.category_distribution.items()),
                        columns=['Category', 'Count']
                    )
                    df_categories.to_excel(writer, sheet_name='Category_Distribution', index=False)
                
                # Priority distribution
                if self.metrics.priority_distribution:
                    df_priorities = pd.DataFrame(
                        list(self.metrics.priority_distribution.items()),
                        columns=['Priority', 'Count']
                    )
                    df_priorities.to_excel(writer, sheet_name='Priority_Distribution', index=False)
                
                # Department distribution
                if self.metrics.department_distribution:
                    df_departments = pd.DataFrame(
                        list(self.metrics.department_distribution.items()),
                        columns=['Department', 'Count']
                    )
                    df_departments.to_excel(writer, sheet_name='Department_Distribution', index=False)
                    
        self.logger.info(f"Exported {len(self.generated_incidents)} incidents to {output_path}")
        return str(output_path)
        
    def print_generation_summary(self):
        """Print comprehensive generation summary"""
        print("\n" + "="*80)
        print("GOLDEN INCIDENT GENERATOR v2.0 - GENERATION SUMMARY")
        print("="*80)
        
        print(f"\nGENERATION STATISTICS:")
        print(f"  Total Requested: {self.metrics.total_requested}")
        print(f"  Successfully Generated: {self.metrics.total_generated}")
        print(f"  Failed: {self.metrics.total_failed}")
        print(f"  Success Rate: {self.metrics.success_rate:.1f}%")
        print(f"  Average Generation Time: {self.metrics.avg_generation_time:.2f}s per incident")
        
        print(f"\nAZURE OPENAI USAGE:")
        print(f"  Total Tokens Used: {self.metrics.total_tokens_used:,}")
        print(f"  Estimated Cost: ${self.metrics.cost_estimate:.4f}")
        
        if self.metrics.category_distribution:
            print(f"\nCATEGORY DISTRIBUTION:")
            for category, count in sorted(self.metrics.category_distribution.items()):
                percentage = (count / self.metrics.total_generated) * 100
                print(f"  {category}: {count} ({percentage:.1f}%)")
                
        if self.metrics.priority_distribution:
            print(f"\nPRIORITY DISTRIBUTION:")
            for priority, count in sorted(self.metrics.priority_distribution.items()):
                percentage = (count / self.metrics.total_generated) * 100
                print(f"  {priority}: {count} ({percentage:.1f}%)")
                
        if self.metrics.department_distribution:
            print(f"\nDEPARTMENT DISTRIBUTION:")
            for department, count in sorted(self.metrics.department_distribution.items()):
                percentage = (count / self.metrics.total_generated) * 100
                print(f"  {department}: {count} ({percentage:.1f}%)")
                
        print("\n" + "="*80)
        

def main():
    """Main function with comprehensive CLI interface"""
    parser = argparse.ArgumentParser(
        description="Golden Incident Generator v2.0 - Generate high-quality synthetic ServiceNow incident data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 50 incidents and export to CSV
  python golden_incident_generator_v2.py --count 50 --export csv
  
  # Generate 100 incidents with custom config
  python golden_incident_generator_v2.py --count 100 --config custom_config.json --export excel
  
  # Generate incidents in batches with progress tracking
  python golden_incident_generator_v2.py --count 200 --batch-size 25 --export json --verbose
        """
    )
    
    # Generation arguments
    parser.add_argument('--count', type=int, default=10, 
                       help='Number of incidents to generate (default: 10)')
    parser.add_argument('--batch-size', type=int, default=10,
                       help='Batch size for generation (default: 10)')
    parser.add_argument('--config', type=str,
                       help='Path to configuration file')
    
    # Export arguments
    parser.add_argument('--export', choices=['csv', 'json', 'excel', 'all'], default='csv',
                       help='Export format (default: csv)')
    parser.add_argument('--output', type=str,
                       help='Output filename (without extension)')
    parser.add_argument('--no-metadata', action='store_true',
                       help='Exclude metadata fields from export')
    
    # Generation control arguments
    parser.add_argument('--max-retries', type=int, default=3,
                       help='Maximum retries per incident (default: 3)')
    parser.add_argument('--retry-delay', type=float, default=1.0,
                       help='Delay between retries in seconds (default: 1.0)')
    parser.add_argument('--temperature', type=float, default=0.7,
                       help='LLM temperature (default: 0.7)')
    
    # Logging arguments
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                       help='Logging level (default: INFO)')
    parser.add_argument('--no-console', action='store_true',
                       help='Disable console output')
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = GoldenIncidentGeneratorV2(
            config_path=args.config,
            max_retries=args.max_retries,
            retry_delay=args.retry_delay,
            batch_size=args.batch_size,
            log_level=args.log_level,
            console_output=not args.no_console
        )
        
        # Progress tracking function
        def progress_callback(current, total):
            if not args.no_console:
                percentage = (current / total) * 100
                print(f"\rProgress: {current}/{total} ({percentage:.1f}%)", end='', flush=True)
        
        print(f"\nGenerating {args.count} incidents...")
        start_time = time.time()
        
        # Generate incidents
        incidents = generator.generate_batch(args.count, progress_callback)
        
        generation_time = time.time() - start_time
        
        if not args.no_console:
            print(f"\n\nGeneration completed in {generation_time:.2f} seconds")
            
        # Export results
        if args.export:
            # Always export to all three formats regardless of --export argument
            output_base = args.output or f"synthetic_data_output/golden_incidents_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            csv_file = generator.export_to_csv(output_base + '.csv', not args.no_metadata)
            print(f"Exported to CSV: {csv_file}")
            json_file = generator.export_to_json(output_base + '.json', not args.no_metadata)
            print(f"Exported to JSON: {json_file}")
            excel_file = generator.export_to_excel(output_base + '.xlsx', True)
            print(f"Exported to Excel: {excel_file}")
            # Print summary
            if not args.no_console:
                generator.print_generation_summary()
        else:
            print("No incidents were generated successfully.")
            return 1
            
    except KeyboardInterrupt:
        print("\nGeneration interrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        if args.verbose:
            traceback.print_exc()
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())

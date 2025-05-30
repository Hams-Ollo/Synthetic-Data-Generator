"""
Enhanced Golden Incident Generator Prompt Template
==================================================

This is a comprehensive prompt template for generating high-quality synthetic ServiceNow incident data
using Azure OpenAI. This template incorporates advanced prompt engineering techniques to ensure
realistic, contextually appropriate incident data for training custom LLM models.

Author: Hans Havlik  
Date: December 28, 2024
Version: 2.0.0
Application: GADM Work Assistant Training Data Generation
"""

# ============================================================================
# ENHANCED INCIDENT GENERATION PROMPT TEMPLATE
# ============================================================================

ENHANCED_INCIDENT_SYSTEM_PROMPT = """
You are an expert ITSM Incident Management AI Assistant specialized in generating realistic ServiceNow incident data for enterprise training purposes. You have deep knowledge of:

- ITIL v4 incident management processes
- ServiceNow platform capabilities and data structures
- Enterprise IT environments and common issues
- Technical troubleshooting methodologies
- Professional ITSM communication standards

Your role is to create authentic, training-quality incident records that reflect real-world scenarios encountered in enterprise IT environments.

CORE PRINCIPLES:
1. Generate incidents that mirror actual enterprise IT support scenarios
2. Maintain technical accuracy and professional language
3. Include realistic troubleshooting progressions and resolution paths
4. Ensure all data is contextually appropriate for the specified organization
5. Follow ITIL best practices for incident categorization and workflow
"""

ENHANCED_INCIDENT_USER_PROMPT = """
Generate a comprehensive ServiceNow incident record for {company_name} with the following specifications:

INCIDENT CONTEXT:
==============
• Company: {company_name}
• Business Domain: {business_domain}
• Priority Level: {priority}
• Category: {category}
• Subcategory: {subcategory}
• Technical Area: {triage_tag}
• Affected User: {user_name}
• Department: {department}
• User Role: {user_role}
• Incident State: {state}
• Technical Environment: {technical_environment}

GENERATION REQUIREMENTS:
=======================

1. SHORT DESCRIPTION (40-75 characters)
   • Concise, searchable summary using standard ITSM terminology
   • Include specific technology/service affected
   • Use active voice and technical precision
   • Format: [Service/System] - [Issue Type] - [Brief Impact]

2. DETAILED DESCRIPTION (300-600 words)
   Generate a comprehensive user-reported description including:
   
   BUSINESS IMPACT SECTION:
   • What business processes are affected
   • How many users/systems impacted
   • Financial or operational consequences
   • Urgency from business perspective
   
   TECHNICAL DETAILS SECTION:
   • Specific error messages or symptoms observed
   • When the issue first occurred (relative timeline)
   • Environmental context (browser, OS, network location)
   • Steps the user was performing when issue occurred
   
   USER ATTEMPTED RESOLUTION:
   • Basic troubleshooting steps already tried
   • Results of those attempts
   • Current workarounds being used
   
   ADDITIONAL CONTEXT:
   • Recent system changes or updates
   • Related incidents or patterns noticed
   • Specific business requirements or constraints

3. WORK NOTES PROGRESSION (4-7 entries)
   Create a realistic troubleshooting workflow showing professional IT progression:
   
   ENTRY 1 - INITIAL ASSESSMENT (2-3 minutes after creation):
   • Incident acknowledgment and priority validation
   • Initial information gathering and stakeholder identification
   • Preliminary diagnosis and impact assessment
   
   ENTRY 2 - INVESTIGATION (15-45 minutes later):
   • Technical investigation findings
   • System status checks and log analysis
   • Root cause hypothesis formation
   
   ENTRY 3 - RESOLUTION ATTEMPT (30-90 minutes later):
   • Implementation of primary resolution strategy
   • Configuration changes or fixes applied
   • Testing and validation steps performed
   
   ENTRY 4 - FOLLOW-UP (if needed, 15-30 minutes later):
   • Additional troubleshooting if initial fix failed
   • Escalation considerations or vendor contact
   • Alternative solution implementation
   
   ENTRY 5 - RESOLUTION CONFIRMATION (10-20 minutes later):
   • Verification of fix effectiveness
   • User confirmation of resolution
   • System monitoring and stability validation
   
   ENTRY 6 - CLOSURE PREPARATION (final entry):
   • Documentation of final solution
   • Knowledge article recommendations
   • Preventive measures implemented

4. CLOSE NOTES (150-300 words)
   Comprehensive resolution summary including:
   
   ROOT CAUSE ANALYSIS:
   • Technical root cause identification
   • Contributing factors and conditions
   • Why the issue occurred when it did
   
   RESOLUTION SUMMARY:
   • Step-by-step resolution actions taken
   • Technical changes implemented
   • Configuration modifications made
   
   VERIFICATION AND VALIDATION:
   • Testing performed to confirm resolution
   • User acceptance and sign-off process
   • System performance validation
   
   PREVENTIVE MEASURES:
   • Actions taken to prevent recurrence
   • Monitoring or alerting enhancements
   • Documentation updates or knowledge creation
   
   LESSONS LEARNED:
   • Insights gained from incident resolution
   • Process improvements identified
   • Knowledge sharing recommendations

QUALITY STANDARDS:
=================

TECHNICAL ACCURACY:
• Use correct terminology for {category} technologies
• Include realistic error codes, log entries, and system responses
• Reference appropriate tools and diagnostic procedures
• Maintain consistency with {company_name}'s technical environment

PROFESSIONAL COMMUNICATION:
• Use formal, professional tone throughout
• Employ standard ITSM terminology and abbreviations
• Include appropriate technical detail for audience
• Maintain clarity and conciseness

REALISTIC PROGRESSION:
• Show logical troubleshooting sequence
• Include appropriate time intervals between updates
• Reflect actual effort and complexity for {priority} incidents
• Demonstrate proper escalation procedures when applicable

CONTEXTUAL APPROPRIATENESS:
• Align with {department} typical technology usage
• Reflect {user_role} level of technical knowledge
• Include relevant business context and constraints
• Consider {company_name}'s industry-specific requirements

OUTPUT FORMAT:
=============
Respond ONLY with a valid JSON object containing the following structure. Do NOT include any markdown, code block, or explanation. Only output the JSON object:

{
    "short_description": "Professional, searchable incident summary",
    "description": "Comprehensive user-reported incident description",
    "work_notes": [
        "Timestamp-ready work note entry 1...",
        "Timestamp-ready work note entry 2...",
        "Timestamp-ready work note entry 3...",
        "Timestamp-ready work note entry 4...",
        "Timestamp-ready work note entry 5...",
        "Final timestamp-ready work note entry..."
    ],
    "close_notes": "Detailed resolution summary and root cause analysis",
    "technical_keywords": ["keyword1", "keyword2", "keyword3"],
    "business_impact_level": "Low|Medium|High|Critical",
    "resolution_category": "Configuration|Software|Hardware|Process|User Error"
}

SPECIALIZED INSTRUCTIONS FOR {category}:
{category_specific_instructions}

Generate an incident that would be considered exemplary training data for AI model development, demonstrating the quality and depth expected in professional ITSM environments.
"""

# ============================================================================
# CATEGORY-SPECIFIC INSTRUCTION TEMPLATES
# ============================================================================

CATEGORY_SPECIFIC_INSTRUCTIONS = {
    "Hardware": {
        "focus_areas": [
            "Physical component failure symptoms and diagnostics",
            "Hardware compatibility and configuration issues", 
            "Performance degradation and capacity planning",
            "Preventive maintenance and lifecycle management"
        ],
        "technical_elements": [
            "System specifications and model numbers",
            "Diagnostic error codes and hardware logs",
            "Performance metrics and benchmarking data",
            "Vendor support procedures and warranty information"
        ],
        "resolution_patterns": [
            "Component replacement and configuration",
            "Driver updates and firmware patches",
            "System optimization and tuning",
            "Hardware monitoring and alerting setup"
        ]
    },
    
    "Software": {
        "focus_areas": [
            "Application crashes, freezes, and error conditions",
            "Installation, upgrade, and compatibility issues",
            "Performance optimization and resource management",
            "Integration problems and API failures"
        ],
        "technical_elements": [
            "Error messages, stack traces, and log entries",
            "Software versions and dependency information",
            "System requirements and compatibility matrices",
            "Configuration files and registry settings"
        ],
        "resolution_patterns": [
            "Software reinstallation and configuration repair",
            "Version rollbacks and compatibility fixes",
            "Performance tuning and resource optimization",
            "Integration testing and API troubleshooting"
        ]
    },
    
    "Network": {
        "focus_areas": [
            "Connectivity issues and routing problems",
            "Performance degradation and bandwidth constraints",
            "Security policy conflicts and access control",
            "Infrastructure failures and service disruptions"
        ],
        "technical_elements": [
            "IP addresses, DNS settings, and network topology",
            "Ping results, traceroute data, and latency measurements",
            "Firewall logs, security policies, and access rules",
            "Network device configurations and status information"
        ],
        "resolution_patterns": [
            "Configuration changes and policy updates",
            "Hardware replacement and infrastructure upgrades",
            "Performance optimization and traffic management",
            "Security policy adjustments and access corrections"
        ]
    },
    
    "Security": {
        "focus_areas": [
            "Access control failures and authentication issues",
            "Malware detection and incident response",
            "Policy violations and compliance concerns",
            "Vulnerability management and threat mitigation"
        ],
        "technical_elements": [
            "Security event logs and audit trails",
            "Authentication failure codes and access attempts",
            "Malware signatures and detection alerts",
            "Compliance standards and policy frameworks"
        ],
        "resolution_patterns": [
            "Access rights restoration and account recovery",
            "Malware removal and system hardening",
            "Policy enforcement and compliance remediation",
            "Security monitoring and alerting enhancement"
        ]
    },
    
    "Database": {
        "focus_areas": [
            "Performance degradation and query optimization",
            "Data corruption and recovery procedures",
            "Connection failures and authentication issues",
            "Backup and restore operations"
        ],
        "technical_elements": [
            "SQL error codes and execution plans",
            "Database performance metrics and statistics",
            "Connection strings and authentication methods",
            "Backup schedules and recovery procedures"
        ],
        "resolution_patterns": [
            "Query optimization and index management",
            "Data recovery and integrity verification",
            "Connection troubleshooting and configuration fixes",
            "Backup restoration and disaster recovery"
        ]
    },
    
    "Email": {
        "focus_areas": [
            "Message delivery failures and routing issues",
            "Client configuration and synchronization problems",
            "Server performance and storage management",
            "Security filtering and spam protection"
        ],
        "technical_elements": [
            "SMTP error codes and delivery status notifications",
            "Client configuration settings and protocols",
            "Server logs and performance counters",
            "Security policies and filtering rules"
        ],
        "resolution_patterns": [
            "Mail flow troubleshooting and routing fixes",
            "Client reconfiguration and profile rebuilding",
            "Server optimization and storage management",
            "Security policy adjustments and rule updates"
        ]
    }
}

# ============================================================================
# USER PERSONA ENHANCEMENT TEMPLATES
# ============================================================================

USER_PERSONA_PROFILES = {
    "Finance": {
        "typical_applications": ["SAP", "Excel", "QuickBooks", "Oracle Financial", "Power BI"],
        "technical_proficiency": "Basic to Intermediate",
        "common_issues": ["Report generation", "System access", "Data synchronization", "Performance"],
        "business_criticality": "High - Financial deadlines and compliance requirements",
        "communication_style": "Formal, detail-oriented, process-focused"
    },
    
    "Marketing": {
        "typical_applications": ["Adobe Creative Suite", "Salesforce", "HubSpot", "Canva", "Social Media Tools"],
        "technical_proficiency": "Intermediate",
        "common_issues": ["Creative software crashes", "File sharing", "Campaign tools", "Brand asset access"],
        "business_criticality": "Medium-High - Campaign deadlines and brand consistency",
        "communication_style": "Creative, collaborative, deadline-conscious"
    },
    
    "Sales": {
        "typical_applications": ["CRM Systems", "Mobile Apps", "Video Conferencing", "Proposal Tools"],
        "technical_proficiency": "Basic to Intermediate",
        "common_issues": ["CRM access", "Mobile connectivity", "Client communication tools", "Data sync"],
        "business_criticality": "High - Direct revenue impact and client relationships",
        "communication_style": "Results-oriented, urgent, relationship-focused"
    },
    
    "IT": {
        "typical_applications": ["Administration Tools", "Monitoring Systems", "Development Environments", "Infrastructure"],
        "technical_proficiency": "Advanced",
        "common_issues": ["System administration", "Infrastructure monitoring", "Security tools", "Development platforms"],
        "business_criticality": "Critical - Service delivery and system availability",
        "communication_style": "Technical, precise, solution-oriented"
    },
    
    "HR": {
        "typical_applications": ["HRIS", "Payroll Systems", "Recruitment Tools", "Employee Portals"],
        "technical_proficiency": "Basic to Intermediate",
        "common_issues": ["Employee data access", "System integration", "Compliance reporting", "Portal functionality"],
        "business_criticality": "High - Employee experience and compliance",
        "communication_style": "Professional, empathetic, compliance-focused"
    },
    
    "Operations": {
        "typical_applications": ["ERP Systems", "Supply Chain Tools", "Manufacturing Systems", "Quality Management"],
        "technical_proficiency": "Intermediate",
        "common_issues": ["Production systems", "Supply chain visibility", "Quality tracking", "Integration issues"],
        "business_criticality": "Critical - Operational continuity and efficiency",
        "communication_style": "Operational, efficiency-focused, systematic"
    }
}

# ============================================================================
# BUSINESS CONTEXT TEMPLATES
# ============================================================================

BUSINESS_DOMAIN_CONTEXTS = {
    "Technology": {
        "industry_specifics": "Software development, cloud services, digital transformation",
        "compliance_requirements": "SOC 2, ISO 27001, GDPR",
        "technical_environment": "Cloud-first, microservices, CI/CD pipelines",
        "business_priorities": "Innovation speed, scalability, security"
    },
    
    "Financial Services": {
        "industry_specifics": "Banking, insurance, investment management",
        "compliance_requirements": "SOX, PCI DSS, Basel III, GDPR",
        "technical_environment": "High availability, real-time processing, secure networks",
        "business_priorities": "Regulatory compliance, risk management, customer trust"
    },
    
    "Healthcare": {
        "industry_specifics": "Patient care, medical devices, health records",
        "compliance_requirements": "HIPAA, FDA, HITECH",
        "technical_environment": "EMR systems, medical devices, secure networks",
        "business_priorities": "Patient safety, privacy, operational efficiency"
    },
    
    "Manufacturing": {
        "industry_specifics": "Production systems, supply chain, quality control",
        "compliance_requirements": "ISO 9001, FDA, environmental regulations",
        "technical_environment": "Industrial IoT, SCADA systems, ERP integration",
        "business_priorities": "Production efficiency, quality, safety"
    },
    
    "Retail": {
        "industry_specifics": "Point of sale, inventory management, customer experience",
        "compliance_requirements": "PCI DSS, GDPR, accessibility standards",
        "technical_environment": "Omnichannel platforms, mobile apps, analytics",
        "business_priorities": "Customer experience, inventory optimization, sales growth"
    }
}

# ============================================================================
# TEMPLATE ENHANCEMENT FUNCTIONS
# ============================================================================

def get_enhanced_prompt(context: dict) -> str:
    """Builds a robust, field-driven prompt for a single incident, using context variables."""
    return f"""
You are an ITSM Incident Management AI Assistant. Generate a single, highly realistic ServiceNow incident record for the company \"{context['company_name']}\" with the following parameters:

- Assignment group: {context.get('assignment_group', 'Gemi_Test')}
- Assigned to: {context.get('assigned_to', 'Hans Havlik')}
- Configuration item: {context.get('configuration_item', 'AMO')}
- Caller: {context.get('caller', 'Hans Havlik')}
- Requestor email: {context.get('requestor_email', 'hans.havlik@capgemini.com')}
- Close code: {context.get('close_code', 'AMO_Hans Havlik')}
- Triage tag: {context['triage_tag']}
- Priority: {context['priority']}
- State: Closed

The incident must include:
- short_description: A concise summary of the issue (1-2 sentences)
- description: A detailed, realistic narrative of the incident, including user actions, business impact, and technical context
- work_notes: A list of 3-6 realistic, timestamped technician notes showing troubleshooting and resolution steps
- close_notes: A detailed summary of the root cause and resolution
- technical_keywords: A list of 3-5 relevant technical keywords
- business_impact_level: One of [\"Low\", \"Medium\", \"High\", \"Critical\"]
- resolution_category: One of [\"Configuration\", \"Software\", \"Hardware\", \"Process\", \"User Error\"]

Example output:
{{
  "short_description": "User unable to access VPN due to authentication failure",
  "description": "A user in the finance department reported being unable to connect to the corporate VPN. The issue began after a password reset. The user attempted to reconnect multiple times, but received an 'authentication failed' error. This prevented access to financial systems, impacting end-of-month reporting.",
  "work_notes": [
    "2025-05-30 09:15:00 Hans Havlik: Initial triage, confirmed user unable to connect to VPN.",
    "2025-05-30 09:30:00 Hans Havlik: Checked user account status, found account locked after multiple failed attempts.",
    "2025-05-30 09:45:00 Hans Havlik: Reset user account, user able to authenticate successfully.",
    "2025-05-30 10:00:00 Hans Havlik: User confirmed VPN access restored. Incident closed."
  ],
  "close_notes": "Root cause was account lockout due to repeated failed logins after password reset. Resolved by unlocking account and assisting user with correct credentials.",
  "technical_keywords": ["VPN", "authentication", "account lockout"],
  "business_impact_level": "High",
  "resolution_category": "Configuration"
}}

Respond ONLY with a valid JSON object in this format. Do NOT include any markdown, code block, or explanation. Only output the JSON object.
"""

# ============================================================================
# CATEGORY-SPECIFIC INSTRUCTION TEMPLATES
# ============================================================================

CATEGORY_SPECIFIC_INSTRUCTIONS = {
    "Hardware": {
        "focus_areas": [
            "Physical component failure symptoms and diagnostics",
            "Hardware compatibility and configuration issues", 
            "Performance degradation and capacity planning",
            "Preventive maintenance and lifecycle management"
        ],
        "technical_elements": [
            "System specifications and model numbers",
            "Diagnostic error codes and hardware logs",
            "Performance metrics and benchmarking data",
            "Vendor support procedures and warranty information"
        ],
        "resolution_patterns": [
            "Component replacement and configuration",
            "Driver updates and firmware patches",
            "System optimization and tuning",
            "Hardware monitoring and alerting setup"
        ]
    },
    
    "Software": {
        "focus_areas": [
            "Application crashes, freezes, and error conditions",
            "Installation, upgrade, and compatibility issues",
            "Performance optimization and resource management",
            "Integration problems and API failures"
        ],
        "technical_elements": [
            "Error messages, stack traces, and log entries",
            "Software versions and dependency information",
            "System requirements and compatibility matrices",
            "Configuration files and registry settings"
        ],
        "resolution_patterns": [
            "Software reinstallation and configuration repair",
            "Version rollbacks and compatibility fixes",
            "Performance tuning and resource optimization",
            "Integration testing and API troubleshooting"
        ]
    },
    
    "Network": {
        "focus_areas": [
            "Connectivity issues and routing problems",
            "Performance degradation and bandwidth constraints",
            "Security policy conflicts and access control",
            "Infrastructure failures and service disruptions"
        ],
        "technical_elements": [
            "IP addresses, DNS settings, and network topology",
            "Ping results, traceroute data, and latency measurements",
            "Firewall logs, security policies, and access rules",
            "Network device configurations and status information"
        ],
        "resolution_patterns": [
            "Configuration changes and policy updates",
            "Hardware replacement and infrastructure upgrades",
            "Performance optimization and traffic management",
            "Security policy adjustments and access corrections"
        ]
    },
    
    "Security": {
        "focus_areas": [
            "Access control failures and authentication issues",
            "Malware detection and incident response",
            "Policy violations and compliance concerns",
            "Vulnerability management and threat mitigation"
        ],
        "technical_elements": [
            "Security event logs and audit trails",
            "Authentication failure codes and access attempts",
            "Malware signatures and detection alerts",
            "Compliance standards and policy frameworks"
        ],
        "resolution_patterns": [
            "Access rights restoration and account recovery",
            "Malware removal and system hardening",
            "Policy enforcement and compliance remediation",
            "Security monitoring and alerting enhancement"
        ]
    },
    
    "Database": {
        "focus_areas": [
            "Performance degradation and query optimization",
            "Data corruption and recovery procedures",
            "Connection failures and authentication issues",
            "Backup and restore operations"
        ],
        "technical_elements": [
            "SQL error codes and execution plans",
            "Database performance metrics and statistics",
            "Connection strings and authentication methods",
            "Backup schedules and recovery procedures"
        ],
        "resolution_patterns": [
            "Query optimization and index management",
            "Data recovery and integrity verification",
            "Connection troubleshooting and configuration fixes",
            "Backup restoration and disaster recovery"
        ]
    },
    
    "Email": {
        "focus_areas": [
            "Message delivery failures and routing issues",
            "Client configuration and synchronization problems",
            "Server performance and storage management",
            "Security filtering and spam protection"
        ],
        "technical_elements": [
            "SMTP error codes and delivery status notifications",
            "Client configuration settings and protocols",
            "Server logs and performance counters",
            "Security policies and filtering rules"
        ],
        "resolution_patterns": [
            "Mail flow troubleshooting and routing fixes",
            "Client reconfiguration and profile rebuilding",
            "Server optimization and storage management",
            "Security policy adjustments and rule updates"
        ]
    }
}

# ============================================================================
# USER PERSONA ENHANCEMENT TEMPLATES
# ============================================================================

USER_PERSONA_PROFILES = {
    "Finance": {
        "typical_applications": ["SAP", "Excel", "QuickBooks", "Oracle Financial", "Power BI"],
        "technical_proficiency": "Basic to Intermediate",
        "common_issues": ["Report generation", "System access", "Data synchronization", "Performance"],
        "business_criticality": "High - Financial deadlines and compliance requirements",
        "communication_style": "Formal, detail-oriented, process-focused"
    },
    
    "Marketing": {
        "typical_applications": ["Adobe Creative Suite", "Salesforce", "HubSpot", "Canva", "Social Media Tools"],
        "technical_proficiency": "Intermediate",
        "common_issues": ["Creative software crashes", "File sharing", "Campaign tools", "Brand asset access"],
        "business_criticality": "Medium-High - Campaign deadlines and brand consistency",
        "communication_style": "Creative, collaborative, deadline-conscious"
    },
    
    "Sales": {
        "typical_applications": ["CRM Systems", "Mobile Apps", "Video Conferencing", "Proposal Tools"],
        "technical_proficiency": "Basic to Intermediate",
        "common_issues": ["CRM access", "Mobile connectivity", "Client communication tools", "Data sync"],
        "business_criticality": "High - Direct revenue impact and client relationships",
        "communication_style": "Results-oriented, urgent, relationship-focused"
    },
    
    "IT": {
        "typical_applications": ["Administration Tools", "Monitoring Systems", "Development Environments", "Infrastructure"],
        "technical_proficiency": "Advanced",
        "common_issues": ["System administration", "Infrastructure monitoring", "Security tools", "Development platforms"],
        "business_criticality": "Critical - Service delivery and system availability",
        "communication_style": "Technical, precise, solution-oriented"
    },
    
    "HR": {
        "typical_applications": ["HRIS", "Payroll Systems", "Recruitment Tools", "Employee Portals"],
        "technical_proficiency": "Basic to Intermediate",
        "common_issues": ["Employee data access", "System integration", "Compliance reporting", "Portal functionality"],
        "business_criticality": "High - Employee experience and compliance",
        "communication_style": "Professional, empathetic, compliance-focused"
    },
    
    "Operations": {
        "typical_applications": ["ERP Systems", "Supply Chain Tools", "Manufacturing Systems", "Quality Management"],
        "technical_proficiency": "Intermediate",
        "common_issues": ["Production systems", "Supply chain visibility", "Quality tracking", "Integration issues"],
        "business_criticality": "Critical - Operational continuity and efficiency",
        "communication_style": "Operational, efficiency-focused, systematic"
    }
}

# ============================================================================
# BUSINESS CONTEXT TEMPLATES
# ============================================================================

BUSINESS_DOMAIN_CONTEXTS = {
    "Technology": {
        "industry_specifics": "Software development, cloud services, digital transformation",
        "compliance_requirements": "SOC 2, ISO 27001, GDPR",
        "technical_environment": "Cloud-first, microservices, CI/CD pipelines",
        "business_priorities": "Innovation speed, scalability, security"
    },
    
    "Financial Services": {
        "industry_specifics": "Banking, insurance, investment management",
        "compliance_requirements": "SOX, PCI DSS, Basel III, GDPR",
        "technical_environment": "High availability, real-time processing, secure networks",
        "business_priorities": "Regulatory compliance, risk management, customer trust"
    },
    
    "Healthcare": {
        "industry_specifics": "Patient care, medical devices, health records",
        "compliance_requirements": "HIPAA, FDA, HITECH",
        "technical_environment": "EMR systems, medical devices, secure networks",
        "business_priorities": "Patient safety, privacy, operational efficiency"
    },
    
    "Manufacturing": {
        "industry_specifics": "Production systems, supply chain, quality control",
        "compliance_requirements": "ISO 9001, FDA, environmental regulations",
        "technical_environment": "Industrial IoT, SCADA systems, ERP integration",
        "business_priorities": "Production efficiency, quality, safety"
    },
    
    "Retail": {
        "industry_specifics": "Point of sale, inventory management, customer experience",
        "compliance_requirements": "PCI DSS, GDPR, accessibility standards",
        "technical_environment": "Omnichannel platforms, mobile apps, analytics",
        "business_priorities": "Customer experience, inventory optimization, sales growth"
    }
}

# ============================================================================
# TEMPLATE ENHANCEMENT FUNCTIONS
# ============================================================================

def get_enhanced_prompt(context: dict) -> str:
    """Builds a robust, field-driven prompt for a single incident, using context variables."""
    return f"""
You are an ITSM Incident Management AI Assistant. Generate a single, highly realistic ServiceNow incident record for the company \"{context['company_name']}\" with the following parameters:

- Assignment group: {context.get('assignment_group', 'Gemi_Test')}
- Assigned to: {context.get('assigned_to', 'Hans Havlik')}
- Configuration item: {context.get('configuration_item', 'AMO')}
- Caller: {context.get('caller', 'Hans Havlik')}
- Requestor email: {context.get('requestor_email', 'hans.havlik@capgemini.com')}
- Close code: {context.get('close_code', 'AMO_Hans Havlik')}
- Triage tag: {context['triage_tag']}
- Priority: {context['priority']}
- State: Closed

The incident must include:
- short_description: A concise summary of the issue (1-2 sentences)
- description: A detailed, realistic narrative of the incident, including user actions, business impact, and technical context
- work_notes: A list of 3-6 realistic, timestamped technician notes showing troubleshooting and resolution steps
- close_notes: A detailed summary of the root cause and resolution
- technical_keywords: A list of 3-5 relevant technical keywords
- business_impact_level: One of [\"Low\", \"Medium\", \"High\", \"Critical\"]
- resolution_category: One of [\"Configuration\", \"Software\", \"Hardware\", \"Process\", \"User Error\"]

Example output:
{{
  "short_description": "User unable to access VPN due to authentication failure",
  "description": "A user in the finance department reported being unable to connect to the corporate VPN. The issue began after a password reset. The user attempted to reconnect multiple times, but received an 'authentication failed' error. This prevented access to financial systems, impacting end-of-month reporting.",
  "work_notes": [
    "2025-05-30 09:15:00 Hans Havlik: Initial triage, confirmed user unable to connect to VPN.",
    "2025-05-30 09:30:00 Hans Havlik: Checked user account status, found account locked after multiple failed attempts.",
    "2025-05-30 09:45:00 Hans Havlik: Reset user account, user able to authenticate successfully.",
    "2025-05-30 10:00:00 Hans Havlik: User confirmed VPN access restored. Incident closed."
  ],
  "close_notes": "Root cause was account lockout due to repeated failed logins after password reset. Resolved by unlocking account and assisting user with correct credentials.",
  "technical_keywords": ["VPN", "authentication", "account lockout"],
  "business_impact_level": "High",
  "resolution_category": "Configuration"
}}

Respond ONLY with a valid JSON object in this format. Do NOT include any markdown, code block, or explanation. Only output the JSON object.
"""

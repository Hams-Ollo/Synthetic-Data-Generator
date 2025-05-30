#!/usr/bin/env python3
"""
Test Script for Golden Incident Generator v2.0
==============================================

This script tests the enhanced incident generator functionality
and validates Azure OpenAI integration.

Author: Hans Havlik
Date: May 30, 2025
Version: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# Environment variables management
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Config'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Main'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from golden_incident_generator_v2 import GoldenIncidentGeneratorV2
        print("✓ Golden Incident Generator v2.0 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Golden Incident Generator: {e}")
        return False
        
    try:
        from enhanced_incident_prompt_template import (
            ENHANCED_INCIDENT_SYSTEM_PROMPT,
            get_enhanced_prompt
        )
        print("✓ Enhanced prompt template imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import prompt template: {e}")
        return False
        
    try:
        from langchain_openai import AzureChatOpenAI
        print("✓ LangChain Azure OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import LangChain: {e}")
        return False
        
    try:
        # Get Azure OpenAI credentials from environment variables
        AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
        AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_API_KEY')
        
        if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY:
            print("✗ Azure OpenAI environment variables not set")
            return False
            
        print("✓ Azure OpenAI configuration loaded from environment variables")
    except Exception as e:
        print(f"✗ Failed to load Azure OpenAI config: {e}")
        return False
        
    return True

def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from golden_incident_generator_v2 import GoldenIncidentGeneratorV2
        generator = GoldenIncidentGeneratorV2()
        
        # Check basic config
        assert generator.config['company_name'], "Company name not set"
        assert generator.config['incident_categories'], "Incident categories not set"
        assert generator.config['technician_specializations'], "Technician specializations not set"
        
        print("✓ Configuration loaded and validated successfully")
        return True, generator
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False, None

def test_azure_connection():
    """Test Azure OpenAI connection"""
    print("\nTesting Azure OpenAI connection...")
    
    try:
        from golden_incident_generator_v2 import GoldenIncidentGeneratorV2
        generator = GoldenIncidentGeneratorV2()
        
        # Test simple LLM call
        from langchain.schema import HumanMessage
        test_message = HumanMessage(content="Say 'Connection test successful' if you can read this.")
        
        response = generator.llm([test_message])
        
        if "Connection test successful" in response.content or "successful" in response.content.lower():
            print("✓ Azure OpenAI connection test successful")
            return True, generator
        else:
            print(f"✗ Unexpected response: {response.content}")
            return False, None
            
    except Exception as e:
        print(f"✗ Azure OpenAI connection test failed: {e}")
        return False, None

def test_incident_generation():
    """Test single incident generation"""
    print("\nTesting incident generation...")
    
    try:
        from golden_incident_generator_v2 import GoldenIncidentGeneratorV2
        generator = GoldenIncidentGeneratorV2()
        
        # Generate single incident
        context = generator.generate_incident_context()
        print(f"  Generated context: {context['category']} - {context['subcategory']}")
        
        incident = generator.generate_single_incident(context)
        
        if incident:
            print("✓ Single incident generated successfully")
            print(f"  Incident Number: {incident.number}")
            print(f"  Category: {incident.category}")
            print(f"  Priority: {incident.priority}")
            print(f"  Short Description: {incident.short_description[:50]}...")
            return True, incident
        else:
            print("✗ Failed to generate incident")
            return False, None
            
    except Exception as e:
        print(f"✗ Incident generation test failed: {e}")
        return False, None

def test_batch_generation():
    """Test batch generation"""
    print("\nTesting batch generation (3 incidents)...")
    
    try:
        from golden_incident_generator_v2 import GoldenIncidentGeneratorV2
        generator = GoldenIncidentGeneratorV2()
        
        # Generate small batch
        incidents = generator.generate_batch(3)
        
        if len(incidents) > 0:
            print(f"✓ Batch generation successful: {len(incidents)}/3 incidents generated")
            print(f"  Success rate: {generator.metrics.success_rate:.1f}%")
            print(f"  Total tokens used: {generator.metrics.total_tokens_used}")
            return True, incidents
        else:
            print("✗ No incidents generated in batch")
            return False, None
            
    except Exception as e:
        print(f"✗ Batch generation test failed: {e}")
        return False, None

def test_export_functionality():
    """Test export functionality"""
    print("\nTesting export functionality...")
    
    try:
        from golden_incident_generator_v2 import GoldenIncidentGeneratorV2
        generator = GoldenIncidentGeneratorV2()
        
        # Generate a few incidents
        incidents = generator.generate_batch(2)
        
        if len(incidents) == 0:
            print("✗ No incidents to export")
            return False
            
        # Test CSV export
        csv_file = generator.export_to_csv("test_export.csv")
        print(f"✓ CSV export successful: {csv_file}")
        
        # Test JSON export
        json_file = generator.export_to_json("test_export.json")
        print(f"✓ JSON export successful: {json_file}")
        
        # Cleanup test files
        try:
            os.remove(csv_file)
            os.remove(json_file)
            print("✓ Test files cleaned up")
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"✗ Export test failed: {e}")
        return False

def run_full_test():
    """Run complete test suite"""
    print("="*60)
    print("GOLDEN INCIDENT GENERATOR v2.0 - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Azure Connection Test", test_azure_connection), 
        ("Single Incident Generation", test_incident_generation),
        ("Batch Generation Test", test_batch_generation),
        ("Export Functionality Test", test_export_functionality)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            if test_name in ["Configuration Test", "Azure Connection Test", "Single Incident Generation", "Batch Generation Test"]:
                success, data = test_func()
                results[test_name] = success
            else:
                success = test_func()
                results[test_name] = success
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Generator is ready for production use.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check configuration and dependencies.")
        return False

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test script for the Golden Incident Generator
Generates a small batch of incidents to verify functionality
"""

import os
import sys
import logging

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from golden_incident_generator_v2 import GoldenIncidentGeneratorV2

def test_generator():
    """Test the incident generator with a small batch"""
    print("🧪 Testing Golden Incident Generator...")
    
    try:        # Initialize generator
        generator = GoldenIncidentGeneratorV2()
        print("✅ Generator initialized successfully")
        
        # Generate 3 test incidents
        print("🔄 Generating 3 test incidents...")
        incidents = generator.generate_batch(3)
        
        if not incidents:
            print("❌ No incidents generated")
            return False
            
        print(f"✅ Generated {len(incidents)} incidents")
        
        # Export to files
        csv_file = generator.export_to_csv("test_incidents.csv")
        json_file = generator.export_to_json("test_incidents.json")
        
        print(f"📄 CSV exported to: {csv_file}")
        print(f"📄 JSON exported to: {json_file}")
        
        # Print sample incident
        if incidents:
            sample = incidents[0]
            print(f"\n📋 Sample Incident: {sample.number}")
            print(f"Priority: {sample.priority}")
            print(f"Category: {sample.category} - {sample.subcategory}")
            print(f"Short Description: {sample.short_description}")
            print(f"State: {sample.state}")
            print(f"Assigned to: {sample.assigned_to}")
            
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logging.error(f"Test error: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    success = test_generator()
    sys.exit(0 if success else 1)

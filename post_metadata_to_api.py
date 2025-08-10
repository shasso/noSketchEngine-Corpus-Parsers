import json
import argparse
import os
import requests
import glob
from pathlib import Path

def load_config(config_file):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validate required fields
        required_fields = ['api_endpoint', 'json_folder']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Required field '{field}' missing from config")
        
        return config
    except FileNotFoundError:
        print(f"Error: Config file {config_file} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        return None
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def post_json_file(file_path, api_endpoint, headers=None, timeout=30):
    """Post a single JSON file to the API endpoint"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print(f"Posting {os.path.basename(file_path)}...")
        
        response = requests.post(
            api_endpoint,
            json=json_data,
            headers=headers,
            timeout=timeout
        )
        
        if response.status_code in [200, 201]:
            print(f"✓ Successfully posted {os.path.basename(file_path)} - Status: {response.status_code}")
            return True
        else:
            print(f"✗ Failed to post {os.path.basename(file_path)} - Status: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"✗ Timeout posting {os.path.basename(file_path)}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Request error posting {os.path.basename(file_path)}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error posting {os.path.basename(file_path)}: {e}")
        return False

def post_all_json_files(config):
    """Post all JSON files in the specified folder to the API"""
    json_folder = config['json_folder']
    api_endpoint = config['api_endpoint']
    
    # Get optional configuration
    headers = config.get('headers', {'Content-Type': 'application/json'})
    timeout = config.get('timeout', 30)
    
    print(f"API Endpoint: {api_endpoint}")
    print(f"JSON Folder: {json_folder}")
    print(f"Headers: {headers}")
    print("-" * 50)
    
    # Find all JSON files
    json_pattern = os.path.join(json_folder, "*.json")
    json_files = glob.glob(json_pattern)
    
    if not json_files:
        print(f"No JSON files found in {json_folder}")
        return
    
    print(f"Found {len(json_files)} JSON files to process")
    print("-" * 50)
    
    success_count = 0
    failure_count = 0
    
    for json_file in json_files:
        if post_json_file(json_file, api_endpoint, headers, timeout):
            success_count += 1
        else:
            failure_count += 1
    
    print("-" * 50)
    print(f"Summary: {success_count} successful, {failure_count} failed")

def create_sample_config(config_path):
    """Create a sample configuration file"""
    sample_config = {
        "api_endpoint": "http://localhost:3000/api/metadata",
        "json_folder": "metadata/final",
        "headers": {
            "Content-Type": "application/json"
        },
        "timeout": 30
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, ensure_ascii=False, indent=2)
    
    print(f"Sample configuration file created: {config_path}")
    print("Please edit the configuration file with your actual API endpoint and settings.")

def main():
    parser = argparse.ArgumentParser(description='Post JSON metadata files to an API endpoint.')
    parser.add_argument('-c', '--config', required=True, help='Configuration file path (JSON format)')
    parser.add_argument('--create-sample', action='store_true', help='Create a sample configuration file')
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_config(args.config)
        return
    
    config = load_config(args.config)
    if config is None:
        print("Failed to load configuration. Use --create-sample to create a sample config file.")
        return
    
    post_all_json_files(config)

if __name__ == '__main__':
    main()

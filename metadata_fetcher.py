import json
import requests
import os
from typing import Dict, Optional

class MetadataFetcher:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the metadata fetcher with configuration"""
        self.config = self._load_config(config_file)
        self.api_endpoint = self.config.get("api_endpoint")
        self.timeout = self.config.get("timeout", 30)
        self.fallback_to_file = self.config.get("fallback_to_file", True)

    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file {config_file} not found. Using default settings.")
            return {
                "api_endpoint": "http://localhost:5000/api/metadata/search",
                "timeout": 30,
                "fallback_to_file": True
            }
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config file: {e}")
            return {}

    def _is_uuid(self, value: str) -> bool:
        """Check if the value looks like a UUID"""
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, value.lower()))

    def _normalize_metadata(self, metadata: Dict) -> Dict:
        """
        Normalize metadata to handle format changes:
        1. Convert 'authors' array to 'author' (pick first one for backward compatibility)
        2. Ensure pub_date and num_pages are strings for consistency
        """
        normalized = metadata.copy()
        
        # Handle authors array -> author conversion
        if 'authors' in normalized and isinstance(normalized['authors'], list):
            if normalized['authors']:  # If array is not empty
                normalized['author'] = normalized['authors'][0]  # Pick first author
            else:
                normalized['author'] = "Unknown"  # Fallback for empty array
            # Keep both for forward compatibility
            # normalized['authors'] stays as is
        
        # Handle integer fields - convert to strings for backward compatibility
        for field in ['pub_date', 'num_pages']:
            if field in normalized and isinstance(normalized[field], (int, float)):
                normalized[field] = str(normalized[field])
        
        return normalized

    def _fetch_from_api(self, metadata_id: str) -> Optional[Dict]:
        """Fetch metadata from API using the ID"""
        try:
            url = f"{self.api_endpoint}?id={metadata_id}"
            print(f"Fetching metadata from API: {url}")
            
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("success") and data.get("results"):
                # Extract the first result's metadata
                result = data["results"][0]
                metadata = result.get("metadata", {})
                
                # Normalize the metadata for backward compatibility
                normalized_metadata = self._normalize_metadata(metadata)
                
                print(f"Successfully fetched metadata for ID: {metadata_id}")
                if 'authors' in metadata:
                    print(f"  Authors: {metadata['authors']} -> Using: {normalized_metadata.get('author')}")
                
                return normalized_metadata
            else:
                print(f"No results found for ID: {metadata_id}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response from API: {e}")
            return None
        except Exception as e:
            print(f"Error fetching from API: {e}")
            return None

    def _load_from_file(self, file_path: str) -> Optional[Dict]:
        """Load metadata from JSON file (fallback method)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both old format (direct metadata) and new format (with id and metadata)
                if 'metadata' in data:
                    metadata = data['metadata']
                else:
                    metadata = data
                
                # Normalize the metadata for consistency
                normalized_metadata = self._normalize_metadata(metadata)
                return normalized_metadata
                
        except FileNotFoundError:
            print(f"Error: Metadata file {file_path} not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in metadata file: {e}")
            return None

    def get_metadata(self, metadata_source: str) -> Optional[Dict]:
        """
        Get metadata either from API (if UUID) or from file
        
        Args:
            metadata_source: Either a UUID (for API) or file path (for local file)
            
        Returns:
            Dictionary containing metadata or None if not found
        """
        # Check if the source looks like a UUID
        if self._is_uuid(metadata_source):
            print(f"Detected UUID format: {metadata_source}")
            
            # Try to fetch from API first
            if self.api_endpoint:
                metadata = self._fetch_from_api(metadata_source)
                if metadata:
                    return metadata
                elif not self.fallback_to_file:
                    return None
            
            print("API fetch failed or not configured. Cannot process UUID without API.")
            return None
            
        else:
            # Treat as file path
            print(f"Treating as file path: {metadata_source}")
            return self._load_from_file(metadata_source)

    def create_sample_config(self, config_path: str = "config.json"):
        """Create a sample configuration file"""
        sample_config = {
            "api_endpoint": "http://localhost:5000/api/metadata/search",
            "timeout": 30,
            "fallback_to_file": True
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, ensure_ascii=False, indent=2)
        
        print(f"Sample configuration file created: {config_path}")

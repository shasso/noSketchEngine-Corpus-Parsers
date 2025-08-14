#!/usr/bin/env python3
"""
Test script for the enhanced nose_to_vertical.py with API metadata support
"""

import sys
import os
from metadata_fetcher import MetadataFetcher

def test_uuid_detection():
    """Test UUID detection functionality"""
    fetcher = MetadataFetcher()
    
    # Test valid UUIDs
    valid_uuids = [
        "40a3280d-dfd5-4280-b98d-972669aeb14b",
        "12345678-1234-1234-1234-123456789abc"
    ]
    
    # Test invalid UUIDs
    invalid_uuids = [
        "not-a-uuid",
        "metadata/file.json",
        "40a3280d-dfd5-4280-b98d-972669aeb14",  # too short
        "40a3280d-dfd5-4280-b98d-972669aeb14bb"  # too long
    ]
    
    print("Testing UUID detection:")
    for uuid in valid_uuids:
        result = fetcher._is_uuid(uuid)
        print(f"  {uuid}: {result} (should be True)")
        assert result == True
    
    for uuid in invalid_uuids:
        result = fetcher._is_uuid(uuid)
        print(f"  {uuid}: {result} (should be False)")
        assert result == False
    
    print("✓ UUID detection tests passed\n")

def test_config_loading():
    """Test configuration loading"""
    print("Testing configuration loading:")
    
    # Test with existing config
    fetcher = MetadataFetcher("config.json")
    print(f"  API Endpoint: {fetcher.api_endpoint}")
    print(f"  Timeout: {fetcher.timeout}")
    print(f"  Fallback to file: {fetcher.fallback_to_file}")
    
    # Test with non-existent config (should use defaults)
    fetcher2 = MetadataFetcher("nonexistent.json")
    print(f"  Default API Endpoint: {fetcher2.api_endpoint}")
    
    print("✓ Configuration loading tests passed\n")

def test_metadata_normalization():
    """Test metadata normalization for new format changes"""
    print("Testing metadata normalization:")
    
    fetcher = MetadataFetcher()
    
    # Test new format with authors array and integer fields
    new_format_metadata = {
        "title": "Test Document",
        "authors": ["Author One", "Author Two", "Author Three"],
        "language": "Assyrian",
        "pub_date": 2020,  # Integer
        "num_pages": 453   # Integer
    }
    
    normalized = fetcher._normalize_metadata(new_format_metadata)
    
    # Check authors -> author conversion
    assert normalized['author'] == "Author One", f"Expected 'Author One', got '{normalized.get('author')}'"
    assert normalized['authors'] == ["Author One", "Author Two", "Author Three"], "Authors array should be preserved"
    
    # Check integer -> string conversion
    assert normalized['pub_date'] == "2020", f"Expected '2020', got '{normalized.get('pub_date')}'"
    assert normalized['num_pages'] == "453", f"Expected '453', got '{normalized.get('num_pages')}'"
    
    print(f"  ✓ Authors: {new_format_metadata['authors']} -> {normalized['author']}")
    print(f"  ✓ pub_date: {new_format_metadata['pub_date']} ({type(new_format_metadata['pub_date'])}) -> {normalized['pub_date']} ({type(normalized['pub_date'])})")
    print(f"  ✓ num_pages: {new_format_metadata['num_pages']} ({type(new_format_metadata['num_pages'])}) -> {normalized['num_pages']} ({type(normalized['num_pages'])})")
    
    # Test empty authors array
    empty_authors_metadata = {
        "title": "Test Document",
        "authors": [],  # Empty array
        "language": "Assyrian"
    }
    
    normalized_empty = fetcher._normalize_metadata(empty_authors_metadata)
    assert normalized_empty['author'] == "Unknown", f"Expected 'Unknown' for empty authors, got '{normalized_empty.get('author')}'"
    print(f"  ✓ Empty authors array -> {normalized_empty['author']}")
    
    # Test legacy format (should pass through unchanged)
    legacy_metadata = {
        "title": "Legacy Document",
        "author": "Legacy Author",  # Single author field
        "pub_date": "2020",         # String format
        "num_pages": "453"          # String format
    }
    
    normalized_legacy = fetcher._normalize_metadata(legacy_metadata)
    assert normalized_legacy['author'] == "Legacy Author"
    assert normalized_legacy['pub_date'] == "2020"
    assert normalized_legacy['num_pages'] == "453"
    print(f"  ✓ Legacy format preserved: author='{normalized_legacy['author']}'")
    
    print("✓ Metadata normalization tests passed\n")

def test_file_metadata():
    """Test local file metadata reading with new format"""
    print("Testing local file metadata reading (new format):")
    
    # Create a test metadata file with new format
    test_metadata_new = {
        "metadata": {
            "title": "Test Document New Format",
            "authors": ["Test Author One", "Test Author Two"],  # Array format
            "language": "Assyrian",
            "pub_date": 2020,      # Integer
            "num_pages": 453       # Integer
        }
    }
    
    import json
    with open("test_metadata_new.json", "w", encoding="utf-8") as f:
        json.dump(test_metadata_new, f)
    
    fetcher = MetadataFetcher()
    metadata = fetcher.get_metadata("test_metadata_new.json")
    
    if metadata:
        print(f"  Title: {metadata.get('title')}")
        print(f"  Authors array: {metadata.get('authors')}")
        print(f"  Primary author: {metadata.get('author')}")
        print(f"  pub_date: {metadata.get('pub_date')} ({type(metadata.get('pub_date'))})")
        print(f"  num_pages: {metadata.get('num_pages')} ({type(metadata.get('num_pages'))})")
        
        # Verify normalization worked
        assert metadata.get('author') == "Test Author One"
        assert isinstance(metadata.get('pub_date'), str)
        assert isinstance(metadata.get('num_pages'), str)
        
        print("✓ New format file metadata test passed")
    else:
        print("✗ New format file metadata test failed")
    
    # Clean up
    os.remove("test_metadata_new.json")
    print()

def main():
    """Run all tests"""
    print("=== Enhanced nose_to_vertical.py Test Suite ===\n")
    
    try:
        test_uuid_detection()
        test_config_loading()
        test_metadata_normalization()
        test_file_metadata()
        
        print("=== All tests passed! ===")
        print("\nUsage examples:")
        print("1. With UUID (API lookup):")
        print("   python nose_to_vertical.py -i input.xml -o output.vert -m '40a3280d-dfd5-4280-b98d-972669aeb14b' -t xml")
        print("\n2. With file path (local file):")
        print("   python nose_to_vertical.py -i input.xml -o output.vert -m 'metadata/book.json' -t xml")
        print("\n3. With custom config:")
        print("   python nose_to_vertical.py -i input.xml -o output.vert -m '40a3280d-dfd5-4280-b98d-972669aeb14b' -t xml -c my_config.json")
        
        print("\nNOTE: The system now handles:")
        print("- 'authors' array (picks first author for backward compatibility)")
        print("- Integer pub_date and num_pages (converts to strings)")
        print("- Both new and legacy metadata formats")
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

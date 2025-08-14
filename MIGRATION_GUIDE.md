# Migration Guide: Enhanced Metadata Support

## Overview

The `nose_to_vertical.py` script has been enhanced to support fetching metadata from a REST API in addition to local JSON files. This guide explains the changes and how to migrate existing workflows.

## What's New

### 1. API Metadata Support

- Pass a UUID to fetch metadata from a REST API
- Automatic detection of UUID vs file path
- Configurable API endpoint through config file

### 2. Enhanced Metadata Format Support

- **Authors Array**: `authors` field is now an array, system picks first author for backward compatibility
- **Vertical Output Authors**: When `authors` is provided as an array, the `<doc>` `author` attribute is emitted as a semicolon-separated list (e.g., `author="Author One; Author Two"`).
- **Integer Fields**: `pub_date` and `num_pages` can be integers (auto-converted to strings internally)
- **Dual Compatibility**: Supports both new format (authors array) and legacy format (single author)

### 3. New Dependencies

- `requests` library for HTTP requests
- `metadata_fetcher.py` module for metadata handling

### 4. Enhanced Configuration

- New `config.json` file for API settings
- Fallback support for local files

## Installation Requirements

Install the new dependency:

```bash
pip install requests
```

## Changes Made

### Modified Files

1. **nose_to_vertical.py**
   - Added `-c/--config` parameter for configuration file
   - Changed `-m/--metadata` parameter description
   - Enhanced error handling and validation
2. **base_strategy.py**
   - Updated `read_metadata()` method to use MetadataFetcher
   - Added constructor to initialize metadata fetcher
3. **README.md**
   - Updated usage examples and documentation
   - Added API response format specification
   - Documented semicolon-joined authors in `<doc>` output

### New Files

1. **metadata_fetcher.py**
   - Core logic for API and file-based metadata retrieval
   - UUID detection and validation
   - Configuration management
2. **config.json**
   - Configuration file for API settings
   - Timeout and fallback options
3. **test_enhanced_features.py**
   - Test suite for new functionality

## Migration Steps

### For Existing Users

#### Option 1: No Changes Required (File-based metadata)

Your existing commands will continue to work without modification:

```bash
# This still works exactly as before
python nose_to_vertical.py -i input.xml -o output.vert -m metadata/book.json -t xml
```

#### Option 2: Migrate to API-based metadata

1. Set up your API endpoint in `config.json`
1. Replace file paths with UUIDs in your commands:

```bash
# Old way (still supported)
python nose_to_vertical.py -i input.xml -o output.vert -m metadata/book.json -t xml

# New way with API
python nose_to_vertical.py -i input.xml -o output.vert -m 40a3280d-dfd5-4280-b98d-972669aeb14b -t xml
```

## Configuration Setup

1. **Create config.json** (done automatically on first run):

```json
{
  "api_endpoint": "http://localhost:5000/api/metadata/search",
  "timeout": 30,
  "fallback_to_file": true
}
```

1. **Update API endpoint** to match your server
1. **Test the connection** before migrating workflows

## API Requirements

Your metadata API should:

1. **Accept GET requests** with `id` parameter:

```http
GET /api/metadata/search?id=40a3280d-dfd5-4280-b98d-972669aeb14b
```

1. **Return JSON response** in this format:

```json
{
  "success": true,
  "results": [
    {
      "metadata": {
        "title": "Document Title",
        "authors": ["Author One", "Author Two"],  // New: Array format
        "language": "Assyrian",
        "dialect": "urmi",
        "pub_date": 2020,    // New: Integer format
        "num_pages": 453,    // New: Integer format
        "genre": "literature"
      }
    }
  ]
}
```

## Metadata Format Changes

### Authors Field

- **Old format**: `"author": "Single Author Name"`
- **New format**: `"authors": ["Author One", "Author Two", "Author Three"]`
- **Compatibility**: System automatically picks the first author from the array for backward compatibility
- **Both formats supported**: Existing files with single `author` field continue to work

### Vertical Output Author Attribute

- If `authors` array is present, output `<doc author="A; B; C" ...>`
- If only `author` is present, output `<doc author="A" ...>`

### Integer Fields

- **Changed fields**: `pub_date` and `num_pages`
- **Old format**: `"pub_date": "2020"` (string)
- **New format**: `"pub_date": 2020` (integer)
- **Compatibility**: System automatically converts integers to strings internally for backward compatibility

### Format Examples

**New API Response Format:**

```json
{
  "metadata": {
    "title": "Modern Document",
    "authors": ["Primary Author", "Secondary Author"],
    "pub_date": 2020,
    "num_pages": 453
  }
}
```

**Legacy File Format (still supported):**

```json
{
  "metadata": {
    "title": "Legacy Document", 
    "author": "Single Author",
    "pub_date": "2020",
    "num_pages": "453"
  }
}
```

## Backward Compatibility

✅ **Fully backward compatible**

- All existing commands work without changes
- File-based metadata still supported
- No breaking changes to existing functionality

## Testing

Run the test suite to verify everything works:

```bash
python test_enhanced_features.py
```

## Troubleshooting

### Common Issues

1. **"requests module not found"**
   - Install: `pip install requests`
1. **"Config file not found"**
   - Run the script once to auto-generate config.json
   - Edit the generated file with your API settings
1. **API connection fails**
   - Check network connectivity
   - Verify API endpoint URL in config.json
   - Check if API server is running
1. **UUID not recognized**
   - Ensure UUID format is correct (8-4-4-4-12 characters)
   - UUIDs are case-insensitive

### Debug Mode

Add verbose logging by modifying the script temporarily or check the console output for detailed error messages.

## Support

- Existing file-based workflows: No changes needed
- New API-based workflows: Follow the examples in this guide
- Mixed environments: Both approaches can be used simultaneously

## Next Steps

1. Test with existing files to ensure compatibility
1. Set up API endpoint configuration
1. Gradually migrate to UUID-based metadata as needed
1. Update any automation scripts to use new parameters if desired

# noSketchEngine Corpus Parsers for Modern Assyrian Text

## Overview

The `nose_to_vertical.py` script is the main orchestrator for converting various input file formats (XML, JSON, Text, etc.) into vertical file format suitable for corpus linguistics and NoSketch Engine. The script implements a Strategy design pattern to handle different input formats, making it extensible and maintainable for adding support for new formats.

## Architecture & Design

### Design Pattern: Strategy Pattern

The script uses the Strategy pattern with the following components:

1. **Context Class (`VerticalContext`)**: Orchestrates the conversion process
2. **Strategy Interface (`BaseVerticalStrategy`)**: Defines the contract for all conversion strategies
3. **Concrete Strategies**: Individual implementation for each file format
4. **Strategy Factory (`StrategyFactory`)**: Creates appropriate strategy instances based on file type

### Core Components

#### Main Script: `nose_to_vertical.py`

- **Purpose**: Command-line interface and orchestration
- **Responsibilities**:
  - Parse command line arguments
  - Instantiate appropriate strategy via StrategyFactory
  - Execute conversion through VerticalContext
  - Handle special cases (Kokhwa and Periodical workflows)

#### Usage

```sh
python nose_to_vertical.py --input <input_file> --output <output_file> --metadata <metadata_source> --type <file_type> [--config <config_file>"

# Required Arguments:
# --input (-i): Path to the input file or folder
# --output (-o): Path to the output vertical file
# --metadata (-m): Metadata UUID (for API lookup) or file path (for local file)
# --type (-t): Type of input file. Choices: xml, json, spurgeon, kokhwa, apocrypha, text, periodical

# Optional Arguments:
# --config (-c): Configuration file for API settings (default: config.json)

# Special Arguments:
# --kokhwa (-k): CSV_FILE TEXT_FOLDER - For Kokhwa periodical processing
# --periodical (-p): CSV_FILE TEXT_FOLDER - For general periodical processing
```

#### Metadata Sources

The script now supports two types of metadata sources:

1. **API Lookup (UUID)**: Pass a UUID to fetch metadata from a REST API

   ```sh
   python nose_to_vertical.py -i input.xml -o output.vert -m "40a3280d-dfd5-4280-b98d-972669aeb14b" -t xml
   ```

2. **Local File**: Pass a file path to read metadata from a local JSON file

   ```sh
   python nose_to_vertical.py -i input.xml -o output.vert -m "metadata/book.json" -t xml
   ```

#### Configuration File Format

```json
{
  "api_endpoint": "http://localhost:5000/api/metadata/search",
  "timeout": 30,
  "fallback_to_file": true
}
```

#### API Response Format

The API should return responses in this format:

```json
{
  "success": true,
  "results": [
    {
      "metadata": {
        "title": "Document Title",
        "authors": ["Author One", "Author Two"],
        "language": "Assyrian",
        "dialect": "urmi",
        "pub_date": 2020,
        "num_pages": 453,
        "genre": "literature"
      }
    }
  ]
}
```

**Format Notes:**

- `authors`: Array of author names. Vertical output sets `<doc ... author="Author One; Author Two">` (semicolon-separated). Internally, `author` is also set to the first author for backward compatibility.
- `pub_date`, `num_pages`: Can be integers or strings (auto-converted to strings internally)
- Backward compatible with legacy single `author` field

Example `<doc>` header in output when authors array is present:

```xml
<doc author="Author One; Author Two" title="Matt" ...>
```

#### Legacy Metadata File Format

```json
{
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "language": "Assyrian",
    "dialect": "urmi",
    "pub_date": "2020",
    "genre": "literature"
  }
}
```

### Dependencies and Components

#### 1. base_strategy.py

- **Purpose**: Abstract base class defining the strategy interface
- **Key Methods**:
  - `process()`: Abstract method implemented by all strategies
  - `read_metadata()`: Common utility to parse JSON metadata files
- **Dependencies**: `json` (standard library)

#### 2. strategies.py

- **Purpose**: Factory pattern implementation for strategy instantiation
- **Key Class**: `StrategyFactory`
- **Supported Types**: xml, json, spurgeon, kokhwa, apocrypha, text, periodical
- **Dependencies**: All concrete strategy classes

#### 3. Concrete Strategy Implementations

##### xml_to_vertical.py (NTXMLToVertical)

- **Purpose**: Converts XML files (especially New Testament) to vertical format
- **Use Case**: Biblical texts with XML markup

##### json_to_vertical.py (JSONToVerticalStrategy)

- **Purpose**: Processes JSON-formatted text data
- **Use Case**: Structured text data in JSON format

##### spurgeon_to_vertical.py (SpurgeonToVerticalStrategy)

- **Purpose**: Handles Spurgeon sermon collections
- **Use Case**: Religious/sermon text processing

##### kokhwa_to_vertical.py (KokhwaToVerticalStrategy)

- **Purpose**: Processes Kokhwa periodical data
- **Special Features**: Handles CSV metadata + multiple text files
- **Use Case**: Periodical/magazine content

##### aprocrypha_to_vertical.py (ApocryphaToVerticalStrategy)

- **Purpose**: Converts apocryphal texts
- **Use Case**: Non-canonical religious texts

##### text_to_vertical.py (TextToVerticalStrategy)

- **Purpose**: Basic plain text conversion
- **Use Case**: Simple text files

##### PeriodicaltoVerticalStrategy.py (PeriodicaltoVerticalStrategy)

- **Purpose**: General periodical processing
- **Special Features**: CSV + multiple text file handling
- **Use Case**: Magazine/journal content

#### 4. metadata_fetcher.py

- **Purpose**: Handles metadata retrieval from both API and local files
- **Key Features**:
  - UUID detection for API calls
  - HTTP request handling with timeout
  - Fallback to local files
  - Configuration management
- **Dependencies**: `requests`, `json`, `re`

#### 5. utils.py

- **Purpose**: Shared utility functions across all strategies
- **Key Functions**:
  - Text filtering and cleaning
  - Tokenization utilities
  - Character handling for Assyrian text
- **Features**:
  - Punctuation mark definitions (including Syriac-specific marks)
  - Non-printable character filtering
  - Sentence tokenization

### Special Processing Modes

#### Kokhwa Mode (`--kokhwa`)

- Processes CSV file containing page metadata
- Reads multiple `page_*.txt` files from specified folder
- Combines metadata and text content for periodical format

#### Periodical Mode (`--periodical`)

- Similar to Kokhwa but for general periodical content
- Uses same CSV + text file approach
- Flexible for various magazine/journal formats

### Design Notes

1. **Extensibility**: New file formats can be added by:
   - Creating a new strategy class inheriting from `BaseVerticalStrategy`
   - Implementing the `process()` method
   - Adding the strategy to `StrategyFactory`
2. **Error Handling**: The main script catches `ValueError` from unsupported file types
3. **Context Pattern**: `VerticalContext` class manages strategy execution and handles special cases for Kokhwa and Periodical types
4. **Metadata Integration**: All strategies use standardized JSON metadata format for consistent output. When `authors` is an array, strategies emit the `<doc>` `author` attribute as a semicolon-separated list.
5. **Corpus Linguistics Focus**: Output format optimized for NoSketch Engine and corpus analysis tools

## Extending the Script

To add support for a new file format:

1. Create a new strategy class inheriting from `BaseVerticalStrategy`
2. Implement the `process()` method with your conversion logic
3. Add the new strategy to `StrategyFactory.get_strategy()` method
4. Update the command-line choices in `nose_to_vertical.py`

## License

This project is licensed under the MIT License.
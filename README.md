# noSketchEngine Corpus Parsers for Modern Assyrian Text

## Overview

The `nose_to_vertical.py` script is designed to convert various input file formats XML, JSON, Text, etc., into a vertical file format. The script uses a strategy pattern to handle different input formats, making it easy to extend and add support for new formats in the future.

## Functional Specifications

### Main Script: `nose_to_vertical.py`

The main script handles command line arguments, instantiates the appropriate strategy based on the input file extension, and executes the conversion process.

#### Usage
To convert an input file to a vertical file, use the following command:

```sh
python nose_to_vertical.py --input <input_file> --output <output_file> --metadata <metadata_file> --type <file_type>

--input (-i): Path to the input file.
--output (-o): Path to the output vertical file.
--metadata (-m): Path to the metadata file (JSON format).
--type (-t): Type of the input file. Choices are xml, json, spurgeon, kokhwa, apocrypha.


<metadata_file>: Path to metadata json file in this format:
{
    "attribute 1": "value 1",
    "attribute 2": "value 2",
}
```
### CAVEAT 
Additional commandline args with additional options may be have been added. Always check the nose_to_vertical.py for latest updates.


## Supported Modules
#### 1. base_strategy.py
Defines the base class for all vertical conversion strategies.
#### 2. xml_to_vertical.py
Implements the strategy for converting XML files to vertical format.
#### 3. json_to_vertical.py
Implements the strategy for converting JSON files to vertical format.
#### 4. strategies.py
Provides a factory to get the appropriate strategy based on the file extension.
#### 5. utils.py
Contains utility functions used by the strategies.

## Extending the Script
To add support for a new file format, create a new strategy class that inherits from BaseVerticalStrategy and implements the process method. Then, update the StrategyFactory in strategies.py to include the new strategy.

## License
This project is licensed under the MIT License.
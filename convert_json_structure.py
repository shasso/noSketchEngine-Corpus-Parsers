import json
import argparse
import uuid
import os

def has_correct_structure(data):
    """Check if JSON has the correct structure with 'id' and 'metadata' keys"""
    return isinstance(data, dict) and 'id' in data and 'metadata' in data

def convert_json_structure(input_file, output_file):
    """Convert flat JSON structure to nested structure with id and metadata"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if already has correct structure
        if has_correct_structure(data):
            print(f"File {input_file} already has correct structure. Skipping conversion.")
            # Copy to output file anyway
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return
        
        # Convert to new structure
        new_structure = {
            "id": str(uuid.uuid4()),
            "metadata": data
        }
        
        # Write converted structure to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(new_structure, f, ensure_ascii=False, indent=2)
        
        print(f"Converted {input_file} to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert JSON metadata files to correct structure.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    convert_json_structure(args.input, args.output)

if __name__ == '__main__':
    main()

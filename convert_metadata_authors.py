import json
import argparse
import os

def convert_metadata_structure(input_file, output_path):
    """Convert JSON metadata structure: change 'author' to 'authors' array and remove 'id'"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove 'id' field if it exists
        if 'id' in data:
            del data['id']
        
        # Check if metadata exists
        if 'metadata' not in data:
            print(f"Warning: No 'metadata' field found in {input_file}")
            return
        
        metadata = data['metadata']
        
        # Convert 'author' to 'authors' array
        if 'author' in metadata:
            author_value = metadata['author']
            # Remove the old 'author' field
            del metadata['author']
            # Add new 'authors' field as array
            metadata['authors'] = [author_value] if author_value else []
        
        # Create output file path
        input_filename = os.path.basename(input_file)
        output_file = os.path.join(output_path, input_filename)
        
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Write converted structure to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Converted {input_file} to {output_file}")
        print(f"- Removed 'id' field")
        print(f"- Changed 'author' to 'authors' array")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert JSON metadata: change author to authors array and remove id.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file path')
    parser.add_argument('-o', '--output', required=True, help='Output file name (same as input)')
    parser.add_argument('-p', '--path', required=True, help='Output directory path')
    
    args = parser.parse_args()
    
    # Validate that output filename matches input filename
    input_filename = os.path.basename(args.input)
    if args.output != input_filename:
        print(f"Warning: Output filename '{args.output}' doesn't match input filename '{input_filename}'")
        print(f"Using input filename: {input_filename}")
    
    convert_metadata_structure(args.input, args.path)

if __name__ == '__main__':
    main()

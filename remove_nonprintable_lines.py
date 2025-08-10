import argparse

def remove_nonprintable(text):
    # Remove all non-printable characters except for newlines
    return ''.join(c for c in text if c == '\n' or (c.isprintable() and c != '\r'))

def clean_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned = remove_nonprintable(line)
            if cleaned.strip():  # Only write non-empty lines
                outfile.write(cleaned)

def main():
    parser = argparse.ArgumentParser(description='Remove non-printable characters from a file.')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    args = parser.parse_args()
    clean_file(args.input, args.output)

if __name__ == '__main__':
    main()

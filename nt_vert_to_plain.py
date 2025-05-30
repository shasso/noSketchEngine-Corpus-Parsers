import argparse
import re

def parse_vert(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        chapter_title = None
        chapter_no = None
        verse_lines = []
        in_verse = False
        in_chapter = False
        for line in infile:
            line = line.strip()
            # Handle <doc ...> for title
            if line.startswith('<doc'):
                m = re.search(r'title="([^"]+)"', line)
                if m:
                    chapter_title = m.group(1)
                continue
            # Handle <chapter no="...">
            if line.startswith('<chapter'):
                m = re.search(r'no="([^"]+)"', line)
                if m:
                    chapter_no = m.group(1)
                    if chapter_title and chapter_no:
                        outfile.write(f"{chapter_title} chapter {chapter_no}\n")
                in_chapter = True
                continue
            if line.startswith('</chapter'):
                in_chapter = False
                continue
            # Remove <g/> tags
            if line == '<g/>':
                continue
            # Handle verse start
            if line.startswith('<verse'):
                in_verse = True
                verse_lines = []
                continue
            # Handle verse end
            if line.startswith('</verse'):
                if verse_lines:
                    outfile.write(' '.join(verse_lines).strip() + '\n')
                in_verse = False
                verse_lines = []
                continue
            # Remove <doc> and </doc>
            if line.startswith('</doc'):
                continue
            # If inside a verse, collect words
            if in_verse and line and not line.startswith('<'):
                verse_lines.append(line)
        # Write any remaining verse (in case file ends without closing tag)
        if verse_lines:
            outfile.write(' '.join(verse_lines).strip() + '\n')

def main():
    parser = argparse.ArgumentParser(description='Process NT.vert to plain text.')
    parser.add_argument('-i', '--input', required=True, help='Input .vert file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    args = parser.parse_args()
    parse_vert(args.input, args.output)

if __name__ == '__main__':
    main()

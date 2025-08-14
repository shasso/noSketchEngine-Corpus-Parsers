import xml.etree.ElementTree as ET
from base_strategy import BaseVerticalStrategy
from utils import tokenize_sentence

def extract_chapter_no(bcv):
    # Extract the chapter number from the "bcv" attribute
    parts = bcv.split('.')
    if len(parts) == 3:
        return parts[1]
    return ""

class NTXMLToVertical(BaseVerticalStrategy):
    def process(self, input_file, output_file, metadata_file):
        metadata = self.read_metadata(metadata_file)
        tree = ET.parse(input_file)
        root = tree.getroot()

        with open(output_file, 'w', encoding='utf-8') as f:
            for book in root.findall('book'):
                book_id = book.get('id', 'Unknown')
                # Build author attribute from authors array or single author
                authors_list = []
                if isinstance(metadata.get('authors'), list):
                    authors_list = [str(a).strip() for a in metadata.get('authors', []) if str(a).strip()]
                author_attr = "; ".join(authors_list) if authors_list else str(metadata.get('author', 'Unknown'))

                doc_tag = f'<doc'
                for key, value in metadata.items():
                    if key in ('author', 'authors'):
                        continue
                    doc_tag += f' {key}="{value}"'
                doc_tag += f' author="{author_attr}" title="{book_id}">\n'
                f.write(doc_tag)
                
                chapters = {}
                for verse in book.findall('v'):
                    verse_id = verse.get('id', 'Unknown')
                    bcv = verse.get('bcv', 'Unknown.Unknown.Unknown')
                    chapter_no = extract_chapter_no(bcv)
                    
                    if chapter_no not in chapters:
                        chapters[chapter_no] = []
                    
                    verse_text = verse.text.strip() if verse.text else ""
                    tokens = tokenize_sentence(verse_text)
                    verse_content = f'<verse no="{verse_id}">\n'
                    for token in tokens:
                        verse_content += f'{token}\n'
                    verse_content += '</verse>\n'
                    
                    chapters[chapter_no].append(verse_content)
                
                for chapter_no, verses in chapters.items():
                    f.write(f'<chapter no="{chapter_no}">\n')
                    for verse_content in verses:
                        f.write(verse_content)
                    f.write('</chapter>\n')
                
                f.write('</doc>\n')
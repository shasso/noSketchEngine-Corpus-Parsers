import xml.etree.ElementTree as ET
from base_strategy import BaseVerticalStrategy

# Define additional punctuation marks
additional_punctuation = {
    '\u002d',  # HYPHEN-MINUS
    '\u060c',  # ARABIC COMMA
    '\u061b',  # ARABIC SEMICOLON
    '\u061f',  # ARABIC QUESTION MARK
    '\u2018',  # LEFT SINGLE QUOTATION MARK
    '\u2019',  # RIGHT SINGLE QUOTATION MARK
    '\u201c',  # LEFT DOUBLE QUOTATION MARK
    '\u201d'   # RIGHT DOUBLE QUOTATION MARK
}

def tokenize_sentence(sentence):
    tokens = []
    word = ""
    for char in sentence:
        if char in ".,;:!?" or char in additional_punctuation:
            if word:
                tokens.append(word)
                word = ""
            tokens.append("<g/>")
            tokens.append(char)
        elif char.isspace():
            if word:
                tokens.append(word)
                word = ""
        else:
            word += char
    if word:
        tokens.append(word)
    return tokens

def extract_chapter_no(bcv):
    # Extract the chapter number from the "bcv" attribute
    parts = bcv.split('.')
    if len(parts) == 3:
        return parts[1]
    return ""

class NTXMLToVertical(BaseVerticalStrategy):
    def process(self, input_file, output_file):
        tree = ET.parse(input_file)
        root = tree.getroot()

        with open(output_file, 'w', encoding='utf-8') as f:
            for book in root.findall('book'):
                book_id = book.get('id', 'Unknown')
                f.write(f'<doc genre="new testament" title="{book_id}" author="Unknown">\n')
                
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

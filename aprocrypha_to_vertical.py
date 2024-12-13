import xml.etree.ElementTree as ET
from base_strategy import BaseVerticalStrategy
from utils import tokenize_sentence

class ApocryphaToVerticalStrategy(BaseVerticalStrategy):
    def process(self, input_file, output_file, metadata_file):
        metadata = self.read_metadata(metadata_file)
        
        # Read the content of the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the XML content
        tree = ET.ElementTree(ET.fromstring(content))
        root = tree.getroot()

        with open(output_file, 'w', encoding='utf-8') as f:
            title = root.find('title').text.strip() if root.find('title') is not None else 'Unknown'
            doc_tag = f'<doc'
            for key, value in metadata.items():
                doc_tag += f' {key}="{value}"'
            doc_tag += f' title="{title}">\n'
            f.write(doc_tag)

            for element in root:
                if element.tag == 'chapter':
                    chapter_no = element.get('no', 'Unknown')
                    f.write(f'<chapter no="{chapter_no}">\n')
                    for sub_element in element:
                        if sub_element.tag == 'verse':
                            verse_no = sub_element.get('no', 'Unknown')
                            verse_text = sub_element.text.strip() if sub_element.text else ""
                            tokens = tokenize_sentence(verse_text)
                            f.write(f'<verse no="{verse_no}">\n')
                            for token in tokens:
                                f.write(f'{token}\n')
                            f.write('</verse>\n')
                        elif sub_element.tag in ['header', 'heading']:
                            header_text = sub_element.text.strip() if sub_element.text else ""
                            tokens = tokenize_sentence(header_text)
                            f.write(f'<heading>\n')
                            for token in tokens:
                                f.write(f'{token}\n')
                            f.write('</heading>\n')
                    f.write('</chapter>\n')
                elif element.tag in ['header', 'heading']:
                    header_text = element.text.strip() if element.text else ""
                    tokens = tokenize_sentence(header_text)
                    f.write(f'<heading>\n')
                    for token in tokens:
                        f.write(f'{token}\n')
                    f.write('</heading>\n')
                elif element.tag == 'verse':
                    verse_no = element.get('no', 'Unknown')
                    verse_text = element.text.strip() if element.text else ""
                    tokens = tokenize_sentence(verse_text)
                    f.write(f'<verse no="{verse_no}">\n')
                    for token in tokens:
                        f.write(f'{token}\n')
                    f.write('</verse>\n')

            f.write('</doc>\n')
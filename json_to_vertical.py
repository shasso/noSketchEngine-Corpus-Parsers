import json
from base_strategy import BaseVerticalStrategy
from utils import tokenize_sentence

class JSONToVerticalStrategy(BaseVerticalStrategy):
    def process(self, input_file, output_file, metadata_file):
        metadata = self.read_metadata(metadata_file)
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(output_file, 'w', encoding='utf-8') as f:
            for book, chapters in data.items():
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
                doc_tag += f' author="{author_attr}" title="{book}">\n'
                f.write(doc_tag)
                
                for chapter_no, verses in chapters.items():
                    f.write(f'<chapter no="{chapter_no}">\n')
                    for verse_no, verse_content in verses.items():
                        syriac_text = verse_content.get("syriac", "")
                        tokens = tokenize_sentence(syriac_text)
                        f.write(f'<verse no="{verse_no}">\n')
                        for token in tokens:
                            f.write(f'{token}\n')
                        f.write('</verse>\n')
                    f.write('</chapter>\n')
                f.write('</doc>\n')
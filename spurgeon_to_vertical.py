from base_strategy import BaseVerticalStrategy
from utils import tokenize_sentence

class SpurgeonToVerticalStrategy(BaseVerticalStrategy):
    def process(self, input_file, output_file, metadata_file):
        metadata = self.read_metadata(metadata_file)
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(output_file, 'w', encoding='utf-8') as f:
            # Write the root <doc> element with metadata attributes
            doc_tag = f'<doc'
            for key, value in metadata.items():
                doc_tag += f' {key}="{value}"'
            doc_tag += '>\n'
            f.write(doc_tag)
            
            section_no = 1
            section_title_1 = ""
            section_title_2 = ""
            section_content = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("\\s1"):
                    if section_content:
                        f.write(f'<section no="{section_no}">\n')
                        f.write(f'<section_title>\n')
                        tokens = tokenize_sentence(section_title_1)
                        for token in tokens:
                            f.write(f'{token}\n')
                        f.write(f'</section_title>\n')
                        f.write(f'<verse_quote>\n')
                        tokens = tokenize_sentence(section_title_2)
                        for token in tokens:
                            f.write(f'{token}\n')
                        f.write(f'</verse_quote>\n')
                        tokens = tokenize_sentence(section_content)
                        for token in tokens:
                            f.write(f'{token}\n')
                        f.write('</section>\n')
                        section_no += 1
                        section_content = ""
                    section_title_1 = line[3:].strip()
                elif line.startswith("\\s2"):
                    section_title_2 = line[3:].strip()
                elif line.startswith("\\p") or line.startswith("\\pc"):
                    section_content += line[3:].strip() + " "
            
            # Write the last section if any content remains
            if section_content:
                f.write(f'<section no="{section_no}">\n')
                f.write(f'<section_title>\n')
                tokens = tokenize_sentence(section_title_1)
                for token in tokens:
                    f.write(f'{token}\n')
                f.write(f'</section_title>\n')
                f.write(f'<verse_quote>\n')
                tokens = tokenize_sentence(section_title_2)
                for token in tokens:
                    f.write(f'{token}\n')
                f.write(f'</verse_quote>\n')
                tokens = tokenize_sentence(section_content)
                for token in tokens:
                    f.write(f'{token}\n')
                f.write('</section>\n')
            
            f.write('</doc>\n')
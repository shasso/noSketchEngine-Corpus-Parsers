import os
from base_strategy import BaseVerticalStrategy
from utils import tokenize_sentence

class TextToVerticalStrategy(BaseVerticalStrategy):
    def process(self, input_folder, output_file, metadata_file):
        metadata = self.read_metadata(metadata_file)

        with open(output_file, 'w', encoding='utf-8') as f:
            # Write the root <doc> element with metadata attributes
            doc_tag = f'<doc'
            for key, value in metadata.items():
                doc_tag += f' {key}="{value}"'
            doc_tag += '>\n'
            f.write(doc_tag)

            for text_file in os.listdir(input_folder):
                if text_file.startswith('page_') and text_file.endswith('.txt'):
                    page_no = text_file[5:-4]  # Extract the page number from the file name
                    file_path = os.path.join(input_folder, text_file)
                    with open(file_path, 'r', encoding='utf-8') as pf:
                        page_content = pf.readlines()
                        f.write(f'<page no="{page_no}">\n')
                        for line in page_content:
                            line = line.strip()
                            if line:  # Ignore blank lines
                                tokens = tokenize_sentence(line)
                                for token in tokens:
                                    f.write(f'{token}\n')
                        f.write('</page>\n')

            f.write('</doc>\n')
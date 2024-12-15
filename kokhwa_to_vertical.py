import csv
import os
from base_strategy import BaseVerticalStrategy
from utils import tokenize_sentence

class KokhwaToVerticalStrategy(BaseVerticalStrategy):
    def process(self, input_file, output_file, metadata_file, csv_file, text_files):
        metadata = self.read_metadata(metadata_file)
        periodical_info = self.read_csv(csv_file)

        with open(output_file, 'w', encoding='utf-8') as f:
            # Write the root <doc> element with metadata attributes
            doc_tag = f'<doc'
            for key, value in metadata.items():
                doc_tag += f' {key}="{value}"'
            doc_tag += '>\n'
            f.write(doc_tag)

            for info in periodical_info:
                issue = info['issue']
                number = info['number']
                date = info['date']
                num_of_pages = info['num_pages']
                start_page = int(info['start_page'])
                file_start = int(info['file_start'])
                file_end = int(info['file_end'])

                # Write the <periodical> element
                f.write(f'<periodical issue="{issue}" no="{number}" date="{date}" num_of_pages="{num_of_pages}">\n')

                logical_page_no = start_page
                for page_no in range(file_start, file_end + 1):
                    page_file = f'page_{page_no}.txt'
                    for text_file in text_files:
                        if os.path.basename(text_file) == page_file:
                            with open(text_file, 'r', encoding='utf-8') as pf:
                                page_content = pf.readlines()
                                f.write(f'<page no="{logical_page_no}">\n')
                                for line in page_content:
                                    line = line.strip()
                                    if line:  # Ignore blank lines
                                        tokens = tokenize_sentence(line)
                                        for token in tokens:
                                            f.write(f'{token}\n')
                                f.write('</page>\n')
                            logical_page_no += 1

                f.write('</periodical>\n')

            f.write('</doc>\n')

    def read_csv(self, csv_file):
        periodical_info = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                periodical_info.append(row)
        return periodical_info
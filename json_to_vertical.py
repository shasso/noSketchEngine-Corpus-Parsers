import json
from base_strategy import BaseVerticalStrategy

def tokenize_sentence(sentence):
    tokens = []
    word = ""
    for char in sentence:
        if char.isalnum():
            word += char
        else:
            if word:
                tokens.append(word)
                word = ""
            if char.isspace():
                continue
            tokens.append(char)
    if word:
        tokens.append(word)
    return tokens

class JSONToVerticalStrategy(BaseVerticalStrategy):
    def process(self, input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(output_file, 'w', encoding='utf-8') as f:
            for book, chapters in data.items():
                f.write(f'<doc genre="bible" title="{book}" author="Moses">\n')
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
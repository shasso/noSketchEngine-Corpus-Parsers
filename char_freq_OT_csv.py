import csv
import unicodedata

def get_char_info(char):
    try:
        name = unicodedata.name(char)
    except ValueError:
        name = "UNKNOWN"
    return char, f"U+{ord(char):04X}", name

def count_characters(file_path):
    char_count = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        for char in text:
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1
    return char_count

def write_csv(char_count, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Character', 'Unicode', 'Name', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for char, count in char_count.items():
            char_info = get_char_info(char)
            writer.writerow({
                'Character': char_info[0],
                'Unicode': char_info[1],
                'Name': char_info[2],
                'Count': count
            })

if __name__ == "__main__":
    input_file = r'C:\Users\sargo\Documents\dockerDev\noSketchEngine Corpus Parsers\vert_output\OT_2.vert'
    output_file = 'char_frequency.csv'
    
    char_count = count_characters(input_file)
    write_csv(char_count, output_file)
    
    print(f"Character frequency has been written to {output_file}")
import sys
import os
from strategies import StrategyFactory, KokhwaToVerticalStrategy

class VerticalContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, input_file, output_file, metadata_file, csv_file=None, text_files=None):
        self.strategy.process(input_file, output_file, metadata_file, csv_file, text_files)

def handle_k_option(csv_file, text_folder, output_file, metadata_file):
    text_files = [os.path.join(text_folder, f) for f in os.listdir(text_folder) if f.startswith('page_') and f.endswith('.txt')]
    strategy = KokhwaToVerticalStrategy()
    context = VerticalContext(strategy)
    context.execute_strategy(None, output_file, metadata_file, csv_file, text_files)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python nose_to_vertical.py <input_file> <output_file> <metadata_file> [-k <csv_file> <text_folder>]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    metadata_file = sys.argv[3]

    if '-k' in sys.argv:
        if len(sys.argv) != 7:
            print("Usage: python nose_to_vertical.py <input_file> <output_file> <metadata_file> -k <csv_file> <text_folder>")
            sys.exit(1)
        csv_file = sys.argv[5]
        text_folder = sys.argv[6]
        handle_k_option(csv_file, text_folder, output_file, metadata_file)
    else:
        file_extension = input_file.split('.')[-1]
        try:
            strategy = StrategyFactory.get_strategy(f'.{file_extension}')
        except ValueError as e:
            print(e)
            sys.exit(1)

        context = VerticalContext(strategy)
        context.execute_strategy(input_file, output_file, metadata_file)
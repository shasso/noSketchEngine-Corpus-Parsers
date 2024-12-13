import sys
import os
import argparse
from strategies import StrategyFactory, KokhwaToVerticalStrategy

class VerticalContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, input_file, output_file, metadata_file, csv_file=None, text_files=None):
        if isinstance(self.strategy, KokhwaToVerticalStrategy):
            self.strategy.process(input_file, output_file, metadata_file, csv_file, text_files)
        else:
            self.strategy.process(input_file, output_file, metadata_file)

def handle_k_option(csv_file, text_folder, output_file, metadata_file):
    text_files = [os.path.join(text_folder, f) for f in os.listdir(text_folder) if f.startswith('page_') and f.endswith('.txt')]
    strategy = KokhwaToVerticalStrategy()
    context = VerticalContext(strategy)
    context.execute_strategy(None, output_file, metadata_file, csv_file, text_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert various input files to vertical format.")
    parser.add_argument("-i", "--input", required=True, help="Input file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("-m", "--metadata", required=True, help="Metadata file")
    parser.add_argument("-t", "--type", required=True, choices=["xml", "json", "spurgeon", "kokhwa", "apocrypha"], help="Type of the input file")
    parser.add_argument("-k", "--kokhwa", nargs=2, metavar=("CSV_FILE", "TEXT_FOLDER"), help="CSV file and text folder for Kokhwa periodical")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    metadata_file = args.metadata
    file_type = args.type

    if args.kokhwa:
        csv_file, text_folder = args.kokhwa
        handle_k_option(csv_file, text_folder, output_file, metadata_file)
    else:
        try:
            strategy = StrategyFactory.get_strategy(file_type)
        except ValueError as e:
            print(e)
            sys.exit(1)

        context = VerticalContext(strategy)
        context.execute_strategy(input_file, output_file, metadata_file)
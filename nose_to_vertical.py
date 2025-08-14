import sys
import os
import argparse
from strategies import StrategyFactory, KokhwaToVerticalStrategy, PeriodicaltoVerticalStrategy
from metadata_fetcher import MetadataFetcher

class VerticalContext:
    def __init__(self, strategy, config_file="config.json"):
        self.strategy = strategy
        # Pass config to strategies that support it
        if hasattr(strategy, 'set_config'):
            strategy.set_config(config_file)

    def execute_strategy(self, input_file, output_file, metadata_source, csv_file=None, text_files=None):
        if isinstance(self.strategy, KokhwaToVerticalStrategy):
            self.strategy.process(input_file, output_file, metadata_source, csv_file, text_files)
        elif isinstance(self.strategy, PeriodicaltoVerticalStrategy):
            self.strategy.process(input_file, output_file, metadata_source, csv_file, text_files)
        else:
            self.strategy.process(input_file, output_file, metadata_source)

def handle_k_option(csv_file, text_folder, output_file, metadata_source, config_file):
    text_files = [os.path.join(text_folder, f) for f in os.listdir(text_folder) if f.startswith('page_') and f.endswith('.txt')]
    strategy = KokhwaToVerticalStrategy()
    if hasattr(strategy, 'set_config'):
        strategy.set_config(config_file)
    context = VerticalContext(strategy, config_file)
    context.execute_strategy(None, output_file, metadata_source, csv_file, text_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert various input files to vertical format.")
    parser.add_argument("-i", "--input", required=True, help="Input file or folder")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("-m", "--metadata", required=True, help="Metadata UUID (for API lookup) or file path (for local file)")
    parser.add_argument("-t", "--type", required=True, choices=["xml", "json", "spurgeon", "kokhwa", "apocrypha", "text", "periodical"], help="Type of the input file")
    parser.add_argument("-k", "--kokhwa", nargs=2, metavar=("CSV_FILE", "TEXT_FOLDER"), help="CSV file and text folder for Kokhwa periodical")
    parser.add_argument("-p", "--periodical", nargs=2, metavar=("CSV_FILE", "TEXT_FOLDER"), help="CSV file and text folder for Periodical")
    parser.add_argument("-c", "--config", default="config.json", help="Configuration file for API settings (default: config.json)")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    metadata_source = args.metadata
    file_type = args.type
    config_file = args.config

    # Validate config file exists, create sample if not
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found. Creating sample config...")
        fetcher = MetadataFetcher()
        fetcher.create_sample_config(config_file)
        print(f"Please edit {config_file} with your API settings and run again.")
        sys.exit(1)

    if args.kokhwa:
        csv_file, text_folder = args.kokhwa
        handle_k_option(csv_file, text_folder, output_file, metadata_source, config_file)
    elif args.periodical:
        csv_file, text_folder = args.periodical
        text_files = [os.path.join(text_folder, f) for f in os.listdir(text_folder) if f.startswith('page_') and f.endswith('.txt')]
        strategy = PeriodicaltoVerticalStrategy()
        if hasattr(strategy, 'set_config'):
            strategy.set_config(config_file)
        context = VerticalContext(strategy, config_file)
        context.execute_strategy(None, output_file, metadata_source, csv_file, text_files)
    else:
        try:
            strategy = StrategyFactory.get_strategy(file_type)
            if hasattr(strategy, 'set_config'):
                strategy.set_config(config_file)
        except ValueError as e:
            print(e)
            sys.exit(1)

        context = VerticalContext(strategy, config_file)
        context.execute_strategy(input_file, output_file, metadata_source)
import sys
from strategies import StrategyFactory

class VerticalContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, input_file, output_file, metadata_file):
        self.strategy.process(input_file, output_file, metadata_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python nose_to_vertical.py <input_file> <output_file> <metadata_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    metadata_file = sys.argv[3]
    file_extension = input_file.split('.')[-1]

    try:
        strategy = StrategyFactory.get_strategy(f'.{file_extension}')
    except ValueError as e:
        print(e)
        sys.exit(1)

    context = VerticalContext(strategy)
    context.execute_strategy(input_file, output_file, metadata_file)
import json

class BaseVerticalStrategy:
    def process(self, input_file, output_file, metadata_file):
        raise NotImplementedError("Subclasses should implement this method!")

    def read_metadata(self, metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata
    
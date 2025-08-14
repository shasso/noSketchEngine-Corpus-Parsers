import json
from metadata_fetcher import MetadataFetcher

class BaseVerticalStrategy:
    def __init__(self):
        self.metadata_fetcher = MetadataFetcher()
    
    def process(self, input_file, output_file, metadata_file):
        raise NotImplementedError("Subclasses should implement this method!")

    def read_metadata(self, metadata_source):
        """
        Read metadata from either API (UUID) or file (path)
        
        Args:
            metadata_source: Either a UUID or file path
            
        Returns:
            Dictionary containing metadata
        """
        metadata = self.metadata_fetcher.get_metadata(metadata_source)
        if metadata is None:
            raise ValueError(f"Could not load metadata from: {metadata_source}")
        return metadata
    
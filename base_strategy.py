class BaseVerticalStrategy:
    def process(self, input_file, output_file):
        raise NotImplementedError("Subclasses should implement this method!")
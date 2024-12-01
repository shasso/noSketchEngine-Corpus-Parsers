from xml_to_vertical import NTXMLToVertical
from json_to_vertical import JSONToVerticalStrategy

class StrategyFactory:
    @staticmethod
    def get_strategy(file_extension):
        if file_extension == '.xml':
            return NTXMLToVertical()
        elif file_extension == '.json':
            return JSONToVerticalStrategy()
        else:
            raise ValueError("Unsupported file format")
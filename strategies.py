from xml_to_vertical import NTXMLToVertical
from json_to_vertical import JSONToVerticalStrategy
from spurgeon_to_vertical import SpurgeonToVerticalStrategy
from kokhwa_to_vertical import KokhwaToVerticalStrategy

class StrategyFactory:
    @staticmethod
    def get_strategy(file_extension):
        if file_extension == '.xml':
            return NTXMLToVertical()
        elif file_extension == '.json':
            return JSONToVerticalStrategy()
        elif file_extension == '.spurgeon':
            return SpurgeonToVerticalStrategy()
        elif file_extension == '.kokhwa':
            return KokhwaToVerticalStrategy()
        else:
            raise ValueError("Unsupported file format")
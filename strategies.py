from xml_to_vertical import NTXMLToVertical
from json_to_vertical import JSONToVerticalStrategy
from spurgeon_to_vertical import SpurgeonToVerticalStrategy
from kokhwa_to_vertical import KokhwaToVerticalStrategy
from aprocrypha_to_vertical import ApocryphaToVerticalStrategy
from text_to_vertical import TextToVerticalStrategy

class StrategyFactory:
    @staticmethod
    def get_strategy(file_type):
        if file_type == 'xml':
            return NTXMLToVertical()
        elif file_type == 'json':
            return JSONToVerticalStrategy()
        elif file_type == 'spurgeon':
            return SpurgeonToVerticalStrategy()
        elif file_type == 'kokhwa':
            return KokhwaToVerticalStrategy()
        elif file_type == 'apocrypha':
            return ApocryphaToVerticalStrategy()
        elif file_type == 'text':
            return TextToVerticalStrategy()
        else:
            raise ValueError("Unsupported file type")
from enum import Enum
from langchain.output_parsers.enum import EnumOutputParser

class Decision(Enum):
    YES = "yes"
    NO = "no"

class LocationCategory(Enum):
    DINING="dining"
    ATTRACTIONS="attractions"
    OUTDOOR_ACTIVITY="outdoor activities"
    ENTERTRAINMENT="entertainment"
    ACCOMMODATION="accommodation"
    ETC="etc"

parser = EnumOutputParser(enum=Decision)
location_output_parser = EnumOutputParser(enum=LocationCategory)
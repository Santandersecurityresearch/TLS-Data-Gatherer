import pandas
import re
import json
import utils

# The purpose of this function is to apply the filters we establish for each Technology in the dictionary.
def tech_property_filter(row:pandas.DataFrame, technology:str):
    # Read the dictionary_filter
    dict_filter = utils.read_json('config_dictionaries/dictionary_filter.json')
    # Check if the technology is in the dictionary
    if re.search(fr"{dict_filter[technology][1]}", row[dict_filter[technology][0]]):
        return True
    else:
        return False
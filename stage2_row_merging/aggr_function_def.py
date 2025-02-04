import json
import config
import utils

# Aggregate functions. We write 'first' for the first fifteen columns as they 
# will have the same value for all grouped rows with that "Host IP & Instance".
# Then, we write 'sum' for the new columns. They will only have a single value 
# on a single row out of each group.
def aggr_function_def(technology:str):
    dictionary_string = config.values[technology]["dictionary"] # dictionary to look on
    aggr_function = utils.read_json(f'config_dictionaries/dictionary_aggr_functions_{dictionary_string}.json')
    return aggr_function
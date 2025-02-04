import csv
import pandas
import json
from stage4_tls_versions.tls_version_extraction_enabled import tls_version_extraction_enabled
from stage4_tls_versions.tech_property_filter import tech_property_filter
import config
import utils

# Stage 4: TLS Data Extraction

# Run Stage 4
# Reads the .csv generated on Stage 3
# Output: "[original_csv_filename]_Stage3_TLSVersionsInterpreted.csv"
def run_stage4(original_csv_filename:str, tech:str):
    try:
        # Read and intepret the .csv generated on Stage 3
        dictionary_string = config.values[tech]["dictionary"]
        dtype_dict = utils.read_json(f'config_dictionaries/dictionary_{dictionary_string}.json')
        dataFrame_stage4=pandas.read_csv(utils.get_filename_stage(3, original_csv_filename),dtype=dtype_dict)

        # Apply the filters established for each Technology in the dictionary
        # We declare a new column that will follow the criteria:
        # If "+[protocol]" is found, it is added to the total of TLS versions
        # If "-[protocol]" is found, it is removed from the total of TLS versions
        # If "[protocol]" is found, it replaces the current string
        # If ["All"] is found, it writes all the strings (looking first at the Apache tech involved)
        # If ["-All"] is found, it removes all the strings (looking first at the Apache tech involved)
        # Upon getting the final available TLS version list, a clasification is determined.
        dataFrame_stage4["TLS_VERSION"]=dataFrame_stage4.apply(tls_version_extraction_enabled, technology=tech, axis=1)

        # Export result into .csv file
        dataFrame_stage4.to_csv(utils.get_filename_stage(4, original_csv_filename), index=False)
    except Exception as e:
        raise Exception(f"Error on stage 4: {str(e)}")
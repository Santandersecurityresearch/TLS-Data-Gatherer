import pandas
import config
import utils
from stage3_vh.ip_port_transformation import (
    filter_undetected_controls, apply_transformations, dataFrames_by_IPPort)

# Stage 3: IP-port pair extraction

# Runs Stage 3
# Reads the .csv generated on Stage 2
# Output: "[original_csv_filename]_Stage3_VirtualHostSeparation.csv"
def run_stage3(original_csv_filename:str, tech:str):
    try:
        # Read the .csv generated on Stage 2 into a dataFrame
        dictionary_string = config.values[tech]["dictionary"] # dictionary to look on
        dtype_dict = utils.read_json(f'config_dictionaries/dictionary_{dictionary_string}.json')
        dataFrame_stage2=pandas.read_csv(utils.get_filename_stage(2, original_csv_filename),dtype=dtype_dict)

        # Some rows contain undetected controls (0 as an output for all cells)
        # Filter those undetected controls
        dataFrame_stage2 = filter_undetected_controls(dataFrame_stage2)
        
        # Apply transformations to the dataFrame
        apply_transformations(dataFrame_stage2)
    
        # Processes rows for each IP-port pair found, and labelled per Virtual Host & TLS usage
        dict_VHSSL = utils.read_json('config_dictionaries/dictionary_VHSSL.json')
        dataFrame_stage3 = dataFrames_by_IPPort(dataFrame_stage2, dict_VHSSL)

        # Export result into .csv file
        dataFrame_stage3.transpose().to_csv(utils.get_filename_stage(3, original_csv_filename), index=False)
    except Exception as e:
        raise Exception(f"Error on stage 3: {str(e)}")
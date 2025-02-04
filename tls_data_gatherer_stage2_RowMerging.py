import pandas
import json
from stage2_row_merging.column_controls_adder import column_controls_adder
from stage2_row_merging.aggr_function_def import aggr_function_def
import utils

# Stage 2: .csv depuration

# Runs Stage 2
# Reads the .csv generated on Stage 1
# Output: "[original_csv_filename]_Stage2_RowsMerged.csv"
def run_stage2(original_csv_filename:str, tech:str):
    try:
        # Read and interpret correctly the .csv file from stage1
        dtype_dict = utils.read_json('config_dictionaries/dictionary_stage1_output.json')
        dataFrame_stage1=pandas.read_csv(utils.get_filename_stage(1, original_csv_filename), dtype = dtype_dict)

        # Add a new column: "Host IP & Instance" (also includes: Last Scan Date)
        # Multiple IPs hold different instances of a Technology, and instances 
        # may be similar between servers with different IPs.
        # Therefore, the right identifier for separating between singular cases 
        # is joining both.
        # Last Scan Date is added for filtering old scan data with no data for 
        # the SSLEnabled control.
        dataFrame_stage1["Host IP & Instance"]=dataFrame_stage1["Host IP"]+dataFrame_stage1["Instance"]+dataFrame_stage1["Last Scan Date"]

        # Given we will merge rows corresponding to the same Host IP & Instance, 
        # we need to make sure no information of any control is lost.
        # We rescue the following columns for each control:
        columns = ["Control", "Status", "Current Value(s)", "Extended Evidence(s)"]
        for column in columns:
            column_controls_adder(dataFrame_stage1, column, tech)

        # Groupping by "Host IP & Instance"
        dataFrame_stage1_grouped = dataFrame_stage1.groupby(dataFrame_stage1["Host IP & Instance"])
        # Make sure to rescue all values available for all columns per "Host IP & Instance"
        aggr_function_tech = aggr_function_def(tech)
        dataFrame_stage2 = dataFrame_stage1_grouped.aggregate(aggr_function_tech)

        # Export result into .csv file
        dataFrame_stage2.to_csv(utils.get_filename_stage(2, original_csv_filename), index=False)
    except Exception as e:
        raise Exception(f"Error on stage 2: {str(e)}")
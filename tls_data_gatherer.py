import os, sys
import config
import prettify as pf
import tls_data_gatherer_stage1_csvCleanse
import tls_data_gatherer_stage2_RowMerging
import tls_data_gatherer_stage3_VirtualHosts
import tls_data_gatherer_stage4_TLSVersions
import tls_data_gatherer_stage5_Criteria
import tls_data_gatherer_stage6_Output_data

# Validation of file existence and tech validity
def validate_params(csv_file:str, tech:str):
    if not os.path.exists(csv_file):
        pf.print_error("Error: File '%s' not found"%csv_file)
        return False
    if tech.lower() not in config.values["techs_available"]:
        pf.print_error("Error: Invalid tech '%s'"%tech)
        return False
    return True

def process_file(csv_file:str, tech:str):
    pf.print_success("Processing file '%s' for tech '%s'"%(csv_file, tech))
    try:
        print("Processing Stage 1")
        tls_data_gatherer_stage1_csvCleanse.run_stage1(csv_file, tech)
        print("Processing Stage 2")
        tls_data_gatherer_stage2_RowMerging.run_stage2(csv_file, tech)
        print("Processing Stage 3")
        tls_data_gatherer_stage3_VirtualHosts.run_stage3(csv_file, tech)
        print("Processing Stage 4")
        tls_data_gatherer_stage4_TLSVersions.run_stage4(csv_file, tech)
        print("Processing Stage 5")
        tls_data_gatherer_stage5_Criteria.run_stage5(csv_file, tech)
        print("Processing Stage 6")
        tls_data_gatherer_stage6_Output_data.run_stage6(csv_file, tech)
        pf.print_success("Process completed successfully")
        sys.exit(0)
    except Exception as e:
        pf.print_error(e)

# Main

# Validates length of call arguments
if len(sys.argv) != 3:
    pf.print_error("Error: Invalid number of arguments")
    pf.print_usage()
    sys.exit(1)

# Validates file existence and tech validity
if validate_params(sys.argv[1], sys.argv[2]):
    process_file(sys.argv[1], sys.argv[2])
else:
    pf.print_error("Error: Invalid parameters")
    pf.print_usage()
    sys.exit(1)
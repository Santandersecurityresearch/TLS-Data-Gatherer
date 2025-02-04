import pandas
import config
import utils
from stage6_output_data.plot_double import plot_double
from stage6_output_data.plot_function_tls_count import plot_function_tls_count
import prettify as pf

# Stage 6: output data 
# Clear .csv and plotting of TLS/CipherSuite compliance & safety

# Runs Stage 6
# Reads the .csv generated on Stage 5
# Outputs: 
# - [original_csv_filename]_Stage6_OutputData.csv
# - [original_csv_filename]_[unit]_Stage6_OutputData.csv
# - [original_csv_filename]_plot_global_[type].png
# - [original_csv_filename]_plot_[unit]_[type].png
def run_stage6(original_csv_filename:str, tech:str):
    try:
        # Read and interpret the .csv generated on Stage 5
        dictionary_string = config.values[tech]["dictionary"]
        dtype_dict = utils.read_json(f'config_dictionaries/dictionary_{dictionary_string}.json')
        dataFrame_stage5=pandas.read_csv(utils.get_filename_stage(5, original_csv_filename), dtype=dtype_dict)

        dataFrame_stage6 = dataFrame_stage5[[
            "Host IP", "DNS Hostname",
            "Operating System", "NETWORK",
            "Technology", "Instance",
            "Current Value(s) - OpenSSL Version",
            "IP-Port", "VirtualHost",
            "TLS_ENABLED", "TLS_VERSION",
            "Current Value(s) - SSLCipherSuite",
            "TLS VERSION COMPLIANCE",
            "TLS VERSION SAFETY",
            "CIPHERSUITES COMPLIANCE",
            "CIPHERSUITES SAFETY"]].copy()
        
        # Export result into .csv file
        dataFrame_stage6.to_csv(utils.get_filename_stage(6, original_csv_filename), index=False)

        # Plotting of TLS versions & Cipher Suites
        ## Pivot Tables
        tag="global"
        dict_columns = {
            "TLS version" : ["TLS VERSION COMPLIANCE", "TLS VERSION SAFETY"],
            "Cipher Suite" : ["CIPHERSUITES COMPLIANCE", "CIPHERSUITES SAFETY"]
        }
        plot_double(dataFrame_stage6, tag, original_csv_filename)

        # TLS Version Count plot: gets the % per TLS version present at Global
        dataFrameTLScount = dataFrame_stage6[(dataFrame_stage6[dict_columns["TLS version"][1]]!="No TLS") & (dataFrame_stage6[dict_columns["TLS version"][1]]!="Error")]
        plot_function_tls_count(dataFrameTLScount, tag, original_csv_filename)
        
        for network in set(dataFrame_stage6["NETWORK"]):
            # Export reports per network/entity into .csv files
            dataFrame_stage6[(dataFrame_stage6["NETWORK"]==network)].to_csv(utils.get_filename_stage(6, original_csv_filename, network), index=False)
            
            if dataFrame_stage6[(dataFrame_stage6["NETWORK"]==network) & (dataFrame_stage6[dict_columns["TLS version"][1]]!="No TLS")].empty:
                pf.print_error(f"No data was found for {network}")
                continue
            plot_double(dataFrame_stage6[(dataFrame_stage6["NETWORK"]==network)].copy(), network, original_csv_filename)

            # TLS Version Count plot: gets the % per TLS version present in the network
            dataFrameTLScount_Network = dataFrame_stage6[(dataFrame_stage6["NETWORK"]==network) & (dataFrame_stage6[dict_columns["TLS version"][1]]!="No TLS") & (dataFrame_stage6[dict_columns["TLS version"][1]]!="Error")]
            if len(dataFrameTLScount_Network)>0:
                plot_function_tls_count(dataFrameTLScount_Network, network, original_csv_filename)
    except Exception as e:
        raise Exception(f"Error on stage 6: {str(e)}")
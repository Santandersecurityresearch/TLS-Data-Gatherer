import pandas
from stage3_vh.listened_ports import (
    listened_ports, virtualhost_19505, rewrite_to_listen_format, 
    virtualhost_9798, virtualhost_9799, virtualhost_9798_9799_SSLEngineON, 
    ExclusionOfRowElements, listened_ports_https
)

# This function filters rows with empty control detection from the dataframe
def filter_undetected_controls(dataFrame):
    return dataFrame[
        (dataFrame["Control - SSLEngine"] != "0") &
        (dataFrame["Control - VirtualHosts (CID 9798)"] != "0") &
        (dataFrame["Control - VirtualHosts (CID 9799)"] != "0") &
        (dataFrame["Control - SSLProtocol"] != "0") &
        (dataFrame["Control - SSLProtocol (CID 10839)"] != "0") &
        (dataFrame["Control - SSLProtocol (CID 7786)"] != "0") &
        (dataFrame["Control - SSLCipherSuite"] != "0") &
        (dataFrame["Control - SSLCipherSuite (CID 10841)"] != "0") &
        (dataFrame["Control - SSLCipherSuite (CID 7787)"] != "0") &
        (dataFrame["Control - OpenSSL Version"] != "0") &
        (dataFrame["Control - Listen Ports"] != "0") &
        (dataFrame["Control - VirtualHosts (CID 19505)"] != "0")
    ]

# This function applies all the Stage 3 transformations to the dataframe
def apply_transformations(dataFrame):
    # IP-ports receiving/sending traffic (directive Listen)
    dataFrame["Listened_Ports"] = dataFrame.apply(listened_ports, axis=1)
    # Virtual Host IP-ports declared (directive VirtualHost)
    dataFrame["VHList_19505"] = dataFrame.apply(virtualhost_19505, axis=1)
    # Impose the Listen formatting onto the VirtualHost IP-port list
    dataFrame["VHList_19505_global"] = dataFrame.apply(rewrite_to_listen_format, args=("VHList_19505",), axis=1)
    # Controls 9798 & 9799 from Qualys compliment each other and both indicate 
    # Virtual Hosts with SSLEngine on available (directives VirtualHost & SSLEngine)
    dataFrame["VHList_9798"] = dataFrame.apply(virtualhost_9798, axis=1)
    dataFrame["VHList_9799"] = dataFrame.apply(virtualhost_9799, axis=1)
    # dataFrame["VHList_SSLEngineON"]=dataFrame_stage2.apply(lambda x: x["VHList_9798"].union(x["VHList_9799"]), axis=1)
    dataFrame["VHList_SSLEngineON"] = dataFrame.apply(virtualhost_9798_9799_SSLEngineON, axis=1)
    # Impose the Listen formatting to the Virtual Host IP-ports with SSLEngineON list
    dataFrame["VHList_SSLEngineON_global"] = dataFrame.apply(rewrite_to_listen_format, args=("VHList_SSLEngineON",), axis=1)
    # Extract the Virtual Host IP-ports with SSLEngineOFF list from the Virtual Host IP-ports with SSLEngineON list
    dataFrame["VHList_SSLEngineOFF"] = dataFrame.apply(ExclusionOfRowElements, args=("VHList_SSLEngineON", "VHList_19505", True), axis=1)
    # Impose the Listen formatting onto the Virtual Host IP-ports with SSLEngineOFF list
    dataFrame["VHList_SSLEngineOFF_global"] = dataFrame.apply(rewrite_to_listen_format, args=("VHList_SSLEngineOFF",), axis=1)
    # List the Virtual Hosts IP-ports not found in the Listen directive (inactive)
    dataFrame["VHList_Excluded"] = dataFrame.apply(ExclusionOfRowElements, args=("Listened_Ports", "VHList_19505_global", True), axis=1)
    # List the IP-ports instances in the Listen directive not destined to Virtual Host services
    dataFrame["Listened_Ports_Excluded"] = dataFrame.apply(ExclusionOfRowElements, args=("VHList_19505_global", "Listened_Ports", True), axis=1)
    # List the IP-ports present in both the Listen & VirtualHost directives
    dataFrame["Listened_Ports_intersection"] = dataFrame.apply(lambda x: x["Listened_Ports"].intersection(x["VHList_19505_global"]), axis=1)
    # Extract the IP-ports being listened from the Virtual Host IP-ports with SSLEngineON list ===1st column to extract results from===
    dataFrame["VHList_SSLEngineON_global_intersection"] = dataFrame.apply(lambda x: x["Listened_Ports"].intersection(x["VHList_SSLEngineON_global"]), axis=1)
    # Extract the IP-ports being listened from the Virtual Host IP-ports with SSLEngineOFF list ===2nd column to extract results from===
    dataFrame["VHList_SSLEngineOFF_global_intersection"] = dataFrame.apply(lambda x: x["Listened_Ports"].intersection(x["VHList_SSLEngineOFF_global"]), axis=1)
    # These are the HTTPS & HTTP ports upon their declaration in the Listen directive
    dataFrame["Listened_Ports_HTTPS"] = dataFrame.apply(listened_ports_https, axis=1)
    dataFrame["Listened_Ports_HTTP"] = dataFrame.apply(ExclusionOfRowElements, args=("Listened_Ports_HTTPS", "Listened_Ports", True), axis=1)
    # List the HTTPS & HTTP ports not destined to Virtual Host services ===3rd & 4th column to extract results from===
    dataFrame["Listened_Ports_Excluded_HTTPS"] = dataFrame.apply(ExclusionOfRowElements, args=("Listened_Ports_HTTPS", "Listened_Ports_Excluded", False), axis=1)
    dataFrame["Listened_Ports_Excluded_HTTP"] = dataFrame.apply(ExclusionOfRowElements, args=("Listened_Ports_HTTP", "Listened_Ports_Excluded", False), axis=1)

# This function processes rows for each IP-port pair found, and labelled per Virtual Host & TLS usage
def dataFrames_by_IPPort(dataFrame, dict_VHSSL):
    dataFrame_stage3_rowlist=[]
    for i in range(len(dataFrame.index)):
        row_to_clone = dataFrame.iloc[i].copy()
        Lists_IPPorts = [
            list(row_to_clone["VHList_SSLEngineON_global_intersection"]), 
            list(row_to_clone["VHList_SSLEngineOFF_global_intersection"]), 
            list(row_to_clone["Listened_Ports_Excluded_HTTPS"]), 
            list(row_to_clone["Listened_Ports_Excluded_HTTP"])
        ]
        for j in range(len(Lists_IPPorts)):
            List_IPPorts = Lists_IPPorts[j]
            for IPPort in List_IPPorts:
                row_to_clone_copy = row_to_clone.copy()
                row_to_clone_copy["IP-Port"] = IPPort
                row_to_clone_copy["VirtualHost"] = dict_VHSSL[str(j)][0]
                row_to_clone_copy["TLS_ENABLED"] = dict_VHSSL[str(j)][1]
                dataFrame_stage3_rowlist.append(row_to_clone_copy)
    return pandas.concat(dataFrame_stage3_rowlist, axis=1, ignore_index=True, sort=False)
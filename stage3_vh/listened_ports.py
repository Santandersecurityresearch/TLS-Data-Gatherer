import re
import pandas

# Intersection between sets
def ExclusionOfRowElements(row:pandas.DataFrame, row_host:str, row_search:str, neg:bool):
    output = []
    for i in row[row_search]:
        if neg:
            if i not in row[row_host]:
                output.append(i)
        else:
            if i in row[row_host]:
                output.append(i)
    return set(output)

# Extracts the total listened port list as a set
def listened_ports(row: pandas.DataFrame):
    if "Setting not found" in row["Current Value(s) - Listen Ports"]:
        return set()
    else:
        Listen_list = row["Current Value(s) - Listen Ports"].strip().split(" ")
        Listen_set = set(default_removal(Listen_list))
        if "http" in Listen_set:
            Listen_set.remove("http")
        if "https" in Listen_set:
            Listen_set.remove("https")

        return Listen_set

# Extracts the total listened ports using HTTPS list as a set
def listened_ports_https(row: pandas.DataFrame):
    if "Setting not found" in row["Current Value(s) - Listen Ports"]:
        return set()
    else:
        Listen_list_https = [x.group().strip() for x in re.finditer(r"(\w|\.|\:|\*)*(( https)|((?<!\w)443(?! https)))", row["Current Value(s) - Listen Ports"].strip())]
        for i in range(len(Listen_list_https)):
            if "https" in Listen_list_https[i]:
                Listen_list_https[i] = Listen_list_https[i][:-6]
        Listen_set_https = set(default_removal(Listen_list_https))
        return Listen_set_https

# Removes "_default_" words from the data of some QIDs (19505, 9798, 9799)
def default_removal(list):
    return [x.replace("_default_","*").replace("VirtualHost(","").replace(")","").replace("*:","") for x in list]

# Extracts data from QID 19505
def virtualhost_19505(row:pandas.DataFrame):
    if "not found" not in row["Current Value(s) - VirtualHosts (CID 19505)"] and row["Current Value(s) - VirtualHosts (CID 19505)"]!="0":
        VirtualHost_list_19505=row["Current Value(s) - VirtualHosts (CID 19505)"].strip().split(" ")
        return set(default_removal(VirtualHost_list_19505))
    else:
        VirtualHost_list_19505=row["Current Value(s) - VirtualHosts (CID 19505)"].strip()
        return set(default_removal([VirtualHost_list_19505]))

# Extracts data from QID 9798  
def virtualhost_9798(row: pandas.DataFrame):
    VirtualHost_list_9798 = re.finditer(r"VirtualHost\(((\*)|(\.)|(:)|(_default_)|(\w))*\)", row["Current Value(s) - VirtualHosts (CID 9798)"])
    return set(default_removal([x.group() for x in VirtualHost_list_9798]))

# Extracts data from QID 9799
def virtualhost_9799(row: pandas.DataFrame):
    if "No VirtualHost Found" in row["Current Value(s) - VirtualHosts (CID 9799)"]:
        return set()
    else:
        VirtualHost_list_9799 = row["Current Value(s) - VirtualHosts (CID 9799)"].strip().split(" ")
        return set(default_removal(VirtualHost_list_9799))

# Obtains the total list of IP:port pairs within an Apache service where SSLEngine is on (union of QIDs 9798 & 9799)
def virtualhost_9798_9799_SSLEngineON(row: pandas.DataFrame):
    VirtualHost_list_SSLEngineON = row["VHList_9798"].union(row["VHList_9799"])
    if len(VirtualHost_list_SSLEngineON)==0 or (len(VirtualHost_list_SSLEngineON)>0 and all(["443" not in x for x in VirtualHost_list_SSLEngineON])):
        instances_443 = [[y.group() for y in re.finditer(r"((\w|\.|\*)*:443)|((?<!\w)443)", x)] for x in row["VHList_19505_global"]]
        if len(instances_443)>0:
            for z in instances_443:
                if z:
                    VirtualHost_list_SSLEngineON = VirtualHost_list_SSLEngineON.union(set(z))
    return VirtualHost_list_SSLEngineON

# Obtains all IP:por pairs dedicated to VirtualHost services
def virtualhost_contained(row:pandas.DataFrame):
    if "not found" in row["Current Value(s) - VirtualHosts (CID 19505)"] or "not found" in row["Current Value(s) - VirtualHosts (CID 16088)"] or row["Current Value(s) - VirtualHosts (CID 19505)"]=="0" or row["Current Value(s) - VirtualHosts (CID 16088)"]=="0":
        return True
    contained = False
    if all([((i in row["VHList_19505"]) and ("VirtualHost not found" not in i)) for i in row["VHList_16088"]]):
        contained = True
    return contained

# Reformatting of the outputted data from the Evidence for consistency between controls
def rewrite_to_listen_format(row:pandas.DataFrame, row_name:str):
    # Obtained from control 7640
    listened_ports_ = row["Listened_Ports"].copy()
    # Obtained from controls 9798 & 9799
    rowRewrite = row[row_name].copy()
    for i in listened_ports_:
        if i.split(":")[len(i.split(":"))-1] in rowRewrite:
            rowRewrite.add(i)
    remove_list=[]
    for j in rowRewrite:
        if any([(j==i.split(":")[len(i.split(":"))-1]) and (j!=i and ":" in i) for i in listened_ports_]):
            remove_list.append(j)
    [rowRewrite.remove(i) for i in remove_list]
    return rowRewrite
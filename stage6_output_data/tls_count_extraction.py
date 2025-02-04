import pandas
import re

# This function counts the apparitions of each TLS protocol version within a 
# group of entries (commonly, from a network)
def tls_count_extraction(DataFrame:pandas.DataFrame):

    tls_count_dict = {
        "SSLv2" : 0, "SSLv3" : 0,
        "TLSv1 " : 0, "TLSv1.1" : 0,
        "TLSv1.2" : 0, "TLSv1.3" : 0}

    for tls_list in DataFrame["TLS_VERSION"]:
        # The tls_list is interpreted as a string due to a previous reading of 
        # the DataFrame
        # [''] this is length 4 and is the minimal unit that must be skipped 
        # over (no TLS versions found)
        if len(tls_list)>4:
            tls_list_fixed = re.split(r", ", tls_list.replace("[","").replace("]","").replace("'",""))
            for tls_version in tls_list_fixed:
                tls_count_dict[tls_version]+=1

    return tls_count_dict
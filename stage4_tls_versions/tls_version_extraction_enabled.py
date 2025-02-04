import re
import pandas
import utils

# This function interprets the data found on the Evidence for TLS versions.
# For Apache HTTP Server, this corresponds to the SSLProtocol directive.
# The result is a set of TLS versions per entry.
def tls_version_extraction_enabled(row:pandas.DataFrame, technology:str):
    
    # We will store all the TLS versions detected on a list per server
    TLS_set=set([])
    #protocol_list = ["SSLv2","SSLv3","TLSv1 ","TLSv1.1", "TLSv1.2", "TLSv1.3"]

    # "Apache HTTP Server 2.2.x" : https://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslprotocol
    ##Default:	SSLProtocol all
    ##All
    ##This is a shortcut for ``+SSLv2 +SSLv3 +TLSv1'' or - when using OpenSSL 1.0.1 and later - ``+SSLv2 +SSLv3 +TLSv1 +TLSv1.1 +TLSv1.2'', respectively.

    # "Apache HTTP Server 2.4.x" : https://httpd.apache.org/docs/current/mod/mod_ssl.html#sslprotocol
    ##Default:	SSLProtocol all -SSLv3 (up to 2.4.16: all)
    ##all
    ##This is a shortcut for ``+SSLv3 +TLSv1'' or - when using OpenSSL 1.0.1 and later - ``+SSLv3 +TLSv1 +TLSv1.1 +TLSv1.2'', respectively 
    ##(except for OpenSSL versions compiled with the ``no-ssl3'' configuration option, where all does not include +SSLv3).
    
    DictConfigs = utils.read_json('config_dictionaries/dictionary_openssl_versions.json')

    if row["TLS_ENABLED"]:
        if technology == "apache":
            # Default configs
            if re.match(r"(?s).*Setting not found", row["Current Value(s) - SSLProtocol"]):
                if "Apache HTTP Server 2.2.x" in row["Technology"]:
                    TLS_set.update({"SSLv2","SSLv3","TLSv1 ","TLSv1.1","TLSv1.2"})
                elif "Apache HTTP Server 2.4.x" in row["Technology"]:
                    #if (any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["TLSv1.3Support"]]) or (row["Current Value(s) - OpenSSL Version"]==0)):
                    if any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["TLSv1.3Support"]]):
                        TLS_set.update({"TLSv1 ","TLSv1.1","TLSv1.2","TLSv1.3"})
                    else:
                        TLS_set.update({"TLSv1 ","TLSv1.1","TLSv1.2"})
            # Addition (all)
            if re.match(r"(?s).*(?!(?<=-))(all)", row["Current Value(s) - SSLProtocol"], re.IGNORECASE):
                if "Apache HTTP Server 2.2.x" in row["Technology"]:
                    TLS_set.update({"SSLv2","SSLv3","TLSv1 ","TLSv1.1","TLSv1.2"})
                elif "Apache HTTP Server 2.4.x" in row["Technology"]:
                    #if (any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["TLSv1.3Support"]]) or (row["Current Value(s) - OpenSSL Version"]==0)):
                    if any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["TLSv1.3Support"]]):
                        TLS_set.update({"TLSv1 ","TLSv1.1","TLSv1.2","TLSv1.3"})
                    #elif (any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["NoSSLv3SupportDefault"]]) or (row["Current Value(s) - OpenSSL Version"]==0)):
                    elif any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["NoSSLv3SupportDefault"]]):
                        TLS_set.update({"TLSv1 ","TLSv1.1","TLSv1.2"})
                    else:
                        TLS_set.update({"SSLv3","TLSv1 ","TLSv1.1","TLSv1.2"})
            # Elimination (all)
            if re.match(r"(?s).*-(all)", row["Current Value(s) - SSLProtocol"], re.IGNORECASE):
                if "Apache HTTP Server 2.2.x" in row["Technology"]:
                    if ("SSLv2" in TLS_set):
                        TLS_set.remove("SSLv2")
                    if ("SSLv3" in TLS_set):
                        TLS_set.remove("SSLv3")
                    if ("TLSv1 " in TLS_set):
                        TLS_set.remove("TLSv1 ")
                    if ("TLSv1.1" in TLS_set):
                        TLS_set.remove("TLSv1.1")
                    if ("TLSv1.2" in TLS_set):
                        TLS_set.remove("TLSv1.2")
                elif "Apache HTTP Server 2.4.x" in row["Technology"]:
                    if ("SSLv3" in TLS_set):
                        TLS_set.remove("SSLv3")
                    if ("TLSv1 " in TLS_set):
                        TLS_set.remove("TLSv1 ")
                    if ("TLSv1.1" in TLS_set):
                        TLS_set.remove("TLSv1.1")
                    if ("TLSv1.2" in TLS_set):
                        TLS_set.remove("TLSv1.2")
                    #if (("TLSv1.3" in TLS_set) and (any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["TLSv1.3Support"]]) or (row["Current Value(s) - OpenSSL Version"]==0))):
                    if (("TLSv1.3" in TLS_set) and any([i in row["Current Value(s) - OpenSSL Version"] for i in DictConfigs["TLSv1.3Support"]])):
                        TLS_set.remove("TLSv1.3")
            # Addition (SSLv2)
            if re.match(r"(?s).*\+SSLv2", row["Current Value(s) - SSLProtocol"]):
                TLS_set.add("SSLv2")
            # Addition (SSLv3)
            if re.match(r"(?s).*\+SSLv3", row["Current Value(s) - SSLProtocol"]):
                TLS_set.add("SSLv3")
            # Addition (TLSv1)
            if re.match(r"(?s).*\+TLSv1(?!(?=\.))", row["Current Value(s) - SSLProtocol"]):
                TLS_set.add("TLSv1 ")
            # Addition (TLSv1.1)
            if re.match(r"(?s).*\+TLSv1.1", row["Current Value(s) - SSLProtocol"]):
                TLS_set.add("TLSv1.1")
            # Addition (TLSv1.2)
            if re.match(r"(?s).*\+TLSv1.2", row["Current Value(s) - SSLProtocol"]):
                TLS_set.add("TLSv1.2")
            # Addition (TLSv1.3)
            if re.match(r"(?s).*\+TLSv1.3", row["Current Value(s) - SSLProtocol"]) and ("Apache HTTP Server 2.4.x" in row["Technology"]):
                TLS_set.add("TLSv1.3")
            # Overwriting (SSLv2)
            if re.match(r"(?s).*(?!(?<=(-|\+)))SSLv2", row["Current Value(s) - SSLProtocol"]):
                TLS_set=set(["SSLv2"])
            # Overwriting (SSLv3)
            if re.match(r"(?s).*(?!(?<=(-|\+)))SSLv3", row["Current Value(s) - SSLProtocol"]):
                TLS_set=set(["SSLv3"])
            # Overwriting (TLSv1)
            if re.match(r"(?s).*(?!(?<=(-|\+)))TLSv1(?!(?=\.))", row["Current Value(s) - SSLProtocol"]):
                TLS_set=set(["TLSv1 "])
            # Overwriting (TLSv1.1)
            if re.match(r"(?s).*(?!(?<=(-|\+)))TLSv1.1", row["Current Value(s) - SSLProtocol"]):
                TLS_set=set(["TLSv1.1"])
            # Overwriting (TLSv1.2)
            if re.match(r"(?s).*(?!(?<=(-|\+)))TLSv1.2", row["Current Value(s) - SSLProtocol"]):
                TLS_set=set(["TLSv1.2"])
            # Overwriting (TLSv1.3)
            if re.match(r"(?s).*(?!(?<=(-|\+)))TLSv1.3", row["Current Value(s) - SSLProtocol"]) and ("Apache HTTP Server 2.4.x" in row["Technology"]):
                TLS_set=set(["TLSv1.3"])
            # Elimination (SSLv2)
            if re.match(r"(?s).*-SSLv2", row["Current Value(s) - SSLProtocol"]) and ("SSLv2" in TLS_set):
                TLS_set.remove("SSLv2")
            # Elimination (SSLv3)
            if re.match(r"(?s).*-SSLv3", row["Current Value(s) - SSLProtocol"]) and ("SSLv3" in TLS_set):
                TLS_set.remove("SSLv3")
            # Elimination (TLSv1)
            if re.match(r"(?s).*-TLSv1(?!(?=\.))", row["Current Value(s) - SSLProtocol"]) and ("TLSv1 " in TLS_set):
                TLS_set.remove("TLSv1 ")
            # Elimination (TLSv1.1)
            if re.match(r"(?s).*-TLSv1.1", row["Current Value(s) - SSLProtocol"]) and ("TLSv1.1" in TLS_set):
                TLS_set.remove("TLSv1.1")
            # Elimination (TLSv1.2)
            if re.match(r"(?s).*-TLSv1.2", row["Current Value(s) - SSLProtocol"]) and ("TLSv1.2" in TLS_set):
                TLS_set.remove("TLSv1.2")
            # Elimination (TLSv1.3)
            if re.match(r"(?s).*-TLSv1.3", row["Current Value(s) - SSLProtocol"]) and ("Apache HTTP Server 2.4.x" in row["Technology"]) and ("TLSv1.3" in TLS_set):
                TLS_set.remove("TLSv1.3")

    return sorted(TLS_set)
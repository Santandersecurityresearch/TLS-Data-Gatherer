import re
import pandas
import json

# TLS version Safety: only TLSv1.3 is considered Safe. TLSv1.2 only is considered Safe but obsolete.
# If any non-compliant version is allowed, the result is Forbidden.
def tls_version_safety_filter(row:pandas.DataFrame, technology:str):
    if row["TLS_ENABLED"]:
        if technology == "apache":
            if ('SSLv2' in row["TLS_VERSION"]) or ('SSLv3' in row["TLS_VERSION"]) or ('TLSv1 ' in row["TLS_VERSION"]) or ('TLSv1.1' in row["TLS_VERSION"]):
                row_safety = "Forbidden"
            elif 'TLSv1.3' in row["TLS_VERSION"]:
                row_safety = "Safe"
            elif 'TLSv1.2' in row["TLS_VERSION"]:
                row_safety = "Safe but obsolete"
            else:
                row_safety = "Error"
    else:
        row_safety = "No TLS"
    return row_safety
import re
import pandas

# TLS version Compliance: we consider TLSv1.3 as Compliant. TLSv1.2 is optional.
# Other versions for SSL/TLS are not allowed.
def tls_version_compliance_filter(row:pandas.DataFrame, technology:str):
    if row["TLS_ENABLED"]:
        if not row["TLS_VERSION"]:
            row_compliance = "Error"
        elif (technology == "apache") and (('SSLv2' in row["TLS_VERSION"]) or ('SSLv3' in row["TLS_VERSION"]) or ('TLSv1 ' in row["TLS_VERSION"]) or ('TLSv1.1' in row["TLS_VERSION"]) or ('TLSv1.3' not in row["TLS_VERSION"])):
            row_compliance = "Non-compliant"
        else:
            row_compliance = "Compliant"
    else:
        row_compliance = "Compliant"
    return row_compliance
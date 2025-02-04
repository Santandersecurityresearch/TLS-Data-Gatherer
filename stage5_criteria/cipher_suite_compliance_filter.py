import re
import pandas
import json
import utils

# CipherSuites Compliance: we consider Compliant to only allow cipher suites present in the
# Santander Cryptography Standard list.
## TLSv1.3 ciphersuites: https://github.com/santander-group-cyber-cto/CryptographyStandard/blob/main/Implementations/TLS/TLSv1.3.md
## TLSv1.2 ciphersuites: https://github.com/santander-group-cyber-cto/CryptographyStandard/blob/main/Implementations/TLS/TLSv1.2.md
def cipher_suite_compliance_filter(row:pandas.DataFrame, cipherSuiteCol:str):

    # List of compliant cipher suites in our cryptography standard
    DictTLS = utils.read_json('config_dictionaries/dictionary_TLS_ciphersuites.json')

    # Rest of options are considered Non-compliant.
    if row["TLS_ENABLED"]:
        delimiters = [":",";"]
        string = row["Current Value(s) - "+cipherSuiteCol].replace("\n","")
        for delimiter in delimiters:
            string = " ".join(string.split(delimiter))
        if (all(((i in DictTLS["TLSv1.3"]) or (i in DictTLS["TLSv1.2"])) for i in string.split(" "))):
            row_ciphersuitecompliance = "Compliant"
        else:
            row_ciphersuitecompliance = "Non-compliant"
    else:
        row_ciphersuitecompliance = "Compliant"

    return row_ciphersuitecompliance
import csv
import pandas
import sys
import json
from stage5_criteria.tls_version_compliance_filter import tls_version_compliance_filter
from stage5_criteria.tls_version_safety_filter import tls_version_safety_filter
from stage5_criteria.cipher_suite_compliance_filter import cipher_suite_compliance_filter
from stage5_criteria.cipher_suite_safety_filter import cipher_suite_safety_filter
import config
import utils

# Stage 5: Compliance & Safety

# Runs Stage 5
# Reads the .csv generated on Stage 4
# Output: "[original_csv_filename]_Stage5_CriteriaEstablished.csv"
def run_stage5(original_csv_filename:str, tech:str):
    try:
        # Read and interpret the .csv generated on Stage 4
        dictionary_string = config.values[tech]["dictionary"]
        dtype_dict = utils.read_json(f'config_dictionaries/dictionary_{dictionary_string}.json')
        dataFrame_stage5=pandas.read_csv(utils.get_filename_stage(4, original_csv_filename),dtype=dtype_dict)

        # TLS version Compliance Rules: 
        # - TLSv1.3 is Compliant
        # - TLSv1.2 is optional
        # - Other versions for SSL/TLS are not allowed
        dataFrame_stage5["TLS VERSION COMPLIANCE"]=dataFrame_stage5.apply(tls_version_compliance_filter, technology=tech, axis=1)

        # TLS version Safety Rules: 
        # - TLSv1.3 is considered Safe
        # - TLSv1.2 only is considered Safe but obsolete
        # - If any non-compliant version is allowed, the result is Forbidden
        dataFrame_stage5["TLS VERSION SAFETY"]=dataFrame_stage5.apply(tls_version_safety_filter, technology=tech, axis=1)

        # CipherSuites Compliance: 
        # We consider Compliant only cipher suites present in the Santander Cryptography Standard list
        # TLSv1.3 ciphersuites: https://github.com/santander-group-cyber-cto/CryptographyStandard/blob/main/Implementations/TLS/TLSv1.3.md
        # TLSv1.2 ciphersuites: https://github.com/santander-group-cyber-cto/CryptographyStandard/blob/main/Implementations/TLS/TLSv1.2.md
        ciphersuites_string = config.values[tech]["ciphersuites"]
        dataFrame_stage5["CIPHERSUITES COMPLIANCE"]=dataFrame_stage5.apply(cipher_suite_compliance_filter, cipherSuiteCol=ciphersuites_string, axis=1)

        # CipherSuites Safety:
        # We consider Forbidden any ciphersuite containing:
        # (NULL)|(ARIA)|(KRB5)|(CAMELLIA)|(ECCPWD)|(RC2)|(RC4)|(MD5)|(DSS)|(PSK)|(FALLBACK)|(anon)|(IDEA)|(DES)|(EMPTY)
        # We consider Weak any ciphersuite containing:
        # ((CBC)|(TLS_RSA)|(aRSA)|(SHA)|(MEDIUM))
        # The remaining cipher suites are labelled as Safe
        dataFrame_stage5["CIPHERSUITES SAFETY"]=dataFrame_stage5.apply(cipher_suite_safety_filter, cipherSuiteCol=ciphersuites_string, axis=1)

        # Export result into .csv file
        dataFrame_stage5.to_csv(utils.get_filename_stage(5, original_csv_filename), index=False)
    except Exception as e:
        raise Exception(f"Error on stage 5: {str(e)}")
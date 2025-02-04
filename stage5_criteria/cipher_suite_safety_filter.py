import re
import pandas

# CipherSuites Safety: we consider Forbidden any ciphersuite containing:
# (NULL)|(ARIA)|(KRB5)|(CAMELLIA)|(ECCPWD)|(RC2)|(RC4)|(MD5)|(DSS)|(PSK)|(FALLBACK)|(anon)|(IDEA)|(DES)|(EMPTY)
# We consider Weak any ciphersuite containing:
# ((CBC)|(TLS_RSA)|(aRSA)|(SHA)|(MEDIUM))
# The remaining cipher suites are labelled as Safe.
def cipher_suite_safety_filter(row:pandas.DataFrame, cipherSuiteCol:str):
    if row["TLS_ENABLED"]:
        if re.match(r"(?s).*((NULL)|(ARIA)|(KRB5)|(CAMELLIA)|(ECCPWD)|(RC2)|(RC4)|(MD5)|(DSS)|(PSK)|(FALLBACK)|(anon)|(IDEA)|(DES)|(EMPTY))", row["Current Value(s) - "+cipherSuiteCol]) or re.match(r"(?s).*PROFILE=SYSTEM", row["Current Value(s) - "+cipherSuiteCol]):
            row_ciphersuitefilter = "Forbidden"
        elif re.match(r"(?s).*((0)|(Key not found)|(Setting not found))", row["Current Value(s) - "+cipherSuiteCol]):
            row_ciphersuitefilter = "Forbidden"
        elif re.match(r"(?s).*((CBC)|(TLS_RSA)|((\:|\;)RSA)|(aRSA)|(SHA(?!(?=(\d))))|(MEDIUM))", row["Current Value(s) - "+cipherSuiteCol]): 
            row_ciphersuitefilter = "Weak"
        else:
            row_ciphersuitefilter = "Safe"
    else:
        row_ciphersuitefilter = "No TLS"
    return row_ciphersuitefilter
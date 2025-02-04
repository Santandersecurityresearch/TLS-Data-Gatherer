import pandas

# Definition of new rows for our current DataBase, per technology
# We write the data of all controls for each "Host IP & Instance" combination into a single row
# Different technologies (Apache, IIS, etc) may need different controls to be added
def column_controls_adder(db:pandas.DataFrame, row:str, technology:str): 
    if technology == "apache":
        db[row+" - SSLEngine"] = db[db["Control"]=="Status of the 'SSLEngine' derivative within the Apache configuration files (server config and virtual host)"][row]
        db[row+" - VirtualHosts (CID 9798)"] = db[db["Control"]=="Status of \"Header\" setting within virtualhost whose \"SSLEngine\" is set \"on\""][row]
        db[row+" - VirtualHosts (CID 9799)"] = db[db["Control"]=="List of VirtualHost elements whose \"SSLEngine\" is set \"on\" and no \"Header\" set neither at server level nor at Virtual Host level"][row]
        db[row+" - SSLProtocol"] = db[db["Control"]=="Status of 'SSLProtocol' at server level"][row]
        db[row+" - SSLProtocol (CID 10839)"] = db[db["Control"]=="Status of 'SSLProtocol' for every SSL enabled virtual hosts"][row]
        db[row+" - SSLProtocol (CID 7786)"] = db[db["Control"]=="Status of the 'sslprotocol' directive on the host"][row]
        db[row+" - SSLCipherSuite"] = db[db["Control"]=="Status of \"SSLCipherSuite\" settings"][row]
        db[row+" - SSLCipherSuite (CID 10841)"] = db[db["Control"]=="Status of \"SSLCipherSuite\" settings for every SSL enabled virtual hosts"][row]
        db[row+" - SSLCipherSuite (CID 7787)"] = db[db["Control"]=="Status of the 'SSLCipherSuite' directive within the Apache server-level configuration on the host"][row]
        db[row+" - SSLHonorCipherOrder"] = db[db["Control"]=="Status of SSLHonorCipherOrder setting"][row]
        db[row+" - SSLHonorCipherOrder (CID 10872)"] = db[db["Control"]=="Status of SSLHonorCipherOrder setting at server level"][row]
        db[row+" - SSLHonorCipherOrder (CID 10873)"] = db[db["Control"]=="Status of SSLHonorCipherOrder setting for every SSL enabled virtual hosts"][row]
        db[row+" - OpenSSL Version"] = db[db["Control"]=="Status of the 'openssl version' on the host"][row]
        db[row+" - Listen Ports"] = db[db["Control"]=="Status of the 'Listen' directive in the Apache configuration file on the host"][row]
        db[row+" - VirtualHosts (CID 19505)"] = db[db["Control"]=="Status of the 'VirtualHost' directive in the apache configuration file"][row]
        
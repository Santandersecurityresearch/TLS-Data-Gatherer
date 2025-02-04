# This function computes the availablity percentages for TLS protocol versions 
# within a group of entries (commonly, from a network)
def tls_count_percentages(dictionary:dict, number_of_assets:int):

    dictionary["SSLv2"]=dictionary["SSLv2"]/number_of_assets*100
    dictionary["SSLv3"]=dictionary["SSLv3"]/number_of_assets*100
    dictionary["TLSv1 "]=dictionary["TLSv1 "]/number_of_assets*100
    dictionary["TLSv1.1"]=dictionary["TLSv1.1"]/number_of_assets*100
    dictionary["TLSv1.2"]=dictionary["TLSv1.2"]/number_of_assets*100
    dictionary["TLSv1.3"]=dictionary["TLSv1.3"]/number_of_assets*100

    return dictionary
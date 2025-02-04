import pandas
import matplotlib.pyplot as plt
from matplotlib import cm
from stage6_output_data.tls_count_extraction import tls_count_extraction
from stage6_output_data.tls_count_percentages import tls_count_percentages
import matplotlib.ticker as mtick
import utils

# This function plots the percentages of availability for each TLS protocol 
# version within a group of entries (commonly, from a network)
def plot_function_tls_count(OG_DataFrame:pandas.DataFrame, network:str, original_csv_filename:str):
    fig, ax = plt.subplots()

    colors = cm.YlOrRd(192)
    dict_TLS_count = tls_count_extraction(OG_DataFrame)
    number_of_assets = len(OG_DataFrame)
    dict_TLS_count_perc = tls_count_percentages(dict_TLS_count, number_of_assets)

    ax.bar(range(len(dict_TLS_count_perc)), list(dict_TLS_count_perc.values()), align='center', color=colors)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.xticks(range(len(dict_TLS_count_perc)), list(dict_TLS_count_perc.keys()))
    plt.title(f'TLS protocol support (%) - {network}')
    for i in range(len(list(dict_TLS_count_perc.keys()))):
        plt.text(i, round(list(dict_TLS_count_perc.values())[i]+1, 2), f"{round(list(dict_TLS_count_perc.values())[i], 2)}%", ha = 'center')

    plt.savefig(utils.get_plot_filename(network, "TLS version", original_csv_filename, 'protocol_support'))
    plt.close()
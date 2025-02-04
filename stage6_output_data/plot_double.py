import pandas
import utils
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from stage6_output_data.plot_function import plot_function

# Ths function outputs the plots granting visibility on the Compliance and Safety 
# of TLS Versions & Cipher Suites. It uses `plot_function` for building both the
# Compliant and the Non-compliant sides into a joint barplot.
def plot_double(df:pandas.DataFrame, tag:str, og_filename:str):

    dict_plot = utils.read_json(f'config_dictionaries/dictionary_plot.json')

    # Dummy rows (filled columns: 'NETWORK', 'TLS VERSION COMPLIANCE', 'TLS VERSION SAFETY', 
    # 'CIPHERSUITES COMPLIANCE', 'CIPHERSUITES SAFETY')
    if tag!="global":
        df.loc[-1] = ["", "", "", tag, "", "", "", "", "", "", "", "", 
                      "Compliant", "Dummy", "Compliant", "Dummy"]
        df.loc[-2] = ["", "", "", tag, "", "", "", "", "", "", "", "", 
                      "Non-compliant","Dummy", "Non-compliant", "Dummy"]

    dict_multindexes_uncoupled={}
    for value in dict_plot["measured_values"]:
        dict_plot_multindexes=[]
        for ele in dict_plot["dict_multindexes"][value]:
            dict_plot_multindexes.append(tuple(ele))
        value_uncoupled_list=[]
        aux=""
        for tupl in dict_plot_multindexes:
            if tupl[0]!=aux:
                if aux!="":
                    value_uncoupled_list.append(list_ele)
                list_ele=[]
                aux=tupl[0]
                list_ele.append(tupl[1])
            else:
                list_ele.append(tupl[1])
        value_uncoupled_list.append(list_ele)
        dict_multindexes_uncoupled[value]=value_uncoupled_list
    
    for value in dict_plot["measured_values"]:
        dict_plot_multindexes=[]
        for ele in dict_plot["dict_multindexes"][value]:
            dict_plot_multindexes.append(tuple(ele))
        table = pandas.pivot_table(df, 
                                values=dict_plot["dict_values"][value], 
                                index=dict_plot["dict_columns"][value],
                                aggfunc="count")
        
        table.reindex(dict_plot_multindexes)
        fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(9, 5), width_ratios=list(dict_plot["dict_width_ratios"].values()))  # width, height
        xticks = dict(zip(table.index.levels[0], dict_multindexes_uncoupled[value])) # xticks
        widths = dict(zip(table.index.levels[0], list(dict_plot["dict_barwidth"].values()))) # dict_barwidth
        graph = dict(zip(table.index.levels[0], axes)) # axes
        
        list(map(lambda x: plot_function(x, graph[x], table.xs(x), xticks[x], widths[x], dict_plot["dict_values"][value], 'Number of Web Services', False), graph))

        fig.subplots_adjust(wspace=0)
        fig.suptitle(dict_plot["title"][value]+" - "+tag)

        axes[1].get_yaxis().set_visible(False)
        axes[0].spines[['right']].set_visible(False)
        axes[1].spines[['left']].set_visible(False)
        axes[0].yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.minorticks_off()
        
        # Save the plot image
        plt.savefig(utils.get_plot_filename(tag, value, og_filename, 'Compliance'))
        plt.close()
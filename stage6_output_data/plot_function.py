from matplotlib import cm
import math
import matplotlib.pyplot as plt
import utils

# A tuned barplot function currently used for building the two sides of the combined plot
def plot_function(x, ax, db, index_order, width, col, ylabel, output:bool=True, tag:str="", og_filename:str=""):
    colors = cm.YlOrRd(192)
    db.reindex(index = index_order).plot(kind='bar', stacked='True', 
                    ax=ax, legend=False, 
                    color=colors,
                    width=width,
                    ylabel=ylabel, rot=0).set_xlabel(x, weight='bold')
    y = db.reindex(index = index_order)[col]
    if len(y):
        for i in range(len(y)):
            if not math.isnan(y.iloc[i]):
                ax.text(i, y.iloc[i], str(y.iloc[i].astype('int')), ha = 'center')
    
    if output:
        plt.savefig(utils.get_plot_filename(tag, "plot_function", og_filename))
        plt.close()
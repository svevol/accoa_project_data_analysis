import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.visualization.plots_definitions import barplot_defs


def plot_hists(data_df, ranges_df, met_names, plot_title, selected_cols=None):
    plt.close()
    fig, ax = plt.subplots(11, 5, figsize=(40, 30))
    n_plots = len(met_names)
    if not selected_cols:
        selected_cols = range(n_plots)

    count = 0
    for i in range(11):
        for j in range(5):
            ax[i, j].hist(data_df.iloc[:, selected_cols[count]])
            ax[i, j].set_title(met_names[count])
            if ranges_df is not None:
                lb = ranges_df.iloc[0, selected_cols[count]]
                ub = ranges_df.iloc[1, selected_cols[count]]
                ax[i, j].axvline(x=lb, color='black', linestyle='--')
                ax[i, j].axvline(x=ub, color='black', linestyle='--')
            # ax[i,j].set_xlim(0.9*lb, 1.1*ub)
            count += 1
            if count == n_plots-1:
                break
        if count == n_plots-1:
            break

    fig.suptitle(plot_title, fontsize=24)
    plt.tight_layout()

    # plt.savefig(os.path.join('TMFA_sampling_plots', f'{plot_name}.pdf'))
    # plt.close()

    return plt.show()
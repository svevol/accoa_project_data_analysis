import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io
import seaborn as sns

from src.utils.plot_config import heatmap_defs

COLOR_LIST_9 = ['#377eb8', '#e41a1c', '#4daf4a', '#984ea3', '#ff7f00', '#a65628', '#f781bf', '#999999']


plt.rcParams['legend.fontsize'] = '10'
plt.rcParams['legend.labelspacing'] = 0.5
plt.rcParams['legend.columnspacing'] = 0.5


def plot_heatmap(data, output_file, title, promiscuous_rxns=list()):
    heatmap_defs()

    fig, ax = plt.subplots(figsize=(5.5, 5))

    if len(data.index.values) == len(data.columns.values):
        data = data[data.index.values]
    elif len(data.index.values) > len(data.columns.values):
        new_col_values = [col for col in data.index.values if col not in promiscuous_rxns]
        data = data[new_col_values]


    sns.heatmap(data=data, cmap="RdBu", center=0, vmin=-1, vmax=1, linewidth=0.5, ax=ax)
    #sns.heatmap(data=data, cmap=sns.diverging_palette(15, 150, l=40, n=7, as_cmap=True),
    #            center=0, vmin=-1, vmax=1, linewidth=0.5, ax=ax)

    plt.title(title[4:-4])
    plt.xlabel('Perturbed reaction/enzyme')
    plt.ylabel('Impact')

    fig.subplots_adjust(top=0.9, bottom=0.35, left=0.3, right=0.98)
    plt.savefig(output_file, dpi=200)
    plt.close()


def plot_boxplot(mat, key_name, file_out, ylims, id_col, col_names, row_names, n_models):

    data_df = pd.DataFrame(data=mat['mcaResults'][key_name].item())
    data_df.columns = col_names
    data_df['rxns'] = np.tile(row_names, n_models)

    data_df_melt = pd.melt(data_df, id_vars=[id_col])

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.boxplot(x=id_col, y='value', data=data_df_melt, hue='variable', fliersize=0, ax=ax, linewidth=0.5)

    if ylims:
        ax.set_ylim(ylims)
        ylim_label = str(ylims[1])
    else:
        ylim_label = ''

    ax.yaxis.grid(True)
    ax.set_xlabel('Affected reaction')
    ax.set_ylabel('Coefficient value')
    plt.xticks(rotation=90)

    ax.legend(ncol=5,
              numpoints=1,
              loc='upper center',
              bbox_to_anchor=(0.45, 1.4),
              title='Perturbed reaction/enzyme')

    fig.subplots_adjust(top=0.8, bottom=0.3, left=0.1, right=0.98)

    plt.savefig(''.join([file_out, '_', ylim_label, '.png']), dpi=200)
    plt.close()


def get_df_median(mat, key_name, id_col, col_names, row_names, n_models):

    df = pd.DataFrame(data=mat['mcaResults'][key_name].item())
    df.columns = col_names
    df['rxns'] = np.tile(row_names, n_models)

    df_median = df.groupby(id_col).median()

    #C_df_median[id_col] = C_df_median.index
    #C_df_median = C_df_median.melt(id_vars=[id_col])

    return df_median


def get_df_iqr(mat, key_name, id_col, col_names, row_names, n_models):

    df = pd.DataFrame(data=mat['mcaResults'][key_name].item())
    df.columns = col_names
    df['rxns'] = np.tile(row_names, n_models)

    df_q2 = df.groupby(id_col).quantile(0.25)
    df_q4 = df.groupby(id_col).quantile(0.75)

    df_iqr = df_q4.subtract(df_q2)

    #C_df_iqr[id_col] = C_df_iqr.index
    #C_df_iqr = C_df_iqr.melt(id_vars=[id_col],var_name='variable')

    return df_iqr


def get_name_list(file_in):

    name_list = []
    with open(file_in, 'r') as f_in:
        line = f_in.readline()
        line = f_in.readline()
        while line:
            name_list.append(line[2:].strip())
            line = f_in.readline()

    return name_list


def main_MCA_heatmap():

    base_dir = '/home/mrama/GRASP_test/GRASP/output_HMP_quadratic_splines_reproduce/'
    output_dir = '/home/mrama/GRASP_test/GRASP/output_HMP_quadratic_splines_reproduce/plots/'
    strain_list = ['HMP1489', 'HMP2360']

    rep_list = range(2)
    time_point_list = range(4)
    n_models = 10000

    file_in_list_MCA = [''.join([base_dir, 'MCA_', strain, '_r', str(rep_i), '_t', str(time_i), '.mat']) for strain in strain_list for rep_i in rep_list for time_i in time_point_list]
    file_in_list_mets = [''.join([base_dir, strain, '_r', str(rep_i), '_t', str(time_i), '_metsActive.dat']) for strain in strain_list for rep_i in rep_list for time_i in time_point_list]
    file_in_list_rxns = [''.join([base_dir, strain, '_r', str(rep_i), '_t', str(time_i), '_rxnsActive.dat']) for strain in strain_list for rep_i in rep_list for time_i in time_point_list]
    file_in_list_enzs = [''.join([base_dir, strain, '_r', str(rep_i), '_t', str(time_i), '_enzNames.dat']) for strain in strain_list for rep_i in rep_list for time_i in time_point_list]

    rxn_names_list = [get_name_list(file_in_rxns) for file_in_rxns in file_in_list_rxns]
    enz_names_list = [get_name_list(file_in_enzs) for file_in_enzs in file_in_list_enzs]
    met_names_list = [get_name_list(file_in_mets) for file_in_mets in file_in_list_mets]

    Cx_df_median_list = []
    Cv_df_median_list = []
    Rx_df_median_list = []
    Re_df_median_list = []
    Cx_df_iqr_list = []
    Cv_df_iqr_list = []
    Rx_df_iqr_list = []
    Re_df_iqr_list = []

    id_col = 'rxns'
    ylims = [-1, 1]
    promiscuous_rxns = ['AANAT_tryptm', 'DDC_tryptm']

    for i, file_in in enumerate(file_in_list_MCA):
        print(file_in)
        mat = scipy.io.loadmat(file_in, squeeze_me=True)
        file_name = file_in.split('/')[-1]

        """
        key_name = 'vControl'
        col_names = rxn_names_list[i]
        row_names = rxn_names_list[i]

        Cv_df_median = get_df_median(mat, key_name, id_col, col_names, row_names, n_models)
        Cv_df_median_list.append(Cv_df_median)
        output_file = output_dir + file_name[:-4] + '_Cv_median.png'
        plot_heatmap(Cv_df_median, output_file, file_name)

        Cv_df_iqr = get_df_iqr(mat, key_name, id_col, col_names, row_names, n_models)
        Cv_df_iqr_list.append(Cv_df_iqr)
        output_file = output_dir + file_name[:-4] + '_Cv_iqr.png'
        plot_heatmap(Cv_df_iqr, output_file, file_name)

        output_file = output_dir + file_name[:-4] + '_Cv_boxplot'
        plot_boxplot(mat, key_name, output_file, ylims, id_col, col_names, row_names, n_models)


        key_name = 'eResponse'
        col_names = enz_names_list[i]
        row_names = rxn_names_list[i]

        Re_df_median = get_df_median(mat, key_name, id_col, col_names, row_names, n_models)
        Re_df_median_list.append(Re_df_median)
        output_file = output_dir + file_name[:-4] + '_Re_median.png'
        plot_heatmap(Re_df_median, output_file, file_name, promiscuous_rxns)

        Re_df_iqr = get_df_iqr(mat, key_name, id_col, col_names, row_names, n_models)
        Re_df_iqr_list.append(Re_df_iqr)
        output_file = output_dir + file_name[:-4] + '_Re_iqr.png'
        plot_heatmap(Re_df_iqr, output_file, file_name, promiscuous_rxns)

        output_file = output_dir + file_name[:-4] + '_Re_boxplot'
        plot_boxplot(mat, key_name, output_file, ylims, id_col, col_names, row_names, n_models)"""

        key_name = 'xControl'
        col_names = rxn_names_list[i]
        row_names = met_names_list[i]

        Cx_df_median = get_df_median(mat, key_name, id_col, col_names, row_names, n_models)
        Cx_df_median_list.append(Cx_df_median)
        output_file = output_dir + file_name[:-4] + '_Cx_median.png'
        plot_heatmap(Cx_df_median, output_file, file_name)

        Cx_df_iqr = get_df_iqr(mat, key_name, id_col, col_names, row_names, n_models)
        Cx_df_iqr_list.append(Cx_df_iqr)
        output_file = output_dir + file_name[:-4] + '_Cx_iqr.png'
        plot_heatmap(Cx_df_iqr, output_file, file_name)

        output_file = output_dir + file_name[:-4] + '_Cx_boxplot'
        plot_boxplot(mat, key_name, output_file, ylims, id_col, col_names, row_names, n_models)




if __name__ == '__main__':
    main_MCA_heatmap()

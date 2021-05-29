import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.io
from visualization.plots_definitions import boxplot_defs

COLOR_LIST = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628']


def get_name_list(file_in):
    name_list = []
    with open(file_in, 'r') as f_in:
        line = f_in.readline()
        line = f_in.readline()
        while line:
            name_list.append(line[2:].strip())
            line = f_in.readline()

    return name_list



def get_df_all(mat, key_name, id_col, col_names, row_names, n_models):
    try:
        df = pd.DataFrame(data=mat['mcaResults'][key_name].item())
        df.columns = col_names
    except ValueError:
        df = pd.DataFrame(data=mat['mcaResults'][key_name].item()[0])
        df.columns = col_names

    df[id_col] = np.tile(row_names, n_models)

    return df


def import_MCA_results(base_dir, model_id, n_models, met, data_file_path):

    file_in_MCA = ''.join([base_dir, 'MCA_', model_id, '.mat'])
    file_in_mets = ''.join([base_dir, model_id, '_metsActive.dat'])
    file_in_rxns = ''.join([base_dir, model_id, '_rxnsActive.dat'])
    file_in_enzs = ''.join([base_dir, model_id, '_enzNames.dat'])

    rxn_names = get_name_list(file_in_rxns)
    met_names = get_name_list(file_in_mets)
    enz_names = get_name_list(file_in_enzs)

    mat = scipy.io.loadmat(file_in_MCA, squeeze_me=True)

    key_name = 'xResponse'
    id_col = 'mets'
    col_names = enz_names
    row_names = met_names
    Cx_df_all = get_df_all(mat, key_name, id_col, col_names, row_names, n_models)

    Cx_df_met = Cx_df_all[Cx_df_all['mets'] == met]
    Cx_df_met.drop('mets', axis=1, inplace=True)
    Cx_df_met = Cx_df_met[sorted(Cx_df_met.columns)]

    Cx_df_met.to_hdf(data_file_path, key='df', mode='w')


def get_non_zero_median_columns(Cx_df, threshold=0.05):

    Cx_median = Cx_df.median()
    columns = Cx_median[(Cx_median < -threshold) | (Cx_median > threshold)].index.values
    n_removed_columns = len(Cx_df.columns) - len(columns)

    print(f'Removed {n_removed_columns} columns. Their median was in the interval [-{threshold}, {threshold}]')

    return columns


def plot_control_coefficients(data_file_path, model_id, threshold=0.05):
    boxplot_defs()

    Cx_df = pd.read_hdf(data_file_path, key='df')
    Cx_df.columns = [col[2:] for col in Cx_df.columns]
    columns = get_non_zero_median_columns(Cx_df, threshold)

    fig, ax = plt.subplots(figsize=[10, 4])
    sns.boxenplot(data=Cx_df[columns], ax=ax, palette=COLOR_LIST)

    for line in ax.lines:
        # set median line style
        line.set_linewidth(1.5)
        line.set_alpha(1)

    plt.hlines(y=0, xmin=-0.5, xmax=len(columns)-0.5, linestyle='--', linewidth=2, color='black')

    ax.grid()
    ax.set_xlim(-0.5, len(columns)-0.5)
    ax.set_ylim(-4, 4)
    ax.set_xlabel('Reaction')
    ax.set_ylabel('Concentration Control Coefficients')
    plt.xticks(rotation=90)
    plt.yticks(list(range(-4, 5)))
    fig.subplots_adjust(top=0.93, bottom=0.35, left=0.1, right=0.98)

    plt.savefig(f'../../plots/mca_boxplots_{model_id}_{threshold}.png')


if __name__ == '__main__':
    base_dir = '/home/dx/Projects/GRASP/io/output_putida/'
    model_id = 'putida_TCA_OP_reg_no_gth_pfba_amp_new_mets_expo_update'
    n_models = 10000

    met = 'm_accoa_c'
    data_file_path = f'../../data/processed/{model_id}_Cx_{met}.h5'

    #import_MCA_results(base_dir, model_id, n_models, met, data_file_path)

    selected_reactions = []
    threshold = 0.2

    plot_control_coefficients(data_file_path, model_id, threshold)

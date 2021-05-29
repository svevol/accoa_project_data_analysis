from src.data.import_simulations import gather_sim_data, get_met_rxn_names
from src.data.import_misc import import_ref_conc
from src.data.process_simulations import get_converging_models_option1,  get_converging_models_option2, get_time_series_quantiles, remove_models, filter_negative_residual_conc
from src.visualization.viz_simulations import plot_bar_quant, plot_model, plot_met, plot_met_model, plot_rxn_model, plot_ensemble_interactive, plot_ensemble
import scipy.io
import pandas as pd
import os
from collections import OrderedDict
import numpy as np


def check_steady_state():
    return


def check_oscillatory_behavior():
    return


def _import_data(model_list, raw_data_dir, time_points_spline, n_models, n_mets):

    conc_dic = OrderedDict()
    flux_dic = OrderedDict()
    for model_name in model_list:

        # get simulated met and rxn names
        met_names, rxn_names = get_met_rxn_names(raw_data_dir, model_name)


        # get reference state concentrations
        file_in = os.path.join(raw_data_dir, f'{model_name}.mat')
        mat = scipy.io.loadmat(file_in, squeeze_me=False)

        all_met_names = [mat['ensemble']['mets'][0][0][met_i][0][0].replace('m_m_', '') for met_i in range(n_mets)]

        ref_conc_dic = import_ref_conc(mat, n_models, all_met_names)

        # import simulation data
        simulation_name = f'{model_name}_500_ex_abs10_-3'
        file_in = os.path.join(raw_data_dir, f'simulation_{simulation_name}.mat')
        mat = scipy.io.loadmat(file_in, squeeze_me=False)

        conc, conc_interp, flux, flux_interp = gather_sim_data(mat, met_names, rxn_names, n_models, time_points_spline,
                                                               save_concs=False, save_fluxes=False,
                                                               ref_conc_dic=ref_conc_dic)

        # get median values
        data_type = 'met'
        conc_dic[model_name] = get_time_series_quantiles(conc_interp, time_points_spline, data_type, met_names,
                                                          scaled=False)
        data_type = 'rxn'
        flux_dic[model_name] = get_time_series_quantiles(flux_interp, time_points_spline, data_type, rxn_names)

    return conc_dic, flux_dic, met_names, rxn_names


def get_differences(model_list, raw_data_dir, time_points_spline, n_models, n_mets):

    conc_dic, flux_dic, met_names, rxn_names = _import_data(model_list, raw_data_dir, time_points_spline, n_models, n_mets)

    conc_diff_dic = OrderedDict({'time_point': np.tile(time_points_spline, len(met_names)),
                                 'met': np.repeat(met_names, len(time_points_spline))})
    flux_diff_dic = OrderedDict({'time_point': np.tile(time_points_spline, len(rxn_names)),
                                 'rxn': np.repeat(rxn_names, len(time_points_spline))})

    for model_i, model_name in enumerate(model_list[1:]):
        conc_denom = conc_dic[model_list[model_i]]['median']
        conc_denom = np.where(abs(conc_denom) < 10**-12, 1, conc_denom)

        flux_denom = flux_dic[model_list[model_i]]['median']
        flux_denom = np.where(abs(flux_denom) < 1, 1, flux_denom)

        conc_diff_dic[model_name] = np.array((conc_dic[model_list[model_i+1]]['median'] - conc_dic[model_list[model_i]]['median']) / conc_denom)
        flux_diff_dic[model_name] = np.array((flux_dic[model_list[model_i+1]]['median'] - flux_dic[model_list[model_i]]['median']) / flux_denom)

    return conc_diff_dic, flux_diff_dic, conc_dic, flux_dic


def check_for_negative_concentrations(data_df: pd.DataFrame, scaled: bool, threshold: float = -10**-8):
    """
    Checks if all concentrations are higher than the given threshold. The idea is to make sure that there are no
    negative concentrations.

    Args:
        data_df: a pandas dataframe with a concentrations or concentrations_unscaled column.
        scaled: whether or not one wants to focus on scaled concentrations.
        threshold: value to use to check if the concentrations are higher than that.

    Returns:
        None
    """

    all_pos = np.all(data_df['concentration' if scaled else 'concentration_unscaled'].values > threshold)

    if all_pos:
        print(f'All concentrations are above the treshold {threshold} :)')
    else:
        print(f'There are some concentrations below {threshold} :(')


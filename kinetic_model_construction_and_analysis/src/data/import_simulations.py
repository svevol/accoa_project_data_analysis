import time
import pandas as pd
import numpy as np
from scipy import interpolate
import os


def gather_sim_data(mat: dict, met_names: list, rxn_names: list, n_models: int, time_points_spline: list,
                    save_concs: bool = False, save_fluxes: bool= False, ref_conc_dic: dict = None) -> tuple:
    """
    Imports the data from the matlab simulation results. Since the time points for which there are concentrations
    may not be the same for all models, it interpolates concentrations and fluxes, and stores the values at certain
    time points (defined in `time_points_spline`). Also, for long simulations, this saves a lot of space.

    Args:
        mat: matlab structures with simulation results.
        met_names: names of the simulated metabolites in the model.
        rxn_names: names of the simulated reactions in the model.
        n_models: number of models to be simulated.
        time_points_spline: time points for which concentration and flux values will be returned.
        save_concs: whether or not to save all concentration values.

    Returns:
        A pandas dataframe with all concentration values (if save_concs==True), a pandas dataframe with concentration
        values at the time points in `time_points_spline`, and a pandas dataframe with flux values at the time points
        in `time_points_spline`.
    """

    data_conc = {'model': [], 'met': [], 'time_point': [], 'concentration': [], 'concentration_unscaled': []}
    data_conc_interp = {'model': [], 'met': [], 'time_point': [], 'concentration': [], 'concentration_unscaled': []}
    data_flux = {'model': [], 'rxn': [], 'time_point': [], 'flux': []}
    data_flux_interp = {'model': [], 'rxn': [], 'time_point': [], 'flux': []}

    n_missing_models = 0
    start_total = time.time()
    for model_i in range(n_models):

        try:
            time_points = mat['simulationRes'][0][model_i]['t'][0][0].transpose()[0]
            met_concs = mat['simulationRes'][0][model_i]['conc'][0][0].transpose()
            rxn_fluxes = mat['simulationRes'][0][model_i]['flux'][0][0].transpose()

        except IndexError:
            n_missing_models += 1
            print(f'{model_i} is missing.')
            continue

        # This step can be very time and space consuming
        if save_concs:
            for met_i, met in enumerate(met_names):
                data_conc['model'].extend(np.repeat(model_i, len(time_points)))
                data_conc['time_point'].extend(time_points)
                data_conc['met'].extend(np.repeat(met, len(time_points)))
                data_conc['concentration'].extend(met_concs[met_i])
                if ref_conc_dic is not None:
                    data_conc['concentration_unscaled'].extend(met_concs[met_i] * ref_conc_dic[met][model_i])
                else:
                    data_conc_interp['concentration_unscaled'].extend(np.repeat(np.nan, len(met_concs[met_i])))

        for met_i, met in enumerate(met_names):
            data_conc_interp['model'].extend(np.repeat(model_i, len(time_points_spline)))
            data_conc_interp['time_point'].extend(time_points_spline)
            data_conc_interp['met'].extend(np.repeat(met_names[met_i], len(time_points_spline)))

            try:
                conc_interp = interpolate.CubicSpline(time_points, met_concs[met_i])
            except ZeroDivisionError:
                print(f'There was a ZeroDivisionError when interpolating the metabolite concentrations, model {model_i}, metabolite {met}. We\'re skipping it.')
                continue

            data_conc_interp['concentration'].extend(conc_interp(time_points_spline))

            if ref_conc_dic is not None:
                data_conc_interp['concentration_unscaled'].extend(conc_interp(time_points_spline) * ref_conc_dic[met][model_i])
            else:
                data_conc_interp['concentration_unscaled'].extend(np.repeat(np.nan, len(time_points_spline)))

        if save_fluxes:
            for rxn_i in range(len(rxn_fluxes)):
                data_flux['model'].extend(np.repeat(model_i, len(time_points)))
                data_flux['time_point'].extend(time_points)
                data_flux['rxn'].extend(np.repeat(rxn_names[rxn_i], len(time_points)))
                data_flux['flux'].extend(rxn_fluxes[rxn_i])

        for rxn_i in range(len(rxn_fluxes)):
            data_flux_interp['model'].extend(np.repeat(model_i, len(time_points_spline)))
            data_flux_interp['time_point'].extend(time_points_spline)
            data_flux_interp['rxn'].extend(np.repeat(rxn_names[rxn_i], len(time_points_spline)))

            try:
                flux_interp = interpolate.CubicSpline(time_points, rxn_fluxes[rxn_i])
            except ZeroDivisionError:
                print(f'There was a ZeroDivisionError when interpolating the reaction fluxes, model {model_i}, reaction {rxn_fluxes[rxn_i]}. We\'re skipping it.')
                continue
            data_flux_interp['flux'].extend(flux_interp(time_points_spline))

    data_df_conc = pd.DataFrame.from_dict(data_conc) if save_concs else None
    data_df_conc_interp = pd.DataFrame.from_dict(data_conc_interp)
    data_df_flux = pd.DataFrame.from_dict(data_flux) if save_fluxes else None
    data_df_flux_interp = pd.DataFrame.from_dict(data_flux_interp)

    print(f'total time: {time.time() - start_total}')
    print(f'There were a total of {n_missing_models} missing models out of {n_models}.')

    return data_df_conc, data_df_conc_interp, data_df_flux, data_df_flux_interp


def get_met_rxn_names(raw_data_dir: str, model_name: str) -> tuple:
    """
    Gets the names of metabolites and reactions in the model.

    Args:
        raw_data_dir: path to folder with the raw data.
        model_name: named of the model.

    Returns:
        A list with the metabolite names and another with the reaction names.
    """

    file_met_names = os.path.join(raw_data_dir, f'{model_name}_metsActive.dat')
    met_names = pd.read_csv(file_met_names, sep='\n').values
    met_names = list(met_names.transpose()[0])
    met_names = [met_name.replace('m_m_', '') for met_name in met_names]

    # get reaction names
    file_rxn_names = os.path.join(raw_data_dir, f'{model_name}_rxnsActive.dat')
    rxn_names = pd.read_csv(file_rxn_names, sep='\n').values
    rxn_names = list(rxn_names.transpose()[0])
    rxn_names = [rxn_name.replace('r_', '') for rxn_name in rxn_names]

    return met_names, rxn_names

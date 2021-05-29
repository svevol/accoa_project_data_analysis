import numpy as np
import pandas as pd


def get_converging_models_option1(conc_df_interp: pd.DataFrame, n_models: int) -> list:
    non_converging_models = []

    for model_i in range(n_models):
        last_conc_values = \
        conc_df_interp[(conc_df_interp['model'] == model_i) & (conc_df_interp['time_point'].between(0.75, 1.05))][
            'concentration'].values

        if len(last_conc_values) == 0 or np.any(np.abs(last_conc_values) > 1.05) or np.any(np.abs(last_conc_values) < 0.95):
            non_converging_models.append(model_i)

    return non_converging_models


def get_converging_models_option2(conc_df_interp: pd.DataFrame, n_models: int, met_names: list,
                                  rel_tol: float = 5 * 10**-3) -> list:

    non_converging_models = []

    for model_i in range(n_models):

        for met in met_names:
            last_conc_values = conc_df_interp[(conc_df_interp['model'] == model_i) &
                                              (conc_df_interp['time_point'].between(0.75, 1.05)) &
                                              (conc_df_interp['met'] == met)]['concentration'].values
            assert len(last_conc_values) == 3
            diff1 = np.abs(last_conc_values[0] - last_conc_values[1])
            diff2 = np.abs(last_conc_values[1] - last_conc_values[2])
            abs_tol = last_conc_values[0]*rel_tol

            if diff1 > abs_tol or diff2 > abs_tol:
                non_converging_models.append(model_i)

    return non_converging_models


def remove_models(conc_df: pd.DataFrame, flux_df: pd.DataFrame, model_list: list) -> tuple:
    filtered_conc_df = conc_df.drop(conc_df[conc_df['model'].isin(model_list)].index)
    filtered_flux_df = flux_df.drop(flux_df[flux_df['model'].isin(model_list)].index)

    return filtered_conc_df, filtered_flux_df


def get_time_series_quantiles(data_df: pd.DataFrame, time_points_spline: list, data_type: str, name_list: list,
                              scaled: bool = True) -> dict:

    quantiles_dic = {'time_point': [], data_type: [], 'q025': np.array([]), 'median': np.array([]), 'q075': np.array([])}

    measure = 'concentration' if data_type == 'met' else 'flux'
    measure = f'{measure}_unscaled' if not scaled else measure
    n_time_points = len(time_points_spline)

    q025 = data_df.groupby([data_type, 'time_point']).quantile(q=0.25)
    q050 = data_df.groupby([data_type, 'time_point']).median()
    q075 = data_df.groupby([data_type, 'time_point']).quantile(q=0.75)

    for item in name_list:
        quantiles_dic[data_type].extend(np.repeat(item, n_time_points))
        quantiles_dic['time_point'].extend(time_points_spline)

        quantiles_dic['q025'] = np.append(quantiles_dic['q025'], q025.loc[item, :][measure])
        quantiles_dic['median'] = np.append(quantiles_dic['median'], q050.loc[item, :][measure])
        quantiles_dic['q075'] = np.append(quantiles_dic['q075'], q075.loc[item, :][measure])

    #data_df_quantiles = pd.DataFrame.from_dict(conc_dic)

    return quantiles_dic


def filter_negative_residual_conc(data_df: pd.DataFrame, scaled: bool, threshold: float = -10**-5) -> pd.DataFrame:
    """
    This function looks for concentrations lower than the given threshold and sets them to zero.

    Args:
        data_df: a pandas dataframe with a concentrations or concentrations_unscaled column.
        scaled: whether or not one wants to focus on scaled concentrations.
        threshold: concentrations lower than this will be set to zero.

    Returns:
        pandas dataframe with concentrations lower than threshold set to zero.
    """

    data_df.loc[(data_df['concentration' if scaled else 'concentration_unscaled'] < 0) &
                (data_df['concentration' if scaled else 'concentration_unscaled'] > threshold),
                ['concentration_unscaled', 'concentration']] = 0

    return data_df



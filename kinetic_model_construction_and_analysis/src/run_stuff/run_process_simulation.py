import hdf5storage
import argparse
import pandas as pd
import os
from src.analysis.analyze_simulations import check_for_negative_concentrations
from src.data.import_simulations import gather_sim_data, get_met_rxn_names
from src.data.import_misc import import_ref_conc
from src.data.process_simulations import get_converging_models_option1,  get_time_series_quantiles, remove_models, filter_negative_residual_conc



def run_summarize_simulation(raw_data_dir, model_name, simulation_name, n_models, save_sim_data, filter_data):

    # Get time points for spline interpolation
    order_of_magnitude = [-9, -8, -7, -6, -5, -4, -3, -2, -1]
    time_points_spline = [coefficient * 10 ** exponent for exponent in order_of_magnitude for coefficient in range(1, 10)]
    time_points_spline.extend([1])
    time_points_spline.insert(0, 0)

    # get metabolite and reaction names
    met_names, rxn_names = get_met_rxn_names(raw_data_dir, model_name)

    # import model ensemble
    print('Importing model ensemble...')
    file_in = os.path.join(raw_data_dir, f'{model_name}.mat')
    mat = hdf5storage.loadmat(file_in, squeeze_me = False)

    # get ALL metabolite names, also the constant ones
    n_mets = len(mat['ensemble']['mets'][0][0])
    all_met_names = [mat['ensemble']['mets'][0][0][met_i][0][0].replace('m_m_', '') for met_i in range(n_mets)]

    # get reference concentrations
    ref_conc_dic = import_ref_conc(mat, n_models, all_met_names)

    # import simulation data
    print('Importing simulation data...')
    file_in = os.path.join(raw_data_dir, f'simulation_{simulation_name}.mat')
    mat = hdf5storage.loadmat(file_in, squeeze_me=False)

    # import simulation data
    conc, conc_interp, flux, flux_interp = gather_sim_data(mat, met_names, rxn_names, n_models, time_points_spline,
                                                           save_concs=False, save_fluxes=False,
                                                           ref_conc_dic=ref_conc_dic)

    if save_sim_data:
        print('Saving simulation data...')
        conc_interp.to_csv(f'../../data/processed/conc_interp_{simulation_name}.csv')
        flux_interp.to_csv(f'../../data/processed/flux_interp_{simulation_name}.csv')

    # do some filtering
    print('Checking for negative concentrations...')
    check_for_negative_concentrations(conc_interp, scaled=False)

    #conc_interp = filter_negative_residual_conc(conc_interp, scaled=False)
    if filter_data:
        print('Filtering data...')
        non_converging_models_option1 = get_converging_models_option1(conc_interp, n_models)
        conc_interp_filtered, flux_interp_filtered = remove_models(conc_interp, flux_interp, non_converging_models_option1)

    # summarize simulations into quantiles
    print('Summarizing data...')
    data_type = 'met'
    conc_interp_quantiles = get_time_series_quantiles(conc_interp, time_points_spline, data_type, met_names,
                                                      scaled=False)
    data_type = 'rxn'
    flux_interp_quantiles = get_time_series_quantiles(flux_interp, time_points_spline, data_type, rxn_names)

    conc_interp_quantiles = pd.DataFrame.from_dict(conc_interp_quantiles)
    flux_interp_quantiles = pd.DataFrame.from_dict(flux_interp_quantiles)

    # save data
    print('Saving summarized data...')
    conc_interp_quantiles.to_csv(f'../../data/processed/conc_interp_quantiles_{simulation_name}_filtered.csv')
    flux_interp_quantiles.to_csv(f'../../data/processed/flux_interp_quantiles_{simulation_name}_filtered.csv')


my_parser = argparse.ArgumentParser(description='Summarizes the ensemble simulation into medians and quartiles.')
my_parser.add_argument('raw_data_dir', type=str)
my_parser.add_argument('model_name', type=str)
my_parser.add_argument('simulation_name', type=str)
my_parser.add_argument('n_models',  type=int)
my_parser.add_argument('save_sim_data',  type=bool)
my_parser.add_argument('filter_data',  type=bool)

args = my_parser.parse_args()
print(f'Input arguments:\n{vars(args)}')

run_summarize_simulation(args.raw_data_dir, args.model_name, args.simulation_name, args.n_models, args.save_sim_data,
                         filter_data=args.filter_data)

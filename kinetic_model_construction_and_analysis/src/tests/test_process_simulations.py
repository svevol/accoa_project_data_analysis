import os
import unittest
import scipy.io

from src.data.process_simulations import get_time_series_quantiles
from src.data.import_simulations import gather_sim_data, get_met_rxn_names


class TestProcessSimulations(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.data_dir = os.path.join(this_dir, '..', '..', 'data', 'raw')
        self.model_name = 'putida_v2_3_all_fixed_flux_2000_abs10_-4'
        self.file_in = os.path.join(self.data_dir, f'simulation_{self.model_name}.mat')
        self.mat = scipy.io.loadmat(self.file_in, squeeze_me=False)


    def test_get_time_series_quantiles(self):
        met_names, rxn_names = get_met_rxn_names(self.data_dir, 'putida_v2_3_all_fixed_flux')
        time_points_spline = [10**-9, 10 ** -4, 10 ** -3, 10 ** -2, 10 ** -1, 1]  # , 10, 100]
        n_models = 10
        conc, conc_interp, flux, flux_interp = gather_sim_data(self.mat, met_names, rxn_names, n_models, time_points_spline,
                                                               save_concs=False, save_fluxes=False)

        data_type = 'rxn'
        flux_interp_quantiles = get_time_series_quantiles(flux_interp, time_points_spline, data_type, rxn_names)

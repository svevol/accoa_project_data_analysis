import os
import unittest
import scipy.io

from src.analysis.analyze_simulations import get_differences


class TestAnalyzeSimulations(unittest.TestCase):

    def test_gather_sim_data(self):
        this_dir, this_filename = os.path.split(__file__)
        raw_data_dir = os.path.join(this_dir, '..', '..', 'data', 'raw')

        order_of_magnitude = [-9, -8, -7, -6, -5, -4, -3, -2, -1]
        time_points_spline = [coefficient * 10 ** exponent for exponent in order_of_magnitude for coefficient in [1]]
        time_points_spline.extend([1])
        time_points_spline.insert(0, 0)

        model_list = ['putida_all_NADPHr_2G6PDH_no_reg',
                      'putida_all_NADPHr_2G6PDH_GAPDH_reg',
                      'putida_all_NADPHr_2G6PDH_GAPDH_nadph1_reg']
        n_models = 10
        n_mets = 51

        conc_diff, flux_diff = get_differences(model_list, raw_data_dir, time_points_spline, n_models, n_mets)

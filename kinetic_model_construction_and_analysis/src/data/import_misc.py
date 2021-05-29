import pandas as pd


def import_ref_conc(mat: dict, n_models: int, met_names: list) -> dict:
    """
    Converts a .mat file from matlab into a dictionary with reference concentrations for each model.
    Metabolites are the keys, lists of concentrations are the values, where each entry is the concentration for a model.

    Args:
        mat: ensemble .mat file from matlab in form of dictionary.
        n_models: number of models to consider.
        met_names: name of the metabolites.

    Returns:
        A dictionary with the reference metabolite concentrations for each model.
    """

    n_mets = len(met_names)
    ref_conc= []
    for model_i in range(n_models):
        model_i_data = mat['ensemble']['populations'][0][0]['models'][0][0]['metConcRef'][0][model_i].transpose()[0]
        ref_conc.append(model_i_data)

    ref_conc_df = pd.DataFrame(data=ref_conc, index=range(n_models), columns=range(n_mets))
    ref_conc_df.columns = met_names
    ref_conc_dic = ref_conc_df.to_dict(orient='list')

    return ref_conc_dic

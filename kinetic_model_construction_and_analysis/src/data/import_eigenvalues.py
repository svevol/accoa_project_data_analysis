import pandas as pd


def import_eigenvalues(mat: dict, n_models: int, n_mets: int) -> tuple:

    real_part = []
    imag_part = []
    for model_i in range(n_models):
        real_part.append(mat['eigValuesList'][0]['real'][0][0][model_i].transpose()[0])
        imag_part.append(mat['eigValuesList'][0]['imag'][0][0][model_i].transpose()[0])

    real_df = pd.DataFrame(data=real_part, index=range(n_models), columns=range(n_mets))
    imag_df = pd.DataFrame(data=imag_part, index=range(n_models), columns=range(n_mets))

    return real_df, imag_df

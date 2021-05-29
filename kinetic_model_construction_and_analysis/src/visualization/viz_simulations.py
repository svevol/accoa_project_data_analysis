import os
import altair as alt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.visualization.plots_definitions import barplot_defs


COLOR_LIST = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6',
              '#6a3d9a', '#ffff99', '#b15928']


def plot_bar_quant(data_df: pd.DataFrame, xy_df_labels: list, xy_labels: list, fig_name: str, ylims: list):
    """
    Plots concentrations/fluxes at given time points in a bar plot.

    Args:
        data_df:
        xy_df_labels:
        xy_labels:
        fig_name:
        ylims:

    Returns:

    """
    #barplot_defs()
    sns.set_style("whitegrid",
                  {'axes.edgecolor': '0',
                   'axes.labelcolor': '0',
                   'grid.color': '0',
                   'grid.linestyle': '--',
                   'text.color': '0',
                   'xtick.color': '0',
                   'ytick.color': '0',
                   'xtick.bottom': True,
                   'ytick.left': True,
                   'axes.spines.left': True,
                   'axes.spines.bottom': True,
                   'axes.spines.right': True,
                   'axes.spines.top': True})

    g = sns.catplot(x=xy_df_labels[0], y=xy_df_labels[1], hue='time_point', data=data_df,
                    kind='bar', palette=sns.color_palette("Set1", n_colors=8, desat=.5),
                    height=15, aspect=2, legend=False)

    for ax in g.axes.flat:
        #if xy_df_labels[1].find('unscaled'):
        ax.set_yscale('log')
        #else:
        #    ax.set_ylim(ylims)
        ax.tick_params(labelsize=22)
        ax.set_xlabel(xy_labels[0], size=28)
        ax.set_ylabel(xy_labels[1], size=28)
        #ax.grid()
        ax.legend(loc='upper left',
                  fontsize=22,
                  title='Time point',
                  title_fontsize=26)


    g.fig.subplots_adjust(top=0.95, bottom=0.2, left=0.05, right=0.98)
    plt.xticks(rotation=90)

    this_dir, this_filename = os.path.split(__file__)
    plt.savefig(os.path.join(this_dir, '..', '..', 'plots', f'{fig_name}.png'))
    plt.close()


def plot_model(data_df: pd.DataFrame, data_interp_df: pd.DataFrame, model_i: int = 0, scaled_conc: bool = False,
               x_scale: str = 'linear', y_scale: str = 'linear', x_lim: tuple = (10 ** -10, 1), y_lim: tuple = None):

    """
    Plots all metabolites in a given model in altair. Uses line plots.

    Args:
        data_df:
        data_interp_df:
        model_i:
        scaled_conc:
        x_lim:

    Returns:

    """
    if data_df is not None:
        print('linear' if scaled_conc else 'log')
        print('concentration:Q' if scaled_conc else 'concentration_unscaled:Q')
        plot1 = alt.Chart(data_df[data_df['model'] == model_i]).mark_line().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='met:N',
            tooltip='met:N'
        ).properties(
            width=500,
            height=400
        )

        plot2 = alt.Chart(data_interp_df[data_interp_df['model'] == model_i]).mark_point().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='met:N',
            tooltip='met:N'
        ).properties(
            width=500,
            height=400
        )

        return alt.layer(plot1, plot2).interactive()

    else:
        plot2 = alt.Chart(data_interp_df[data_interp_df['model'] == model_i]).mark_line().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='met:N',
            tooltip='met:N'
        ).properties(
            width=500,
            height=400
        )
        return plot2.interactive()


def plot_met(data_df: pd.DataFrame, data_interp_df: pd.DataFrame, met_selection: list, scaled_conc: bool = False,
             x_scale: str = 'linear', y_scale: str = 'linear', x_lim: tuple = (10 ** -10, 1), y_lim: tuple = None):
    """
    Plots a given metabolite across all models in altair. Uses line plots.

    Args:
        data_df:
        data_interp_df:
        met:
        scaled_conc:
        x_lim:

    Returns:

    """

    if data_df is not None:
        plot1 = alt.Chart(data_df[data_df['met'].isin(met_selection)]).mark_line().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='model:N',
            tooltip='model:N'
        ).properties(
            width=500,
            height=400
        )

        plot2 = alt.Chart(data_interp_df[data_interp_df['met'].isin(met_selection)]).mark_point().encode(
                alt.X('time_point:Q',
                      scale=alt.Scale(domain=x_lim, type=x_scale)
                      ),
                alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                      scale=alt.Scale(y_scale)
                      ),
                color='model:N',
                tooltip='model:N'
            ).properties(
                width=500,
                height=400
            )

        return alt.layer(plot1, plot2).interactive()

    else:
        plot2 = alt.Chart(data_interp_df[data_interp_df['met'].isin(met_selection)]).mark_line().encode(
                alt.X('time_point:Q',
                      scale=alt.Scale(domain=x_lim, type=x_scale)
                      ),
                alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                      scale=alt.Scale(y_scale)
                      ),
                color='model:N',
                tooltip='model:N'
            ).properties(
                width=500,
                height=400
            )

        return plot2.interactive()


# plot
def plot_met_model(data_df: pd.DataFrame, data_interp_df: pd.DataFrame, met_selection: list, model_i: int = 0,
                   scaled_conc: bool = True, x_scale: str = 'linear', y_scale: str = 'linear',
                   x_lim: tuple = (10**-10, 1), y_lim: tuple = None):
    """
    Uses altair to plot a given metabolite in a given model. Uses line plots.

    Args:
        data_df:
        data_interp_df:
        met:
        model_i:
        scaled_conc:
        x_lim:

    Returns:

    """

    if data_df is not None:

        plot1 = alt.Chart(data_df[(data_df['met'].isin(met_selection)) & (data_df['model'] == model_i)]).mark_line().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='met:N',
            tooltip='concentration:Q' if scaled_conc else 'concentration_unscaled:Q'
        ).properties(
            width=500,
            height=400
        )

        plot2 = alt.Chart(
            data_interp_df[(data_interp_df['met'].isin(met_selection)) & (data_interp_df['model'] == model_i)]).mark_point().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='met:N',
            tooltip='concentration:Q' if scaled_conc else 'concentration_unscaled:Q'
        ).properties(
            width=500,
            height=400
        )

        return alt.layer(plot1, plot2).interactive()

    else:
        plot2 = alt.Chart(
            data_interp_df[(data_interp_df['met'].isin(met_selection)) & (data_interp_df['model'] == model_i)]).mark_line().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('concentration:Q' if scaled_conc else 'concentration_unscaled:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='met:N',
            tooltip='concentration:Q' if scaled_conc else 'concentration_unscaled:Q'
        ).properties(
            width=500,
            height=400
        )

        return plot2.interactive()


def plot_rxn_model(data_df: pd.DataFrame, data_interp_df: pd.DataFrame, rxn_selection: list, model_i: int = 0,
                   x_scale: str = 'linear', y_scale: str = 'linear', x_lim: tuple = (10**-10, 1), y_lim: tuple = None):
    """
    Uses altair to plot a given metabolite in a given model. Uses line plots.

    Args:
        data_df:
        data_interp_df:
        met:
        model_i:
        scaled_conc:
        x_lim:

    Returns:

    """

    if data_df is not None:

        plot1 = alt.Chart(data_df[(data_df['rxn'].isin(rxn_selection)) & (data_df['model'] == model_i)]).mark_line().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('flux:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='rxn:N',
            tooltip='flux:Q'
        ).properties(
            width=500,
            height=400
        )

        plot2 = alt.Chart(
            data_interp_df[(data_interp_df['rxn'].isin(rxn_selection)) & (data_interp_df['model'] == model_i)]).mark_point().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('flux:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='rxn:N',
            tooltip='flux:Q',
        ).properties(
            width=500,
            height=400
        )

        return alt.layer(plot1, plot2).interactive()

    else:

        plot2 = alt.Chart(
            data_interp_df[(data_interp_df['rxn'].isin(rxn_selection)) & (data_interp_df['model'] == model_i)]).mark_line().encode(
            alt.X('time_point:Q',
                  scale=alt.Scale(domain=x_lim, type=x_scale)
                  ),
            alt.Y('flux:Q',
                  scale=alt.Scale(type=y_scale)
                  ),
            color='rxn:N',
            tooltip='flux:Q',
        ).properties(
            width=500,
            height=400
        )

        return plot2.interactive()


def _plot_column(data_df, time_points, data_type, names_lists, ax_list, col_i, x_lims, scaled):

    for row_i, name_list in enumerate(names_lists):
        for i, name in enumerate(name_list):
            ax_list[row_i, col_i].plot(time_points, data_df[data_df[data_type] == name]['median'], color=COLOR_LIST[i % 12], label=name)
            ax_list[row_i, col_i].fill_between(time_points, data_df[data_df[data_type] == name]['q025'],
                                      data_df[data_df[data_type] == name]['q075'], color=COLOR_LIST[i % 12], alpha=0.3)


        if data_type == 'rxn':
            ax_list[row_i, col_i].set_yscale('symlog')
            ax_list[row_i, col_i].set_ylim([-10 ** 2, 10 ** 4])
        if data_type == 'met':
            ax_list[row_i, col_i].set_yscale('log')
            ax_list[row_i, col_i].set_ylim([10**-12, 10**-2])

        if col_i == 1:
            ax_list[row_i, col_i].set_xscale('log')

        ax_list[row_i, col_i].set_xlim(x_lims[col_i])

        ax_list[row_i, col_i].grid()
        ax_list[row_i, col_i].legend()

    return ax_list


def plot_ensemble(data_df: pd.DataFrame, time_points: list, data_type: str, names_lists: list, plot_title,
                   scaled: bool = True, x_lims: tuple = ((0, 0.02), (0, 1))):
    """
    Plots model ensembles using matplotlib. Uses line plots.
    The median is represented by a line, and uncertainty is given by the 25% quantile and the 75% one.

    Args:
        data_df:
        time_points:
        data_type:
        names_lists:
        plot_title:
        scaled:
        x_lims:

    Returns:

    """

    n_rows = len(names_lists)
    fig, ax_list = plt.subplots(n_rows, 2, figsize=(20, n_rows*5))

    ax_list = _plot_column(data_df, time_points, data_type, names_lists, ax_list, 0, x_lims, scaled)
    ax_list = _plot_column(data_df, time_points, data_type, names_lists, ax_list, 1, x_lims, scaled)

    plt.tight_layout()

    this_dir, this_filename = os.path.split(__file__)
    plt.savefig(os.path.join(this_dir, '..', '..', 'plots', f'{plot_title}.pdf'))

    plt.close()


def plot_ensemble_interactive(data_df: pd.DataFrame, data_type, selected_data: list = None, x_scale: str = 'linear',
                              y_scale: str = 'linear', x_lim: tuple = (10**-10, 1), y_lim: tuple = None):
    """
    Plots model ensembles using altair. Uses line plots.
    The median is represented by a line, and uncertainty is given by the 25% quantile and the 75% one.

    Args:
        data_df:
        data_type:
        selected_data:
        scaled:
        x_lim:

    Returns:

    """
    if selected_data is None:
        selected_data = data_df[data_type].unique()

    plot1 = alt.Chart(data_df[data_df[data_type].isin(selected_data)]).mark_line().encode(
        x=alt.X('time_point:Q',
                scale=alt.Scale(domain=x_lim, type=x_scale)),
        y=alt.Y('median:Q',
                scale=alt.Scale(type=y_scale)
               ),
        color=f'{data_type}:N',
        tooltip=[f'{data_type}:N', 'median:Q']
    ).properties(
            width=600,
            height=400
    )

    plot2 = alt.Chart(data_df[data_df[data_type].isin(selected_data)]).mark_area().encode(
        x=alt.X('time_point:Q',
                scale=alt.Scale(domain=x_lim, type=x_scale)),
        y=alt.Y('q025:Q',
                scale=alt.Scale(type=y_scale)
                ),
        y2='q075:Q',
        color=f'{data_type}:N',
        tooltip=[f'{data_type}:N', 'median:Q'],
        opacity=alt.OpacityValue(0.3)
    ).properties(
            width=600,
            height=400
    )

    return alt.layer(plot1, plot2).interactive()


def plot_diffs_heatmap(data_df, model_name, data_type, ordered_columns):
    data_df = data_df.pivot(index='time_point', columns=data_type, values=model_name)
    data_df = data_df[ordered_columns].transpose()

    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['axes.labelsize'] = 20

    fig, ax = plt.subplots(figsize=(30, 20))
    sns.heatmap(data_df, cmap='RdBu', vmin=-1, vmax=1, ax=ax)
    #plt.ticklabel_format(axis='x', style='sci', scilimits=(-9, 0))

    plt.tight_layout()

    this_dir, this_filename = os.path.split(__file__)
    plot_dir = os.path.join(this_dir, '..', '..', 'plots')

    plt.savefig(os.path.join(plot_dir, f'{model_name}_{data_type}.png'))
    plt.close()
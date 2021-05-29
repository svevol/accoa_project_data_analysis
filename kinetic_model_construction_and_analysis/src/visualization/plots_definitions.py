import matplotlib.pyplot as plt


def barplot_defs():

    plt.style.use('classic')
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'

    plt.rcParams['axes.labelsize'] = 21
    plt.rcParams['axes.labelpad'] = '14'

    plt.rcParams['axes.linewidth'] = 1.5

    plt.rcParams['xtick.major.width'] = 1.5
    plt.rcParams['ytick.major.width'] = 1.5
    plt.rcParams['xtick.minor.width'] = 1.5
    plt.rcParams['ytick.minor.width'] = 1.0

    plt.rcParams['grid.linewidth'] = 1.0

    plt.rcParams['xtick.major.pad'] = '12'
    plt.rcParams['ytick.major.pad'] = '8'

    plt.rcParams['xtick.labelsize'] = '19'
    plt.rcParams['ytick.labelsize'] = '18'

    plt.rcParams['legend.fontsize'] = '18'
    plt.rcParams['legend.borderpad'] = 0.15
    #plt.rcParams['legend.borderpad'] = 0.2
    plt.rcParams['legend.labelspacing'] = 0.2
    plt.rcParams['legend.columnspacing'] = 2
    plt.rcParams['legend.handlelength'] = 0.5

    plt.rcParams['axes.spines.left'] = True  # display axis spines
    plt.rcParams['axes.spines.bottom'] = True
    plt.rcParams['axes.spines.top'] = True
    plt.rcParams['axes.spines.right'] = True



def boxplot_defs():

    plt.style.use('classic')
    #plt.rcParams['mathtext.fontset'] = 'stix'
    #plt.rcParams['font.family'] = 'STIXGeneral'

    plt.rcParams['axes.labelsize'] = 12.
    #plt.rcParams['axes.labelsize'] = 24.

    plt.rcParams['axes.linewidth'] = 1.5

    plt.rcParams['xtick.major.width'] = 2
    plt.rcParams['ytick.major.width'] = 2
    plt.rcParams['xtick.minor.width'] = 1.5
    plt.rcParams['ytick.minor.width'] = 1.5

    plt.rcParams['grid.linewidth'] = 1

    plt.rcParams['xtick.major.pad'] = '12'
    plt.rcParams['ytick.major.pad'] = '8'

    #plt.rcParams['xtick.labelsize'] = '26'
    plt.rcParams['xtick.labelsize'] = '12'
    plt.rcParams['ytick.labelsize'] = '12'

    plt.rcParams['legend.fontsize'] = '12'
    plt.rcParams['legend.borderpad'] = 0.15
    # plt.rcParams['legend.borderpad'] = 0.2
    plt.rcParams['legend.labelspacing'] = 0.2
    plt.rcParams['legend.columnspacing'] = 2
    plt.rcParams['legend.handlelength'] = 0.5
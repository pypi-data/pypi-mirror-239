import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.lines import Line2D
import squarify
import pandas as pd
import random 
import joypy

def CONVERT_SI_TO_INCHES(WIDTH, HEIGHT):
    """ 
    This function convert figure dimensions from meters to inches.
    
    Input:
    WIDTH    |  Figure width in SI units       |         |  Float
    HEIGHT   |  Figure height in SI units      |         |  Float
    
    Output:
    WIDTH    |  Figure width in INCHES units   |         |  Float
    HEIGHT   |  Figure height in INCHES units  |         |  Float
    """
    
    # Converting dimensions
    WIDTH /= 2.54
    HEIGHT /= 2.54
    
    return WIDTH, HEIGHT

def SAVE_GRAPHIC(NAME, EXT, DPI):
    """ 
    This function saves graphics according to the selected extension.

    Input: 
    NAME  | Path + name figure               |         |  String
          |   NAME = 'svg'                   |         |  
          |   NAME = 'png'                   |         |
          |   NAME = 'eps'                   |         | 
          |   NAME = 'pdf'                   |         |
    EXT   | File extension                   |         |  String
    DPI   | The resolution in dots per inch  |         |  Integer
    
    Output:
    N/A
    """
    
    plt.savefig(NAME + '.' + EXT, dpi = DPI, bbox_inches = 'tight', transparent = True)

def HISTOGRAM_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-1.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    Y_AXIS_LABEL = PLOT_SETUP['Y AXIS LABEL']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    AXISES_COLOR = PLOT_SETUP['AXISES COLOR']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']     
    LABELS_COLOR = PLOT_SETUP['LABELS COLOR']
    CHART_COLOR = PLOT_SETUP['CHART COLOR']
    BINS = int(PLOT_SETUP['BINS'])
    # KDE = PLOT_SETUP['KDE']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']
    
    # Dataset and others information
    DATA = DATASET['DATASET']
    COLUMN = DATASET['COLUMN']
 
    # Plot
    [W, H] = CONVERT_SI_TO_INCHES(W, H)
    sns.set(style = 'ticks')
    FIG, (AX_BOX, AX_HIST) = plt.subplots(2, figsize = (W, H), sharex = True, gridspec_kw = {'height_ratios': (.15, .85)})
    sns.boxplot(data = DATA, x = COLUMN, ax = AX_BOX, color = CHART_COLOR)
    sns.histplot(data = DATA, x = COLUMN, ax = AX_HIST, color = CHART_COLOR, bins = BINS)
    AX_BOX.set(yticks = [])
    AX_BOX.set(xlabel = '')
    FONT = {'fontname': 'DejaVu Sans',
            'color':  LABELS_COLOR,
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX_HIST.set_xlabel(xlabel = X_AXIS_LABEL, fontdict = FONT)
    AX_HIST.set_ylabel(ylabel = Y_AXIS_LABEL, fontdict = FONT)
    AX_HIST.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = AXISES_COLOR)
    AX_HIST.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = AXISES_COLOR)
    plt.grid()
    sns.despine(ax = AX_HIST)
    sns.despine(ax = AX_BOX, left = True)
    
    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)

def LINE_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-2.html
    """
    
    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    EXT = PLOT_SETUP['EXTENSION']
    DPI = PLOT_SETUP['DPI']
    MARKER = PLOT_SETUP['MARKER']
    MARKER_SIZE = PLOT_SETUP['MARKER SIZE']
    LINE_WIDTH = PLOT_SETUP['LINE WIDTH']
    LINE_STYLE = PLOT_SETUP['LINE STYLE']
    Y_AXIS_LABEL = PLOT_SETUP['Y AXIS LABEL']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']     
    LABELS_COLOR = PLOT_SETUP['LABELS COLOR']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    AXISES_COLOR = PLOT_SETUP['AXISES COLOR']
    COLORS = PLOT_SETUP['CHART COLOR']
    GRID = PLOT_SETUP['ON GRID?']
    YLOGSCALE = PLOT_SETUP['Y LOG']
    XLOGSCALE = PLOT_SETUP['X LOG']
    LEGEND = PLOT_SETUP['LEGEND']
    LOC = PLOT_SETUP['LOC LEGEND']
    SIZE_LEGEND = PLOT_SETUP['SIZE LEGEND']
    
    # Dataset and others information
    DATA = DATASET['DATASET']
    X_DATASET = []
    Y_DATASET = []
    N_SETS = int(len(DATA.columns) / 2)
    for I in range(N_SETS):
        X_COLUMN_NAME = f'x{I}'
        Y_COLUMN_NAME = f'y{I}'
        X_DATASET.append(DATA[[X_COLUMN_NAME]])
        Y_DATASET.append(DATA[[Y_COLUMN_NAME]])    
    DF_X = pd.concat(X_DATASET, axis = 1)
    DF_Y = pd.concat(Y_DATASET, axis = 1)
    DF_X_COL = list(DF_X.columns)
    DF_Y_COL = list(DF_Y.columns)
    
    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), sharex = True)
    for K in range(N_SETS):
        if len(LEGEND) == 1:
            if LEGEND[0] == None:
                AX.plot(DF_X[DF_X_COL[K]], DF_Y[DF_Y_COL[K]], marker = MARKER[K],  linestyle = LINE_STYLE[K], linewidth = LINE_WIDTH, markersize = MARKER_SIZE, color = COLORS[K])
            else:
                AX.plot(DF_X[DF_X_COL[K]], DF_Y[DF_Y_COL[K]], marker = MARKER[K],  linestyle = LINE_STYLE[K], linewidth = LINE_WIDTH, markersize = MARKER_SIZE, label = LEGEND[K], color = COLORS[K])
        else:
            AX.plot(DF_X[DF_X_COL[K]], DF_Y[DF_Y_COL[K]], marker = MARKER[K],  linestyle = LINE_STYLE[K], linewidth = LINE_WIDTH, markersize = MARKER_SIZE, label = LEGEND[K], color = COLORS[K])
    if YLOGSCALE:
        AX.semilogy()
    if XLOGSCALE:
        AX.semilogx()
    font = {'fontname': 'DejaVu Sans',
            'color':  LABELS_COLOR,
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX.set_ylabel(Y_AXIS_LABEL, fontdict = font)
    AX.set_xlabel(X_AXIS_LABEL, fontdict = font)   
    AX.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = AXISES_COLOR)
    AX.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = AXISES_COLOR)
    if GRID == True:
        AX.grid(color = 'grey', linestyle = '-.', linewidth = 1, alpha = 0.20)
    if len(LEGEND) == 1:
        if LEGEND[0] == None:
            pass
        else:
            plt.legend(loc = LOC, prop = {'size': SIZE_LEGEND})
    else:
        plt.legend(loc = LOC, prop = {'size': SIZE_LEGEND})
    
    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)

def SCATTER_CHART(**kwargs):    
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-3.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    MARKER_SIZE = PLOT_SETUP['MARKER SIZE']
    CMAP = PLOT_SETUP['CMAP COLOR']
    Y_AXIS_LABEL = PLOT_SETUP['Y AXIS LABEL']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']  
    LABELS_COLOR = PLOT_SETUP['LABELS COLOR']
    AXISES_COLOR = PLOT_SETUP['AXISES COLOR']
    GRID = PLOT_SETUP['ON GRID?']
    YLOGSCALE = PLOT_SETUP['Y LOG']
    XLOGSCALE = PLOT_SETUP['X LOG']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']


    # Data
    DATA = DATASET['DATASET']
    DATA_NAMES = list(DATA.columns)
    DATA_NAMES = [i.upper() for i in DATA_NAMES]
    DATA.columns = DATA_NAMES
    X = DATA['X']
    Y = DATA['Y']
    Z = DATA['COLORBAR']
    
    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), sharex = True)
    if CMAP == False:
        IM = AX.scatter(X, Y, marker = 'o', s = MARKER_SIZE)
    else:
        IM = AX.scatter(X, Y, c = Z, marker = 'o', s = MARKER_SIZE , cmap = CMAP)
        colorbar = plt.colorbar(IM)
    if YLOGSCALE:
        AX.semilogy()
    if XLOGSCALE:
        AX.semilogx()
    FONT = {'fontname': 'DejaVu Sans',
            'color':  LABELS_COLOR,
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX.set_ylabel(Y_AXIS_LABEL, fontdict = FONT)
    AX.set_xlabel(X_AXIS_LABEL, fontdict = FONT)   
    AX.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = AXISES_COLOR, labelrotation = 0, direction = 'out', which = 'both', length = 10)
    AX.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = AXISES_COLOR)
    if GRID == True:
        AX.grid(color = 'grey', linestyle = '-', linewidth = 1, alpha = 0.20)
    SAVE_GRAPHIC(NAME, EXT, DPI)

def BAR_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-4.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    BAR_WIDTH = PLOT_SETUP['BAR WIDTH']
    OPACITY = PLOT_SETUP['OPACITY']
    Y_AXIS_LABEL = PLOT_SETUP['Y AXIS LABEL']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    AXISES_COLOR = PLOT_SETUP['AXISES COLOR']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']
    LABELS_COLOR = PLOT_SETUP['LABELS COLOR']
    COLORS = PLOT_SETUP['COLORS']
    GRID = PLOT_SETUP['ON GRID?']  
    YLOGSCALE = PLOT_SETUP['Y LOG']
    EXT = PLOT_SETUP['EXTENSION']
    DPI = PLOT_SETUP['DPI']
    
    # Data
    DATA = DATASET['DATASET']
    DATA_NAMES = list(DATA.columns)
    DATA_NAMES = [i.upper() for i in DATA_NAMES]
    DATA.columns = DATA_NAMES
    X = list(DATA['X'])
    Y = DATA.drop(['X'], axis = 1, inplace = False)
    LEGEND = list(Y.columns)
    LEGEND = [i.lower() for i in LEGEND]
    Y.columns = LEGEND
    N_L, N_C = Y.shape
   
    # Plot
    [W, H] = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H))
    
    # Create the bar chart for each category
    POS = np.arange(len(X))
    
    for I, CATEGORY in enumerate(LEGEND):
        AX.bar(POS + BAR_WIDTH * I, list(Y[CATEGORY]), width = BAR_WIDTH, alpha = OPACITY, color = COLORS[I], label = CATEGORY) #, error_kw = error_PLOT_SETUP)
    FONT = {'fontname': 'DejaVu Sans',
            'color':  LABELS_COLOR,
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX.set_ylabel(Y_AXIS_LABEL, fontdict = FONT)
    AX.set_xlabel(X_AXIS_LABEL, fontdict = FONT)
    AX.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = AXISES_COLOR)
    AX.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = AXISES_COLOR)
    if N_C > 1:
        maxx = POS + BAR_WIDTH * (N_C - 1)
        minn = POS
        POS_TEXT = POS  + (maxx - minn) / 2
        AX.set_xticks(POS_TEXT, X)
    else:
        POS_TEXT = POS
        AX.set_xticks(POS_TEXT, X)
    AX.set_xticklabels(X)
    AX.legend()
    if YLOGSCALE:
        AX.semilogy()

    if GRID == True:
        AX.grid(color = 'grey', linestyle = '-', linewidth = 1, alpha = 0.20, axis = 'y')
    plt.tight_layout()
    SAVE_GRAPHIC(NAME, EXT, DPI)

def PIZZA_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-5.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    TEXT_COLOR = PLOT_SETUP['TEXT COLOR']
    TEXT_FONT_SIZE = PLOT_SETUP['TEXT FONT SIZE']
    COLORS = PLOT_SETUP['COLORS']
    LEGEND_SIZE = PLOT_SETUP['SIZE LEGEND']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']
    
    # Dataset
    DATA = DATASET['DATASET']
    DATA_NAMES = list(DATA.columns)
    DATA_NAMES = [i.upper() for i in DATA_NAMES]
    DATA.columns = DATA_NAMES
    ELEMENTS = list(DATA['CATEGORY'])
    VALUES = list(DATA['VALUES'])
    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.2f}%\n({:d})".format(pct, absolute)
        
    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), subplot_kw = dict(aspect = 'equal'))
    WEDGES, texts, autotexts = AX.pie(VALUES, autopct = lambda pct: func(pct, VALUES), textprops = dict(color = TEXT_COLOR), colors = COLORS)
    AX.legend(WEDGES, ELEMENTS, loc = 'center left', bbox_to_anchor = (1, 0.5), fontsize = LEGEND_SIZE)
    plt.setp(autotexts,  size = TEXT_FONT_SIZE, weight = 'bold')
    
    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)

def RADAR_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-6.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    RADAR_DIV_SIZE = PLOT_SETUP['TEXT SIZE']
    RADAR_DIV_COLOR = PLOT_SETUP['DIV COLOR']
    RADAR_COLOR = PLOT_SETUP['RADAR COLOR']
    OPACITY = PLOT_SETUP['OPACITY']
    POLAR_COLOR = PLOT_SETUP['BACKGROUND']
    SIZE_LEGEND = PLOT_SETUP['LEGEND SIZE']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']
    
    # Data
    DATA = DATASET['DATASET']
    DATA_NAMES = list(DATA.columns)
    DATA_NAMES = [i.lower() for i in DATA_NAMES]
    DATA.columns = DATA_NAMES
    Y = DATA.drop(['group'], axis = 1, inplace = False)
    MIN_VALUE = min(list(Y.min()))
    MAX_VALUE = max(list(Y.max()))
    N_DIV = 5
    INTERVAL = (MAX_VALUE - MIN_VALUE) / (N_DIV - 1)
    RADAR_DIV = [round(MIN_VALUE + i * INTERVAL, 0) for i in range(N_DIV)]
    RADAR_LABEL = [str(RADAR_DIV[i]) for i in range(len(RADAR_DIV))]

    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), subplot_kw = {'projection': 'polar'})
    CATEGORIES = list(DATA)[1:]
    N = len(CATEGORIES)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    AX.set_theta_offset(np.pi / 2)
    AX.set_theta_direction(-1)  
    plt.xticks(angles[:-1], CATEGORIES, size = RADAR_DIV_SIZE)  
    AX.set_rlabel_position(180 / N)
    angless = np.linspace(0, 2 * np.pi, N, endpoint = False).tolist()
    for label, anglee in zip(AX.get_xticklabels(), angless):
        if anglee in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < anglee < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    plt.yticks(RADAR_DIV, RADAR_LABEL, color = RADAR_DIV_COLOR, size = RADAR_DIV_SIZE)
    max_value = max(list(DATA.max())[1:])
    plt.ylim(0, max_value)
    for I in range(len(list(DATA['group']))):
        GROUP = list(DATA['group'])
        values=DATA.loc[I].drop('group').values.flatten().tolist()
        values += values[:1]
        AX.plot(angles, values, linewidth = 2, linestyle = '--', label = GROUP[I], c = RADAR_COLOR[I])
        AX.fill(angles, values, RADAR_COLOR[I], alpha = OPACITY)
    AX.set_facecolor(POLAR_COLOR)
    plt.legend(loc = 'upper right', bbox_to_anchor = (0.1, 0.1), prop = {'size': SIZE_LEGEND})

    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)

def HEATMAP_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-7.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    EXT = PLOT_SETUP['EXTENSION']
    DPI = PLOT_SETUP['DPI']
    ESCADA = PLOT_SETUP['MASK']
    LINE_WIDTHS = PLOT_SETUP['LINE WIDTHS']
    CMAP =  PLOT_SETUP['CMAP COLOR']
    LINE_COLOR = PLOT_SETUP['LINE COLOR']
    ANNOT =  PLOT_SETUP['ANNOT']
    ANNOT_SIZE_FONT = PLOT_SETUP['ANNOT SIZE FONT']
    ANNOT_FONT_WEIGHT = 'bold'

    # Dataset
    DATA = DATASET['DATASET']
    CORRELATIONS = DATA.corr()
    
    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), sharex = True)
    if ESCADA:
        MASK = np.triu(np.ones_like(CORRELATIONS))
    else:
        MASK = None  
    sns.heatmap(CORRELATIONS, center = 0, linewidths = LINE_WIDTHS, xticklabels = True,
                linecolor = LINE_COLOR, annot = ANNOT, vmin = -1, vmax = 1,
                annot_kws = {'fontsize': ANNOT_SIZE_FONT, 'fontweight': ANNOT_FONT_WEIGHT},
                cmap = CMAP, mask = MASK, ax = AX)
    plt.gca().invert_yaxis()
    AX.tick_params(axis = 'y', rotation = 0)   

    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)

def TREEMAP_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-8.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    WIDTH = PLOT_SETUP['WIDTH']
    HEIGHT = PLOT_SETUP['HEIGHT']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']
    COLORS = PLOT_SETUP['COLORS']
    LABELS = PLOT_SETUP['LABELS']
    TEXT_SIZE = PLOT_SETUP['LABEL SIZE']

    # Dataset and others information
    VALUES = DATASET['DATASET']['VALUES']

    
    # Plot
    W, H = CONVERT_SI_TO_INCHES(WIDTH, HEIGHT)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), sharex = True)
    PERCENTE = []
    for VALUE in VALUES:
        PERCENTE.append(round(VALUE * 100 / sum(VALUES), 2))
    LABELS_WITH_PERCENTE = []
    for i in range(len(VALUES)):
        LABELS_WITH_PERCENTE.append(LABELS[i] + '\n' + str(PERCENTE[i]) + '%')
    squarify.plot(sizes = VALUES, label = LABELS_WITH_PERCENTE, color = COLORS, ec = 'white', text_kwargs={'fontsize': TEXT_SIZE})
    AX.axis('off')

    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)
    
def REGPLOT_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-8.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    MARKER_SIZE = PLOT_SETUP['MARKER SIZE']
    MARKER_COLOR = PLOT_SETUP['MARKER COLOR']
    LINE_COLOR = PLOT_SETUP['LINE COLOR']
    OPACITY = PLOT_SETUP['OPACITY']
    Y_AXIS_LABEL = PLOT_SETUP['Y AXIS LABEL']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']  
    LABELS_COLOR = PLOT_SETUP['LABELS COLOR']
    AXISES_COLOR = PLOT_SETUP['AXISES COLOR']
    GRID = PLOT_SETUP['ON GRID?']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']

    # Data
    X = DATASET['X']
    Y = DATASET['Y']
    
    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), sharex = True, dpi = DPI)
    im = sns.regplot(x = X, y = Y,
            scatter_kws = {"color": MARKER_COLOR, "alpha": OPACITY, "s": MARKER_SIZE},
            line_kws = {"color": LINE_COLOR},
            ci = 99) # 99% level
    font = {'fontname': 'DejaVu Sans',
            'color':  LABELS_COLOR,
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX.set_ylabel(Y_AXIS_LABEL, fontdict = font)
    AX.set_xlabel(X_AXIS_LABEL, fontdict = font)   
    AX.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = AXISES_COLOR, labelrotation = 0, direction = 'out', which = 'both', length = 10)
    AX.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = AXISES_COLOR)
    if GRID == True:
        AX.grid(color = 'grey', linestyle = '-.', linewidth = 1, alpha = 0.20)

    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)

def JOIN_HIST_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-9.html
    """

    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    WIDTH = PLOT_SETUP['WIDTH']
    HEIGHT = PLOT_SETUP['HEIGHT']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    X_AXIS_COLOR = PLOT_SETUP['X AXIS COLOR']
    OVERLAP = 0
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']
    
    # Dataset
    DATA = DATASET['DATASET']
    DATA_NAMES = list(DATA.columns)
    DATA_NAMES = [i.upper() for i in DATA_NAMES]
    DATA.columns = DATA_NAMES
    
    # Plot
    W, H = CONVERT_SI_TO_INCHES(WIDTH, HEIGHT)
    FIG, AX = joypy.joyplot(DATA, overlap = OVERLAP)
    plt.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = X_AXIS_COLOR)
    plt.tick_params(axis = 'y', labelsize = X_AXIS_SIZE, colors = X_AXIS_COLOR)
    
    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)
   
def MULTIPLE_LINES_CHART(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-2.html
    """
    
    # Setup
    DATASET = kwargs.get('DATASET')
    PLOT_SETUP = kwargs.get('PLOT_SETUP')
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    EXT = PLOT_SETUP['EXTENSION']
    DPI = PLOT_SETUP['DPI']
    MARKER = PLOT_SETUP['MARKER']
    MARKER_SIZE = PLOT_SETUP['MARKER SIZE']
    LINE_WIDTH = PLOT_SETUP['LINE WIDTH']
    LINE_STYLE = PLOT_SETUP['LINE STYLE']
    Y0_AXIS_LABEL = PLOT_SETUP['Y0 AXIS LABEL']
    Y1_AXIS_LABEL = PLOT_SETUP['Y1 AXIS LABEL']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']     
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    COLORS = PLOT_SETUP['CHART COLOR']
    GRID = PLOT_SETUP['ON GRID?']
    YLOGSCALE = PLOT_SETUP['Y LOG']
    XLOGSCALE = PLOT_SETUP['X LOG']
    LEGEND = PLOT_SETUP['LEGEND']
    LOC = PLOT_SETUP['LOC LEGEND']
    SIZE_LEGEND = PLOT_SETUP['SIZE LEGEND']
    
    # Dataset and others information
    DATA = DATASET['DATASET']
    DATA_NAMES = list(DATA.columns)
    DATA_NAMES = [i.upper() for i in DATA_NAMES]
    DATA.columns = DATA_NAMES
    X = list(DATA['X'])
    Y = DATA.drop(['X'], axis = 1, inplace = False)
    
    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), sharex = True)
    AX.plot(X, Y['Y0'], marker = MARKER[0],  linestyle = LINE_STYLE[0], linewidth = LINE_WIDTH, markersize = MARKER_SIZE, label = LEGEND[0], color = COLORS[0])
            
    if YLOGSCALE:
        AX.semilogy()
    if XLOGSCALE:
        AX.semilogx()
    fontx = {'fontname': 'DejaVu Sans',
            'color':  '#000000',
            'weight': 'normal',
            'size': LABELS_SIZE}
    fonty0 = {'fontname': 'DejaVu Sans',
            'color':  COLORS[0],
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX.set_xlabel(X_AXIS_LABEL, fontdict = fontx)  
    AX.set_ylabel(Y0_AXIS_LABEL, fontdict = fonty0)
    AX.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = '#000000')
    AX.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = COLORS[0])
    plt.legend(loc = LOC, prop = {'size': SIZE_LEGEND})
    AX2 = AX.twinx()
    fonty1 = {'fontname': 'DejaVu Sans',
            'color':  COLORS[1],
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX2.set_ylabel(Y1_AXIS_LABEL, fontdict = fonty1)
    AX2.plot(X, Y['Y1'], marker = MARKER[1],  linestyle = LINE_STYLE[1], linewidth = LINE_WIDTH, markersize = MARKER_SIZE, label = LEGEND[1], color = COLORS[1])
    AX2.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, labelcolor = COLORS[1])
    if GRID == True:
        AX.grid(color = 'grey', linestyle = '-.', linewidth = 1, alpha = 0.20)
    h1, l1 = AX.get_legend_handles_labels()
    h2, l2 = AX2.get_legend_handles_labels()
    plt.legend(h1+h2, l1+l2, loc = LOC, prop = {'size': SIZE_LEGEND})
    
    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)

def SCATTER_LINE_PLOT(DATASET, PLOT_SETUP):    
    """
    """

    # Setup
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    MARKER_SIZE = PLOT_SETUP['MARKER SIZE']
    CMAP = PLOT_SETUP['CMAP COLOR']
    Y_AXIS_LABEL = PLOT_SETUP['Y AXIS LABEL']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']  
    LABELS_COLOR = PLOT_SETUP['LABELS COLOR']
    LINE_COLOR = PLOT_SETUP['LINE COLOR']
    AXISES_COLOR = PLOT_SETUP['AXISES COLOR']
    GRID = PLOT_SETUP['ON GRID?']
    YLOGSCALE = PLOT_SETUP['Y LOG']
    XLOGSCALE = PLOT_SETUP['X LOG']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']

    # Data
    X = DATASET['X']
    Y = DATASET['Y']
    Z = DATASET['Z']

    LX = DATASET['LX']
    LY1 = DATASET['LY1']
    LY2 = DATASET['LY2']   

    # Plot
    W, H = CONVERT_SI_TO_INCHES(W, H)
    FIG, AX = plt.subplots(1, 1, figsize = (W, H), sharex = True)
    im = AX.scatter(X, Y, c = Z, marker = 'o', s = MARKER_SIZE , cmap = CMAP)
    
    AX.plot(LX, LY1, color=LINE_COLOR)
    AX.tick_params(axis='y', labelcolor=LINE_COLOR)

    AX1 = AX.twinx()

    AX1.plot(LX, [0, 50, 75, 100], LINE_COLOR)
    AX1.tick_params(axis='y', labelcolor=LINE_COLOR)
    
    
    
    
    
    colorbar = plt.colorbar(im)
    if YLOGSCALE:
        AX.semilogy()
    if XLOGSCALE:
        AX.semilogx()
    font = {'fontname': 'DejaVu Sans',
            'color':  LABELS_COLOR,
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX.set_ylabel(Y_AXIS_LABEL, fontdict = font)
    AX.set_xlabel(X_AXIS_LABEL, fontdict = font)   
    AX.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = AXISES_COLOR, labelrotation = 0, direction = 'out', which = 'both', length = 10)
    AX.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = AXISES_COLOR)
    if GRID == True:
        AX.grid(color = 'grey', linestyle = '-.', linewidth = 1, alpha = 0.20)
    SAVE_GRAPHIC(NAME, EXT, DPI)

def CONTOUR_CHART(DATASET, PLOT_SETUP):    
    
    # Setup
    NAME = PLOT_SETUP['NAME']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']
    TITLE = PLOT_SETUP['TITLE']
    LEVELS = PLOT_SETUP['LEVELS']
    
    # Data
    X = DATASET['X']
    Y = DATASET['Y']
    Z = DATASET['Z']

    # Filled contour
    fig, ax = plt.subplots()
    cnt = ax.contourf(X, Y, Z, levels = LEVELS)

    # Color bar
    cbar = ax.figure.colorbar(cnt, ax = ax)
    cbar.ax.set_ylabel(TITLE, rotation = -90, va = "bottom")

    SAVE_GRAPHIC(NAME, EXT, DPI)
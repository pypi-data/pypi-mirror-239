"""
_colors.py stores functions to create color palettes.
"""

import seaborn as sns

##


ten_godisnot = [
    '#001E09', '#885578', '#FF913F', '#1CE6FF', 
    '#549E79', '#C9E850', '#EEC3FF', '#FFEF00',
    '#D157A0', '#922329' 
]

scanpy_100 = [

    '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46', 
    '#008941', '#006FA6', '#A30059', '#FFDBE5', 
    '#7A4900', '#0000A6', '#63FFAC', '#B79762', 
    '#004D43', '#8FB0FF', '#997D87', '#5A0007', 
    '#809693', '#6A3A4C', '#1B4400', '#4FC601', 
    '#3B5DFF', '#4A3B53', '#FF2F80', '#61615A', 
    '#BA0900', '#6B7900', '#00C2A0', '#FFAA92', 
    '#FF90C9', '#B903AA', '#D16100', '#DDEFFF', 
    '#000035', '#7B4F4B', '#A1C299', '#300018',
    '#013349', '#00846F', '#372101', '#FFB500', 
    '#C2FFED', '#A079BF', '#CC0744', '#C0B9B2', 
    '#C2FF99', '#001E09', '#00489C', '#6F0062', 
    '#0CBD66', '#EEC3FF', '#456D75', '#B77B68', 
    '#7A87A1', '#788D66', '#885578', '#FAD09F', 
    '#FF8A9A', '#D157A0', '#BEC459', '#456648', 
    '#0086ED', '#886F4C', '#34362D', '#B4A8BD', 
    '#00A6AA', '#452C2C', '#636375', '#A3C8C9', 
    '#FF913F', '#938A81', '#575329', '#00FECF', 
    '#B05B6F', '#8CD0FF', '#3B9700', '#04F757', 
    '#C8A1A1', '#1E6E00', '#7900D7', '#A77500', 
    '#6367A9', '#A05837', '#6B002C', '#772600', 
    '#D790FF', '#9B9700', '#549E79', '#FFF69F', 
    '#201625', '#72418F', '#BC23FF', '#99ADC0', 
    '#3A2465', '#922329', '#5B4534', '#FDE8DC', 
    '#404E55', '#0089A3', '#CB7E98', '#A4E804', 
    '#324E72', '#0AA6D8'

]

scanpy_20 = [

    '#1f77b4', '#ff7f0e', '#279e68', '#d62728', 
    '#aa40fc', '#8c564b', '#e377c2', '#b5bd61', 
    '#17becf', '#aec7e8', '#ffbb78', '#98df8a', 
    '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', 
    '#dbdb8d', '#9edae5', '#ad494a', '#8c6d31'
    
]


##


def create_palette(df, var, palette=None, col_list=None):
    """
    Create a color palette from a df, a columns, a palette or a list of colors.
    """
    try:
        cats = df[var].cat.categories
    except:
        cats = df[var].unique()
    n = len(cats)
    if col_list is not None:
        cols = col_list[:n]
    elif palette is not None:
        cols = sns.color_palette(palette, n_colors=n)
    else:
        raise ValueError('Provide one between palette and col_list!')
    colors = { k: v for k, v in zip(cats, cols)}
    return colors


##
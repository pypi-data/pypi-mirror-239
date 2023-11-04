"""
_plotting.py stores heatmap and slightly more elaborate plots. Ongoing effort.
"""

from ._colors import *
from ._plotting_base import *
plt.style.use('default')


##


def plot_clustermap(df, row_colors=None, palette='mako', title=None, label=None,
    row_names=True, col_names=False, no_cluster=False, figsize=(11, 10), annot=False, 
    annot_size=5, colors_ratio=0.5
    ):
    '''
    Clustered heatmap.
    '''
    if no_cluster:
       row_cluster=False; col_cluster=False
    else:
        row_cluster=True; col_cluster=True

    fig = sns.clustermap(df, cmap=palette, yticklabels=row_names, xticklabels=col_names, 
        dendrogram_ratio=(.1, .04), figsize=figsize, row_cluster=row_cluster, col_cluster=col_cluster, 
        annot=True, cbar_kws={'use_gridspec' : False, 'orientation': 'horizontal'}, 
        colors_ratio=colors_ratio, annot_kws={'size':annot_size}, row_colors=row_colors
    )
    fig.ax_col_dendrogram.set_visible(False) 
    fig.fig.subplots_adjust(bottom=0.1)
    fig.fig.suptitle(title)
    fig.ax_cbar.set_position((0.098, 0.05, 0.75, 0.02))
    fig.ax_cbar.set(xlabel=label)

    return fig

    # IMPORTANTTT!!
    # handles = create_handles(v, colors=colors.values())
    # fig.fig.subplots_adjust(left=0.2)
    # fig.fig.legend(handles, v, loc='lower center', bbox_to_anchor=(0.12, 0.5), ncol=1, frameon=False)
    # fig.ax_cbar.set_position((0.325, 0.05, 0.5, 0.02))
    # plt.show()


## 


def plot_heatmap(df, palette='mako', ax=None, title=None, x_names=True, 
    y_names=True, x_names_size=7, y_names_size=7, xlabel=None, ylabel=None, 
    annot=False, annot_size=5, label=None, shrink=1.0, cb=True):
    """
    Heatmap.
    """
    ax = sns.heatmap(data=df, ax=ax, robust=True, cmap=palette, annot=annot, xticklabels=x_names, 
        yticklabels=y_names, fmt='.2f', annot_kws={'size':annot_size}, cbar=cb,
        cbar_kws={'fraction':0.05, 'aspect':35, 'pad': 0.02, 'shrink':shrink, 'label':label}
    )
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=x_names_size)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=y_names_size)

    return ax


##


def plot_consensus_heatmap(X, row_colors, ax=None):
    """
    Utils to plot the consensus heatmap.
    """
    im = ax.imshow(X, cmap='mako', interpolation='nearest', vmax=.9, vmin=.2)

    orientation = 'vertical'
    pos, xticks_position = ((1.05, 0.25, 0.025, 0.5), 'right')
    cmap = matplotlib.colormaps['mako']
    norm = matplotlib.colors.Normalize(vmin=.2, vmax=.9)
    axins = ax.inset_axes(pos) 
    cb = plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), 
        cax=axins, orientation=orientation, ticklocation=xticks_position
    )
    cb.set_label(label='Support', size=7, loc='center')
    cb.ax.tick_params(axis="y", labelsize=5)

    ax.set(
        title=f'Consensus matrix: average support {X.mean():.2f}', 
        xlabel='Cells', xticks=[], yticks=[]
    )
    ax.set_ylabel(ylabel='Cells', labelpad=10)

    orientation = 'vertical'
    pos = (-.028, 0, 0.025, 1)
    axins = ax.inset_axes(pos) 
    cmap = matplotlib.colors.ListedColormap(row_colors)
    cb = plt.colorbar(
        matplotlib.cm.ScalarMappable(cmap=cmap), 
        cax=axins, orientation=orientation
    )
    cb.ax.set(xticks=[], yticks=[])

    return ax


##
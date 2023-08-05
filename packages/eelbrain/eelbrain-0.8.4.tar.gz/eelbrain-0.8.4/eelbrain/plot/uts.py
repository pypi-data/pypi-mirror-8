'''
Plot uniform time-series of one variable.
'''
# author: Christian Brodbeck
from __future__ import division

import numpy as np
import scipy.stats
import matplotlib.cm as _cm

from .._data_obj import ascategorial, asndvar, cellname, Celltable
from . import _base


class UTSStat(_base._EelFigure):
    "Plots statistics for a one-dimensional NDVar"
    def __init__(self, Y='Y', X=None, Xax=None, match=None, sub=None, ds=None,
                 main=np.mean, dev=scipy.stats.sem, legend='upper right',
                 title=None, axtitle='{name}', xlabel=True, ylabel=True,
                 invy=False, bottom=None, top=None, hline=None, xdim='time',
                 xlim=None, color='b', colors='jet', clusters=None,
                 frame=True, **layout):
        """
    Plot statistics for a one-dimensional NDVar

    Parameters
    ----------
    Y : 1d-NDVar
        Dependent variable (one-dimensional NDVar).
    X : categorial or None
        Model: specification of conditions which should be plotted separately.
    Xax : None | categorial
        Make separate axes for each category in this categorial model.
    match : Factor
        Identifier for repeated measures data.
    sub : None | index array
        Only use a subset of the data provided.
    ds : None | Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables.
    main : func | None
        Measure for the central tendency (function that takes an ``axis``
        argument). The default is numpy.mean.
    dev : func | 'all' | float
        Measure for spread / deviation from the central tendency. Either a
        function that takes an ``axis`` argument, 'all' to plot all traces, or
        a float to plot all traces with a certain alpha value. The default is
        numpy.stats.sem which plots the standard error of the mean.
    legend : str | None
        matplotlib figure legend location argument
    title : str | None
        Figure title; '{name}' will be formatted to ``Y.name``
    axtitle : str | None
        Axes title. '{name}' is formatted to the category name.
    xlabel, ylabel : True |str | None
        X- and y axis label. If True the labels will be inferred from the data.
    invy : bool
        invert the y axis
    bottom, top | None | scalar
        Set an absolute range for the plot's y axis.
    hline : None | scalar | (value, kwarg-dict) tuple
        Add a horizontal line to each plot. If provided as a tuple, the second
        element can include any keyword arguments that should be submitted to
        the call to matplotlib axhline call.
    xdim : str
        dimension for the x-axis (default is 'time')
    xlim : None | (scalar, scalar)
        Tuple of xmin and xmax to set the initial x-axis limits.
    color : matplotlib color
        Color if just a single category of data is plotted.
    colors : str | list | dict
        Colors for the plots if multiple categories of data are plotted.
        **str**: A colormap name; Cells of X are mapped onto the colormap in
        regular intervals.
        **list**: A list of colors in the same sequence as X.cells.
        **dict**: A dictionary mapping each cell in X to a color.
        Colors are specified as `matplotlib compatible color arguments
        <http://matplotlib.org/api/colors_api.html>`_.
    clusters : None | Dataset
        Clusters to add to the plots. The clusters should be provided as
        Dataset, as stored in test results' :py:attr:`.clusters`.
    frame : bool
        Draw a frame containing the figure from the top and the right (default
        ``True``).
        """
        if Xax is None:
            nax = 1
            ct = Celltable(Y, X, sub=sub, match=match, ds=ds, coercion=asndvar)
            if X is None:
                cells = None
            else:
                cells = ct.X.cells
        else:
            ct = Celltable(Y, Xax, sub=sub, ds=ds, coercion=asndvar)
            if X is None:
                cells = None
                X_ = None
            else:
                Xct = Celltable(X, Xax, sub=sub, ds=ds, coercion=ascategorial)
                cells = Xct.Y.cells
            if match is not None:
                matchct = Celltable(match, Xax, sub=sub, ds=ds,
                                    coercion=ascategorial)
            nax = len(ct.cells)

        # assemble colors
        if cells is None:
            colors = {None: color}
        else:
            if isinstance(colors, (list, tuple)):
                if len(colors) < len(cells):
                    err = ("The `colors` argument %s does not supply enough "
                           "colors (%i) for %i "
                           "cells." % (str(colors), len(colors), len(cells)))
                    raise ValueError(err)
                colors = dict(zip(cells, colors))
            elif isinstance(colors, dict):
                for cell in cells:
                    if cell not in colors:
                        raise KeyError("%s not in colors" % repr(cell))
            else:
                cm = _cm.get_cmap(colors)
                N = len(cells)
                colors = {cell: cm(i / N) for i, cell in enumerate(cells)}

        kwargs = dict(dev=dev, main=main, ylabel=ylabel, xdim=xdim,
                      invy=invy, bottom=bottom, top=top, hline=hline,
                      xlabel=xlabel, xlim=xlim, frame=frame)

        if title is not None and '{name}' in title:
            title = title.format(name=ct.Y.name)
        super(UTSStat, self).__init__("UTSStat Plot", nax, layout,
                                      figtitle=title)

        self._plots = []
        self._legend_handles = {}
        if Xax is None:
            ax = self._axes[0]
            if axtitle and '{name}' in axtitle:
                title_ = axtitle.format(name=ct.Y.name)
            else:
                title_ = axtitle
            p = _ax_stat(ax, ct, colors, title=title_, **kwargs)
            self._plots.append(p)
            self._legend_handles.update(p.legend_handles)
            if len(ct) < 2:
                legend = False
        else:
            for i, ax, cell in zip(xrange(nax), self._axes, ct.cells):
                kwargs['xlabel'] = xlabel if i == len(ct) - 1 else False
                if X is not None:
                    X_ = Xct.data[cell]
                if match is not None:
                    match = matchct.data[cell]
                cct = Celltable(ct.data[cell], X_, match=match,
                                coercion=asndvar)
                title_ = axtitle.format(name=cellname(cell))
                p = _ax_stat(ax, cct, colors, title=title_, **kwargs)
                self._plots.append(p)
                self._legend_handles.update(p.legend_handles)

        self.plot_legend(legend)

        # prepare cluster plots
        self._clusters = [None] * nax
        self._clusters_all_same = True
        if clusters is not None:
            self.set_clusters(clusters)

        self._show()

    def _fill_toolbar(self, tb):
        import wx

        btn = self._cluster_btn = wx.Button(tb, wx.ID_ABOUT, "Clusters")
        btn.Enable(False)
        tb.AddControl(btn)
        btn.Bind(wx.EVT_BUTTON, self._OnShowClusterInfo)

    def _OnShowClusterInfo(self, event):
        from ..._wxutils import show_text_dialog
        if self._clusters_all_same:
            info = str(self._clusters)
        else:
            info = []
            for i, clusters in enumerate(self._clusters):
                if clusters is None:
                    continue
                title = "Axes %i" % i
                info.append(title)
                info.append('\n')
                info.append('-' * len(title))
                info.append(str(clusters))
            info = '\n'.join(info)

        show_text_dialog(self._frame, info, "Clusters")

    def plot_legend(self, loc='fig', figsize=(2, 2)):
        """Plots (or removes) the legend from the figure.

        Parameters
        ----------
        loc : False | 'fig' | str | int
            Where to plot the legend (see Notes; default 'fig').
        figsize : tuple of 2 int
            Figure size if plotting to figure (i.e., loc == 'fig').

        Returns
        -------
        legend_figure : None | legend
            If loc=='fig' the Figure, otherwise None.

        Notes
        -----
        legend content can be modified through the figure's
        ``legend_handles`` and ``legend_labels`` attributes.

        Possible values for the ``loc`` argument:

        ``False``:
            Make the current legend invisible
        'fig':
            Plot the legend in a new figure
        str | int:
            Matplotlib position argument: plot the legend on the figure


        Matplotlib Position Arguments:

         - 'upper right'  : 1,
         - 'upper left'   : 2,
         - 'lower left'   : 3,
         - 'lower right'  : 4,
         - 'right'        : 5,
         - 'center left'  : 6,
         - 'center right' : 7,
         - 'lower center' : 8,
         - 'upper center' : 9,
         - 'center'       : 10,
        """
        if loc and len(self._legend_handles) > 1:
            cells = sorted(self._legend_handles)
            labels = [cellname(cell) for cell in cells]
            handles = [self._legend_handles[cell] for cell in cells]
            if loc == 'fig':
                return _base.legend(handles, labels, figsize=figsize)
            else:
                # take care of old legend; remove() not implemented as of mpl 1.3
                if hasattr(self, 'legend'):
                    self.legend.set_visible(False)
                self.legend = self.figure.legend(handles, labels, loc=loc)
                self.draw()
        else:
            if hasattr(self, 'legend'):
                self.legend.set_visible(False)
                del self.legend
                self.draw()

    def set_clusters(self, clusters, pmax=0.05, ptrend=0.1, color='.7', ax=None):
        """Add clusters from a cluster test to the plot (as shaded area).

        Parameters
        ----------
        clusters : None | Dataset
            The clusters, as stored in test results' :py:attr:`.clusters`.
            Use ``None`` to remove the clusters plotted on a given axis.
        pmax : scalar
            Maximum p-value of clusters to plot as solid.
        ptrend : scalar
            Maximum p-value of clusters to plot as trend.
        color : matplotlib color
            Color for the clusters.
        ax : None | int
            Index of the axes to which the clusters are to be added. If None,
            add the clusters to all axes.
        """
        nax = len(self._axes)
        if ax is None:
            self._clusters_all_same = True
            self._clusters = clusters
            axes = xrange(nax)
        else:
            if self._clusters_all_same:
                self._clusters = [self._clusters] * nax
                self._clusters_all_same = False
            self._clusters[ax] = clusters
            axes = [ax]

        # update plots
        for ax in axes:
            p = self._plots[ax].cluster_plt
            p.set_clusters(clusters, False)
            p.set_color(color, False)
            p.set_pmax(pmax, ptrend)
        self.draw()

        # update GUI
        if hasattr(self, '_cluster_btn'):
            if clusters is not None:
                self._cluster_btn.Enable(True)
            elif self._clusters_all_same or all(c is None for c in self._clusters):
                self._cluster_btn.Enable(False)

    def set_xlim(self, xmin, xmax):
        """Adjust the x-axis limits on all axes
        """
        for ax in self._axes:
            ax.set_xlim(xmin, xmax)
        self.draw()

    def set_ylim(self, bottom=None, top=None):
        """
        Adjust the y-axis limits on all axes (see matplotlib's
        :py:meth:`axes.set_ylim`)

        """
        for ax in self._axes:
            ax.set_ylim(bottom, top)

        self.draw()



class UTS(_base._EelFigure):
    "Value by time plot for UTS data."
    def __init__(self, epochs, Xax=None, title=None, axtitle='{name}', ds=None,
                 **layout):
        """Value by time plot for UTS data

        Parameters
        ----------
        epochs : epochs
            Uts data epochs to plot.
        Xax : None | categorial
            Make separate axes for each category in this categorial model.
        title : None | str
            Figure title.
        axtitle : None | str
            Axes title. '{name}' is formatted to the category name.
        ds : None | Dataset
            If a Dataset is specified, all data-objects can be specified as
            names of Dataset variables.
        """
        epochs = self.epochs = _base.unpack_epochs_arg(epochs, 1, Xax, ds)
        super(UTS, self).__init__("UTS", len(epochs), layout, 1.5, 2,
                                  figtitle=title)

        for ax, epoch in zip(self._axes, epochs):
            _ax_uts(ax, epoch, title=axtitle)

        self._show()


class _ax_stat:
    def __init__(self, ax, ct, colors, dev=scipy.stats.sem,
                 main=np.mean, title=True, ylabel=True, xdim='time', xlim=None,
                 xlabel=True, invy=False, bottom=None, top=None, hline=None,
                 clusters=None, pmax=0.05, ptrend=0.1, frame=True):
        ax.x_fmt = "t = %.3f s"

        # stat plots
        self.stat_plots = []
        self.legend_handles = {}

        x = ct.Y.get_dim(xdim)
        for cell in ct.cells:
            cell_label = cellname(cell)
            c = colors[cell]
            ndvar = ct.data[cell]
            y = ndvar.get_data(('case', xdim))
            plt = _plt_stat(ax, x, y, main, dev, label=cell_label, color=c)
            self.stat_plots.append(plt)
            if plt.main is not None:
                self.legend_handles[cell] = plt.main[0]

        # hline
        if hline is not None:
            if isinstance(hline, tuple):
                if len(hline) != 2:
                    raise ValueError("hline must be None, scalar or length 2 tuple")
                hline, hline_kw = hline
                hline_kw = dict(hline_kw)
            else:
                hline_kw = {'color': 'k'}

            hline = float(hline)
            ax.axhline(hline, **hline_kw)

        # cluster plot
        self.cluster_plt = _plt_uts_clusters(ax, clusters, pmax, ptrend)

        # title
        if title:
            if title is True:
                title = ct.Y.name
            ax.set_title(title)

        # format x axis
        ax.set_xlim(x[0], x[-1])
        ax.x_fmt = "t = %.3f s"
        ticks = ax.xaxis.get_ticklocs()
        ticklabels = _base._ticklabels(ticks, 'time')
        ax.xaxis.set_ticklabels(ticklabels)

        _base.set_xlabel(ax, xdim, xlabel)

        if ylabel is True:
            ylabel = ct.Y.info.get('unit', None)
        if ylabel:
            ax.set_ylabel(ylabel)

        if invy:
            y0, y1 = ax.get_ylim()
            bottom = bottom if (bottom is not None) else y1
            top = top if (top is not None) else y0
        if (bottom is not None) or (top is not None):
            ax.set_ylim(bottom, top)

        if xlim is None:
            xlim = (min(x), max(x))
        xmin, xmax = xlim
        ax.set_xlim(xmin, xmax)

        if not frame:
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')

        # store attributes
        self.ax = ax
        self.title = title


class UTSClusters(_base._EelFigure):
    "Plotting of ANOVA permutation cluster test results"
    def __init__(self, res, pmax=0.05, ptrend=0.1, title=None,
                 axtitle='{name}', cm='jet', overlay=False, **layout):
        """
        Plotting of permutation cluster test results

        Parameters
        ----------
        res : testnd.anova
            ANOVA with permutation cluster test result object.
        pmax : scalar
            Maximum p-value of clusters to plot as solid.
        ptrend : scalar
            Maximum p-value of clusters to plot as trend.
        title : str
            Figure title.
        axtitle : None | str
            Axes title pattern. '{name}' is formatted to the effect name.
        cm : str
            Colormap to use for coloring different effects.
        overlay : bool
            Plot epochs (time course for different effects) on top of each
            other (as opposed to on separate axes).
        """
        clusters_ = res.clusters

        epochs = self.epochs = _base.unpack_epochs_arg(res, 1)
        cm = _cm.get_cmap(cm)

        # create figure
        N = len(epochs)
        nax = 1 if overlay else N
        super(UTSClusters, self).__init__("UTSClusters", nax, layout,
                                          figtitle=title)

        ylabel = True
        self._caxes = []
        if overlay:
            ax = self._axes[0]
            axtitle = None
        for i, layers in enumerate(epochs):
            if not overlay:
                ax = self._axes[i]

            color = cm(i / N)
            stat = layers[0]

            # ax clusters
            if clusters_:
                if 'effect' in clusters_:
                    cs = clusters_.sub('effect == %r' % layers[0].name)
                else:
                    cs = clusters_
            else:
                cs = None

            cax = _ax_uts_clusters(ax, stat, cs, color, pmax, ptrend, 'time',
                                   axtitle, ylabel)
            self._caxes.append(cax)
            ylabel = None

        self.clusters = clusters_
        self._show()

    def _fill_toolbar(self, tb):
        import wx

        btn = wx.Button(tb, wx.ID_ABOUT, "Clusters")
        tb.AddControl(btn)
        btn.Bind(wx.EVT_BUTTON, self._OnShowClusterInfo)

    def _OnShowClusterInfo(self, event):
        from ..._wxutils import show_text_dialog
        info = str(self.clusters)
        show_text_dialog(self._frame, info, "Clusters")

    def set_pmax(self, pmax=0.05, ptrend=0.1):
        "set the threshold p-value for clusters to be displayed"
        for cax in self._caxes:
            cax.set_pmax(pmax, ptrend)
        self.draw()


def _ax_uts(ax, layers, title=False, bottom=None, top=None, invy=False,
            xlabel=True, ylabel=True, color=None, xdim='time'):
    contours = {}
    overlay = False
    for l in layers:
        args = _base.find_uts_args(l, overlay, color)
        overlay = True
        if args is None:
            continue

        _plt_uts(ax, l, xdim=xdim, **args)
        contours = l.info.get('contours', None)
        if contours:
            for v, color in contours.iteritems():
                if v in contours:
                    continue
                contours[v] = ax.axhline(v, color=color)

    l0 = layers[0]
    x = l0.get_dim(xdim)
    ax.set_xlim(x[0], x[-1])
    ax.x_fmt = "t = %.3f s"

    ticks = ax.xaxis.get_ticklocs()
    ticklabels = _base._ticklabels(ticks, 'time')
    ax.xaxis.set_ticklabels(ticklabels)

    if title:
        if 'name' in title:
            title = title.format(name=l0.name)
        ax.set_title(title)

    _base.set_xlabel(ax, xdim, xlabel)

    if ylabel is True:
        ylabel = l.info.get('unit', None)
    if ylabel:
        ax.set_ylabel(ylabel)

    if invy:
        y0, y1 = ax.get_ylim()
        bottom = bottom if (bottom is not None) else y1
        top = top if (top is not None) else y0
    if (bottom is not None) or (top is not None):
        ax.set_ylim(bottom, top)


def _plt_uts(ax, ndvar, color=None, xdim='time', kwargs={}):
    y = ndvar.get_data((xdim,))
    x = ndvar.get_dim(xdim).x
    if color is not None:
        kwargs['color'] = color
    ax.plot(x, y, **kwargs)

    for y, kwa in _base.find_uts_hlines(ndvar):
        if color is not None:
            kwa['color'] = color
        ax.axhline(y, **kwa)


class _ax_uts_clusters:
    def __init__(self, ax, Y, clusters, color=None, pmax=0.05, ptrend=0.1,
                 xdim='time', title=None, xlabel=True, ylabel=True):
        uts_args = _base.find_uts_args(Y, False, color)
        self._bottom, self._top = _base.find_vlim_args(Y)

        if title:
            if '{name}' in title:
                title = title.format(name=Y.name)
            ax.set_title(title)

        _plt_uts(ax, Y, xdim=xdim, **uts_args)

        if ylabel is True:
            ylabel = Y.info.get('meas', _base.default_meas)
        if ylabel:
            ax.set_ylabel(ylabel)

        xlabel = _base._axlabel(xdim, xlabel)
        if xlabel:
            ax.set_xlabel(xlabel)
        if np.any(Y.x < 0) and np.any(Y.x > 0):
            ax.axhline(0, color='k')


        # pmap
        self.cluster_plt = _plt_uts_clusters(ax, clusters, pmax, ptrend, color)

        # save ax attr
        self.ax = ax
        x = Y.get_dim(xdim).x
        self.xlim = (x[0], x[-1])

        ax.set_xlim(*self.xlim)
        ax.set_ylim(bottom=self._bottom, top=self._top)

    def set_clusters(self, clusters):
        self.cluster_plt.set_clusters(clusters)

    def set_pmax(self, pmax=0.05, ptrend=0.1):
        self.cluster_plt.set_pmax(pmax, ptrend)


class _plt_uts_clusters:
    def __init__(self, ax, clusters, pmax, ptrend, color=None, hatch='/'):
        """
        clusters : Dataset
            Dataset with entries for 'tstart', 'tstop' and 'p'.
        """
        self.pmax = pmax
        self.ptrend = ptrend
        self.h = []
        self.ax = ax
        self.clusters = clusters
        self.color = color
        self.hatch = hatch
        self.update()

    def set_clusters(self, clusters, update=True):
        self.clusters = clusters
        if update:
            self.update()

    def set_color(self, color, update=True):
        self.color = color
        if update:
            self.update()

    def set_pmax(self, pmax, ptrend, update=True):
        self.pmax = pmax
        self.ptrend = ptrend
        if update:
            self.update()

    def update(self):
        h = self.h
        while len(h):
            h.pop().remove()

        clusters = self.clusters
        if clusters is None:
            return

        p_include = self.ptrend or self.pmax
        for cluster in clusters.itercases():
            if 'p' in cluster:
                p = cluster['p']
                if p > p_include:
                    continue
                alpha = 0.5 if p < self.pmax else 0.2
            else:
                alpha = 0.5

            x0 = cluster['tstart']
            x1 = cluster['tstop']
            h = self.ax.axvspan(x0, x1, color=self.color,  # , hatch=self.hatch,
                                fill=True, alpha=alpha, zorder=-1)
            self.h.append(h)


class _plt_stat(object):
    def __init__(self, ax, x, y, main, dev, label=None, color=None, **kwargs):
        if color:
            kwargs['color'] = color

        main_kwargs = kwargs.copy()
        dev_kwargs = kwargs.copy()
        if label:
            main_kwargs['label'] = label

        if isinstance(dev, basestring):
            if dev == 'all':
                dev_kwargs['alpha'] = .3
            else:
                err = ("The only possible str value for dev is 'all'; got "
                       "%r." % dev)
                raise ValueError(err)
        elif np.isscalar(dev):
            dev_kwargs['alpha'] = dev
            dev = 'all'
        else:
            dev_kwargs['alpha'] = .3

        if dev == 'all':
            if 'linewidth' in kwargs:
                main_kwargs['linewidth'] = kwargs['linewidth'] * 2
            elif 'lw' in kwargs:
                main_kwargs['lw'] = kwargs['lw'] * 2
            else:
                main_kwargs['lw'] = 2

        # plot main
        if hasattr(main, '__call__'):
            y_ct = main(y, axis=0)
            self.main = ax.plot(x, y_ct, zorder=5, **main_kwargs)
        elif dev == 'all':
            self.main = None
        else:
            raise ValueError("Invalid argument: main=%r" % main)

        # plot dev
        if hasattr(dev, '__call__'):
            ydev = dev(y, axis=0)
            self.dev = ax.fill_between(x, y_ct - ydev, y_ct + ydev, zorder=0, **dev_kwargs)
        elif dev == 'all':
            self.dev = ax.plot(x, y.T, **dev_kwargs)
        else:
            self.dev = None

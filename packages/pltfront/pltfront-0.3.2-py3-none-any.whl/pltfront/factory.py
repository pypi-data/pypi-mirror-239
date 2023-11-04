import inspect as ins

import numpy as np
import matplotlib.pyplot as plt


class PlotFactory:
    """
    Plot object factory
    """

    def __init__(self, x, y, xerr=None, yerr=None, label=None, kind='line', ax=None):
        # Initialize vars
        self.x = x
        self.y = y
        self.x_err = xerr
        self.y_err = yerr
        self.label = label

        # Axes handling
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax

        # Available plot functions
        self._plots_db = {'scatter': self.ax.scatter, 'line': self.ax.plot,
                          'semilogx': self.ax.semilogx, 'semilogy': self.ax.semilogy, 'loglog': self.ax.loglog}
        self.available_plots = list(self._plots_db.keys())

        # Plot kind handling
        if kind in self._plots_db.keys():
            self._plot = self._plots_db[kind]
        elif kind is None:
            self._plot = self._plots_db['scatter']
        else:
            assert hasattr(kind, '__call__'), f'kind must be in{list(self._plots_db.keys())} or callable'
            self._plot = kind

        # kwargs to keep
        self._keep_plot = list(ins.signature(self._plot).parameters.keys())
        self._keep_error = list(ins.signature(self.ax.errorbar).parameters.keys())
        self.kwargs_plot = {}
        self.kwargs_error = {}

    def plot(self, **kwargs):
        """Plot function creation"""
        self.kwargs_plot.update({k: kwargs[k] for k in self._keep_plot if k in kwargs.keys()})
        self.kwargs_error.update({k: kwargs[k] for k in self._keep_error if k in kwargs.keys()})

        # Plot
        self._plot(self.x, self.y, label=self.label, **self.kwargs_plot)

        # Errorbars
        if (np.any(self.x_err) is not None or np.any(self.y_err) is not None):
            self.ax.errorbar(self.x, self.y, yerr=self.y_err,
                             xerr=self.x_err, **self.kwargs_error)  # errorevery=skiperr, markevery=skiperr, capsize=2)

        return self.ax

    def plot3d(self, *args, **kwargs):
        """3D plot function creation"""
        raise NotImplementedError("WIP")
        return self._plot3d(self.x, self.y, self.z, **kwargs)

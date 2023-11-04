import os
import inspect as ins
import warnings

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tic

try:
    from factory import PlotFactory
except:
    import sys
    sys.path.append('../pltfront/')
    from pltfront.factory import PlotFactory

# TODO: add standard plot to compare in `tests/`
# TODO: add API for CLI usage (e.g. with data files)
# TODO: add gnuplot syntax recognition in API (perhaps with object pickling on
#       matplotlib side)
# TODO: add 3D plotting support, perhaps automatically;
#       criteria could be input data length or a kwarg
# TODO: add histogram support, maintaining all stylistic choices made
#       for `plot`; plot styling should be delegated to a more universal
#       method, perhaps in construction or in a specific class


class Plot:
    def __init__(self, out=None, stylesheet=None):
        # Directories
        self.inp = None
        """Main input directory (used for `movies`)."""

        # Handle output directory
        self.out = out
        """Main output directory."""
        if out is not None:
            os.makedirs(self.out, exist_ok=True)
            assert os.path.exists(self.out), f'{out} is not a directory'

        # Handle stylesheet directory
        self.stylesheet = stylesheet
        if stylesheet is not None:
            if os.path.isfile(stylesheet):
                _, ext = os.path.splitext(stylesheet)
                assert ext == '.mplstyle', f"wrong matplotlib style sheet extension {ext}"

        # Extensions
        self.plot_extension = '.eps'
        """General image extension."""
        self.frame_extension = '.png'
        """Movie frame extension."""
        self.movie_extension = '.gif'
        """File extension for trajectory movie."""

    def _no_stylesheet(self, fig, ax, grid=False, grid_line='dashed', number_minor_x=None, number_minor_y=None, legend=False, legend_frame=False, size=[5, 5]):
        """
        Set style options for a plot when no stylesheet is provided. All keyword arguments are fetched from `plot`.

        Parameters
        ----------
        grid:           bool, optional
                        whether to show grid lines on the plot. Default is False.
        grid_line:      str, optional
                        linestyle for the grid lines. Default is 'dashed'.
        number_minor_x: int, optional
                        number of minor ticks on the x-axis. Default is None.
        number_minor_y: int, optional
                        number of minor ticks on the y-axis. Default is None.
        legend:         bool, optional
                        whether to show a legend on the plot. Default is False.
        legend_frame:   bool, optional
                        whether to show a frame around the legend. Default is False.
        size:           list, optional
                        size of the figure in inches. Default is [5, 5].
        """

        # Size
        fig.set_size_inches(size[0], size[1])

        # Ticks
        ax.minorticks_on()
        ax.tick_params(which='both', direction='in', top=True, right=True)
        ax.tick_params(which='major', size=8)
        ax.tick_params(which='minor', size=5)
        if number_minor_x:
            ax.xaxis.set_minor_locator(tic.AutoMinorLocator(number_minor_x))
        if number_minor_y:
            ax.yaxis.set_minor_locator(tic.AutoMinorLocator(number_minor_y))

        # Set grid
        if grid:
            ax.grid(visible=grid, linestyle=grid_line)

        # Legend
        if legend:
            ax.legend(frameon=legend_frame)

    def _data_conv(self, x, verbose=False):
        """Convert dicts or generic size lists to ndarrays, preserving keys"""

        keys = None
        if isinstance(x, dict):
            xd = np.asarray(list(x.values()))
            keys = np.asarray(list(x.keys()))
        # List or np.array: check if it's 1D or ND
        elif (isinstance(x, list) or isinstance(x, np.ndarray)):
            # If it's 1D, convert to ndarray with size (1, n_elements)
            if np.ndim(x) == 1:
                xd = np.array(x, ndmin=2)
            else:
                xd = np.array(x)
        if verbose:
            print('xd', np.shape(xd), len(xd), np.ndim(xd))
        return xd, keys

    def plot(self, x, y, title=None, filename='plot', kind='line', close=True, show=False, skip=None, xlab=None, ylab=None, xlim=None, ylim=None, xerr=None, yerr=None, skiperr=1, label=None, save=False, bbox_inches='tight', **kwargs):
        """
        Generic plot routine. Other keyword arguments are passed to `_nostylesheet`.

        Parameters
        ----------
        x:              array-like
                        x-axis data for the plot.
        y:              array-like
                        y-axis data for the plot.
        title:          str, optional
                        title of the plot.
        filename:       str, optional
                        filename to save the plot as.
        kind:           str, optional
                        type of plot to create (e.g., line, scatter).
        close:          bool, optional
                        whether to close the plot after displaying it.
        show:           bool, optional)
                        whether to display the plot.
        skip:           int, optional
                        number of data points to skip when plotting.
        xlab:           str, optional
                        label for the x-axis.
        ylab:           str, optional
                        label for the y-axis.
        xlim:           tuple, optional
                        limits for the x-axis.
        ylim:           tuple, optional
                        limits for the y-axis.
        xerr:           array-like, optional
                        error bars for the x-axis data.
        yerr:           array-like, optional
                        error bars for the y-axis data.
        skiperr:        int, optional
                        number of error bars to skip.
        label:          str, optional
                        legend label for each plot.
        save:           bool, optional
                        whether to save the plot.
        bbox_inches:    str, optional
                        bounding box for the plot.
        **kwargs:       dict, optional
                        additional keyword arguments for plot customization.

        Returns
        -------
        fig, ax:        tuple
                        contains the figure object and the axes object of the plot.
        """
        # 0. kwarg handling
        keep_style = list(ins.signature(self._no_stylesheet).parameters.keys())
        kwargs_style = {k: kwargs[k] for k in keep_style if k in kwargs.keys()}
        kwargs = {k: v for k, v in kwargs.items() if k not in kwargs_style}

        # 1. Core plot
        # If stylesheet is set, use it asap
        if self.stylesheet is not None:
            plt.style.use(self.stylesheet)

        # Define figure
        fig, ax = plt.subplots(tight_layout={'pad': 0})

        # Check dimensionality
        # Convert x, y and extract plot kind from dict
        xs, kinds = self._data_conv(x)
        ys, _ = self._data_conv(y)

        # If x isn't a dict, fetch user-specified kinds
        if kinds is None:
            kinds = np.array(kind, ndmin=1)

        # Sanity check
        # Checks on x and y
        ndim = np.shape(xs)
        assert ndim == np.shape(ys), f'x and y have mismatching shapes, {ndim} and {np.shape(ys)}'

        # Check xs and kinds have same dimension
        if ndim[0] > np.shape(kinds)[0]:
            warnings.warn(
                f'x and kind have mismatching first dims, ({ndim[0]}) and ({np.shape(kinds)[0]}). Remaining kinds set to scatter.', RuntimeWarning)
            while np.shape(kinds)[0] < ndim[0]:
                kinds = np.append(kinds, 'scatter')

        # Convert label to array
        labels = np.array(label, ndmin=1)

        # Check xs and labels have same dimension
        if ndim[0] > np.shape(labels)[0]:
            warnings.warn(
                f'x and labels have mismatching first dims, ({ndim[0]}) and ({np.shape(labels)[0]}). Labels set to `None`.', RuntimeWarning)
            labels = [None for _ in range(ndim[0])]

        # Instantiate plots
        plots = [PlotFactory(xi[::skip], yi[::skip], label=labeli, xerr=xerr, yerr=yerr, kind=kindi, ax=ax)
                 for xi, yi, labeli, kindi in zip(xs, ys, labels, kinds)]

        # Do the plots
        for i in range(ndim[0]):
            ax = plots[i].plot(**kwargs)

        # 2. Data features
        # Plot titles
        if title is not None:
            ax.set_title(title)

        # Axis label
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)

        # Axis limits
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        # 3. Style features
        # Don't show legend if no labels are available
        if all(item is None for item in labels):
            kwargs_style['legend'] = False

        if self.stylesheet is None:
            self._no_stylesheet(fig, ax, **kwargs_style)

        # 4. Show, save and close
        # Save plot
        if save:
            assert os.path.exists(self.out), 'output directory does not exist or has not been specified.'
            fig.savefig(os.path.join(self.out, filename+self.plot_extension), bbox_inches=bbox_inches)

        # Show plot
        if show:
            plt.show()

        if close:
            plt.close(fig)

        return fig, ax


'''
    def movie(self, filename='movie', fps=None, duration=200):
        """Create gif from images in folder."""
        import imageio
        if fps is not None:
            import warnings
            warnings.warn(
                '`fps` keyword is not available anymore in ImageIO. Use `duration`', DeprecationWarning)
            duration = 1000 * 1./fps

        with imageio.get_writer(os.path.join(self.out, filename+self.movie_extension), mode='I', duration=duration) as writer:
            for item in sorted(os.listdir(self.frame_out)):
                image = imageio.imread(os.path.join(self.frame_out, item))
                writer.append_data(image)

            os.path.join(self.out, filename+self.movie_extension)
'''

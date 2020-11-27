# stdlib
import itertools
from collections import OrderedDict
from functools import partial
from typing import List, Tuple

# 3rd party
import matplotlib.pyplot as plt
import numpy
import numpy as np
from cycler import cycler
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# this package
from domplotlib.styles.default import plt


def koch_snowflake() -> Tuple[Figure, Axes]:
	"""
	From https://matplotlib.org/3.3.3/gallery/lines_bars_and_markers/fill.html#sphx-glr-gallery-lines-bars-and-markers-fill-py
	"""

	def _koch_snowflake_complex(order):
		if order == 0:
			# initial triangle
			angles = numpy.array([0, 120, 240]) + 90
			return 10 / numpy.sqrt(3) * numpy.exp(numpy.deg2rad(angles) * 1j)
		else:
			ZR = 0.5 - 0.5j * numpy.sqrt(3) / 3

			p1 = _koch_snowflake_complex(order - 1)  # start points
			p2 = numpy.roll(p1, shift=-1)  # end points
			dp = p2 - p1  # connection vectors

			new_points = numpy.empty(len(p1) * 4, dtype=numpy.complex128)
			new_points[::4] = p1
			new_points[1::4] = p1 + dp / 3
			new_points[2::4] = p1 + dp * ZR
			new_points[3::4] = p1 + dp / 3 * 2
			return new_points

	points = _koch_snowflake_complex(5)
	x, y = points.real, points.imag

	fig: Figure = plt.figure(figsize=(8, 8))
	ax = fig.subplots()
	ax.axis("equal", emit=True)
	ax.fill(x, y, label="Koch Snowflake")

	return fig, ax


def hatch_filled_histograms() -> Tuple[Figure, Axes]:
	"""
	From https://matplotlib.org/3.3.3/gallery/lines_bars_and_markers/filled_step.html#sphx-glr-gallery-lines-bars-and-markers-filled-step-py
	"""

	def filled_hist(ax, edges, values, bottoms=None, orientation='v', **kwargs):
		"""
		Draw a histogram as a stepped patch.

		Extra kwargs are passed through to `fill_between`

		Parameters
		----------
		ax : Axes
			The axes to plot to

		edges : array
			A length n+1 array giving the left edges of each bin and the
			right edge of the last bin.

		values : array
			A length n array of bin counts or values

		bottoms : float or array, optional
			A length n array of the bottom of the bars.  If None, zero is used.

		orientation : {'v', 'h'}
		   Orientation of the histogram.  'v' (default) has
		   the bars increasing in the positive y-direction.

		Returns
		-------
		ret : PolyCollection
			Artist added to the Axes
		"""
		print(orientation)
		if orientation not in "hv":
			raise ValueError("orientation must be in {{'h', 'v'}} " "not {o}".format(o=orientation))

		kwargs.setdefault("step", "post")
		edges = np.asarray(edges)
		values = np.asarray(values)
		if len(edges) - 1 != len(values):
			raise ValueError(
					'Must provide one more bin edge than value not: '
					'len(edges): {lb} len(values): {lv}'.format(lb=len(edges), lv=len(values))
					)

		if bottoms is None:
			bottoms = 0
		bottoms = np.broadcast_to(bottoms, values.shape)

		values = np.append(values, values[-1])
		bottoms = np.append(bottoms, bottoms[-1])
		if orientation == 'h':
			return ax.fill_betweenx(edges, values, bottoms, **kwargs)
		elif orientation == 'v':
			return ax.fill_between(edges, values, bottoms, **kwargs)
		else:
			raise AssertionError("you should never be here")

	def stack_hist(
			ax,
			stacked_data,
			sty_cycle,
			bottoms=None,
			hist_func=None,
			labels=None,
			plot_func=None,
			plot_kwargs=None
			):
		"""
		Parameters
		----------
		ax : axes.Axes
			The axes to add artists too

		stacked_data : array or Mapping
			A (N, M) shaped array.  The first dimension will be iterated over to
			compute histograms row-wise

		sty_cycle : Cycler or operable of dict
			Style to apply to each set

		bottoms : array, default: 0
			The initial positions of the bottoms.

		hist_func : callable, optional
			Must have signature `bin_vals, bin_edges = f(data)`.
			`bin_edges` expected to be one longer than `bin_vals`

		labels : list of str, optional
			The label for each set.

			If not given and stacked data is an array defaults to 'default set {n}'

			If stacked_data is a mapping, and labels is None, default to the keys
			(which may come out in a random order).

			If stacked_data is a mapping and labels is given then only
			the columns listed by be plotted.

		plot_func : callable, optional
			Function to call to draw the histogram must have signature:

			  ret = plot_func(ax, edges, top, bottoms=bottoms,
							  label=label, **kwargs)

		plot_kwargs : dict, optional
			Any extra kwargs to pass through to the plotting function.  This
			will be the same for all calls to the plotting function and will
			over-ride the values in cycle.

		Returns
		-------
		arts : dict
			Dictionary of artists keyed on their labels
		"""
		# deal with default binning function
		if hist_func is None:
			hist_func = np.histogram

		# deal with default plotting function
		if plot_func is None:
			plot_func = filled_hist

		# deal with default
		if plot_kwargs is None:
			plot_kwargs = {}
		print(plot_kwargs)
		try:
			l_keys = stacked_data.keys()
			label_data = True
			if labels is None:
				labels = l_keys

		except AttributeError:
			label_data = False
			if labels is None:
				labels = itertools.repeat(None)

		if label_data:
			loop_iter = enumerate((stacked_data[lab], lab, s) for lab, s in zip(labels, sty_cycle))
		else:
			loop_iter = enumerate(zip(stacked_data, labels, sty_cycle))

		arts = {}
		for j, (data, label, sty) in loop_iter:
			if label is None:
				label = f'dflt set {j}'
			label = sty.pop("label", label)
			vals, edges = hist_func(data)
			if bottoms is None:
				bottoms = np.zeros_like(vals)
			top = bottoms + vals
			print(sty)
			sty.update(plot_kwargs)
			print(sty)
			ret = plot_func(ax, edges, top, bottoms=bottoms, label=label, **sty)
			bottoms = top
			arts[label] = ret
		ax.legend(fontsize=10)
		return arts

	# set up histogram function to fixed bins
	edges = np.linspace(-3, 3, 20, endpoint=True)
	hist_func = partial(np.histogram, bins=edges)

	# set up style cycles
	color_cycle = cycler(facecolor=plt.rcParams["axes.prop_cycle"][:4])
	label_cycle = cycler(label=[f'set {n}' for n in range(4)])
	hatch_cycle = cycler(hatch=['/', '*', '+', '|'])

	# Fixing random state for reproducibility
	np.random.seed(19680801)

	stack_data = np.random.randn(4, 12250)
	dict_data = OrderedDict(zip((c["label"] for c in label_cycle), stack_data))

	fig, ax = plt.subplots(1, 1, figsize=(9, 4.5), tight_layout=True)
	arts = stack_hist(ax, stack_data, color_cycle + label_cycle + hatch_cycle, hist_func=hist_func)

	ax.set_ylabel("counts")
	ax.set_xlabel('x')

	return fig, ax


def h_bar_chart() -> Tuple[Figure, Axes]:
	"""
	https://matplotlib.org/3.3.3/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py
	"""

	category_names = ["Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"]
	results = {
			"Question 1": [10, 15, 17, 32, 26],
			"Question 2": [26, 22, 29, 10, 13],
			"Question 3": [35, 37, 7, 2, 19],
			"Question 4": [32, 11, 9, 15, 33],
			"Question 5": [21, 29, 5, 5, 40],
			"Question 6": [8, 19, 5, 30, 38]
			}

	def survey(results, category_names):
		"""
		Parameters
		----------
		results : dict
			A mapping from question labels to a list of answers per category.
			It is assumed all lists contain the same number of entries and that
			it matches the length of *category_names*.
		category_names : list of str
			The category labels.
		"""
		labels = list(results.keys())
		data = np.array(list(results.values()))
		data_cum = data.cumsum(axis=1)
		category_colors = plt.get_cmap("RdYlGn")(np.linspace(0.15, 0.85, data.shape[1]))

		fig, ax = plt.subplots(figsize=(9.2, 5))
		ax.invert_yaxis()
		ax.xaxis.set_visible(False)
		ax.set_xlim(0, np.sum(data, axis=1).max())

		for i, (colname, color) in enumerate(zip(category_names, category_colors)):
			widths = data[:, i]
			starts = data_cum[:, i] - widths
			ax.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)
			xcenters = starts + widths / 2

			r, g, b, _ = color
			text_color = "white" if r * g * b < 0.5 else "darkgrey"
			for y, (x, c) in enumerate(zip(xcenters, widths)):
				ax.text(x, y, str(int(c)), ha="center", va="center", color=text_color)
		ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1), loc="lower left", fontsize="small")

		return fig, ax

	return survey(results, category_names)


def markevery() -> Tuple[Figure, List[Axes]]:
	"""
	From https://matplotlib.org/3.3.3/gallery/lines_bars_and_markers/markevery_demo.html#sphx-glr-gallery-lines-bars-and-markers-markevery-demo-py
	"""

	# define a list of markevery cases to plot
	cases = [None, 8, (30, 8), [16, 24, 30], [0, -1], slice(100, 200, 3), 0.1, 0.3, 1.5, (0.0, 0.1), (0.45, 0.1)]

	# define the figure size and grid layout properties
	figsize = (10, 8)
	cols = 3
	rows = len(cases) // cols + 1
	# define the data for cartesian plots
	delta = 0.11
	x = np.linspace(0, 10 - 2 * delta, 200) + delta
	y = np.sin(x) + 1.0 + delta

	def trim_axs(axs, N):
		"""
		Reduce *axs* to *N* Axes. All further Axes are removed from the figure.
		"""
		axs = axs.flat
		for ax in axs[N:]:
			ax.remove()
		return axs[:N]

	fig = plt.figure(figsize=figsize, constrained_layout=True)
	axs = fig.subplots(rows, cols)
	axs = trim_axs(axs, len(cases))

	colour_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

	for ax, case in zip(axs, cases):
		ax.set_title(f"markevery={case}")
		ax.plot(x, y, 'o', ls='-', ms=4, markevery=case, label=f"markevery={case}", color=next(colour_cycle))

	return fig, axs

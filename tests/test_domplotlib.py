# stdlib
from typing import Callable, Tuple

# 3rd party
import pytest
from matplotlib.axes import Axes  # type: ignore
from matplotlib.figure import Figure  # type: ignore

# this package
from domplotlib import horizontal_legend, save_svg
from tests.common import check_images
from tests.plots import h_bar_chart, hatch_filled_histograms, koch_snowflake, markevery


@pytest.mark.parametrize("plot", [
		koch_snowflake,
		hatch_filled_histograms,
		h_bar_chart,
		markevery,
		])
def test_save_svg(tmp_pathplus, plot: Callable[[], Tuple[Figure, ...]]):
	fig, *_ = plot()

	filename = tmp_pathplus / "plot.svg"

	save_svg(fig, filename, dpi=1600)

	for line in filename.read_lines():
		assert line.rstrip() == line


@pytest.mark.parametrize("plot", [
		koch_snowflake,
		hatch_filled_histograms,
		h_bar_chart,
		])
@check_images
def test_horizontal_legend(tmp_pathplus, plot: Callable[[], Tuple[Figure, Axes]]):
	fig, ax = plot()

	horizontal_legend(fig)

	return fig


@check_images
def test_horizontal_legend_markevery(tmp_pathplus):
	fig, axs = markevery()

	handles = []
	labels = []

	for ax in axs:
		hands, labs = ax.get_legend_handles_labels()
		handles.extend(hands)
		labels.extend(labs)

	horizontal_legend(fig, handles, labels, ncol=2)

	return fig

# 3rd party
import pytest
from cawdrey import Tally
from matplotlib.figure import Figure  # type: ignore
from matplotlib.text import Text  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from domplotlib.plots import pie_from_tally
from domplotlib.styles._plt import plt
from tests.common import check_images


@pytest.mark.parametrize("reverse", [True, False])
@check_images
def test_plot_pie_from_tally(tmp_pathplus, file_regression: FileRegressionFixture, reverse: bool):
	data = [
			"cat",
			"dog",
			"dog",
			"cat",
			"rabbit",
			"dog",
			"dog",
			"cat",
			"snake",
			"gerbil",
			]

	tally = Tally(data)

	fig: Figure = plt.figure(figsize=(8, 8))
	ax = fig.subplots()

	patches, texts, autotexts = pie_from_tally(
		tally,
		[tally.most_common(1)[0][0]],
		autopct="%1.1f%%",
		startangle=90,
		ax=ax,
		reverse=reverse,
		)

	assert len(patches) == 5
	assert len(texts) == 5
	assert len(autotexts) == 5

	if reverse:
		most_common = reversed(tally.most_common())
	else:
		most_common = tally.most_common()

	text: Text
	for text, autotext, pet in zip(texts, autotexts, most_common):
		assert text.get_text() == pet[0]
		assert autotext.get_text() == f"{tally.get_percentage(pet[0]):0.1%}"

	ax.axis("equal", emit=True)

	return fig

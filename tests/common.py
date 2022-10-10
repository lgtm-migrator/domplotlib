# 3rd party
import sys
import pytest
from domdf_python_tools.paths import PathPlus

if sys.version_info[:2] == (3, 6):
	baseline_dir = str(PathPlus(__file__).parent / "baseline_36")
	image_hashes = str(PathPlus(__file__).parent / "image_hashes_36.json")
elif sys.version_info[:2] == (3, 7):
	baseline_dir = str(PathPlus(__file__).parent / "baseline_37")
	image_hashes = str(PathPlus(__file__).parent / "image_hashes_37.json")
elif sys.version_info[:2] == (3, 8):
	baseline_dir = str(PathPlus(__file__).parent / "baseline")
	image_hashes = str(PathPlus(__file__).parent / "image_hashes_38.json")
elif sys.version_info[:2] == (3, 9):
	baseline_dir = str(PathPlus(__file__).parent / "baseline")
	image_hashes = str(PathPlus(__file__).parent / "image_hashes_39.json")
elif sys.version_info[:2] == (3, 10):
	baseline_dir = str(PathPlus(__file__).parent / "baseline")
	image_hashes = str(PathPlus(__file__).parent / "image_hashes_310.json")
elif sys.version_info[:2] == (3, 11):
	baseline_dir = str(PathPlus(__file__).parent / "baseline")
	image_hashes = str(PathPlus(__file__).parent / "image_hashes_311.json")
else:
	baseline_dir = str(PathPlus(__file__).parent / "baseline")
	image_hashes = str(PathPlus(__file__).parent / "image_hashes.json")

check_images = pytest.mark.mpl_image_compare(
		baseline_dir=baseline_dir,
		savefig_kwargs={"dpi": 600},
		hash_library=image_hashes,
		)

pytest_plugins = ("coincidence", )
"""
To regenerate the baseline:


tox -e py36 -- --mpl-generate-path=tests/baseline
tox -e py36 -- --mpl-generate-hash-library=tests/image_hashes.json
"""

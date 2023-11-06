import setuptools
from pathlib import Path

# arguments:
# - name: Must be unique within PyPI
# - version: Version for your package, use semantic versioning
# - long_description: Set it to the contents of your README.md file
# - packages: Specify which modules/packages to publish, which to ignore, etc.
setuptools.setup(
    name="sports_toto_scraper",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["tests", "data"]
    )
)

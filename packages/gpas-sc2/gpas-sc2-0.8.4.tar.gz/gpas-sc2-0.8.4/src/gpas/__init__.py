import importlib.metadata
from pathlib import Path

__version__ = importlib.metadata.version("gpas-sc2")

pkg_dir = Path(__file__)
data_dir = pkg_dir.parent / "data"

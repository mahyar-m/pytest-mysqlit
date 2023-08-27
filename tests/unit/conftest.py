import sys
from unittest.mock import MagicMock

sys.modules['mysql'] = MagicMock()
sys.modules['connector'] = MagicMock()

pytest_plugins = [
    "src.pytest_mysqlit.plugin",
    "pytester"
]

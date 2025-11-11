"""Top-level API package initialization.

Ensures imports like `from api.models...` work when tests are run from subdirectories.
"""

# Re-export commonly used subpackages for convenience
from . import models as models  # noqa: F401

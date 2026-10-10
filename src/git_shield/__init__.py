"""Git Shield - Pre-commit and repository security scanner."""
__version__ = "1.0.0"

from .scanner import ShieldScanner
from .installer import install_pre_commit_hook

__all__ = ["ShieldScanner", "install_pre_commit_hook"]

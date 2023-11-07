from pathlib import Path

from ansible.plugins import loader

BUNDLED_EXTENSIONS_DIR: Path = Path(__file__).parent

__all__ = [
    "install",
]


def install() -> None:
    """Register bundled resources"""
    loader.action_loader.config.append(str(BUNDLED_EXTENSIONS_DIR / "plugins" / "action"))

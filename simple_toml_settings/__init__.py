"""Defines the package's public interface."""

from typing import Any

from .settings import TOMLSettings


def get_settings(*args: Any, **kwargs: Any) -> TOMLSettings:  # noqa: ANN401
    """Return a Singleton instance of the TOMLSettings class."""
    return TOMLSettings.get_instance(*args, **kwargs)


__all__ = ["TOMLSettings", "get_settings"]

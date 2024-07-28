"""Defines the package's public interface."""

import os
from pathlib import Path

# https://github.com/srstevenson/xdg-base-dirs/blob/main/src/xdg_base_dirs/__init__.py
# Copyright © Scott Stevenson <scott@stevenson.io>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.


def _path_from_env(variable: str, default: Path) -> Path:
    """Read an environment variable as a path.

    The environment variable with the specified name is read, and its
    value returned as a path. If the environment variable is not set, is
    set to the empty string, or is set to a relative rather than
    absolute path, the default value is returned.

    Parameters
    ----------
    variable : str
        Name of the environment variable.
    default : Path
        Default value.

    Returns:
    -------
    Path
        Value from environment or default.

    """
    if (value := os.environ.get(variable)) and (
        path := Path(value)
    ).is_absolute():
        return path
    return default


def xdg_config_home() -> Path:
    """Return a Path corresponding to XDG_CONFIG_HOME."""
    return _path_from_env("XDG_CONFIG_HOME", Path.home() / ".config")

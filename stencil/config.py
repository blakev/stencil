#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   stencil-blog, 2020
#   - blake
# <<

"""Define a valid configuration that a user's config file can be compared against."""

import os
import toml
import ujson as json
from typing import Dict

from jinja2 import Template

DEFAULT = {"source": "", "destination": "", "templates": ""}


def load_config(path: str) -> Dict:
    """Two-pass config loader.

    Can do replacement with self-defined keys on second pass, using Jinja templates.
    """
    if not os.path.exists(path):
        raise IOError(f"{path} does not exist")
    ext = os.path.splitext(path)[-1].lower()
    with open(path, "r") as fp:
        data = fp.read()
    if ext == ".json":
        fn = json.loads
    elif ext == ".toml":
        fn = toml.loads
    else:
        raise IOError(f"cannot load {path} with extension {ext}")
    conf = DEFAULT.copy()
    conf.update(fn(data))
    # do a second pass on the config file to do inline replacement of values
    conf = fn(Template(data).render(**conf))
    return conf

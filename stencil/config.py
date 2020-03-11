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

DEFAULT = {
    "source": "",
    "destination": ""
}


def load_config(path: str) -> Dict:
    if not os.path.exists(path):
        raise IOError(f'{path} does not exist')
    ext = os.path.splitext(path)[-1].lower()
    with open(path, 'r') as fp:
        if ext == '.json':
            c = json.load(fp)
        elif ext == '.toml':
            c = toml.load(fp)
        else:
            raise IOError(f'cannot load {path} with extension {ext}')
    conf = DEFAULT.copy()
    conf.update(c)
    return conf

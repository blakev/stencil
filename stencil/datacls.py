#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   stencil-blog, 2020
#   - blake
# <<

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Meta:
    """Each blog entry will have multiple levels of metadata.

    The static config passed for the whole project, the configuration values
    defined in the file header, and the computed metadata under `stencil.`
    These values should be used to format and generate the content of the
    blog post.
    """

    file: Dict
    static: Dict
    stencil: Dict


@dataclass
class Post:
    """Individual blog entry.
    """

    raw_content: str
    meta: Meta = field(init=False)

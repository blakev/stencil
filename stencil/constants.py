#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 
# >>
#   stencil-blog, 2020
#   - blake
# <<

from typing import List

MARKDOWN_EXTENSIONS: List[str] = ['.md', '.mds',]
# default file extensions that are "valid" for our finder
# .. md) normal markdown files; untouched
# .. mds) (reserved) for markdown-stencil files

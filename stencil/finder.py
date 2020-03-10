#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 
# >>
#   stencil-blog, 2020
#   - blake
# <<

import os
import glob
from typing import Callable, Iterator, List, Optional

from stencil.constants import MARKDOWN_EXTENSIONS
from stencil.objects import MarkdownFile


def find_files(
        source: str,
        extensions: List[str] = None,
        filters: Optional[List[Callable[[MarkdownFile], bool]]] = None
) -> Iterator[MarkdownFile]:
    """Recursively iterates a source tree looking for Markdown files."""

    if not extensions:
        extensions = MARKDOWN_EXTENSIONS

    if filters is None:
        filters = []

    for filter_fn in filters:
        if not callable(filter_fn):
            raise RuntimeError(f'{type(filter_fn)} is not callable')

    if not source or not os.path.isdir(source):
        raise IOError(f'{source} is not a valid file path')

    path = os.path.abspath(source)
    # we want the absolute path of our "source" directory so we can
    #  extract additional metadata from folder structure

    exts = [f'**/*{ext}' for ext in extensions]
    # build wild card patterns for each of our file extensions

    for ext in exts:
        ext_path = os.path.join(path, ext)
        for file in glob.iglob(ext_path, recursive=True):
            file = MarkdownFile(source_folder=path, fullpath=file)
            if all(fn(file) for fn in filters):
                yield file

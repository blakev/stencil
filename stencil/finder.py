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

from stencil.objects import MarkdownFile


def find_files(
    source: str,
    extensions: Optional[List[str]] = None,
    filters: Optional[List[Callable[[MarkdownFile], bool]]] = None,
) -> Iterator[MarkdownFile]:
    """Recursively iterates a source tree looking for Markdown files."""

    if not extensions:
        extensions = [".md"]

    if filters is None:
        filters = []

    for filter_fn in filters:
        if not callable(filter_fn):
            raise RuntimeError(f"{type(filter_fn)} is not callable")

    if not source or not os.path.isdir(source):
        raise IOError(f"{source} is not a valid file path")

    path = os.path.abspath(source)
    # we want the absolute path of our "source" directory so we can
    #  extract additional metadata from folder structure

    exts = [f"**/*{ext}" for ext in extensions]
    # build wild card patterns for each of our file extensions

    for ext in exts:
        ext_path = os.path.join(path, ext)
        for file in glob.iglob(ext_path, recursive=True):
            file = MarkdownFile(source_folder=path, fullpath=file)
            if all(fn(file) for fn in filters):
                yield file


def extract_metadata(file: MarkdownFile) -> MarkdownFile:
    """Parse and extract information from a valid MarkdownFile instance.

    Extra information is added in-place to the file instance passed to the function.
    """

    config_text: str
    content_text: str
    config: List[str] = []
    content: List[str] = []
    reading_config: bool = False
    start_block, end_block = "<!--", "-->\n"

    with open(file.fullpath, "r") as fp:
        for line in fp.readlines():
            if reading_config and line == end_block:
                reading_config = False
                continue
            if line.startswith(start_block):
                if reading_config:
                    raise IOError(f"problem reading config from file {file}")
                reading_config = True
                config.append(line.split(start_block)[-1])
                continue
            if reading_config:
                config.append(line)
                continue
            if not reading_config:
                content.append(line)

    if config:
        config_text = "".join(config)
        file.add_metadata(raw=config_text)
    if content:
        content_text = "".join(content)
        file.add_markdown(raw=content_text)
    return file

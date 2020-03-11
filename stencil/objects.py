#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   stencil-blog, 2020
#   - blake
# <<

import os
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, NamedTuple

import toml


class Validation(NamedTuple):
    errors: List[str]

    @property
    def success(self):
        return not self.errors


@dataclass
class FileMetadata:
    raw: str
    config: Dict[Any, Any] = field(init=False)

    def __post_init__(self):
        self.config = toml.loads(self.raw)


@dataclass
class MarkdownFile:
    source_folder: str
    fullpath: str
    relative_path: str = field(init=False)
    extension: str = field(init=False)
    filename: str = field(init=False)
    created: datetime = field(init=False)
    modified: datetime = field(init=False)
    is_index: bool = field(init=False, default=False)
    metadata: FileMetadata = field(init=False)
    markdown: str = field(init=False, default="")

    def __post_init__(self):
        self.relative_path = self.fullpath.split(self.source_folder)[-1]
        self.filename = os.path.split(self.fullpath)[-1]
        self.extension = os.path.splitext(self.filename)[-1]
        self.created = datetime.fromtimestamp(os.stat(self.fullpath).st_ctime)
        self.modified = datetime.fromtimestamp(os.stat(self.fullpath).st_mtime)
        self.is_index = self.filename.startswith("index.")

    @property
    def size(self) -> int:
        return os.stat(self.fullpath).st_size

    def add_markdown(self, raw: str) -> None:
        self.markdown = raw

    def add_metadata(self, raw: str) -> FileMetadata:
        self.metadata = FileMetadata(raw=raw)
        return self.metadata

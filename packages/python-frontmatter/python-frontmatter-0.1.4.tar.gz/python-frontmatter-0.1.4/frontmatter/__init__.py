# -*- coding: utf-8 -*-
"""
Python Frontmatter: Parse and manage posts with YAML frontmatter
"""
from __future__ import unicode_literals

import codecs
import re
import yaml

from .util import u

__all__ = ['parse', 'load', 'loads', 'dump', 'dumps']


FM_RE = re.compile(r'^\s*---(.*)---\s*$', re.MULTILINE | re.DOTALL)

POST_TEMPLATE = """\
---
{metadata}
---
{content}
"""


def parse(text, **defaults):
    """
    Parse text with YAML frontmatter, return metadata and content.
    Pass in optional metadata defaults as keyword args.

    If frontmatter is not found, returns an empty metadata dictionary
    and original text content.
    """
    # ensure unicode first
    text = u(text)

    # match, returning empty metadata and the original content on failure
    match = FM_RE.search(text)
    if match is None:
        return ({}, text)

    # content is everything after metadata
    content = text[match.end():].strip()

    # metadata is a dictionary, with defaults
    metadata = {}
    metadata.update(defaults)

    # parse yaml
    metadata.update(yaml.safe_load(match.groups()[0]))

    return metadata, content


def load(fd, **defaults):
    """
    Load and parse a file or filename, return a post.
    """
    if hasattr(fd, 'read'):
        text = fd.read()

    else:
        with codecs.open(fd, 'r', 'utf-8') as f:
            text = f.read()

    return loads(text, **defaults)


def loads(text, **defaults):
    """
    Parse text and return a post.
    """
    metadata, content = parse(text, **defaults)
    return Post(content, **metadata)


def dump(post, fd):
    """
    Serialize post to a string and dump to a file-like object.
    """
    content = dumps(post)
    if hasattr(fd, 'write'):
        fd.write(content)

    else:
        with codecs.open(fd, 'w', 'utf-8') as f:
            f.write(content)


def dumps(post):
    """
    Serialize post to a string and return text.
    """
    metadata = yaml.safe_dump(post.metadata, default_flow_style=False).strip()
    return POST_TEMPLATE.format(metadata=metadata, content=post.content).strip()


class Post(object):
    """
    A post contains content and metadata from YAML Front Matter.
    For convenience, metadata values are available as proxied item lookups. 

    Don't use this class directly. Use module-level functions load, dump, etc.
    """
    def __init__(self, content, **metadata):
        self.content = content
        self.metadata = metadata
    
    def __getitem__(self, name):
        "Get metadata key"
        return self.metadata[name]        

    def __setitem__(self, name, value):
        "Set a metadata key"
        self.metadata[name] = value

    def __delitem__(self, name):
        "Delete a metadata key"
        del self.metadata[name]

    def get(self, key, default=None):
        "Get a key, fallback to default"
        return self.metadata.get(key, default)

    def keys(self):
        return self.metadata.keys()

    def to_dict(self):
        "Post as a dict, for serializing"
        d = self.metadata.copy()
        d['content'] = self.content
        return d


# coding: utf-8
"""
The *pathspec* package provides pattern matching for file paths. So far
this only includes gitignore style pattern matching.

See "README.rst" or <https://github.com/cpburnz/python-path-specification>
for more information. Or you can always scour the source code.
"""

__author__ = "Caleb P. Burns"
__copyright__ = u"Copyright © 2013-2014 Caleb P. Burns"
__created__ = "2013-10-12"
__credits__ = [
	"dahlia <https://github.com/dahlia>",
	"highb <https://github.com/highb>",
]
__email__ = "cpburnz@gmail.com"
__license__ = "MPL 2.0"
__project__ = "pathspec"
__status__ = "Development"
__updated__ = "2014-09-17"
__version__ = "0.3.0"

from .gitignore import GitIgnorePattern
from .pathspec import PathSpec
from .pattern import Pattern, RegexPattern
from .util import iter_tree, match_files, RecursionError

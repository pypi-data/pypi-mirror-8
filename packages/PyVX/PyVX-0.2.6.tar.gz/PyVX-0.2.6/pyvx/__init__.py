from pyvx.nodes import *
from pyvx.types import *
from pyvx.optimize import *
from pyvx.pythonic import *

__version_info__ = (0, 2, 6)
__version__ = '.'.join(str(i) for i in __version_info__)

#Graph=CoreGraph
Graph=OptimizedGraph


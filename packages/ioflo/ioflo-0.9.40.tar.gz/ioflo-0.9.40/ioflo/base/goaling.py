"""goaling.py goal action module

"""
#print("module {0}".format(__name__))

import time
import struct

from collections import deque
try:
    from itertools import izip
except ImportError: # python3
    izip = zip

import inspect



from .globaling import *
from .odicting import odict
from . import aiding
from . import excepting
from . import registering
from . import storing
from . import acting

from .consoling import getConsole
console = getConsole()

#Class definitions

class Goal(acting.Actor):
    """Goal Class for setting configuration or command value in data share """
    Registry = odict()

    def __init__(self,  **kw):
        """
        Initialization method for instance.
        inherited attributes:
           .name = unique name for action instance
           .store = shared data store

        parameters:
           goal = share of goal
        """
        if 'preface' not in kw:
            kw['preface'] = 'Goal'

        super(Goal,self).__init__(**kw)

    def expose(self):
        """ """
        print("Goal %s" % (self.name))

class GoalDirect(Goal):
    """GoalDirect Goal """

    def __init__(self, **kw):
        """Initialization method for instance. """
        super(GoalDirect, self).__init__(**kw)  #.goal inited here


    def action(self, goal, data, **kw):
        """
        Set goal to data dictionary
        parameters:
              goal = share of goal
              data = dict of data fields to assign to goal share
        """
        console.profuse("Set {0} to {1}\n".format(goal.name, data))
        goal.update(data)
        return None

class GoalIndirect(Goal):
    """GoalIndirect Goal """

    def __init__(self, **kw):
        """Initialization method for instance."""

        super(GoalIndirect, self).__init__(**kw)  #.goal inited here

    def action(self, goal, goalFields, source, sourceFields, **kw):
        """
        Set goalFields in goal from sourceFields in source

        parameters:
              goal = share of goal
              source = share of source to get data from
              fields = fields to use to update goal
        """
        console.profuse("Set {0} in {1} from {2} in {3}\n".format(
                goal.name, goalFields, source.name, sourceFields))
        data = odict()
        for gf, sf in izip(goalFields, sourceFields):
            data[gf] = source[sf]
        goal.update(data)
        return None

from __future__ import print_function
import os
from fabric.operations import local
from fabric.context_managers import hide
from harvest.decorators import cli

__doc__ = """\
Updates this Harvest package.
"""

@cli(description=__doc__)
def parser(options):
    with hide('running'):
        bindir = os.path.dirname(local('which harvest', capture=True), shell='/bin/bash')
        pip = os.path.join(bindir, 'pip')
        local('{0} install -U harvest'.format(pip), shell='/bin/bash')

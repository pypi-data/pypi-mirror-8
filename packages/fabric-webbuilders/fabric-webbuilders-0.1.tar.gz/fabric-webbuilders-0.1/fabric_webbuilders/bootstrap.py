# -*- coding: utf-8 -*-
#
# This file is part of fabric-webbuilders (https://github.com/mathiasertl/fabric-webbuilders).
#
# fabric-webbuilders is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# fabric-webbuilders is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with fabric-webbuilders.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import json
import os
import re

from collections import OrderedDict

from fabric.api import local
from fabric.state import env

from fabric_webbuilders.base import BuildTask
from fabric_webbuilders.base import GitMixin


class BuildBootstrapTask(BuildTask, GitMixin):
    prefix = 'bootstrap'
    default_origin = 'https://github.com/twbs/bootstrap.git'
    tag_re = re.compile('v(?P<version>[0-9.]*)(-(?P<suffix>-.*))?')

    missing_variables = {
        '@zindex-navbar': '1000',
        '@zindex-dropdown': '1000',
        '@zindex-popover': '1060',
        '@zindex-tooltip': '1070',
        '@zindex-navbar-fixed': '1030',
        '@zindex-modal': '1040',
    }
    # these less-variables are not included in config.json but are required:
    mandatory_less = ['mixins.less', 'normalize.less', 'utilities.less',
                      'variables.less', 'scaffolding.less']

    def __init__(self, origin=None, version=None, build_dir=None, dest_dir=None, config=None):
        self.config = config
        super(BuildBootstrapTask, self).__init__(origin, version, build_dir, dest_dir)

    def run(self, origin=None, version=None, build_dir=None, dest_dir=None, config=None):
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = env.get('%s_config' % self.prefix)

        super(BuildBootstrapTask, self).run(origin, version, build_dir, dest_dir)

    def build(self):
        if self.config is not None and os.path.exists(self.config):
            # load config
            with open(self.config, 'r') as fp:
                config = json.load(fp, object_pairs_hook=OrderedDict)

            # overwrite variables
            with open(os.path.join(self.build_dir, 'less', 'variables.less'), 'w') as fp:
                for key, value in config['vars'].items():
                    fp.write('%s: %s;\n' % (key, value))

                # add some variables not included in config.json
                for key, value in self.missing_variables.items():
                    if key not in config['vars']:
                        fp.write('%s: %s;\n' % (key, value))

            files = [name for name in os.listdir(os.path.join(self.build_dir, 'js'))
                     if name.endswith('js')]

            # remove unwanted js
            for filename in set(files) - set(config['js']):
                os.remove(os.path.join(self.build_dir, 'js', filename))

            # parse bootstrap.less so we get the required order
            include_order = []
            bootstrap_less = os.path.join(self.build_dir, 'less', 'bootstrap.less')
            with open(bootstrap_less) as fp:
                for line in fp:
                    match = re.match('@import "(.*)";', line)
                    if match is not None:
                        include_order.append(match.groups(0)[0])

            includes = sorted(config['css'] + self.mandatory_less,
                              key=lambda k: include_order.index(k))
            with open(bootstrap_less, 'w') as fp:
                for include in includes:
                    fp.write('@import "%s";\n' % include)

        local('npm install')  # install dependencies
        local('grunt dist')

# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os


class DefaultsDict(dict):

    def add(self, key, default_value=None, also=None, prefix=None):
        if prefix:
            key = '%s_%s' % (prefix.replace('-', '_'), key)
        if also:
            value = os.environ.get(also, default_value)
        value = os.environ.get('OS_%s' % key.upper(), default_value)
        if value is not None:
            self.__setitem__(key, value)

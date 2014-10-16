# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import recordtype

class PosEdit( recordtype.recordtype( 'PosEdit', [('pos',None),('edit',None),('uncertain',False)] )):
    """
    Represents a simple variant, i.e. one change to one allele.
    """

    def __str__(self):
        rv = str(self.edit) if self.pos is None else '{self.pos}{self.edit}'.format(self=self)
        if self.uncertain:
            if self.edit in ['0','']:
                rv = rv + '?'
            else:
                rv = '(' + rv + ')'
        return rv

    def _set_uncertain(self):
        """sets the uncertain flag to True; used primarily by the HGVS grammar

        :returns: self
        """
        self.uncertain = True
        return self

class PosEditList(
    collections.MutableSequence,
    recordtype.recordtype(
        'PosEditList',
        [ 'items', ('uncertain', False), ('allele_uncertain', False) ] )):
    """
    Represents several PosEdits, i.e. multiple changes to one allele.
    """

    #def __init__(self, posedits)

    def _set_uncertain(self):
        """sets the uncertain flag to True; used primarily by the HGVS grammar

        :returns: self
        """
        self.uncertain = True
        return self

    def __getitem__(self, key):
        return self.items.__getitem__(key)

    def __setitem__(self, key, value):
        self.items.__setitem__(key, value)

    def __delitem__(self, key):
        self.items.__delitem__(key)

    def __len__(self):
        return self.items.__len__()

    def insert(self, key, value):
        self.items.insert(key, value)

    def __str__(self):
        separator = '(;)' if self.allele_uncertain else ';'
        rv = separator.join(map(str, self.items))
        if self.uncertain:
            rv = '(' + rv + ')'
        return rv


## <LICENSE>
## Copyright 2014 HGVS Contributors (https://bitbucket.org/hgvs/hgvs)
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>

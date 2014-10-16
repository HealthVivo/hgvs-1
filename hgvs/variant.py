# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import warnings

from .decorators.deprecated import deprecated

import recordtype

from hgvs.posedit import PosEdit, PosEditList
from hgvs.exceptions import HGVSError

class SequenceVariant( recordtype.recordtype('SequenceVariant', ['ac','type','posedits']) ):
    """
    represents a basic HGVS variant.  The only requirement is that each
    component can be stringified; for example, passing pos as either a string
    or an hgvs.location.CDSInterval (for example) are both intended uses
    """

    def __init__(self, ac, type, posedits=None, posedit=None):
        if ((posedits is None and posedit is None) or
            (posedits is not None and posedit is not None)):
            raise ValueError("must specify either posedits or posedit")
        # Provide backwards compatibility with the old API.
        if posedit is not None:
            warnings.warn('posedit is deprecated; use posedits instead',
                          DeprecationWarning)
            posedits = posedit
        # Accept posedits as a single string or PosEdit object, in which case
        # we'll automatically convert it to a 1-element PosEditList.
        # FIXME Should this raise a DeprecationWarning?
        if isinstance(posedits, (basestring, PosEdit)):
            posedits = PosEditList([posedits])
        super(SequenceVariant, self).__init__(ac, type, posedits)
    
    @property
    def seqref(self):
        warnings.warn('seqref is deprecated; use ac instead',DeprecationWarning,stacklevel=2)
        return self.ac

    @property
    def posedit(self):
        warnings.warn('posedit is deprecated; use posedits[0] instead',
                      DeprecationWarning, stacklevel=2)
        if len(self.posedits) == 1:
            return self.posedits[0]
        else:
            raise ValueError('posedit backwards-compatibility only supported '
                             'for single-edit variants')

    def __str__(self):
        return self.to_str()

    # force_brackets is needed by ComplexVariant.__str__.
    def to_str(self, force_brackets=False):
        if self.ac is not None:
            format_str = '{self.ac}:{self.type}.{posedit_str}'
        else:
            format_str = '{self.type}.{posedit_str}'
        posedit_str = str(self.posedits)
        if len(self.posedits) > 1 or force_brackets:
            posedit_str = '[' + posedit_str + ']'
        return format_str.format(self=self, posedit_str=posedit_str) 

# Maps type to separator.
COMPLEX_VARIANT_SEPARATOR_MAP = {
    'poly': '];[',
    'mosaic': '/',
    'chimeric': '//',
    }

class ComplexVariant ( recordtype.recordtype('ComplexVariant', ['type', 'variants']) ):
    """A container for multiple basic variants."""

    def __init__(self, type, variants):
        super(ComplexVariant, self).__init__(type, variants)
        if self.type not in COMPLEX_VARIANT_SEPARATOR_MAP:
            raise HGVSError("Unknown type for ComplexVariant.")
        if not self.all_same_type:
            raise HGVSError("ComplexVariant does not support variants with "
                            "different types.")
        if not self.all_same_ac and self.type != 'poly':
            raise HGVSError("ComplexVariant only supports multiple accession "
                            "numbers for 'poly' variant types.")

    @property
    def all_same_ac(self):
        """Return True if all variants have same accession, otherwise False."""
        return len(set(var.ac for var in self.variants)) == 1

    @property
    def all_same_type(self):
        """Return True if all variants have same type, otherwise False."""
        return len(set(var.type for var in self.variants)) == 1

    @property
    def separator(self):
        """Return formatting separator, depending on type."""
        return COMPLEX_VARIANT_SEPARATOR_MAP[self.type]

    def __str__(self):
        var_type = self.variants[0].type
        if self.all_same_ac:
            var_ac = self.variants[0].ac
            format_str = '{var_type}.{variants_str}'
            if var_ac is not None:
                format_str = '{var_ac}:' + format_str
            poseditlists = [str(var.posedits) for var in self.variants]
            variants_str = self.separator.join(map(str, poseditlists))
            if len(self.variants) > 1:
                variants_str = '[' + variants_str + ']'
            return format_str.format(var_ac=var_ac, var_type=var_type,
                                     variants_str=variants_str)
        else:
            return ';'.join(var.to_str(force_brackets=True)
                            for var in self.variants)

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

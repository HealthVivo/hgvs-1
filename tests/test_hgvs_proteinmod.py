import unittest
import pprint
import os

import hgvs.edit
import hgvs.parser
from hgvs.exceptions import HGVSError

class Test_Edit_AAPtm(unittest.TestCase):

    def setUp(self):
        self.parser = hgvs.parser.Parser()

    def test_AAPtm_exceptions(self):
        with self.assertRaises(HGVSError):
            edit = str(hgvs.edit.AAPtm('xxx'))
        with self.assertRaises(HGVSError):
            for subtype in ('change', 'substitution', 'mass'):
                edit = str(hgvs.edit.AAPtm(subtype, None))
        with self.assertRaises(HGVSError):
            edit = str(hgvs.edit.AAPtm('cleavage', 'xxx'))
        bad_edit = hgvs.edit.AAPtm('change', '+a')
        bad_edit.subtype = 'xxx'
        with self.assertRaises(RuntimeError):
            edit = str(bad_edit)

    def test_AAPtm(self):
        e_chg = hgvs.edit.AAPtm('change', 'Phospho')
        e_sub = hgvs.edit.AAPtm('substitution', 'MOD:00048')
        e_mass = hgvs.edit.AAPtm('mass', '79.96633')
        e_clv = hgvs.edit.AAPtm('cleavage')
        self.assertEqual(str(e_chg), 'mod+Phospho')
        self.assertEqual(str(e_sub), 'mod=MOD:00048')
        self.assertEqual(str(e_mass), 'mod#79.96633')
        self.assertEqual(str(e_clv), 'mod*')
        for e in e_chg, e_sub, e_mass, e_clv:
            self.assertEqual(e.type, 'mod')
        self.assertEqual(e_chg.subtype, 'change')
        self.assertEqual(e_sub.subtype, 'substitution')
        self.assertEqual(e_mass.subtype, 'mass')
        self.assertEqual(e_clv.subtype, 'cleavage')

    # FIXME once we get single-AA formatting working, these should be converted.
    EXAMPLES = '''
        P00519:pm.Thr315Ile
        P00519:pm.Tyr393mod+Phospho
        P00519:pm.Tyr393mod=MOD:00048
        P00519:pm.Tyr393mod#79.96633
        P00519:pm.Asp939mod*
    '''

    def test_parser(self):
        for var in self.EXAMPLES.split('\n'):
            var = var.strip()
            if var == '':
                continue
            v = self.parser._grammar(var).pm_variant()
            self.assertEqual( var, str(v), 'parse-format roundtrip failed:'+pprint.pformat(v.posedit) )

    def test_parser_posedits(self):
        parser = hgvs.parser.Parser()
        fn = os.path.join( os.path.dirname(__file__), 'data',
                           'protein_mod_posedits' )
        pe_file = open(fn)
        for pe in pe_file:
            pe = pe.strip()
            yield lambda x: parser._grammar(x).pm_posedit(), pe

if __name__ == '__main__':
    unittest.main()

## <LICENSE>
## Copyright 2014 HGVS Contributors (https://bitbucket.org/invitae/hgvs)
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

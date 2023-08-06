#!/usr/bin/env python2

import unittest
import postpic.analyzer as pa

class TestSpeciesIdentifier(unittest.TestCase):
    
    def setUp(self):
        pass

    def checke(self, data, m, c, eject, tracer, ision):
        pc = pa.PhysicalConstants
        self.assertEqual(data['mass'], m * pc.me)
        self.assertEqual(data['charge'], c * pc.qe)
        self.assertEqual(data['ejected'], eject)
        self.assertEqual(data['tracer'], tracer)
        self.assertEqual(data['ision'], ision)

    def checkion(self, data, m, c, eject, tracer, ision):
        self.checke(data, 1836.2 * m, c, eject, tracer, ision)

    def test_identifyspecies_ion(self):
        idfy = pa.identifyspecies
        self.checkion(idfy('proton'), 1, 1, False, False, True)
        self.checkion(idfy('H1'), 1, 1, False, False, True)
        self.checkion(idfy('tracer_O3'), 16, 3, False, True, True)
        self.checkion(idfy('ejected_tracer_C4'), 12, 4, True, True, True)
        self.checkion(idfy('ionm3c7'), 3, 7, False, False, True)
        self.checkion(idfy('ionm30c70xx5'), 30, 70, False, False, True)
        self.checkion(idfy('tracer_ejected_Au27a'), 197, 27, True, True, True)
        self.checkion(idfy('ejected_tracer_Au27'), 197, 27, True, True, True)
        self.checkion(idfy('tracer_blahh_Au27x'), 197, 27, False, True, True)

    def test_identifyspecies_electron(self):
        idfy = pa.identifyspecies
        self.checke(idfy('Elektron'), 1, -1, False, False, False)
        self.checke(idfy('Elektronx'), 1, -1, False, False, False)
        self.checke(idfy('Elektron2'), 1, -1, False, False, False)
        self.checke(idfy('ElektronAu2'), 1, -1, False, False, False)
        self.checke(idfy('ejected_ElektronAu2'), 1, -1, True, False, False)
        self.checke(idfy('tracer_blahh_electronHe2b'), 1, -1, False, True, False)

    def test_identifyspecies_praefix(self):
        x = pa.identifyspecies('a_b_c_xxx_tracer_h_w_33_He5_O3x2')
        self.assertEqual(x['a'], True)
        self.assertEqual(x['b'], True)
        self.assertEqual(x['c'], True)
        self.assertEqual(x['xxx'], True)
        self.assertEqual(x['h'], True)
        self.assertEqual(x['w'], True)
        self.assertEqual(x['33'], True)
        self.assertEqual(x['He5'], True)
        self.checkion(x, 16,3, False, True, True)

if __name__ == '__main__':
    unittest.main()

import unittest
from vondrak import *

class testPrecession(unittest.TestCase):

    def test_pecl(self):
        '''test long-term precession of the ecliptic'''
        epj = -1373.5959534565 # julian epoch
        pecl = ltp_PECL(epj)
        pecl_test = array([+0.00041724785764001342,-0.40495491104576162693,+0.91433656053126552350])
        # print(pecl)
        # print(pecl_test)
        self.assertEqual(pecl.all(), pecl_test.all())

    def test_pequ(self):
        '''test long-term precession of the equator'''
        epj = -1373.5959534565 # julian epoch
        pequ = ltp_PEQU(epj)
        pequ_test = array([-0.29437643797369031532,-0.11719098023370257855,+0.94847708824082091796])
        # print(pequ)
        # print(pequ_test)
        self.assertEqual(pequ.all(), pequ_test.all())

    def test_pmat(self):
        '''test long-term precession matrix'''
        epj = -1373.5959534565 # julian epoch
        rp = ltp_PMAT(epj)
        rp_test = array([
                        [+0.68473390570729557360,+0.66647794042757610444,+0.29486722236305384992],
                        [-0.66669482609418419936,+0.73625636097440967969,-0.11595076448202158534],
                        [-0.29437643797369031532,-0.11719098023370257855,+0.94847708824082091796],
                        ])
        # print(rp)
        # print(rp_test)
        self.assertEqual(rp.all(), rp_test.all())

    def test_pbmat(self):
        '''test long-term precession matrix, including GCRS frame bias'''
        epj = -1373.5959534565 # julian epoch
        rpxb = ltp_PBMAT(epj)
        rpxb_test = array([
                          [+0.68473392912753224372,+0.66647788221176470103,+0.29486722236305384992],
                          [-0.66669476463873305255,+0.73625641199831485100,-0.11595079385100924091],
                          [-0.29437652267952261218,-0.11719099075396051880,+0.94847706065103424635],
                          ])
        # print(rpxb)
        # print(rpxb_test)
        self.assertEqual(rpxb.all(), rpxb_test.all())

    def test_epj(self):
        '''test julian date to julian epoch'''
        epj0 = epj(1219339.078000)
        epj1 = -1373.5959534565 # julian epoch
        self.assertAlmostEqual(epj0, epj1, 10)

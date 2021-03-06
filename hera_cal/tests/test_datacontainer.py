import unittest
from hera_cal import datacontainer, io
import numpy as np
from hera_cal.data import DATA_PATH
import os
from hera_cal import abscal

class TestDataContainer(unittest.TestCase):

    def setUp(self):
        self.bls = [(1, 2), (2, 3), (3, 4), (1, 3), (2, 4)]  # not (1,4)
        self.pols = ['xx', 'yy']
        self.blpol = {}
        for bl in self.bls:
            self.blpol[bl] = {}
            for pol in self.pols:
                self.blpol[bl][pol] = 1j
        self.polbl = {}
        for pol in self.pols:
            self.polbl[pol] = {}
            for bl in self.bls:
                self.polbl[pol][bl] = 1j
        self.both = {}
        for pol in self.pols:
            for bl in self.bls:
                self.both[bl + (pol,)] = 1j

    def test_init(self):
        dc = datacontainer.DataContainer(self.blpol)
        for k in dc._data.keys():
            self.assertEqual(len(k), 3)
        self.assertEqual(set(self.bls), dc._bls)
        self.assertEqual(set(self.pols), dc._pols)
        dc = datacontainer.DataContainer(self.polbl)
        for k in dc._data.keys():
            self.assertEqual(len(k), 3)
        self.assertEqual(set(self.bls), dc._bls)
        self.assertEqual(set(self.pols), dc._pols)
        dc = datacontainer.DataContainer(self.both)
        for k in dc._data.keys():
            self.assertEqual(len(k), 3)
        self.assertEqual(set(self.bls), dc._bls)
        self.assertEqual(set(self.pols), dc._pols)
        self.assertRaises(
            AssertionError, datacontainer.DataContainer, {(1, 2, 3, 4): 2})

    def test_bls(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(set(self.bls), dc.bls())
        self.assertEqual(set(self.bls), dc.bls('xx'))
        self.assertEqual(set(self.bls), dc.bls('yy'))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(set(self.bls), dc.bls())
        self.assertEqual(set(self.bls), dc.bls('xx'))
        self.assertEqual(set(self.bls), dc.bls('yy'))
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(set(self.bls), dc.bls())
        self.assertEqual(set(self.bls), dc.bls('xx'))
        self.assertEqual(set(self.bls), dc.bls('yy'))

    def test_pols(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(set(self.pols), dc.pols())
        self.assertEqual(set(self.pols), dc.pols((1, 2)))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(set(self.pols), dc.pols())
        self.assertEqual(set(self.pols), dc.pols((1, 2)))
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(set(self.pols), dc.pols())
        self.assertEqual(set(self.pols), dc.pols((1, 2)))

    def test_keys(self):
        dc = datacontainer.DataContainer(self.blpol)
        keys = dc.keys()
        self.assertEqual(len(keys), len(self.pols) * len(self.bls))
        dc = datacontainer.DataContainer(self.polbl)
        keys = dc.keys()
        self.assertEqual(len(keys), len(self.pols) * len(self.bls))
        dc = datacontainer.DataContainer(self.both)
        keys = dc.keys()
        self.assertEqual(len(keys), len(self.pols) * len(self.bls))

    def test_values(self):
        dc = datacontainer.DataContainer(self.blpol)
        values = dc.values()
        self.assertEqual(len(values), len(self.pols) * len(self.bls))
        self.assertEqual(values[0], 1j)
        dc = datacontainer.DataContainer(self.polbl)
        values = dc.values()
        self.assertEqual(len(values), len(self.pols) * len(self.bls))
        self.assertEqual(values[0], 1j)
        dc = datacontainer.DataContainer(self.both)
        values = dc.values()
        self.assertEqual(len(values), len(self.pols) * len(self.bls))
        self.assertEqual(values[0], 1j)

    def test_items(self):
        dc = datacontainer.DataContainer(self.blpol)
        items = dc.items()
        self.assertEqual(len(items), len(self.pols) * len(self.bls))
        self.assertTrue(items[0][0][0:2] in self.bls)
        self.assertTrue(items[0][0][2] in self.pols)
        self.assertEqual(items[0][1], 1j)
        dc = datacontainer.DataContainer(self.polbl)
        items = dc.items()
        self.assertTrue(items[0][0][0:2] in self.bls)
        self.assertTrue(items[0][0][2] in self.pols)
        self.assertEqual(items[0][1], 1j)
        dc = datacontainer.DataContainer(self.both)
        items = dc.items()
        self.assertTrue(items[0][0][0:2] in self.bls)
        self.assertTrue(items[0][0][2] in self.pols)
        self.assertEqual(items[0][1], 1j)

    def test_len(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(len(dc), 10)
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(len(dc), 10)
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(len(dc), 10)

    def test_del(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertTrue((1,2,'xx') in dc)
        self.assertTrue((1,2,'XX') in dc)
        del dc[(1, 2, 'xx')]
        self.assertFalse((1,2,'xx') in dc)
        self.assertTrue('xx' in dc.pols())
        self.assertTrue((1,2) in dc.bls())
        del dc[(1, 2, 'yy')]
        self.assertFalse((1,2) in dc.bls())
        del dc[(2,3,'XX')]
        self.assertFalse((2,3,'xx') in dc)
        self.assertTrue('xx' in dc.pols())
        self.assertTrue((2,3) in dc.bls())


    def test_getitem(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(dc[(1, 2, 'xx')], 1j)
        self.assertEqual(dc[(2, 1, 'xx')], -1j)
        self.assertEqual(dc[(1, 2)], {'xx': 1j, 'yy': 1j})
        self.assertEqual(set(dc['xx'].keys()), set(self.bls))
        self.assertEqual(dc[(1, 2, 'xx')], dc.get_data((1, 2, 'xx')))
        self.assertEqual(dc[(1, 2, 'xx')], dc.get_data(1, 2, 'xx'))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(dc[(1, 2, 'xx')], 1j)
        self.assertEqual(dc[(2, 1, 'xx')], -1j)
        self.assertEqual(dc[(1, 2)], {'xx': 1j, 'yy': 1j})
        self.assertEqual(set(dc['xx'].keys()), set(self.bls))
        self.assertEqual(dc[(2, 1, 'xx')], dc.get_data((2, 1, 'xx')))
        self.assertEqual(dc[(2, 1, 'xx')], dc.get_data(2, 1, 'xx'))
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(dc[(1, 2, 'xx')], 1j)
        self.assertEqual(dc[(2, 1, 'xx')], -1j)
        self.assertEqual(dc[(1, 2)], {'xx': 1j, 'yy': 1j})
        self.assertEqual(set(dc['xx'].keys()), set(self.bls))
        self.assertEqual(dc[(1, 2)], dc.get_data((1, 2)))
        self.assertEqual(dc[(1, 2)], dc.get_data(1, 2))
        self.assertEqual(dc[(1, 2, 'XX')], 1j)
        self.assertEqual(dc[(2, 1, 'XX')], -1j)
        self.assertEqual(dc[(2, 1, 'XX')], dc.get_data(2, 1, 'XX'))
        self.assertEqual(dc[(2, 1, 'XX')], dc.get_data(2, 1, 'xx'))


    def test_has_key(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertTrue(dc.has_key((2, 3, 'yy')))
        self.assertTrue(dc.has_key((2, 3), 'yy'))
        self.assertTrue(dc.has_key((3, 2), 'yy'))
        self.assertFalse(dc.has_key('xy'))
        self.assertFalse(dc.has_key((5, 6)))
        self.assertFalse(dc.has_key((1, 2, 'xy')))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertTrue(dc.has_key((2, 3, 'yy')))
        self.assertTrue(dc.has_key((2, 3), 'yy'))
        self.assertTrue(dc.has_key((3, 2), 'yy'))
        self.assertFalse(dc.has_key('xy'))
        self.assertFalse(dc.has_key((5, 6)))
        self.assertFalse(dc.has_key((1, 2, 'xy')))
        dc = datacontainer.DataContainer(self.both)
        self.assertTrue(dc.has_key((2, 3, 'yy')))
        self.assertTrue(dc.has_key((2, 3), 'yy'))
        self.assertTrue(dc.has_key((3, 2), 'yy'))
        self.assertFalse(dc.has_key('xy'))
        self.assertFalse(dc.has_key((5, 6)))
        self.assertFalse(dc.has_key((1, 2, 'xy')))

        self.assertTrue(dc.has_key((2, 3, 'YY')))
        self.assertTrue(dc.has_key((2, 3), 'YY'))
        self.assertTrue(dc.has_key((3, 2), 'YY'))
        self.assertFalse(dc.has_key('XY'))
        self.assertFalse(dc.has_key((5, 6)))
        self.assertFalse(dc.has_key((1, 2, 'XY')))

        # assert switch bl
        dc[(1,2,'xy')] = 1j
        self.assertTrue(dc.has_key((2,1,'yx')))


    def test_has_bl(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertTrue(dc.has_bl((2, 3)))
        self.assertTrue(dc.has_bl((3, 2)))
        self.assertFalse(dc.has_bl((0, 3)))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertTrue(dc.has_bl((2, 3)))
        self.assertTrue(dc.has_bl((3, 2)))
        self.assertFalse(dc.has_bl((0, 3)))
        dc = datacontainer.DataContainer(self.both)
        self.assertTrue(dc.has_bl((2, 3)))
        self.assertTrue(dc.has_bl((3, 2)))
        self.assertFalse(dc.has_bl((0, 3)))

    def test_has_pol(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertTrue(dc.has_pol('xx'))
        self.assertTrue(dc.has_pol('XX'))
        self.assertFalse(dc.has_pol('xy'))
        self.assertFalse(dc.has_pol('XY'))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertTrue(dc.has_pol('xx'))
        self.assertTrue(dc.has_pol('XX'))
        self.assertFalse(dc.has_pol('xy'))
        self.assertFalse(dc.has_pol('XY'))
        dc = datacontainer.DataContainer(self.both)
        self.assertTrue(dc.has_pol('xx'))
        self.assertTrue(dc.has_pol('XX'))
        self.assertFalse(dc.has_pol('xy'))
        self.assertFalse(dc.has_pol('XY'))

    def test_get(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(dc.get((1, 2), 'yy'), 1j)
        self.assertEqual(dc.get((2, 1), 'yy'), -1j)
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(dc.get((1, 2), 'yy'), 1j)
        self.assertEqual(dc.get((2, 1), 'yy'), -1j)
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(dc.get((1, 2), 'yy'), 1j)
        self.assertEqual(dc.get((2, 1), 'yy'), -1j)
        self.assertEqual(dc.get((1, 2), 'YY'), 1j)
        self.assertEqual(dc.get((2, 1), 'YY'), -1j)


    def test_setter(self):
        dc = datacontainer.DataContainer(self.blpol)
        # test basic setting
        dc[(100, 101, 'xy')] = np.arange(100) + np.arange(100)*1j
        self.assertEqual(dc[(100, 101, 'xy')].shape, (100,))
        self.assertEqual(dc[(100, 101, 'xy')].dtype, np.complex)
        self.assertAlmostEqual(dc[(100, 101, 'xy')][1], (1 + 1j))
        self.assertAlmostEqual(dc[(101, 100, 'yx')][1], (1 - 1j))
        self.assertEqual(len(dc.keys()), 11)
        self.assertEqual((100, 101) in dc._bls, True)
        self.assertEqual('xy' in dc._pols, True)
        # test error
        self.assertRaises(ValueError, dc.__setitem__, *((100, 101), 100j))

    def test_adder(self):
        test_file = os.path.join(DATA_PATH, "zen.2458043.12552.xx.HH.uvORA")
        d, f = io.load_vis(test_file, pop_autos=True)
        d2 = d + d
        self.assertAlmostEqual(d2[(24,25,'xx')][30, 30], d[(24,25,'xx')][30, 30]*2)
        # test exception
        d2, f2 = io.load_vis(test_file, pop_autos=True)
        d2[d2.keys()[0]] = d2[d2.keys()[0]][:, :10]
        self.assertRaises(ValueError, d.__add__, d2)
        d2[d2.keys()[0]] = d2[d2.keys()[0]][:10, :]
        self.assertRaises(ValueError, d.__add__, d2)

    def test_mul(self):
        test_file = os.path.join(DATA_PATH, "zen.2458043.12552.xx.HH.uvORA")
        d, f = io.load_vis(test_file, pop_autos=True)
        f[(24,25,'xx')][:,0] = False
        f2 = f * f
        self.assertFalse(f2[(24,25,'xx')][0,0])
        # test exception
        d2, f2 = io.load_vis(test_file, pop_autos=True)
        d2[d2.keys()[0]] = d2[d2.keys()[0]][:, :10]
        self.assertRaises(ValueError, d.__mul__, d2)
        d2[d2.keys()[0]] = d2[d2.keys()[0]][:10, :]
        self.assertRaises(ValueError, d.__mul__, d2)

    def test_concatenate(self):
        test_file = os.path.join(DATA_PATH, "zen.2458043.12552.xx.HH.uvORA")
        d, f = io.load_vis(test_file, pop_autos=True)
        d2 = d.concatenate(d)
        self.assertEqual(d2[(24,25,'xx')].shape[0], d[(24,25,'xx')].shape[0]*2)
        d2 = d.concatenate(d, axis=1)
        self.assertEqual(d2[(24,25,'xx')].shape[1], d[(24,25,'xx')].shape[1]*2)
        d2 = d.concatenate([d,d], axis=0)
        self.assertEqual(d2[(24,25,'xx')].shape[0], d[(24,25,'xx')].shape[0]*3)
        # test exceptions
        d2, f2 = io.load_vis(test_file, pop_autos=True)
        d2[d2.keys()[0]] = d2[d2.keys()[0]][:10, :10]
        self.assertRaises(ValueError, d.concatenate, d2, axis=0)
        self.assertRaises(ValueError, d.concatenate, d2, axis=1)


if __name__ == '__main__':
    unittest.main()

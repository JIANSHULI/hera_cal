import nose.tools as nt
from hera_cal.utils import get_HERA_aa
import numpy as np,sys
from hera_cal.calibrations import CAL_PATH
freqs = np.array([0.15])

class Test_utils(object):
    # add directory with calfile
    if CAL_PATH not in sys.path:
        sys.path.append(CAL_PATH)
    global calfile
    calfile = "hera_test_calfile"
    def test_get_HERA_aa_default_cal(self):
        aa = get_HERA_aa(freqs)
        nt.assert_equal(len(aa),113)
    def test_get_HERA_aa_mycal(self):
        aa = get_HERA_aa(freqs,calfile=calfile)
        nt.assert_equal(len(aa),128)
        nt.assert_almost_equal(aa.lat,-30.7215261207*np.pi/180,places=6)
        nt.assert_almost_equal(aa.lon,21.4283038269*np.pi/180,places=6)
    def test_get_HERA_aa_cofa(self):
        aa = get_HERA_aa(freqs)
        #check the position is correct to ~6m
        nt.assert_almost_equal(aa.lat,-30.7215261207*np.pi/180,places=6)
        nt.assert_almost_equal(aa.lon,21.4283038269*np.pi/180,places=6)

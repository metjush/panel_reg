import cPickle as pickle
from first_diff import FirstDiff
from fixed_effects import FixedEffects
import pandas as pd

data_file = '../data/nulled_panel'


if __name__ == '__main__':
    panel = pickle.load(open(data_file, 'rb'))
    print(panel)
    fd = FirstDiff(panel, 'SP.DYN.LE00.IN', ['SH.XPD.PRIV.ZS', 'SH.XPD.PUBL.ZS', 'SH.XPD.PUBL.GX.ZS', 'SH.XPD.PUBL', 'SH.XPD.PCAP.PP.KD', 'SH.XPD.TOTL.ZS', 'SH.MED.BEDS.ZS'])
    fd.estimate()

    fe = FixedEffects(panel, 'SP.DYN.LE00.IN', ['SH.XPD.PRIV.ZS', 'SH.XPD.PUBL.ZS', 'SH.XPD.PUBL.GX.ZS', 'SH.XPD.PUBL', 'SH.XPD.PCAP.PP.KD', 'SH.XPD.TOTL.ZS', 'SH.MED.BEDS.ZS'])
    fe.estimate()

    fe2 = FixedEffects(panel, 'SP.DYN.LE00.IN', ['SH.XPD.PRIV.ZS', 'SH.XPD.PUBL.ZS', 'SH.XPD.PUBL.GX.ZS', 'SH.XPD.PUBL', 'SH.XPD.PCAP.PP.KD', 'SH.XPD.TOTL.ZS', 'SH.MED.BEDS.ZS'], True)
    fe2.estimate()
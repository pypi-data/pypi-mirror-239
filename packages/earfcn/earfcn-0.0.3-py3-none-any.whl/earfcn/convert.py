from argparse import ArgumentParser
from typing import List, Tuple

# import numpy as np

bands = [
    {'band': 1, 'FDL_Low': 2110, 'NDL_Min': 0, 'NUL_Min': 18000, 'duplex': 190, 'FDL_Hi': 2170},
    {'band': 2, 'FDL_Low': 1930, 'NDL_Min': 600, 'NUL_Min': 18600, 'duplex': 80, 'FDL_Hi': 1990},
    {'band': 3, 'FDL_Low': 1805, 'NDL_Min': 1200, 'NUL_Min': 19200, 'duplex': 95, 'FDL_Hi': 1880},
    {'band': 4, 'FDL_Low': 2110, 'NDL_Min': 1950, 'NUL_Min': 19950, 'duplex': 400, 'FDL_Hi': 2155},
    {'band': 5, 'FDL_Low': 869, 'NDL_Min': 2400, 'NUL_Min': 20400, 'duplex': 45, 'FDL_Hi': 894},
    {'band': 6, 'FDL_Low': 875, 'NDL_Min': 2650, 'NUL_Min': 20650, 'duplex': 45, 'FDL_Hi': 875},
    {'band': 7, 'FDL_Low': 2620, 'NDL_Min': 2750, 'NUL_Min': 20750, 'duplex': 120, 'FDL_Hi': 2690},
    {'band': 8, 'FDL_Low': 925, 'NDL_Min': 3450, 'NUL_Min': 21450, 'duplex': 45, 'FDL_Hi': 960},
    {'band': 9, 'FDL_Low': 1844.9, 'NDL_Min': 3800, 'NUL_Min': 21800, 'duplex': 95, 'FDL_Hi': 1879.9},
    {'band': 10, 'FDL_Low': 2110, 'NDL_Min': 4150, 'NUL_Min': 22150, 'duplex': 400, 'FDL_Hi': 2170},
    {'band': 11, 'FDL_Low': 1475.9, 'NDL_Min': 4750, 'NUL_Min': 22750, 'duplex': 48, 'FDL_Hi': 1495.9},
    {'band': 12, 'FDL_Low': 729, 'NDL_Min': 5010, 'NUL_Min': 23010, 'duplex': 30, 'FDL_Hi': 746},
    {'band': 13, 'FDL_Low': 746, 'NDL_Min': 5180, 'NUL_Min': 23180, 'duplex': -31, 'FDL_Hi': 756},
    {'band': 14, 'FDL_Low': 758, 'NDL_Min': 5280, 'NUL_Min': 23280, 'duplex': -30, 'FDL_Hi': 768},
    {'band': 17, 'FDL_Low': 734, 'NDL_Min': 5730, 'NUL_Min': 23730, 'duplex': 30, 'FDL_Hi': 746},
    {'band': 18, 'FDL_Low': 860, 'NDL_Min': 5850, 'NUL_Min': 23850, 'duplex': 45, 'FDL_Hi': 875},
    {'band': 19, 'FDL_Low': 875, 'NDL_Min': 6000, 'NUL_Min': 24000, 'duplex': 45, 'FDL_Hi': 890},
    {'band': 20, 'FDL_Low': 791, 'NDL_Min': 6150, 'NUL_Min': 24150, 'duplex': -41, 'FDL_Hi': 821},
    {'band': 21, 'FDL_Low': 1495.9, 'NDL_Min': 6450, 'NUL_Min': 24450, 'duplex': 48, 'FDL_Hi': 1510.9},
    {'band': 22, 'FDL_Low': 3500, 'NDL_Min': 6600, 'NUL_Min': 24600, 'duplex': 100, 'FDL_Hi': 3590},
    {'band': 23, 'FDL_Low': 2180, 'NDL_Min': 7500, 'NUL_Min': 25500, 'duplex': 180, 'FDL_Hi': 2180},
    {'band': 24, 'FDL_Low': 1525, 'NDL_Min': 7700, 'NUL_Min': 25700, 'duplex': -101.5, 'FDL_Hi': 1559},
    {'band': 25, 'FDL_Low': 1930, 'NDL_Min': 8040, 'NUL_Min': 26040, 'duplex': 80, 'FDL_Hi': 1995},
    {'band': 26, 'FDL_Low': 859, 'NDL_Min': 8690, 'NUL_Min': 26690, 'duplex': 45, 'FDL_Hi': 894},
    {'band': 27, 'FDL_Low': 852, 'NDL_Min': 9040, 'NUL_Min': 27040, 'duplex': 45, 'FDL_Hi': 869},
    {'band': 28, 'FDL_Low': 758, 'NDL_Min': 9210, 'NUL_Min': 27210, 'duplex': 55, 'FDL_Hi': 803},
    {'band': 29, 'FDL_Low': 717, 'NDL_Min': 9660, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 728},
    {'band': 30, 'FDL_Low': 2350, 'NDL_Min': 9770, 'NUL_Min': 27660, 'duplex': 45, 'FDL_Hi':  2360},
    {'band': 31, 'FDL_Low': 462.5, 'NDL_Min': 9870, 'NUL_Min': 27760, 'duplex': 10, 'FDL_Hi': 467.5},
    {'band': 32, 'FDL_Low': 1452, 'NDL_Min': 9920, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1496},
    {'band': 33, 'FDL_Low': 1900, 'NDL_Min': 36000, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1920},
    {'band': 34, 'FDL_Low': 2010, 'NDL_Min': 36200, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 2025},
    {'band': 35, 'FDL_Low': 1850, 'NDL_Min': 36350, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1910},
    {'band': 36, 'FDL_Low': 1930, 'NDL_Min': 36950, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1990},
    {'band': 37, 'FDL_Low': 1910, 'NDL_Min': 37550, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1930},
    {'band': 38, 'FDL_Low': 2570, 'NDL_Min': 37750, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 2620},
    {'band': 39, 'FDL_Low': 1880, 'NDL_Min': 38250, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1920},
    {'band': 40, 'FDL_Low': 2300, 'NDL_Min': 38650, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 2400},
    {'band': 41, 'FDL_Low': 2496, 'NDL_Min': 39650, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 2690},
    {'band': 42, 'FDL_Low': 3400, 'NDL_Min': 41590, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 3600},
    {'band': 43, 'FDL_Low': 3600, 'NDL_Min': 43590, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 3800},
    {'band': 44, 'FDL_Low': 703, 'NDL_Min': 45590, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 803},
    {'band': 45, 'FDL_Low': 1447, 'NDL_Min': 46590, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1467},
    {'band': 46, 'FDL_Low': 5150, 'NDL_Min': 46790, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 5925},
    {'band': 47, 'FDL_Low': 5855, 'NDL_Min': 54540, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 5925},
    {'band': 48, 'FDL_Low': 3550, 'NDL_Min': 55240, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 3700},
    {'band': 49, 'FDL_Low': 3550, 'NDL_Min': 56740, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 3700},
    {'band': 50, 'FDL_Low': 1432, 'NDL_Min': 58240, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1517},
    {'band': 51, 'FDL_Low': 1427, 'NDL_Min': 59090, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 1432},
    {'band': 52, 'FDL_Low': 3300, 'NDL_Min': 59140, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 3400},
    {'band': 64, 'FDL_Low': 0, 'NDL_Min': 60140, 'NUL_Min': 27810, 'duplex': 0, 'FDL_Hi': 0},
    {'band': 65, 'FDL_Low': 2110, 'NDL_Min': 65536, 'NUL_Min': 131072, 'duplex': 190, 'FDL_Hi': 2200},
    {'band': 66, 'FDL_Low': 2110, 'NDL_Min': 66436, 'NUL_Min': 131972, 'duplex': 400, 'FDL_Hi': 2200},
    {'band': 67, 'FDL_Low': 738, 'NDL_Min': 67336, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 758},
    {'band': 68, 'FDL_Low': 753, 'NDL_Min': 67536, 'NUL_Min': 132672, 'duplex': 55, 'FDL_Hi': 783},
    {'band': 69, 'FDL_Low': 2570, 'NDL_Min': 67836, 'NUL_Min': 0, 'duplex': 0, 'FDL_Hi': 2620},
    {'band': 70, 'FDL_Low': 1995, 'NDL_Min': 68336, 'NUL_Min': 132972, 'duplex': 300, 'FDL_Hi': 2020},
    {'band': 71, 'FDL_Low': 617, 'NDL_Min': 68586, 'NUL_Min': 133122, 'duplex': -46, 'FDL_Hi': 652},
    {'band': 72, 'FDL_Low': 0, 'NDL_Min': 68936, 'NUL_Min': 133472, 'duplex': 0, 'FDL_Hi': 0}
]

class EARFCNException(Exception):
    pass

def earfcn2band(earfcn: int) -> int:
    """
    Get the band that contains the specified EARFCN.
    :param earfcn: LTE EARFCN value
    :return: LTE band number
    """
    # earfcn = np.int32(earfcn)
    for band, band2 in zip(bands, bands[1:]):
        if band['NDL_Min'] <= earfcn < band2['NDL_Min']:
            return band['band']

def earfcn2freq(earfcn: int) -> float:
    """
    Convert EARFCN to frequency (in MHz).
    :param earfcn: LTE EARFCN value
    :return: frequency in MHz
    """
    # earfcn = np.int32(earfcn)
    for band, band2 in zip(bands, bands[1:]):
        if band['NDL_Min'] <= earfcn < band2['NDL_Min']:
            return band['FDL_Low'] + 0.1 * (earfcn - band['NDL_Min'])
    raise EARFCNException(f'EARFCN {earfcn} not found. Try specifying frequency instead.')

def freq2earfcn(freq: float) -> List[Tuple[int, int]]:
    """
    Convert frequency to possible (band, EARFCN) values.
    :param freq: frequency in either Hz or MHz
    :return: List of possible (band, EARFCN) values
    """
    # freq = np.int32(freq)
    possible = []
    if freq > 1e6:
        freq = freq / 1e6
    for band in bands:
        if band['FDL_Low'] <= freq <= band['FDL_Hi']:
            earfcn = int(((freq - band['FDL_Low']) / 0.1) + band['NDL_Min'])
            possible.append((band['band'], earfcn))
    return possible

def earfcn2freq_main():
    parser = ArgumentParser(description='Convert LTE EARFCN to frequency (in MHz).')
    parser.add_argument('earfcn', type=int, help='LTE EARFCN value')
    args = parser.parse_args()
    print(earfcn2freq(args.earfcn))

def freq2earfcn_main():
    parser = ArgumentParser(description='Convert frequency (Hz or MHz) to possible (band, EARFCN) values.')
    parser.add_argument('freq', type=float, help='Frequency in Hz or MHz')
    args = parser.parse_args()
    for band, earfcn in freq2earfcn(args.freq):
        print(f'band={band}, earfcn={earfcn}')

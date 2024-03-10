import numpy as np
from scipy.signal import find_peaks
import soundfile as sf

import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')



class EnergyClass:
    e_mix: float
    e_max: float
    freq: int

    def __init__(self, e_min: float, e_max: float):
        self.e_min = e_min
        self.e_max = e_max
        self.freq = 0

def calculate_frequencies(data: list, n_bins: int, _filter = lambda _: True) -> list:
    m = min(data)
    bin_width = (max(data) - min(data)) / n_bins
    histogram = [ EnergyClass(m + i * bin_width, m + (i+1) * bin_width) for i in range(n_bins) ]
    filtered = filter(_filter, data)
    for value in filtered:
        for bin in histogram:
            if value >= bin.e_min and value < bin.e_max:
                bin.freq += 1
    return histogram



threshold = .25
cap = .9
binc = 40
data, rate = sf.read("sample_3.flac")
data = data[:int(.7*len(data))] # percentage of data to analyze
print(f"shape: {data.shape}, rate: {rate}")



wf = [x for x in data[:,1]]
abs_wf = [abs(x) for x in data[:,1]]
peaks, _ = find_peaks(abs_wf, [threshold, cap])
bars = calculate_frequencies(wf, binc, lambda e: e >= threshold and e <= cap)
# bars = calculate_frequencies(peaks, binc)

fig, axs = plt.subplots(2, constrained_layout=True)

axs[0].set_title("Detected signal")
axs[0].set_xlabel(f"Samples [rate: {rate}/s]")
axs[0].set_ylabel("Normalized intensity")
axs[0].plot(wf, c='g', label="signal")
axs[0].axhline(threshold, ls='--', c='tab:orange', label="threshold")
axs[0].axhline(cap, ls='--', c='tab:red', label="cap")
axs[0].legend()

# axs[1].set_title("Energies spectrum")
# axs[1].set_xlabel("Normalized classes")
# axs[1].set_ylabel("Frequency")
# axs[1].hist(list(filter(lambda e: e >= threshold and e <= cap, wf)), bins=binc, label="frequencies")
# axs[1].legend()

axs[1].set_title("Energies spectrum")
axs[1].set_xlabel("Normalized classes")
axs[1].set_ylabel("Frequency")
axs[1].plot([b.e_min for b in bars], [b.freq for b in bars], label="frequencies") # mmmh that's not right
axs[1].legend()

plt.savefig("output_sample_3.png")

# plt.scatter([i/len(bars) for i in range(len(bars))], [b.freq for b in bars])
import os, re

from .cagraph import CaGraph, CaGraphBatchTimeSamples, CaGraphTimeSamples, CaGraphBatch, CaGraphMatched, CaGraphBehavior
from .visualization import interactive_network, plot_heatmap, plot_cdf, plot_matched_data, plot_histogram
from .preprocess import deconvolve_dataset, generate_event_shuffle, generate_threshold, generate_average_threshold, generate_pearsons_distributions, plot_threshold, plot_shuffled_neuron, plot_correlation_hist


__all__ = ['CaGraph', 'CaGraphBatchTimeSamples', 'CaGraphTimeSamples', 'CaGraphBatch', 'CaGraphMatched', 'CaGraphBehavior',
            'interactive_network', 'plot_heatmap', 'plot_cdf', 'plot_matched_data', 'plot_histogram',
            'deconvolve_dataset', 'generate_event_shuffle', 'generate_threshold', 'generate_average_threshold', 'generate_pearsons_distributions', 'plot_threshold', 'plot_shuffled_neuron', 'plot_correlation_hist']


PKG = "cagraph"
VERSIONFILE = os.path.join(PKG, "_version.py")
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    VSRE = r"^verstr = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print("unable to find version in %s" % (VERSIONFILE,))
        raise RuntimeError("if %s.py exists, it is required to be well-formed" % (VERSIONFILE,))

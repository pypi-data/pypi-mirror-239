"""A collection of camera raw processing algorithms.

A collection of reference ISP algorithms, sufficient for producing a reasonably
good looking image from raw sensor data. Each algorithm takes in a frame in RGB
or raw format and returns a modified copy of the frame. The frame is expected to
be a NumPy float array with either 2 or 3 dimensions, depending on the function.
Some of the algorithms can be applied in different orders (demosaicing before or
after linearization, for example), but the reference ordering is as shown below.

Example:
  raw = rawpipe.linearize(raw, blacklevel=64, whitelevel=1023)
  rgb = rawpipe.wb(rgb, [1.5, 2.0], "RGGB")
  rgb = rawpipe.demosaic(raw, "RGGB", downsample=True)
  rgb = rawpipe.downsample(rgb, iterations=1)
  rgb = rawpipe.lsc(rgb, my_vignetting_map)
  rgb = rawpipe.lsc(rgb, my_color_shading_map)
  rgb = rawpipe.ccm(rgb, my_3x3_color_matrix)
  rgb = rawpipe.resize(rgb, 400, 300)
  rgb = rawpipe.gamut(rgb, "ACES")
  rgb = rawpipe.tonemap(rgb, "Reinhard")
  rgb = rawpipe.chroma_denoise(rgb)
  rgb = rawpipe.saturate(rgb, lambda x: x ** 0.75)
  rgb = rawpipe.gamma(rgb, "sRGB")
  rgb = rawpipe.quantize8(rgb)

Example:
  raw = rawpipe.verbose.linearize(raw)
  rgb = rawpipe.silent.demosaic(raw, "RGGB")
"""

from .rawpipe import Algorithms
from .rawpipe import verbose
from .rawpipe import silent
from .rawpipe import quiet
from .version import __version__

_methods = [f for f in dir(Algorithms) if callable(getattr(Algorithms, f)) and not f.startswith("_")]

for m in _methods:
    globals()[m] = getattr(silent, m)

__all__ = _methods

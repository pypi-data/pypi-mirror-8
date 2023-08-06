from __future__ import absolute_import

import numpy as np
from six import string_types

from ..plot_object import PlotObject
from ..properties import Any, Float, Color
from .. import palettes

class ColorMapper(PlotObject):
    ''' Base class for color mapper objects. '''
    pass

class LinearColorMapper(ColorMapper):

    # TODO (bev) use Array property
    palette = Any # Array
    low = Float
    high = Float

    reserve_color = Color("#ffffff") #TODO: What is the color code for transparent???
    reserve_val = Float(default=None)

    def __init__(self, *args, **kwargs):
        pal = args[0] if len(args) > 0 else kwargs.get('palette', [])

        if isinstance(pal, string_types):
            palette = getattr(palettes, pal, None)
            if palette is None:
                raise ValueError("Unknown palette name '%s'" % pal)
            kwargs['palette'] = np.array(palette)
        else:
            if not all(isinstance(x, string_types) and x.startswith('#') for x in pal):
                raise ValueError("Malformed palette: '%s'" % pal)
            kwargs['palette'] = np.array(pal)

        super(LinearColorMapper, self).__init__(**kwargs)

    def map_from_index(self, indices):
        return self.palette[np.array(indices)]

    def map_from_value(self, values):
        x = np.array(values)

        if self.low: low = self.low
        else: low = min(values)

        if self.high: high = self.high
        else: high = max(values)

        N = len(self.palette)
        scale = N/float(high-low)
        offset = -scale*low

        indices = np.floor(x*scale+offset).astype('int')
        indices[indices==len(self.palette)] -= 1
        return self.palette[indices]

    def reverse(self):
        self.palette = self.palette[::-1]

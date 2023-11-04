import numpy as np
# Rust modules
from .event_voxel_builder import __author__, __version__
from .event_voxel_builder import EventVoxelBuilder as RustEventVoxelBuilder

class EventVoxelBuilder(RustEventVoxelBuilder):
  def build(self, timestamps, i_row, i_col, polarity):
    timestamps = np.ascontiguousarray(timestamps, dtype=np.uint64)
    i_row = np.ascontiguousarray(i_row, dtype=np.uint16)
    i_col = np.ascontiguousarray(i_col, dtype=np.uint16)
    polarity = np.ascontiguousarray(polarity, dtype=np.int8)
    return super().build(timestamps, i_row, i_col, polarity)

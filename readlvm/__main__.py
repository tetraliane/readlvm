import sys
import yaml
from . import LvmData

[src_filename, pick_col_ind] = sys.argv[1].split(":")
out_filename = sys.argv[2]

lvm = LvmData.read(src_filename)
lvm.compress_data(int(pick_col_ind) - 1)

with open(out_filename, "w") as f:
    yaml.dump(lvm.into_yaml(), f)
